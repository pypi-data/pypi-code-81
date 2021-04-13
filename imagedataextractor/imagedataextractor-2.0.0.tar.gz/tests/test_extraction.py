import os
import unittest
import logging
import numpy as np
from PIL import Image

from imagedataextractor.scalebar import ScalebarDetector


class TestExtraction(unittest.TestCase):

    def test_extraction(self):
        test_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/testimage.png')
        test_image = np.array(Image.open(test_image_path))