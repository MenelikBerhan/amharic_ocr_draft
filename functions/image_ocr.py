#!/usr/bin/env python3
import pytesseract as pts
from os import path
from .output_to_docx import write_to_docx
from .output_to_pdf import write_to_pdf
from .process_image import process_image_simple, process_image_detailed
from .tesseract_config import config_tesseract

INPUT_DIR_DEFAULT_IMG = 'test_files/images/'
INPUT_DIR_DEFAULT_PDF = 'test_files/pdfs/'
OUTPUT_DIR_DEFAULT = 'test_files/outputs/'
OUTPUT_MODES = ['print', 'txt', 'docx', 'pdf']
OUTPUT_MODE_DEFAULT = 'print'
IMAGE_EXTENSIONS = ['png', 'jpeg', 'jpg']


def image_ocr(**args):
    """
    Performs OCR on images and depending on user input, output to either:
        * standard output (default),
        * text file (*.txt),
        * MS word file (*.docx), or
        * pdf file (*.pdf)
    
    Args:
        **args (dict): a keyword dictionary generated from parsed and
            validated user command line input.
    """
    input_images = args.get('input_files')
    input_directory = args.get('input_directory')

    input_path_prefix = input_directory if input_directory else ''
    input_path_prefix += '/' if (input_path_prefix and input_path_prefix[-1] != '/')  else ''

    output_mode = args.get('output_mode')
    output_file = args.get('output_file')
    output_directory = args.get('output_directory')  # None if output file contains path

    output_path_prefix = output_directory if output_directory else ''
    output_path_prefix += '/' if (output_path_prefix and output_path_prefix[-1] != '/')  else ''

    join = args.get('join')

    output_document = None  # a docx Documnet object or a pdf Object from FPDF

    output_file_path = output_path_prefix + output_file if output_file else None

    for i, image in enumerate(input_images):

        image_file_path = input_path_prefix + image

        # process image
        # TODO add global variable for simple/detailed choice
        processed_image = process_image_simple(image_file_path)

        # sets environ variables and returns tesseract config string
        # TODO add parameters to args or create new dict
        options = config_tesseract(**args)
    
        # other formats image_to_[...] - 'data' with dict option, pdf, box ...
        text = pts.image_to_string(processed_image, config=options)

        # save output file if not join or this is last page
        # TODO check system strain for too many image inputs with join
        # and save after specified images
        save = not join or (i == len(input_images) - 1)
        
        # output_file_path = None

        if save and output_mode != 'print':
            if not output_file:
                output_file_end = path.splitext(image_file_path)[0]  # before extension
                output_file_end = path.split(output_file_end)[1]     # after last '/'
                output_file_end += '_output.' + output_mode
                output_file_path = output_path_prefix + output_file_end

        footer = '\n\t\t\t\t\t--- Page {} ---\n\n'.format(i + 1)  # to be added after each page

        base_dict = {       # base dict to pass to txt, docx or pdf writer functions
            'save': save    # add common params here (font, layout ...)
        }

        # =============== OUTPUT based on output_mode ==============

        if output_mode == 'print':
            print(text + footer)

        elif output_mode == 'txt':  # TODO move to separate function
            write_mode = 'a' if i else 'w'  # truncate for 1st page, then append
            with open(output_file_path, write_mode, encoding='utf-8') as file:
                file.write(text + footer)

        elif output_mode == 'docx':
            params = base_dict  # add specific params here
            text += footer
            output_document = write_to_docx(text, output_file_path, output_document, **params)

        elif output_mode == 'pdf':
            params = base_dict
            text += footer
            output_document = write_to_pdf(text, output_file_path, output_document, **params)

    # display successful OCR summary
    output_file_path = 'stdout' if output_mode == 'print' else output_file_path
    print("Successfuly OCR'ed {} no. of pages and wrote to {}"
          .format(len(input_images), output_file_path))
