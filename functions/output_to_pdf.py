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
from fpdf import FPDF


def write_to_pdf(text, output_file_path, pdf=None, **args):

    pdf = pdf if pdf else FPDF()
    pdf.add_page()
    font_path = args.get('font_path', '/usr/share/fonts/truetype/abyssinica/AbyssinicaSIL-Regular.ttf')
    font_name = args.get('font_name', 'sil')
    pdf.add_font(font_name, fname=font_path)
    pdf.set_font(font_name)
    pdf.set_auto_page_break(True)
    # pdf.cell(text=text)
    w = args.get('w', 0)
    h = args.get('h', 5)
    pdf.multi_cell(w=w, h=h, text=text)
    if args.get('last_page') or args.get('save'):
        pdf.output(output_file_path)

    # TODO handle other args for pdf formatting
