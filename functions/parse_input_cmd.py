#!/usr/bin/env python3
"""
Module containing command line input parsing (converting to keyword dict)
functions.
"""
import argparse
from pprint import pprint
from shlex import split


class ArgumentParser(argparse.ArgumentParser):
        """
        Custom argument parser class inherited from argparse.
        """
        def error(self, message):
            """Override default error handling to prevent default
            error display and system exit"""
            # print("ERRRRR")
            raise(Exception(message))


def parse_cmd(line):
    """Parses user input from command line and create a keyword dictionary.
    
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

    parser.add_argument('-m', '--output-mode', dest='output_mode', choices=['print', 'txt', 'docx', 'pdf'], required=False, nargs=1, metavar='output_mode')

    parser.add_argument('-j', '--join', action='store_true', help='join outputs from multiple inputs into one file')

    parser.add_argument('-v', '--verbose', action='store_true', help='display details of OCR (Confidence level, total pages ...)')

    try:
        args = parser.parse_args(split(line))
        # print('\n----PARSE_INPUT RETURN-------')
        # pprint(vars(args))
        return(vars(args))
    except Exception as e:
        print('*** Argument Error:', e)
        return (None)