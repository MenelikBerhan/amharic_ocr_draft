#!/usr/bin/env python3
"""
Contains a function to validate parsed user input.

Attributes:
    INPUT_DIR_DEFAULT_IMG (str): default input directory for images.
    INPUT_DIR_DEFAULT_PDF (str): default input directory for pdfs.
    OUTPUT_DIR_DEFAULT (str): default output directory.
    OUTPUT_MODES (list): available output modes.
    OUTPUT_MODE_DEFAULT (str): default output mode.
    IMAGE_EXTENSIONS (list): list of valid image extensions.
"""
from os import listdir, path
from pprint import pprint
from . import defaults_dict, tesseract_dict, write_dict


# TODO break up function into parts based on what it validates
# TODO for input output file/dir in current working directory
    # For now must prefix with './'

def validate_parsed_ocr_cmd(line, **args):
    """Validates user input command by checking:
        * if command has valid syntax
        * if required arguments exist and are valid
        * if proper combination of arguments and options are provided
        * if valid input file/s exist
        * if output folder exists

    Args:
        line (str): input from command line.
        **args (dict): input parsed into dict using argparse.

    Returns:
        dict: If successful a validated keyword dictionary, else None.

    Raises:
    """

    # check if either input_file or input_files is None
    # Both not None: incorrect syntax (a.png -i b.png ...)
    input_file = args.get('input_file')  # str or None
    input_files = args.get('input_files')  # list or None
    if (input_file and input_files):
        print('*** Syntax Error: input file specified before -i option')
        return (None)

    # for multiple inputs check if no input is repeated
    if input_files:
        counts = list(map(input_files.count, input_files))
        repeats_index = [i for i, c in enumerate(counts) if c > 1]
        if repeats_index:
            print("*** Input Error: repeated input file: '{}'"
                  .format(input_files[repeats_index[0]]))
            return (None)

    input_directory = args.get('input_directory')  # list or None
    input_directory = input_directory[0] if input_directory else input_directory
    # If both input_file and input_files are None, input_directoy must be present
    if (not (input_file or input_files)) and (not input_directory):
        print('*** Argument Error: neither input file/s or input directory passed')
        return (None)

    # If input_file/s contain path, input_directory must be None
    # TODO if only part of input_files contain path
    if input_directory and (
        (input_file and '/' in input_file) or
        (input_files and any(['/' in i for i in input_files]))
        ):
            print('*** Argument Error: input directory passed while input file/s contain path')
            return (None)


    # ========= Get default params from dict ====================

    IMAGE_EXTENSIONS = defaults_dict.get('image_extensions')
    OUTPUT_MODES = defaults_dict.get('output_modes')
    INPUT_DIR_DEFAULT_IMG = defaults_dict.get('input_dir_def_img')
    INPUT_DIR_DEFAULT_PDF = defaults_dict.get('input_dir_def_pdf')
    OUTPUT_DIR_DEFAULT = defaults_dict.get('output_dir_def')
    OUTPUT_MODE_DEFAULT = defaults_dict.get('output_mode_def')

    # ===========================================================


    input_file_type = args.get('input_file_type')
    # Check if input_file/s exist their extensions are of the same input type and
    # matches input_file_type: (.pdf for pdf) and (.png, .jpeg, .jpg for image)
    if (input_file or input_files):
        inputs = input_files if input_files else [input_file]
        extensions = [i.split('.')[-1] for i in inputs]
        all_pdf = all([ext == 'pdf' for ext in extensions])
        all_image = all([ext in IMAGE_EXTENSIONS for ext in extensions])
        if not(all_image or all_pdf):
            print('*** Input Error: input files must be of the same type. Either image (.jpeg|.png|.jpg) or pdf (.pdf).')
            return (None)
        check_input_type = 'image' if all_image else 'pdf'
        # if input_file_type (image|pdf) is not None, must match input file/s type
        if (input_file_type and input_file_type != check_input_type):
            print('*** Input Error: image|pdf input file type prefix must match input file/s')
            return (None)


    output_file = args.get('output_file')  # list when passed with -o flag, else string/None
    output_file = output_file[0] if type(output_file) == list else output_file
    output_directory = args.get('output_directory')  # list or None
    output_directory = output_directory[0] if output_directory else output_directory
    output_mode = args.get('output_mode')  # list or None. Verified by argparse
    output_mode = output_mode[0] if output_mode else output_mode

    # check if output file is passed with valid extension
    # and if extension matches any arg passed with -m
    # TODO flag commands like `1.png 3.png -o test.pdf`
    # Now 1.png is used as single input file & 3.png ignored
    if output_file:
        ouput_extension = output_file.split('.')[-1]
        if (ouput_extension not in OUTPUT_MODES):
            print("*** Input Error: output file with invalid extension: '{}'".format(ouput_extension))
            return (None)
        if output_mode and output_mode != ouput_extension:
            print(
                "*** Input Error: output file extension '{}' does not match output mode '{}'".
                format(ouput_extension, output_mode))
            return (None)
        # set output_mode from file extension
        output_mode = output_mode if output_mode else ouput_extension

    # check if output directory is passed while output file has path
    if output_file and ('/' in output_file and output_directory):
        print('*** Argument Error: output directory passed while output file contain path')
        return (None)


    # ======== Set inputs, path_in_inputs/output and input/output dir ========

    inputs = input_files if input_files else ([input_file] if input_file else [])  # list of string or []
    path_in_inputs = any(['/' in i for i in inputs])
    if not (input_directory or path_in_inputs):
        # set default directories
        input_directory = INPUT_DIR_DEFAULT_IMG if input_file_type == 'image' else INPUT_DIR_DEFAULT_PDF

    path_in_output = output_file and '/' in output_file
    if not (output_directory or path_in_output):
        output_directory = OUTPUT_DIR_DEFAULT

    # ========================================================================


    # Check if passed or default input directory exists and is dir
    if input_directory:  # None if path in input_file/s
        if not path.exists(input_directory):
            print("*** Input Error: input directory '{}' does not exist".format(input_directory))
            return (None)
        if not path.isdir(input_directory):
            print("*** Input Error: input directory '{}' is not a directory".format(input_directory))
            return (None)

    # Check if inputs exist (in input_dir if no path in inputs)
    prefix = '' if path_in_inputs else input_directory
    prefix += '/' if prefix and prefix[-1] != '/' else ''
    for inp in inputs:
        if not path.exists(prefix + inp):
            print("*** Input Error: input file '{}' does not exist".format(prefix + inp))
            return (None)

    # Check if files with input_file_type exist in input_directory
    if not inputs:  # use files in input_directory
        files_in_dir = listdir(input_directory)
        if input_file_type == 'pdf':
            inputs = [f for f in files_in_dir if f.split('.')[-1] == 'pdf']
        elif input_file_type == 'image':
            inputs = [f for f in files_in_dir if f.split('.')[-1] in IMAGE_EXTENSIONS]
        if not inputs:
            print("*** Input Error: no '{}' file in '{}'".format(input_file_type, input_directory))
            return (None)

    # if $ in output file or directory expand it from shell vars
    if output_file and '$' in output_file:
        output_file = path.expandvars(output_file)
    if output_directory and '$' in output_directory:
        output_directory = path.expandvars(output_directory)

    output_dir_check = path.split(output_file)[0] if not output_directory else output_directory
    # Check if output_dir exists and is dir
    if not path.exists(output_dir_check):
        print("*** Input Error: output directory '{}' does not exist".format(output_dir_check))
        return (None)
    if not path.isdir(output_dir_check):
        print("*** Input Error: output directory '{}' is not a directory".format(output_dir_check))
        return (None)
    
    # set -j (join) to true if output_file
    join = args.get('join')
    join = True if output_file else join

    # set default output mode if None
    output_mode = output_mode if output_mode else OUTPUT_MODE_DEFAULT

    # TODO check if output_file already exist in output_dir,
    # and prompt for deletion/overwriting confirmation from user

    verbose = args.get('verbose')
    result = {
        'input_directory': input_directory,
        'input_files': inputs,
        'input_file_type': input_file_type,
        'join': join,
        'output_directory': output_directory,
        'output_file': output_file,
        'output_mode': output_mode,
        'verbose': verbose
        }

    """
    BY NOW: (changed attrs in args)
        input_file_type: image|pdf
        inputs: list of input files (from input_file/s or input_directory)
        input_directory: None if path in inputs (passed or default)

        output_mode: From -m/output_file, or default
        output_file: string/None (un altered)
        output_dir: None if path in output_file (passed or default)

        join: set to True if output_file. (else unaltered)
    """
    return (result)


def validate_parsed_defalt_cmd(line, **args):
    """Validates user input for `defalut` command by checking:
        * if command has valid syntax
        * if required arguments exist and are valid
        * if proper combination of arguments and options are provided
        * if valid input file/s exist
        * if output folder exists

    Args:
        line (str): input from command line.
        **args (dict): input parsed into dict using argparse.

    Returns:
        dict: If successful a validated keyword dictionary, else None.

    Raises:
    """
    
    # get params. all values, if not None, are list of one
    input_directory_img = args.get('input_directory_img')
    if input_directory_img:
        input_directory_img = input_directory_img[0]
        if not path.exists(input_directory_img):
            print("*** Input Error: image input directory '{}' does not exist".format(input_directory_img))
            return (None)
        if not path.isdir(input_directory_img):
            print("*** Input Error: image input directory '{}' is not a directory".format(input_directory_img))
            return (None)
        # TODO check if images exist

    input_directory_pdf = args.get('input_directory_pdf')
    if input_directory_pdf:
        input_directory_pdf = input_directory_pdf[0]
        if not path.exists(input_directory_pdf):
            print("*** Input Error: pdf input directory '{}' does not exist".format(input_directory_pdf))
            return (None)
        if not path.isdir(input_directory_pdf):
            print("*** Input Error: pdf input directory '{}' is not a directory".format(input_directory_pdf))
            return (None)
        # TODO check if pdfs exist

    output_directory = args.get('output_directory')
    if output_directory:
        output_directory = output_directory[0]
        if not path.exists(output_directory):
            print("*** Input Error: pdf input directory '{}' does not exist".format(output_directory))
            return (None)
        if not path.isdir(output_directory):
            print("*** Input Error: pdf input directory '{}' is not a directory".format(output_directory))
            return (None)

    output_mode = args.get('output_mode')   # checked for valid values by argparse
    if output_mode:
        output_mode = output_mode[0]


    font_name = args.get('font_name')
    if font_name:
        font_name = font_name[0]
    # TODO list available fonts in fonts directory
    font_path = args.get('font_path')
    if font_path:
        font_path = font_path[0]
        if not path.exists(font_path):
            print("*** Input Error: font path '{}' does not exist".format(font_path))
            return (None)
        # TODO if font file is valid

    height = args.get('height') # checked for type=int by argparse
    if height:
        height = height[0]
    width = args.get('width')   # checked for type=int by argparse
    if width:
        width = width[0]


    training_dir = args.get('training_dir')
    if training_dir:
        training_dir = training_dir[0]
        if not path.exists(training_dir):
            print("*** Input Error: training directory '{}' does not exist".format(training_dir))
            return (None)
        # TODO if training directory contains valid training file

    lang = args.get('lang')     # checked for valid values by argparse
    if lang:
        lang = lang[0]
    psm = args.get('psm')       # checked for valid values by argparse
    if psm:
        psm = psm[0]
    oem = args.get('oem')       # checked for valid values by argparse
    if oem :
        oem = oem[0]

    """     print('font-name {}, font-path {}, height {}, width {}'.format(font_name, font_path, height, width))

    print('lang {}, psm {}, oem {}'.format(lang, psm, oem))

    print('img dir {}, pdf dir {}, out dir {}, mode {}'.format(input_directory_img, input_directory_pdf, output_directory, output_mode)) """

    # by now all params set, either from user input or from default
    result = {
        'font_name_def': font_name,
        'font_path_def': font_path,
        'height_def': height,
        'width_def': width,

        'lang_def': lang,
        'psm_def': psm,
        'oem_def': oem,

        'input_dir_def_img': input_directory_img,
        'input_dir_def_pdf': input_directory_pdf,
        'output_dir_def': output_directory,
        'output_mode_def': output_mode
        }

    return (result)
