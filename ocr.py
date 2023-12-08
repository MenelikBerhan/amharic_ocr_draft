#!/usr/bin/env python3
"""
Command line interface for Ethiopic Text OCR app

Attributes:
    usage (str): information about image and pdf commands.

"""
import cmd
from functions import defaults_dict, tesseract_dict, write_dict
from functions.image_ocr import image_ocr
from functions.pdf_ocr import pdf_ocr
from functions.parse_input_cmd import parse_ocr_cmd, parse_default_cmd
from functions.validate_input_cmd import validate_parsed_ocr_cmd
from functions.validate_input_cmd import validate_parsed_defalt_cmd
from pprint import pprint
from shlex import split

usage = """
Usage: [image|pdf] INPUT_FILE [OUTPUT_FILE] [OPTION]...
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


class OCRCommand(cmd.Cmd):
    """ OCR CLI """
    prompt = '(ocr) '

    def preloop(self) -> None:
        # print(usage)
        return super().preloop()

    def do_EOF(self, arg):
        """Exits CLI"""
        print()
        return True

    def emptyline(self):
        """Do nothing for empty line commands"""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def precmd(self, line):
        """Hook method executed just before the command line is
        interpreted, but after the input prompt is generated and issued."""

        if line and split(line)[0] not in ['image', 'pdf']:  # add image/pdf depending on input file extension
            file_ext = ''
            for i in split(line):
                if not i.startswith('-'):
                    file_ext = i.split('.')[-1]
                    break
            if (file_ext in ['png', 'jpeg', 'jpg']):
                line = 'image ' + line
            elif (file_ext == 'pdf'):
                line = 'pdf ' + line

        return line

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
        """
        if line and line.startswith('-s'):  # -s flag (wihtout INPUT_FILES) not prefixed with image|pdf
            self.stdout.write('*** Syntax Error: must provide input file type [image|pdf] before -s flag\n')
        elif line and line.startswith('-i'):  # -i flag (not prefixed with image|pdf) followed by file with invalid file extention
            self.stdout.write('*** Input Error: input file must be image (.jpeg|.png|.jpg) or pdf (.pdf).\n')
        else:
            super().default(line)

    def do_image(self, arg):
        """Performs an OCR on images."""
        args = parse_ocr_cmd('image ' + arg)

        print('\n----PARSE_INPUT RETURN-------')
        pprint(args)
        print('--------------------------------')
        if not args:
            return
        validated_args = validate_parsed_ocr_cmd('image ' + arg, **args)

        print('\n----VALIDATE_ARGS RETURN-------')
        pprint(validated_args)
        print('--------------------------------')

        if validated_args:
            image_ocr(**validated_args)

    def do_pdf(self, arg):
        """Performs an OCR on pdfs."""
        args = parse_ocr_cmd('pdf ' + arg)

        print('\n----PARSE_INPUT RETURN-------')
        pprint(args)
        print('--------------------------------')
        if not args:
            return
        validated_args = validate_parsed_ocr_cmd('pdf ' + arg, **args)

        print('\n----VALIDATE_ARGS RETURN-------')
        pprint(validated_args)
        print('--------------------------------')

        if validated_args:
            pdf_ocr(**validated_args)

    def do_default(self, arg):
        """Sets default params or prints default parameters."""
        # TODO add defaults setter , defaults reseter feature
        # Parse arg and set dicts accordingly
        if not arg:
            print('============ Input and Output Defaults ============\n')
            pprint(defaults_dict)
            print('\n============ Tesseract Params Defaults ============\n')
            pprint(tesseract_dict)
            print('\n============ Ouput file Writing Defaults ============\n')
            pprint(write_dict)
        else:
            args = parse_default_cmd(arg)
            print('\n----PARSE_INPUT RETURN-------')
            pprint(args)
            print('--------------------------------')

            if args is not None:
                validated_args = validate_parsed_defalt_cmd('default ' + arg, **args)
                print('\n----VALIDATE_ARGS RETURN-------')
                pprint(validated_args)
                print('--------------------------------')

            # if validated_args:
            #     set_defaults(**validated_args)

if __name__ == '__main__':
    OCRCommand().cmdloop()
