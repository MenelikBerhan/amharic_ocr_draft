#!/usr/bin/env python3
"""
Module containing command line input parsing (converting to keyword dict)
functions.

Attributes:
    INPUT_DIR_DEFAULT_IMG (str): default input directory for images.
    INPUT_DIR_DEFAULT_PDF (str): default input directory for pdfs.
    OUTPUT_DIR_DEFAULT (str): default output directory.
    OUTPUT_MODE_DEFAULT (str): default output mode.
        Available options - ['print', 'txt', 'docx', 'pdf'].
"""
import argparse
from pprint import pprint
from shlex import split

INPUT_DIR_DEFAULT_IMG = 'test_files/images/'
INPUT_DIR_DEFAULT_PDF = 'test_files/pdfs/'
OUTPUT_DIR_DEFAULT = 'test_files/outputs/'
OUTPUT_MODE_DEFAULT = 'print'

usage = """[image|pdf] INPUT_FILE [OUTPUT_FILE] [OPTION]...
   or: [image|pdf] -i INPUT_FILE... [-o OUTPUT_FILE] [OPTION]...
   or: image|pdf -s INPUT_DIR [-o OUTPUT_FILE] [OPTION]...

OCR INPUT_FILE/s and output to OUTPUT_FILE.

OCR INPUT_FILE/s or all image|pdf files in INPUT_DIR,
and output to OUTPUT_FILE.

Multiple INPUT_FILEs can be passed with the -i flag. All inputs must be
of the same file type. Types - image [*(.jpeg|.png|.jpg)] or pdf [*.pdf].

Specifying image|pdf prefix is mandatory only when passing INPUT_DIR
without preceeding INPUT_FILE/s. Otherwise, will be inferred from
INPUT_FILE/s extention.

If OUTPUT_FILE is passed along with multiple input files (using -i flag)
and/or with INPUT_DIR (using -s flag), must use the -o flag.


Mandatory arguments to long options are mandatory for short options too.

-i, --input-files=INPUT_FILE...     pass multiple input files. Must use the -o flag for
                                    OUTPUT_FILE.

-s, --src-dir=INPUT_DIR             specify INPUT_FILE/s' directory. If no INPUT_FILE is
                                    also passed, must specify image|pdf prefix and will use
                                    all images|pdfs in INPUT_DIR directory as input files.

                                    If INPUT_FILE/s is/are also passed, and is/are a path
                                    (contains /), INPUT_DIR will be ignored.

                                    Must use the -o flag for OUTPUT_FILE.

-o, --output-file=OUTPUT_FILE       save output with provided file name. Implies -j flag.
                                    Can pass destination directory by prefixing it to OUTPUT_FILE. 

                                    If OUTPUT_FILE has a valid extention ('.txt'|'.docx'|'.pdf'),
                                    will implicitly override output file type specified by -m.

-d, --dest-dir=OUTPUT_DIR           save output file/s in the specified OUTPUT_DIR directory.
                                    If OUTPUT_FILE is also passed and is a path (contains /),
                                    OUTPUT_DIR will be ignored.

-j, --join                          output to a single file. If not used when passing multiple
                                    input files without an OUTPUT_FILE, an output file is created
                                    for each input file.

-m, --mode='print'|'txt'|'pdf'|'docx'                   specify output mode (output file type).
                                    'print' to stdout (default), 'txt' to text, 'docx' to MSword
                                    and 'pdf' to pdf file.

-v, --verbose                       display details of OCR (Confidence level, total pages ...)
"""


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
        dict: a keyword dictionary parsed from user input.

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

    parser.add_argument('input_file_type', choices=['image', 'pdf'], nargs='?')

    parser.add_argument('input_file', nargs='?')
    parser.add_argument('-i', '--input-file', dest='input_files', nargs='+', required=False, metavar='input_files')

    parser.add_argument('-s', '--source-directory', dest='input_directory', nargs=1, required=False, default=INPUT_DIR_DEFAULT_IMG, metavar='input_directory')

    parser.add_argument('output_file', nargs='?')
    parser.add_argument('-o', '--output-file', dest='output_file', nargs=1, required=False, metavar='outptut_file')

    parser.add_argument('-d', '--dest-directory', dest='output_directory', nargs=1, required=False, default=OUTPUT_DIR_DEFAULT, metavar='output_directory')

    parser.add_argument('-m', '--output-mode', dest='output_mode', choices=['print', 'txt', 'docx', 'pdf'], required=False, default=OUTPUT_MODE_DEFAULT, nargs=1, metavar='output_mode')

    parser.add_argument('-j', '--join', action='store_true', help='join outputs from multiple inputs into one file')

    parser.add_argument('-v', '--verbose', action='store_true', help='display details of OCR (Confidence level, total pages ...)')

    try:
        args = parser.parse_args(split(line))
        # print(args)
        pprint(vars(args))
    except Exception as e:
        print('*** Argument Error:', e)
