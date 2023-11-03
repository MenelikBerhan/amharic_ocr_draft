#!/usr/bin/python3
import cv2
import pytesseract as pts
from sys import argv
from os import environ, path, remove
from pdf2image import convert_from_path
from io import BytesIO
from PIL import Image
import numpy as np


# OUTPUT MODE ['print', 'file'] # output directory for 'file' mode
output_mode = 'file'
output_directory = path.abspath('test_files/outputs')


# INPUT FILE test pdf file location
pdf_test_directory = 'test_files/pdfs/'
test_file = 'kidane_wolde_dictionary_3pgs.pdf'  # no '.' in file name


# PAGE LOADING MODE from pdf ['bytes', 'file']
# 'bytes': as buffer w/o saving to disk, 'file': by saving individual images to disk
page_loading_mode = 'bytes'


# TRAINING DATA directory (if not provieded uses tesseracts default dir)
# TESSDATA_PREFIX='/home/menelikberhan/amharic_ocr/test_data' (doesnt work)
environ['TESSDATA_PREFIX'] = '/home/menelikberhan/amharic_ocr/training_data'

################ END OF CONFIG #################





################ PROGRAM ENTRY #################

pdf_file_path = pdf_test_directory + test_file

# check if input file exists
if not path.exists(pdf_file_path):
    print("Error: Specified input file '{}' doesn't exist".format(pdf_file_path))
    exit(1)

# read pdf
pages = convert_from_path(pdf_file_path)


# evaluate absolute file path and remove file if it exists for 'file' output mode
if output_mode == 'file':
    output_file = test_file.split('.')[0] + '_output.txt'
    output_file_path = output_directory + '/' + output_file

    if not path.exists(output_directory):
        print("Error: Specified output directory '{}' doesn't exist".format(output_directory))
        exit(1)

    if path.exists(output_file_path):
        print("Warning: Output file with same name exists.")
        remove(output_file_path)
        print("Removed previous output file '{}' ".format(output_file_path))

    page_no = 1


# iterate over pdf pages
for page in pages:

    # use BytesIO object, without saving to disk
    with BytesIO() as img_stream:

        print('Scanning page #{}"'.format(page_no))

        # specify format to save in bytes object
        page.save(img_stream, format="jpeg")  # test different formats quality?

        """ # if reading and writing from disk (page_loading_mode = 'file')
            image_path = "page_image.jpg"
            page.save(image_path, "jpg")
            image = cv2.imread(image_path) """

        img_stream.seek(0)
        
        # load image with cv2 using numpy on buffer for page_loading_mode='bytes' 
        image = cv2.imdecode(np.frombuffer(img_stream.read(), np.uint8), 1)
        
        # cv2 uses BGR, so convert to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


        # config tesseract options
        lang = 'amh'
        psm = 1         # image processing option (1 & 3 for full page). refer doc.
        options = "-l {} --psm {}".format(lang, psm)


        # other formats image_to_[...] - 'data' with dict option, pdf, box ...
        text = pts.image_to_string(rgb_image, config=options)

        # out put based on output_mode
        if output_mode == 'print':
            print(text)

        elif output_mode == 'file':
            with open(output_file_path, 'a', encoding='utf-8') as file:
                footer = '\n\n\t{} Page # {} {}\n\n'.format('-' * 20, page_no, '-' * 20)
                page_no += 1
                file.write(text + footer)


print('Saved #{} number of pages in file: "{}"'.format(page_no - 1, output_file_path))
