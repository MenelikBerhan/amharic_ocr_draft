#!/usr/bin/env python3
from fpdf import FPDF


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

    pdf = pdf if pdf else FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(True)

    # get params
    font_path = args.get('font_path','/usr/share/fonts/truetype/abyssinica/AbyssinicaSIL-Regular.ttf')
    font_name = args.get('font_name', 'sil')

    # set params
    pdf.add_font(font_name, fname=font_path)
    pdf.set_font(font_name)
    w = args.get('w', 0)
    h = args.get('h', 5)

    # write text
    pdf.multi_cell(w=w, h=h, text=text)

    if args.get('save'):
        pdf.output(output_file_path)

    return(pdf)
    # TODO handle other args for pdf formatting
