#!/usr/bin/env python3
from os import environ

TRAINING_DATA_DIR = '/home/menelikberhan/amharic_ocr/training_data_new'

def config_tesseract(**args):
    """Creates a string containing options to pass to tesseract based on args.
    
    Args:
        **args (dict): dictionary containing custom parameters

    Returns:
        str: A string to be used for tesseract configuration.
    """

    training_folder = args.get('training_folder')  # TODO check if it contains training data
    
    # TRAINING DATA directory (if not provieded uses tesseracts default dir)
    environ['TESSDATA_PREFIX'] = training_folder if training_folder else TRAINING_DATA_DIR


    # config tesseract options
    # TODO add config params to **args from calling function & handle here
    lang = args.get('lang', 'amh')
    psm = args.get('psm', 3)        # image processing option (1 & 3 for full page). refer doc.
    oem = args.get('oem', 1)        # refer doc
    options = """
    -l {} --psm {} --oem {}
    -c load_system_dawg=false
    -c load_freq_dawg=false
    -c textord_space_size_is_variable=1
    """.format(lang, psm, oem)

    return options