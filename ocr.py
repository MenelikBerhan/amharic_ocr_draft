#!/usr/bin/env python3
"""
Command line interface for Ethiopic Script OCR app
"""
import cmd
from functions import defaults_dict, tesseract_dict, write_dict
from functions.ocr_image import ocr_image
from functions.ocr_pdf import ocr_pdf
from functions.parse_input_cmd import parse_ocr_cmd, parse_default_cmd
from functions.set_defaults import set_defaults
from functions.validate_input_cmd import validate_parsed_ocr_cmd
from functions.validate_input_cmd import validate_parsed_defalt_cmd
from pprint import pprint
from shlex import split


class OCRCommand(cmd.Cmd):
    """
    Command line interface for Ethiopic Script OCR app
    """
    prompt = '(ocr) '

    def preloop(self) -> None:
        return super().preloop()

    def do_EOF(self, arg):
        """\nUsage: EOF\nExits the program\n"""
        print()
        return True

    def emptyline(self):
        """Do nothing for empty line commands"""
        return False

    def do_quit(self, arg):
        """\nUsage: quit\nExits the program\n"""
        return True

    def precmd(self, line):
        """Hook method executed just before the command line is
        interpreted, but after the input prompt is generated and issued."""
        # add image/pdf prefix depending on input file extension
        if line and split(line)[0] not in ['image', 'pdf']:
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
        # -s flag (wihtout INPUT_FILES) not prefixed with image|pdf
        if line and line.startswith('-s'):
            self.stdout.write('*** Syntax Error: must provide input file type [image|pdf] before -s flag\n')
        # -i flag (not prefixed with image|pdf) followed by file with invalid file extention
        elif line and line.startswith('-i'):
            self.stdout.write('*** Input Error: input file must be image (.jpeg|.png|.jpg) or pdf (.pdf).\n')
        else:
            super().default(line)

    def do_image(self, arg):
        """Performs an OCR on images."""
        args = parse_ocr_cmd('image ' + arg)

        if not args:
            return
        validated_args = validate_parsed_ocr_cmd('image ' + arg, **args)

        if validated_args:
            ocr_image(**validated_args)

    def do_pdf(self, arg):
        """Performs an OCR on pdfs."""
        args = parse_ocr_cmd('pdf ' + arg)

        if not args:
            return
        validated_args = validate_parsed_ocr_cmd('pdf ' + arg, **args)

        if validated_args:
            ocr_pdf(**validated_args)

    def do_default(self, arg):
        """Sets default params or prints default parameters."""
        # TODO add defaults reseter feature
        if not arg:
            print('\n============ Input and Output Defaults ============\n')
            pprint(defaults_dict)
            print('\n============ Tesseract Params Defaults ============\n')
            pprint(tesseract_dict)
            print('\n=========== Ouput file Writing Defaults ===========\n')
            pprint(write_dict)
            print()
        else:
            args = parse_default_cmd(arg)
            if args is not None:
                validated_args = validate_parsed_defalt_cmd('default ' + arg, **args)
                if validated_args:
                    set_defaults(**validated_args)

    def help_image(self):
        """Prints help text for `image` command"""
        return (self.ocr_help('image'))

    def help_pdf(self):
        """Prints help text for `pdf` command"""
        return (self.ocr_help('pdf'))

    def ocr_help(self, input_type):
        """Prints help text for `image` and `pdf` OCR commands"""
        usage = """
Usage: [{input_type}] INPUT_FILE [OUTPUT_FILE] [OPTION]...
   or: [{input_type}] -i INPUT_FILE... [-o OUTPUT_FILE] [OPTION]...
   or: {input_type} [{{INPUT_FILE|-i INPUT_FILE...}}] -s INPUT_DIRECTORY [-o OUTPUT_FILE] [OPTION]...

Perform OCR on INPUT_FILE/s and output to OUTPUT_FILE.

Perform OCR on INPUT_FILE/s or on all {input_type} files located
in INPUT_DIRECTORY, and output to OUTPUT_FILE.

Multiple INPUT_FILEs can be given using the -i option.

If OUTPUT_FILE is not given, output file name is generated
from INPUT_FILE/s name.

Specifying the -o option for OUTPUT_FILE is madatory only when:
    - multiple INPUT_FILEs are given using the -i option
    - INPUT_DIRECTORY is given using the -s option

Specifying `{input_type}` prefix is mandatory only when INPUT_DIRECTORY
is specified (using the -s option) without preceeding INPUT_FILE/s.

Mandatory arguments to long options are mandatory for short options too.
-i, --input-files=INPUT_FILE...     OCR multiple input {input_type}s. Must use
                                      the -o option for OUTPUT_FILE.
-s, --src-dir=INPUT_DIRECTORY       specify INPUT_FILE/s' directory. Must
                                      use the -o option for OUTPUT_FILE.
-o, --output-file=OUTPUT_FILE       save output with provided file name.
                                      Implies the -j option.
-d, --dest-dir=OUTPUT_DIRECTORY     save output file/s in the specified
                                      OUTPUT_DIRECTORY.
-j, --join                          output to a single file.
-m, --mode={{'print'|'txt'|'pdf'|'docx'}}       specify OUTPUT_FILE type.
                                      'print' for stdout (default),
                                      'txt' for plain text,
                                      'docx' for MS word and 'pdf' for pdf.
-c, --confidence                    display average OCR confidence level.
-v, --verbose                       display detailed process information.

Use `default` command to display or change default values for:
    - INPUT_DIRECTORY
    - OUTPUT_FILE type (output mode)
    - OUTPUT_DIRECTORY
"""
        print(usage.format(input_type=input_type))

    def help_default(self):
        """Prints help text for `default` command"""
        usage = """
Usage: default [OPTION]...

Without options:
  Displays default values for:
    - input directory for image files
    - input directory for pdf files
    - output directory for image and pdf files
    - output mode (output file type)
    - tesseract training data directory
    - tesseract language
    - tesseract page segmentation mode
    - tesseract OCR engine mode
    - path and name of font for MS word and pdf outputs
    - line width and height for pdf outputs

With options change default values for the above parameters.

Mandatory arguments to long options are mandatory for short options too.

For input and output
====================
-ii, --in-dir-image=INPUT_DIR       set default image file input directory.
-ip, --in-dir-pdf=INPUT_DIR         set default pdf file input directory.
 -o, --out-dir=OUTPUT_DIRECTORY     set default output file directory.
 -m, --mode={'print'|'txt'|'pdf'|'docx'}      set default output file type.
                                      'print' for stdout (default),
                                      'txt' for plain text,
                                      'docx' for MS word and 'pdf' for pdf.

For tesseract
=============
-td, --training-dir=TRAIN_DIR       set default training data directory.
-tl, --lang={'amh', 'tir', 'eng'}   set default tesseract language.
                                      'amh' for Amharic,
                                      'tir' for Tigrigna and
                                      'eng' for English.
-tp, --psm                          set default page segmentation mode.
-to, --oem                          set default OCR engine mode.

For writing to output file
==========================
-fp, --font-path                    set default path to a font file.
-fn, --font-name                    set default name of font.
 -w, --width                        set line width for output file.
 -h, --height                       set line heigh for output file.
"""
        print(usage)


if __name__ == '__main__':
    OCRCommand().cmdloop()
