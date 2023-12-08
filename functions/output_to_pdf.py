#!/usr/bin/env python3
from fpdf import FPDF
from . import write_dict


def write_to_pdf(text, output_file_path, pdf=None, **args):
    """Writes OCR'ed text to a pdf document.
    
    Args:
        text (str): output from OCR by tesseract.
        output_file_path (str): path (including file name) of output file.
        document (Document): an FPDF class instance representing the pdf document.
            If not provided a new one will be created.
        **args (dict): dictionary of parameters (font, layout ...)
            for formatting document.

    Retruns:
        FPDF instance: an FPDF class instance object (pdf object), with newly added
            page containing text.

    """
    # TODO set and get defaults from module level variables

    # to check if this is the first time setting up pdf
    new_pdf = pdf is None

    pdf = pdf if pdf else FPDF()

    if new_pdf:     # set common pdf properties only for new pdf
        # get params
        # TODO handle font errors (missing the following glyphs:...)
        font_path = args.get('font_path', write_dict.get('font_path_def'))
        font_name = args.get('font_name', write_dict.get('font_name_def'))

        # set params
        pdf.set_auto_page_break(True)
        pdf.add_font(font_name, fname=font_path)
        pdf.set_font(font_name)
        
    w = args.get('w', write_dict.get('width_def'))
    h = args.get('h', write_dict.get('height_def'))
    # add new page
    pdf.add_page()

    # write text
    pdf.multi_cell(w=w, h=h, text=text)

    if args.get('save'):
        pdf.output(output_file_path)

    return(pdf)
    # TODO handle other args for pdf formatting
