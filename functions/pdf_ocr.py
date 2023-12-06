#!/usr/bin/env python3
import cv2
import numpy as np
import pytesseract as pts
from io import BytesIO
from pdf2image import convert_from_path
from os import path
from .process_image import process_image_simple, process_image_detailed
from .output_to_docx import write_to_docx
from .output_to_pdf import write_to_pdf
from .tesseract_config import config_tesseract

INPUT_DIR_DEFAULT_IMG = 'test_files/images/'
INPUT_DIR_DEFAULT_PDF = 'test_files/pdfs/'
OUTPUT_DIR_DEFAULT = 'test_files/outputs/'
OUTPUT_MODES = ['print', 'txt', 'docx', 'pdf']
OUTPUT_MODE_DEFAULT = 'print'
IMAGE_EXTENSIONS = ['png', 'jpeg', 'jpg']

def pdf_ocr(**args):
    """
    Performs OCR on pdfs and depending on user input, output to either:
        * standard output (default),
        * text file (*.txt),
        * MS word file (*.docx), or
        * pdf file (*.pdf)
    
    Args:
        **args (dict): a keyword dictionary generated from parsed and
            validated user command line input.
    """
    input_pdfs = args.get('input_files')
    input_directory = args.get('input_directory')

    input_path_prefix = input_directory if input_directory else ''
    input_path_prefix += '/' if (input_path_prefix and input_path_prefix[-1] != '/')  else ''

    output_mode = args.get('output_mode')
    output_file = args.get('output_file')
    output_directory = args.get('output_directory')  # None if output file contains path

    output_path_prefix = output_directory if output_directory else ''
    output_path_prefix += '/' if (output_path_prefix and output_path_prefix[-1] != '/')  else ''

    join = args.get('join')

    # set output file from input pdfs if join and output file not passed
    if (join and not output_file and output_mode != 'print'):
        output_file = ''
        for in_pdf in input_pdfs:
            pdf_end = path.splitext(in_pdf)[0]  # before extension
            pdf_end = path.split(pdf_end)[1]     # after last '/'
            output_file += pdf_end + '-'
        output_file += 'joined_output.' + output_mode

    # set output file path if output file
    output_file_path = output_path_prefix + output_file if output_file else None

    output_document = None  # a docx Documnet object or a pdf Object from FPDF

    # to count total pages
    total_pages = 0

    # sets environ variables and returns tesseract config string
    # TODO add parameters to args or create new dict
    options = config_tesseract(**args)

    for pdf_index, input_pdf in enumerate(input_pdfs):

        # if not join create new output_doc for each pdf, else use one output_doc for all
        # TODO check system strain when join is True
        if not join:
            output_document = None

        pdf_file_path = input_path_prefix + input_pdf

        # set output file path from input file name for each image.
        # Used when join is False (if True output_file is already set or passed)
        if not output_file and output_mode != 'print':
            output_file_end = path.splitext(pdf_file_path)[0]  # before extension
            output_file_end = path.split(output_file_end)[1]     # after last '/'
            output_file_end += '-output.' + output_mode
            output_file_path = output_path_prefix + output_file_end

        # to check if this is last pdf for join. used to set save to True
        last_pdf = pdf_index == len(input_pdfs) - 1

        # display pdf processing start
        print("Processing pdf file no. {}: '{}'".format(pdf_index + 1, pdf_file_path))

        # read pdf
        pages = convert_from_path(pdf_file_path)

        # reset total_pages for not join
        if not join:
            total_pages = 0

        # iterate over each pdf's pages
        for page_index, page in enumerate(pages):

            # use BytesIO object, without saving to disk
            with BytesIO() as img_stream:

                # notify start of scan
                print('Scanning page {}'.format(page_index + 1))

                # specify format to save in bytes object
                page.save(img_stream, format="jpeg")  # test different formats quality?

                """ # if reading and writing from disk (page_loading_mode = 'file')
                    image_path = "page_image.jpg"
                    page.save(image_path, "jpg")
                    image = cv2.imread(image_path) """

                img_stream.seek(0)
                
                # load image with cv2 using numpy on buffer for page_loading_mode='bytes' 
                image = cv2.imdecode(np.frombuffer(img_stream.read(), np.uint8), 1)
                
                # process image
                # TODO add global variable for simple/detailed choice
                # processed_image = process_image_simple(image_file_path)
                
                # Temporary
                processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # other formats image_to_[...] - 'data' with dict option, pdf, box ...
                text = pts.image_to_string(processed_image, config=options)

                # save output if this is last page of current pdf and,
                # not join or join and current pdf is last one in list of pdfs  
                last_page = page_index == len(pages) - 1
                save = last_page and (not join or last_pdf)

                # to be added after each page
                # page no. starts from 1 for each pdf file
                footer = '\n\t\t\t\t\t--- Page {} ---\n\n'.format(page_index + 1)

                # base dict to pass to txt, docx or pdf writer functions
                base_dict = {
                    'save': save    # add common params here (font, layout ...)
                }

                # =============== OUTPUT based on output_mode ==============

                if output_mode == 'print':
                    if page_index == 0:
                        print("OUTPUT for pdf file: '{}'".format(pdf_file_path))
                    print(text + footer)

                elif output_mode == 'txt':  # TODO move to separate function
                    # if join: truncate for 1st page of 1st pdf, then append
                    # if not join: truncate for 1st page of each pdf, then append
                    if join:
                        write_mode = 'w' if pdf_index == 0 and page_index == 0 else 'a'
                    else:
                        write_mode = 'w' if page_index == 0 else 'a'
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
        

        total_pages += len(pages)
        # if save display successful OCR summary
        if save:
            saved_to = 'stdout' if output_mode == 'print' else output_file_path
            print("Successfuly OCR'ed {} no. of pages and wrote to '{}'\n"
                .format(total_pages, saved_to))
