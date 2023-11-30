#!/usr/bin/env python3
import cv2
from os import environ, path, remove
import pytesseract as pts
from sys import argv
import docx
from fpdf import FPDF
from .validate_input import validate_input
from .tesseract_config import config_tesseract
from .output_to_docx import write_to_docx
from .process_image import process_image_simple, process_image_detailed


def image_ocr(**args):
    """Performs OCR on a single image and output to given medium"""

    # validate user inputs
    image_file_path, output_file_path, output_mode = validate_input(**args)

    # # load image
    # image = cv2.imread(image_file_path)
    # # cv2 uses BGR, so convert to RGB
    # rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    processed_image = process_image_detailed(image_file_path)
    # sets environ variables and return dictionary to be used for tesseract
    options = config_tesseract(**args)
    
    # other formats image_to_[...] - 'data' with dict option, pdf, box ...
    text = pts.image_to_string(processed_image, config=options)

    # out put based on output_mode
    if output_mode == 'print':
        print(text)
    else:
        # with open(output_file_path, 'w', encoding='utf-8') as file:
        #     file.write(text)
        if output_mode == 'docx':
            write_to_docx(text, output_file_path)
        # elif output_mode == 'pdf':
        #     write_to_pdf(text, output_file_path)
