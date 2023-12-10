#!/usr/bin/env python3
import pytesseract as pts
from os import path
from statistics import mean
from .confidence import ocr_confidence
from .output_to_docx import write_to_docx
from .output_to_pdf import write_to_pdf
from .output_to_txt import write_to_txt
from .process_image import process_image_simple, process_image_detailed
from .tesseract_config import config_tesseract


def ocr_image(**args):
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

    # set output file from input images if join and output file not passed
    if (join and not output_file and output_mode != 'print'):
        output_file = ''
        for img in input_images:
            img_end = path.splitext(img)[0]  # before extension
            img_end = path.split(img_end)[1]     # after last '/'
            output_file += img_end + '-'
        output_file += 'joined_output.' + output_mode

    # set output file path if output file
    output_file_path = output_path_prefix + output_file if output_file else None

    output_document = None  # a docx Documnet object, or a pdf Object from FPDF, or a buffer

    # sets environ variables and returns tesseract config string
    # TODO add parameters to args or create new dict
    options = config_tesseract(**args)

    display_confidence = args.get('display_confidence')   # display OCR confidence summary if True

    confidence_dict = {}    # to store average confidenece for each image ({image_name: avg_conf})
    for i, image in enumerate(input_images):
        
        # if not join create new output_doc for each image, else use one output_doc for all
        # TODO check system strain when join is True
        if not join:
            output_document = None

        image_file_path = input_path_prefix + image

        # display image processing start
        print("Processing image file no. {}: '{}'".format(i + 1, image_file_path))

        # process image
        # TODO add global variable for simple/detailed choice
        processed_image = process_image_simple(image_file_path, **args)
    
        # other formats image_to_[...] - 'data' with dict option, pdf, box ...
        text = pts.image_to_string(processed_image, config=options)

        # find and store average confidence for each image
        if display_confidence:
            current_image_conf = ocr_confidence(processed_image, options, **args)
            confidence_dict[image_file_path] = current_image_conf
 
        # save output file if not join or this is last page
        # TODO check system strain for too many image inputs with join
        save = not join or (i == len(input_images) - 1)

        # set output file path from input file name for each image.
        # Used when join is False (if True output_file is already set or passed)
        if not output_file and output_mode != 'print':
            output_file_end = path.splitext(image_file_path)[0]  # before extension
            output_file_end = path.split(output_file_end)[1]     # after last '/'
            output_file_end += '-output.' + output_mode
            output_file_path = output_path_prefix + output_file_end

        # to be added after each page if join
        footer = '\n\t\t\t\t\t--- Page {} ---\n\n'.format(i + 1) if join else ''

        # base dict to pass to txt, docx or pdf writer functions
        base_dict = {
            'save': save,    # add common params here (font, layout ...)
            'join': join,
            'page_index': i,
            'input_file_type': 'image'
        }

        # =============== OUTPUT based on output_mode ==============

        if output_mode == 'print':
            print("OUTPUT for image file: '{}':\n".format(image_file_path))
            print(text + footer)

        elif output_mode == 'txt':  # TODO move to separate function
            params = base_dict  # add specific params here
            text += footer
            output_document = write_to_txt(text, output_file_path, output_document, **params)

        elif output_mode == 'docx':
            params = base_dict  # add specific params here
            text += footer
            output_document = write_to_docx(text, output_file_path, output_document, **params)

        elif output_mode == 'pdf':
            params = base_dict
            text += footer
            output_document = write_to_pdf(text, output_file_path, output_document, **params)

        # display successful OCR summary
        if save:
            saved_to = 'stdout' if output_mode == 'print' else path.abspath(output_file_path)
            total_pages = len(input_images)
            if join and total_pages > 1:
                info = "{} images".format(total_pages)
            else:
                info = "image '{}'".format(image_file_path)

            # TODO move conf display to confidence/other separate function
            conf_info = ''  # TODO for verbose display words with low conf
            if display_confidence:
                if join and total_pages > 1:  # display average of each image's average confidence
                    avg_conf_list = confidence_dict.values()
                    avg_conf = round(mean(avg_conf_list), 2)

                else:       # display average confidence for each image
                    avg_conf = current_image_conf
                conf_info = ' with an average confidence of {}%'.format(avg_conf)

            print("Successfuly OCR'ed {}{} and wrote to '{}'\n"
                .format(info, conf_info, saved_to))
