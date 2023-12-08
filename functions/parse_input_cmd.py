#!/usr/bin/env python3
"""
Module containing command line input parsing (converting to keyword dict)
functions.
"""
import argparse
from pprint import pprint
from shlex import split
from . import defaults_dict

class ArgumentParser(argparse.ArgumentParser):
        """
        Custom argument parser class inherited from argparse.
        """
        def error(self, message):
            """Override default error handling to prevent default
            error display and system exit"""
            raise(Exception(message))


def parse_ocr_cmd(line):
    """Parses user input from command line for ocr commands (`image` and `pdf`) and creates a keyword dictionary.
    
    Args:
        line (str): command line user input

    Returns:
        dict: If successful a keyword dictionary parsed from user input,
            else None.

    Raises:
    """
    parser = ArgumentParser(
        prog='ocr',
        allow_abbrev=False, # to avoid recognition of abbreviated long options
        # argument_default=argparse.SUPPRESS,  # to globally suppress attribute creation for optional arguments and options (nargs='?')
        # exit_on_error=False, # prevent exit on errors (not available in python 3.8)
        usage=argparse.SUPPRESS, # to suppress usage display
        # usage=usage
        add_help=False  # so that -h flag doesn't display argparse help
        )

    parser.add_argument('input_file_type', choices=['image', 'pdf'], nargs='?')  # ?? nargs='?'

    parser.add_argument('input_file', nargs='?')
    parser.add_argument('-i', '--input-file', dest='input_files', nargs='+', required=False, metavar='input_files')

    parser.add_argument('-s', '--source-directory', dest='input_directory', nargs=1, required=False, metavar='input_directory')

    parser.add_argument('output_file', nargs='?')
    parser.add_argument('-o', '--output-file', dest='output_file', nargs=1, required=False, metavar='outptut_file')

    parser.add_argument('-d', '--dest-directory', dest='output_directory', nargs=1, required=False, metavar='output_directory')

    parser.add_argument('-m', '--output-mode', dest='output_mode', choices=defaults_dict.get('OUTPUT_MODES'), required=False, nargs=1, metavar='output_mode')

    parser.add_argument('-j', '--join', action='store_true', help='join outputs from multiple inputs into one file')

    parser.add_argument('-v', '--verbose', action='store_true', help='display details of OCR (Confidence level, total pages ...)')

    try:
        args = parser.parse_args(split(line))
        return(vars(args))
    except Exception as e:
        print('*** Argument Error:', e)
        return (None)


def parse_default_cmd(line):
    """Parses user input from command line for the `default` command.
    
    Args:
        line (str): command line user input after `default` command

    Returns:
        dict: If successful a keyword dictionary parsed from user input,
            else None.

    Raises:
    """
    parser = ArgumentParser(
        prog='default',
        allow_abbrev=False, # to avoid recognition of abbreviated long options
        usage=argparse.SUPPRESS, # to suppress usage display
        add_help=False  # so that -h flag doesn't display argparse help
        )

    # TODO validate argument values in a separate function

    parser.add_argument('-ii', '--in-dir-image', dest='input_dir_def_img', required=False, nargs=1, metavar='input_dir_default_img', help='Set default input directory for images')

    parser.add_argument('-ip', '--in-dir-pdf', dest='input_dir_def_pdf', required=False, nargs=1, metavar='input_dir_default_pdf', help='Set default input directory for pdfs')

    parser.add_argument('-o', '--out-dir', dest='output_dir_def', required=False, nargs=1, metavar='output_dir_default', help='Set default output directory')

    parser.add_argument('-m', '--output-mode', dest='output_mode_def', choices=defaults_dict.get('OUTPUT_MODES'), required=False, nargs=1, metavar='output_mode_default', help='Set default output mode (file type)')

    parser.add_argument('-td', '--train-dir', dest='train_dir', required=False, nargs=1, metavar='train_dir', help='Set default tesseract training data directory')

    parser.add_argument('-tl', '--lang', dest='lang', required=False, nargs=1, choices=['amh', 'eng', 'tir'], metavar='lang', help='Set default tesseract OCR language')

    parser.add_argument('-tp', '--psm', dest='psm', required=False, nargs=1, choices=list(range(14)), metavar='psm', help='Set default tesseract page segmentation mode')

    parser.add_argument('-to', '--oem', dest='oem', required=False, nargs=1, choices=list(range(4)), metavar='oem', help='Set default tesseract OCR engine mode')

    parser.add_argument('-fp', '--font-path', dest='font_path', required=False, nargs=1, metavar='font_path', help='Set default font path, to be used for writing output to pdf')

    parser.add_argument('-fn', '--font-name', dest='font_name', required=False, nargs=1, metavar='font_name', help='Set default font name, to be used for writing output to pdf and MS word')

    parser.add_argument('-w', '--width', dest='w', required=False, nargs=1, metavar='width', help='Set default line width for writing output to pdf')

    parser.add_argument('-h', '--height', dest='h', required=False, nargs=1, metavar='line_height', help='Set default line height for writing output to pdf')

    try:
        args = parser.parse_args(split(line))
        return(vars(args))
    except Exception as e:
        print('*** Argument Error:', e)
        return (None)
