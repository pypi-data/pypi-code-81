import numpy as np

from PIL import Image
from tsbb15_labs import IMAGE_DIRECTORY


def make_circle(x,y,radius, image_sz = 256):
    xx,yy = np.meshgrid(np.arange(image_sz),np.arange(image_sz))
    circle = (xx-x)**2 + (yy-y)**2 < radius**2

    return circle

def load_lab_image(filename):
    """Load a grayscale image by filename from the CVL image directory
    
    Example:
    >>> img = load_lab_image('cornertest.png')    
    """
    path = str(IMAGE_DIRECTORY / filename)
    return np.asarray(Image.open(path).convert('L'))


def get_cameraman():
    "Return I, J and true (col, row) displacement"
    n = 10 # Border crop
    img = load_lab_image('cameraman.tif')
    I = img[n:-n, n:-n]
    x, y = 1, -2
    J = img[n-y:-n-y, n-x:-n-x]
    assert I.shape == J.shape
    return I, J, (x, y)