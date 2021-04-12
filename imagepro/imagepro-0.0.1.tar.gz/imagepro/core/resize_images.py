import math
from PIL import Image


def resize_images(image, min_width=640, min_height=480):
    """
    Resize images in stream data (could be downloaded from a url)
    with default ratio

    Args:
        image (stream data): image in treamed testdata
        min_width (int): image target min width
        min_height (int): image target min height

    Output:
        new_image (stream data): resized image
    """
    im = Image.open(image)
    width, height = im.size
    width_ratio, height_ratio = width/min_width, height/min_height

    if width_ratio < 1 or height_ratio < 1:
        ratio = min(width_ratio, height_ratio)
        new_image = im.resize((math.ceil(width/ratio), math.ceil(height/ratio)))
    return new_image
