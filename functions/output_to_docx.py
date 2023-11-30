#!/usr/bin/env python3
import cv2
import pytesseract as pts
from sys import argv
from os import environ, path, remove
from pdf2image import convert_from_path
from io import BytesIO
from PIL import Image
import numpy as np
import math
import docx


def write_to_docx(text, output_file_path, document=None, **args):

    doc = document if document else docx.Document()
    par = doc.add_paragraph().add_run(text)
    par.font.name = args.get('font_name', 'Abyssinica SIL')
    if args.get('last_page') or args.get('save'):
        doc.save(output_file_path)

    # TODO - handle other args for MSword formatiing

