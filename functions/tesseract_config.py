#!/usr/bin/env python3
import cv2
from os import environ, path, remove
import pytesseract as pts
from sys import argv
import docx
from fpdf import FPDF
from .validate_input import validate_input


def config_tesseract(**args):


    training_folder = args.get('training_folder')
    # TRAINING DATA directory (if not provieded uses tesseracts default dir)
    # TESSDATA_PREFIX='/home/menelikberhan/amharic_ocr/test_data' (doesnt work)
    environ['TESSDATA_PREFIX'] = '/home/menelikberhan/amharic_ocr/training_data_new'

    # environ['TESSDATA_PREFIX'] = '/home/menelikberhan/amharic_ocr/training_data'

    # config tesseract options
    lang = 'amh'
    psm = 1         # image processing option (1 & 3 for full page). refer doc.
    options = """-l {} --psm {} --oem 1
    -c load_system_dawg=false
    -c load_freq_dawg=false
    -c textord_space_size_is_variable=1""".format(lang, psm)

    return options