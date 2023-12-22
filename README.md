# Menelik's Berhan Ethiopic Script OCR app

![logo1](https://github.com/MenelikBerhan/amharic_ocr_draft/assets/125494245/0b1f5abb-da5e-47fb-ac87-3a492db27eaf)

## Introduction

Menelik's Berhan (loosely translated as Menelik's light) is a command line interface app that performs OCR on image and pdf files with Ehtiopic (Amharic/Gee'z) script. Its developed with the intention of using it for a web/mobile app of old Amharic and Gee'z dictionaries.

__Implemented and Tested on Ubuntu 20.04 with Python 3.8__

### [Project Blog Article](https://www.linkedin.com/pulse/implementing-ethiopic-script-ocr-app-girma-eshete-srp3e)

## Installation

#### Install tesseract

```
sudo apt update
sudo apt install -y tesseract-ocr
```

#### Clone the repo
```
git clone https://github.com/MenelikBerhan/amharic_ocr_draft.git
cd amharic_ocr_draft
```

#### (Optional) Set up a python vertual environment using venv:
Its recommended to setup a python vertual environment before installing requirements:
```
python3 -m venv .venv
source .venv/bin/activate
```

#### Install required packages using pip:
```
python3 -m pip install -r requirements.txt
```

#### Start the app:
```
./ocr.py
```

## Usage

The CLI has three commands:
- `help` for displaying help txt
- `image` for performing OCR on image files,
- `pdf` for performing OCR on pdf files and
- `default` for diplaying or setting default parameters.

### `help`

```
Usage: help
Displays list of available commands

Usage: help <command>
Display detailed help about the specific command
```

### `image` and `pdf`

```
Usage: [image|pdf] INPUT_FILE [OUTPUT_FILE] [OPTION]...
   or: [image|pdf] -i INPUT_FILE... [-o OUTPUT_FILE] [OPTION]...
   or: image|pdf [{INPUT_FILE|-i INPUT_FILE...}] -s INPUT_DIRECTORY [-o OUTPUT_FILE] [OPTION]...

Perform OCR on INPUT_FILE/s and output to OUTPUT_FILE.

Perform OCR on INPUT_FILE/s or on all image|pdf files located
in INPUT_DIRECTORY, and output to OUTPUT_FILE.

Multiple INPUT_FILEs can be given using the -i option.

If OUTPUT_FILE is not given, output file name is generated
from INPUT_FILE/s name.

Specifying the -o option for OUTPUT_FILE is madatory only when:
    - multiple INPUT_FILEs are given using the -i option
    - INPUT_DIRECTORY is given using the -s option

Specifying `image|pdf` prefix is mandatory only when INPUT_DIRECTORY
is specified (using the -s option) without preceeding INPUT_FILE/s.

Mandatory arguments to long options are mandatory for short options too.
-i, --input-files=INPUT_FILE...     OCR multiple input images/pdfs. Must use
                                      the -o option for OUTPUT_FILE.
-s, --src-dir=INPUT_DIRECTORY       specify INPUT_FILE/s' directory. Must
                                      use the -o option for OUTPUT_FILE.
-o, --output-file=OUTPUT_FILE       save output with provided file name.
                                      Implies the -j option.
-d, --dest-dir=OUTPUT_DIRECTORY     save output file/s in the specified
                                      OUTPUT_DIRECTORY.
-j, --join                          output to a single file.
-m, --mode={'print'|'txt'|'pdf'|'docx'}      specify OUTPUT_FILE type.
                                      'print' for stdout (default),
                                      'txt' for plain text,
                                      'docx' for MS word and 'pdf' for pdf.
-c, --confidence                    display average OCR confidence level.

Use `default` command to display or change default values for:
    - INPUT_DIRECTORY
    - OUTPUT_FILE type (output mode)
    - OUTPUT_DIRECTORY
```

### `default`

```
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
```

## Image OCR demo

https://github.com/MenelikBerhan/amharic_ocr_draft/assets/125494245/89ac29ce-0e73-4f62-b4f9-390ddea74038


## Contributors
### Girma Eshete aka Menelik Berhan
[Linkedin](https://www.linkedin.com/in/menelikberhan)
