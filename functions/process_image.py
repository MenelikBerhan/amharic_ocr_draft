#!/usr/bin/env python3
import cv2
import numpy as np
import tempfile
from PIL import Image


def process_image_simple(input_file, **args):
    """Performs image preprocessing before passing image to tesseract.
    
    Args:
        input_file: a string path of image file to be processed for
            image input files, or image as a bytes array for pdf input files.
        **args (dict): dictionary of parameters

    Returns:
        MatLike: the processed image as a MatLike Object of OpenCV2.
    
    """
    
    input_file_type = args.get('input_file_type')

    # TODO - check if loading images using buffer improves efficency
    # load image based on input file type
    if input_file_type == 'image':
        image = cv2.imread(input_file)
    elif input_file_type == 'pdf':
        image = cv2.imdecode(np.frombuffer(input_file.read(), np.uint8), 1)

    # cv2.imshow("orginal", image)
    # cv2.waitKey(0)

    # convert image to grayscale (black & white)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("temp/gray.jpg", gray_image)

    thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    # cv2.imwrite("temp/bw_image.jpg", im_bw)

    # TODO Check if adding smoothening and border validation here increase accuracy

    return (im_bw)


# TODO - set image size and treshold dynamically based on user input
IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.LANCZOS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))
    return temp_filename

def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41,
                                     3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image

def process_image_detailed(file_path):
    # TODO : Implement using opencv and check inputs for helper funcs
    temp_filename = set_image_dpi(file_path)
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new
