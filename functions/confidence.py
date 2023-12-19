#!/usr/bin/env python3
"""
Module for functions related to tesseract OCR confidence.
"""
import pytesseract as pts
from pprint import pprint
from statistics import mean, stdev

def ocr_confidence(processed_image, options, **args):
    """Extracts OCR confidence summary from tesseract's dict return.

    Args:
        processed_image (image): an image object preprocessed using OpenCV2.
        options (dict): a dictionary to be used for tesseract config
        **args (dict): a dictionary of params from user input for ocr command

    Returns:
        int: average confidence level of OCR for all words in image.
    """
    # TODO extract text, replacing empty words with newline
    ocr_dict = pts.image_to_data(processed_image, config=options, output_type=pts.Output.DICT)

    # list of confidence level and words (including empty strings)
    conf_list = ocr_dict['conf']
    text_list = ocr_dict['text']
    # par_num = ocr_dict['par_num']
    # line_num = ocr_dict['line_num']
    # word_num = ocr_dict['word_num']

    # extract confidence list for non empty word strings
    valid_index = [i for i, word in enumerate(text_list) if word]
    valid_conf_list = [conf for i, conf in enumerate(conf_list)
                       if i in valid_index]

    # TODO if verbose: calc stdev and display words with conf < mean - k*stdev (k=1 or 2)
    # print('PAR\tLINE\tCONF\tTEXT\tIN_AVG_CALC')
    # for i in range(len(conf_list)):
    #     print('{}\t{}\t{}\t{}\t{}'.format(
    #         par_num[i], line_num[i], conf_list[i], text_list[i], i in valid_index))

    return(round(mean(valid_conf_list), 2))
