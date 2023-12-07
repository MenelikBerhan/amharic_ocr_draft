#!/usr/bin/env python3
"""
Package containing core functions and default variables dictionary.

Attributes:
    defaults_dict (dict): dictionary of default input and output parameters
    tesseract_dict (dict): dictionary of default tesseract options and parameters
    output_dict (dict): dictionary of default params for writing to output files
"""

defaults_dict = {
    'INPUT_DIR_DEFAULT_IMG': 'test_files/images/',      # default directory for image input files
    'INPUT_DIR_DEFAULT_PDF': 'test_files/pdfs/',        # default directory for pdf input files
    'OUTPUT_DIR_DEFAULT': 'test_files/outputs/',        # default directory for output files
    'OUTPUT_MODES': ['print', 'txt', 'docx', 'pdf'],    # available output types(modes)
    'OUTPUT_MODE_DEFAULT': 'print',                     # default output type(mode)
    'IMAGE_EXTENSIONS': ['png', 'jpeg', 'jpg'],         # valid image input files extension
}
"""defaults_dict (dict): dictionary of default input and output parameters"""


tesseract_dict = {
    'TRAINING_DATA_DIR': '/home/menelikberhan/amharic_ocr/training_data_new',   # tesseract training data directory
    'lang': 'amh',      # default language for OCR
    'psm' : 3,          # default page segmentation mode in tesseract
    'oem' : 1,          # default OCR engine mode for tesseract
}
"""tesseract_dict (dict): dictionary of default tesseract options parameters"""


output_dict = {
    'font_path_def': 'fonts/AbyssinicaSIL-Regular.ttf', # default font path (for writing to pdf)
    'font_name_def': 'Abyssinica SIL',                  # default font name (for writing to pdf & MS word)
    'w_def' : 0,            # default line width (for writing to pdf). 0 means use all available width
    'h_def' : 5             # default line spacing (for writing to pdf)
}
"""tesseract_dict (dict): dictionary of default tesseract options parameters"""
