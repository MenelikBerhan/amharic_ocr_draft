#!/usr/bin/env python3
"""
Package containing core functions and default variables dictionary.

Attributes:
    defaults_dict (dict): dictionary of default input and output parameters
    tesseract_dict (dict): dictionary of default tesseract options and parameters
    output_dict (dict): dictionary of default params for writing to output files
"""
# TODO save defaults in text file(json form) for persistence
# TODO store last 20 commands

defaults_dict = {
    'input_dir_def_img': 'test_files/images/',      # default directory for image input files
    'input_dir_def_pdf': 'test_files/pdfs/',        # default directory for pdf input files
    'output_dir_def': 'test_files/outputs/',        # default directory for output files
    'output_modes': ['print', 'txt', 'docx', 'pdf'],    # available output types(modes)
    'output_mode_def': 'print',                     # default output type(mode)
    'image_extensions': ['png', 'jpeg', 'jpg'],         # valid image input files extension
}
"""defaults_dict (dict): dictionary of default input and output parameters"""


tesseract_dict = {
    'training_dir_def': 'training_data/fast',   # default tesseract training data directory
    'lang_def': 'amh',      # default language for OCR
    'psm_def' : 3,          # default page segmentation mode in tesseract
    'oem_def' : 1,          # default OCR engine mode for tesseract
}
"""tesseract_dict (dict): dictionary of default tesseract options and parameters"""


write_dict = {
    'font_path_def': 'fonts/AbyssinicaSIL-Regular.ttf', # default font path (for writing to pdf)
    'font_name_def': 'Abyssinica SIL',                  # default font name (for writing to pdf & MS word)
    'width_def' : 0,            # default line width (for writing to pdf). 0 means use all available width
    'height_def' : 5             # default line height (for writing to pdf)
}
"""write_dict (dict): dictionary of default ouput file writing options and parameters"""
