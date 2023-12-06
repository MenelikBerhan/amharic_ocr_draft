#!/usr/bin/env python3
import docx


def write_to_txt(text, output_file_path, output_document, **args):
    """Writes OCR'ed text to plain text file.

    Args:
        text (str): output from OCR by tesseract.
        output_file_path (str): path (including file name) of output file.
        output_document (str): buffer to store text from inputs
        **args (dict): dictionary of parameters for formatting output text.

    """
    # TODO check if buffer size passes treshold and write to file

    join = args.get('join')
    pdf_index = args.get('pdf_index')
    page_index = args.get('page_index')
    input_file_type = args.get('input_file_type')

    # if join: truncate for 1st page of 1st pdf, then append
    # if not join: truncate for 1st page of each pdf, then append
    if join and input_file_type == 'pdf':
        write_mode = 'w' if pdf_index == 0 and page_index == 0 else 'a'
    else:
        write_mode = 'w' if page_index == 0 else 'a'

    with open(output_file_path, write_mode, encoding='utf-8') as file:
        file.write(text)

    return (output_document)