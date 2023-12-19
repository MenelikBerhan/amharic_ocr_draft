#!/usr/bin/env python3
"""
Contains a function to set defeault parameters value.
"""

from . import defaults_dict, tesseract_dict, write_dict

defaults_reset_dict = {
    'defaults_dict': {
        'input_dir_def_img': 'test_files/images/',          # default directory for image input files
        'input_dir_def_pdf': 'test_files/pdfs/',            # default directory for pdf input files
        'output_dir_def': 'test_files/outputs/',            # default directory for output files
        'output_modes': ['print', 'txt', 'docx', 'pdf'],    # available output types(modes)
        'output_mode_def': 'print',                         # default output type(mode)
        'image_extensions': ['png', 'jpeg', 'jpg']},        # valid image input files extension

    'tesseract_dict': {
        'training_dir_def': 'training_data_new',   # default tesseract training data directory
        'lang_def': 'amh',      # default language for OCR
        'psm_def' : 3,          # default page segmentation mode in tesseract
        'oem_def' : 1},         # default OCR engine mode for tesseract

    'write_dict': {
        'font_path_def': 'fonts/AbyssinicaSIL-Regular.ttf', # default font path (for writing to pdf)
        'font_name_def': 'Abyssinica SIL',                  # default font name (for writing to pdf & MS word)
        'width_def' : 0,        # default line width (for writing to pdf). 0 means use all available width
        'height_def' : 5}       # default line height (for writing to pdf)
    }
"""dict: dictionary containg default params, to be used for resetting default params"""


def set_defaults(**args):
    """Sets default params in `defaults_dict`, `tesseract_dict`
    and `write_dict` dictionaries by using params from `args`
    
    Args:
        **args (dict): parsed and validated dictionary created from user input,
            contains keys [defaults_dict, tesseract_dict, write_dict] with dict values.

    """
    defaults_update = args.get('defaults_dict')
    defaults_update = {param: value for param, value in defaults_update.items() if value is not None}

    tesseract_update = args.get('tesseract_dict')
    tesseract_update = {param: value for param, value in tesseract_update.items() if value is not None}

    write_update = args.get('write_dict')
    write_update = {param: value for param, value in write_update.items() if value is not None}

    defaults_dict.update(defaults_update)
    tesseract_dict.update(tesseract_update)
    write_dict.update(write_update)

    # TODO - save defaults in a file using json
    # TODO - handle defaults reset
