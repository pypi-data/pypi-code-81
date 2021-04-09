import os.path

import numpy as np

import dito.io


####
#%%% resource filenames
####


RESOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
RESOURCES_FILENAMES = {
    "colormap:plot": os.path.join(RESOURCES_DIR, "colormaps", "plot.png"),

    "font:scientifica-12": os.path.join(RESOURCES_DIR, "fonts", "scientifica", "scientifica_lh4rb.png"),

    "font:source-10": os.path.join(RESOURCES_DIR, "fonts", "source_code_pro", "10_lh4rb.png"),
    "font:source-15": os.path.join(RESOURCES_DIR, "fonts", "source_code_pro", "15_lh4rb.png"),
    "font:source-20": os.path.join(RESOURCES_DIR, "fonts", "source_code_pro", "20_lh4rb.png"),
    "font:source-25": os.path.join(RESOURCES_DIR, "fonts", "source_code_pro", "25_lh4rb.png"),
    "font:source-30": os.path.join(RESOURCES_DIR, "fonts", "source_code_pro", "30_lh4rb.png"),
    "font:source-35": os.path.join(RESOURCES_DIR, "fonts", "source_code_pro", "35_lh4rb.png"),
    "font:source-40": os.path.join(RESOURCES_DIR, "fonts", "source_code_pro", "40_lh4rb.png"),
    "font:source-50": os.path.join(RESOURCES_DIR, "fonts", "source_code_pro", "50_lh4rb.png"),
    "font:source-70": os.path.join(RESOURCES_DIR, "fonts", "source_code_pro", "70_lh4rb.png"),

    "font:tamzen-9": os.path.join(RESOURCES_DIR, "fonts", "tamzen", "Tamzen5x9_lh4rb.png"),
    "font:tamzen-12": os.path.join(RESOURCES_DIR, "fonts", "tamzen", "Tamzen6x12_lh4rb.png"),
    "font:tamzen-14": os.path.join(RESOURCES_DIR, "fonts", "tamzen", "Tamzen7x14_lh4rb.png"),
    "font:tamzen-16": os.path.join(RESOURCES_DIR, "fonts", "tamzen", "Tamzen8x16_lh4rb.png"),
    "font:tamzen-20": os.path.join(RESOURCES_DIR, "fonts", "tamzen", "Tamzen10x20_lh4rb.png"),

    "font:terminus-12": os.path.join(RESOURCES_DIR, "fonts", "terminus", "ter-u12_lh4rb.png"),
    "font:terminus-14": os.path.join(RESOURCES_DIR, "fonts", "terminus", "ter-u14_lh4rb.png"),
    "font:terminus-16": os.path.join(RESOURCES_DIR, "fonts", "terminus", "ter-u16_lh4rb.png"),
    "font:terminus-18": os.path.join(RESOURCES_DIR, "fonts", "terminus", "ter-u18_lh4rb.png"),
    "font:terminus-20": os.path.join(RESOURCES_DIR, "fonts", "terminus", "ter-u20_lh4rb.png"),
    "font:terminus-22": os.path.join(RESOURCES_DIR, "fonts", "terminus", "ter-u22_lh4rb.png"),
    "font:terminus-24": os.path.join(RESOURCES_DIR, "fonts", "terminus", "ter-u24_lh4rb.png"),
    "font:terminus-28": os.path.join(RESOURCES_DIR, "fonts", "terminus", "ter-u28_lh4rb.png"),
    "font:terminus-32": os.path.join(RESOURCES_DIR, "fonts", "terminus", "ter-u32_lh4rb.png"),

    "image:PM5544": os.path.join(RESOURCES_DIR, "images", "PM5544.png"),
}

####
#%%% real images
####


def pm5544():
    return dito.io.load(filename=RESOURCES_FILENAMES["image:PM5544"])


####
#%%% synthetic images
####


def xslope(height=32, width=256):
    """
    Return image containing values increasing from 0 to 255 along the x axis.
    """
    
    slope = np.linspace(start=0, stop=255, num=width, endpoint=True, dtype=np.uint8)
    slope.shape = (1,) + slope.shape
    slope = np.repeat(a=slope, repeats=height, axis=0)
    return slope


def yslope(width=32, height=256):
    """
    Return image containing values increasing from 0 to 255 along the y axis.
    """
    
    return xslope(height=width, width=height).T


def checkerboard(size=(512, 288), block_size=16, low=0, high=255):
    """
    Returns a gray-scale image of the given `size` containing a checkerboard
    grid with squares of size `block_size`. The arguments `low` and `high`
    specify the gray scale values to be used for the squares.
    """

    image = np.zeros(shape=(size[1], size[0]), dtype=np.uint8) + low
    for (n_row, y) in enumerate(range(0, size[1], block_size)):
        offset = block_size if ((n_row % 2) == 0) else 0
        for x in range(offset, size[0], 2 * block_size):
            image[y:(y + block_size), x:(x + block_size)] = high

    return image


def background_checkerboard(size=(512, 288), block_size=16):
    """
    Returns a gray-scale image of the given `shape` containing a checkerboard
    grid of light and dark gray squares of size `block_size`.
    """
    return checkerboard(size=size, block_size=block_size, low=80, high=120)


def random_image(size=(512, 288), color=True):
    """
    Returns a random `uint8` image of the given `shape`.
    """
    shape = tuple(size[::-1])
    if color:
        shape = shape + (3,)
    image_random = np.random.rand(*shape)
    return dito.core.convert(image=image_random, dtype=np.uint8)
