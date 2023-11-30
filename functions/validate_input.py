#!/usr/bin/env python3
import cv2
from os import environ, path, remove
import pytesseract as pts
from sys import argv
import argparse
def validate_input(**args):
    """Validates user input command by checking:
        * if input file exists
        * if input file is an image or pdf
        * if proper options are provided
        * if output folder exists"""
    
    # INPUT FILE test pdf file location
    input_file_path = args.get('input_file')
    if not input_file_path:
        print("Error: No input file specified")
        exit(1)
    input_file_type = input_file_path.split('.')[-1]
    if input_file_type not in ['pdf', 'jpeg', 'png', 'jpg']:
        print("Error: Invalid Input File Type: {}".format(input_file_type))
        exit(1)

    if '/' in input_file_path:
        input_directory = "/".join(input_file_path.split('/')[:-1])
        input_directory = path.abspath(input_directory)
        input_file = input_file_path.split('/')[-1]
        input_file_path = input_directory + '/' + input_file
    else:
        input_file = input_file_path
        default_input = 'test_files/pdfs/' if input_file_type == 'pdf' else 'test_files/images/'
        input_directory = args.get('input_directory', default_input)
        input_directory = path.abspath(input_directory)
        input_file = input_file_path
        input_file_path = input_directory + '/' + input_file

    # OUTPUT MODE ['print', 'file'] # output directory for 'file' mode
    output_mode = args.get('output_mode', 'print')
    if output_mode not in ['print', 'txt', 'docx', 'pdf']:
        print("Error: Invalid Output Fromat: {}".format(output_mode))
        exit(1)
    output_file_path = args.get('output_file', '')
    if '/' in output_file_path:
        output_directory = "/".join(output_file_path.split('/')[:-1])
        output_directory = path.abspath(output_directory)
        output_file = output_file_path.split('/')[-1]
    else:
        output_directory =  args.get('output_directory', 'test_files/outputs')
        output_directory = path.abspath(output_directory)
        if output_file_path:
            output_mode = output_file_path.split('.')[-1]
            if output_mode not in ['txt', 'docx', 'pdf']:
                print("Error: Invalid Output Fromat: {}".format(output_mode))
                exit(1)
            output_file = output_file_path
        else:
            output_file = input_file.split('.')[0] + '_output.' + output_mode



    # TRAINING DATA directory (if not provieded uses tesseracts default dir)
    # TESSDATA_PREFIX='/home/menelikberhan/amharic_ocr/test_data' (doesnt work)
    # environ['TESSDATA_PREFIX'] = '/home/menelikberhan/amharic_ocr/training_data'


    

    # image_file_path = image_test_directory + test_file

    # check if input file exists
    if not path.exists(input_file_path):
        print("Error: Specified input file '{}' doesn't exist".format(input_file_path))
        exit(1)

    # evaluate absolute file path and remove file if it exists for 'file' output mode
    if output_mode != 'print':
        output_file_path = output_directory + '/' + output_file

        if not path.exists(output_directory):
            print("Error: Specified output directory '{}' doesn't exist".format(output_directory))
            exit(1)

        if path.exists(output_file_path):
            print("Warning: Output file with same name exists.")
            remove(output_file_path)
            print("Removed previous output file '{}' ".format(output_file_path))

    return(input_file_path, output_file_path, output_mode)


# defaults = {'input_file': 'sample_images/img1.png', 'output_file': 'a.docx'}
# print(validate_input(**defaults))