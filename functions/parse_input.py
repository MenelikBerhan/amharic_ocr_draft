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

INPUT_DIR_DEFAULT_IMG = 'test_files/imgaes/'
INPUT_DIR_DEFAULT_PDF = 'test_files/pdfs/'
OUTPUT_DIR_DEFAULT = 'test_files/outputs/'
OUTPUT_MODE_DEFAULT = 'print'

usage = """[image|pdf] INPUT_FILE [OUTPUT_FILE] [-d OUTPUT_DIR] [OPTION]...
   or: [image|pdf] [-i] INPUT_FILE... [-jo OUTPUT_FILE] [-d OUTPUT_DIR] [OPTION]...
   or: image|pdf -s INPUT_DIR [-jo OUTPUT_FILE] [-d OUTPUT_DIR] [OPTION]...

OCR INPUT_FILE or INPUT_FILES, and output to OUTPUT_FILE in OUTPUT_DIR.
OCR INPUT_FILES in INPUT_DIR, and output to OUTPUT_FILE in OUTPUT_DIR.

Specifying image|pdf is mandatory only when passing INPUT_DIR using -s flag.

Multiple INPUT_FILEs can be passed without the -i flag.

Specifying -o flag for OUTPUT_FILE is madatory only when passing multiple inputs
(with or without the -i flag) or when passing INPUT_DIR using -s flag.

When passing OUTPUT_FILE along with multiple input files the -j flag must be used
to join output files.


Mandatory arguments to long options are mandatory for short options too.
-i, --input-files=INPUT_FILE...     pass multiple input files. Must use the -o flag for
                                    OUTPUT_FILE if -i flag is used for input files.
-s, --src-dir=INPUT_DIR             use all images|pdfs in the specified INPUT_DIR directory
                                    as input files. Must specify image|pdf. Must use the -o
                                    flag for output file.
-o, --output-file=OUTPUT_FILE       save output with provided file name. Can pass destination
                                    directory by prefixing it to OUTPUT_FILE.
-d, --dest-dir=OUTPUT_DIR           save output file in the specified OUTPUT_DIR directory.
-j, --join                          output to a single file. If not used when passing multiple
                                    input files, an output file is created for each input file.
-m, --mode=['print', 'txt', 'pdf', 'docx']  specify output mode. Default 'print' to stdout.
                                    'txt' to text, 'docx' to MSword and 'pdf' to pdf file.
"""


class ArgumentParser(argparse.ArgumentParser):
        """
        Custom argument parser class inherited from argparse.
        """
        def error(self, message):
            """Override default error handling to prevent default
            error display and system exit"""
            print("ERRRRR")
            raise(Exception(message))


def parse_cmd(self, line):
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

    parser.add_argument('-s', '--source-directory', dest='input_directory', nargs=1, required=False, default=INPUT_DIR_DEFAULT_IMG, metavar='source_directory')

    parser.add_argument('output_file', nargs='?')
    parser.add_argument('-o', '--output-file', dest='output_file', nargs=1, required=False, metavar='outptut_file')

    parser.add_argument('-d', '--dest-directory', dest='output_directory', nargs=1, required=False, default=OUTPUT_DIR_DEFAULT, metavar='destination_directory')

    parser.add_argument('-m', '--output-mode', dest='output_mode', choices=['print', 'txt', 'docx', 'pdf'], required=False, default=OUTPUT_MODE_DEFAULT, nargs=1, metavar='output_mode')

    parser.add_argument('-j', '--join', action='store_true', help='join outputs from multiple inputs into one file')

    parser.add_argument('-v', '--verbose', action='store_true', help='display details of OCR (Confidence level, total pages ...)')
    try:
        args = parser.parse_args(split(line))
        print(args)
        pprint(vars(args))
    except Exception as e:
        print('here', e.args)
