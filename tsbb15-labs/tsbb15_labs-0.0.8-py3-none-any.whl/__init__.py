from pathlib import Path
import os

try:
    IMAGE_DIRECTORY = Path(os.environ['CVL_LAB_IMAGEDIR'])
except KeyError:
    IMAGE_DIRECTORY = Path('/courses/TSBB15/images/')

if not IMAGE_DIRECTORY.exists():
    IMAGE_DIRECTORY = Path(os.path.join(os.path.dirname(__file__),'images'))
    if not IMAGE_DIRECTORY.exists():
        raise RuntimeError("Image directory '{}' does not exist. Try setting the CVL_LAB_IMAGEDIR environment variable".format(IMAGE_DIRECTORY))