# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['steganography_tools', 'steganography_tools..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0', 'numpy>=1.18,<1.20']

entry_points = \
{'console_scripts': ['cli_command_hello = steganography_tools:main']}

setup_kwargs = {
    'name': 'steganography-tools',
    'version': '0.1.0',
    'description': 'A Python library for higher level python functions used in image analysis and computer vision for steganography',
    'long_description': '# Steganography Tools\n\n## Installation\n\n`pip install steganography_tools`\n\n## References\n\n### Module: Steganography for Image, Sounds, Text\n\n**Available formats**\n- PNG\n- JPEG\n\n**Importation**\n\n`from steganography_tools import st`\n\n**Usage**\n\n```\n# Encoding\nsteg = st.LSBSteganography(cv2.imread("image.jpg"))\nimg_encoded = steg.encode_text("my message")\ncv2.imwrite("image_enc.png", img_encoded)\nplt.imshow(img_encoded)\n\n# Decoding\nim = cv2.imread("image_enc.png")\nsteg = st.LSBSteganography(im)\nprint("Text value:",steg.decode_text())\n```\n\n**Compare original and encoded images**\n\n```\noriginal = cv2.imread(\'image.jpg\')\nlsbEncoded = cv2.imread("image_enc.png")\noriginal = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)\nlsb_encoded_img = cv2.cvtColor(lsbEncoded, cv2.COLOR_BGR2RGB)\n\ncompare_images = st.Compare(original, lsb_encoded_img)\ncompare_images.get_results()\n```\n\n### Module: Image processing\n\n**Importation**\n\n`from steganography_tools import image_processing as st_processing`\n\n**Usage**\n\n```\nTEST_PHOTO = "image.jpg"\n\n# This function allows us to get the basic information of an image\nst_processing.img_information(TEST_PHOTO)\n\n# Check for potential metadata\nst_processing.get_metadata(TEST_PHOTO)\n\n# TRANSFORMATION\n\nst_processing.rgb2grayscale(TEST_PHOTO_GRAYSCALE)\n\nTEST_PHOTO = cv2.imread(TEST_PHOTO) \nprint("Type: ",type(TEST_PHOTO))\nTEST_PHOTO = TEST_PHOTO[:,:,0]\n\nst_processing.plot_histogram(TEST_PHOTO)\nst_processing.thresholding(TEST_PHOTO, 55)\n\n# Left to right : grayscale image | contrast increased\nst_processing.display_images(TEST_PHOTO)\n\n# Image manipulation and numpy arrays\nst_processing.image_manipulation("image_grayscale.jpg")\n\n# Geometrical transformations\nst_processing.geo_transfomation(TEST_PHOTO)\n\n# Blurring\nst_processing.blurring(TEST_PHOTO)\n\n# Sharpenning\nst_processing.sharpenning(TEST_PHOTO)\n\n# Denoising\nst_processing.denoising(TEST_PHOTO)\n```\n\n## CLI\n\n```\nCommand Line Arguments:\n -h, --hide                      To hide data in an image file\n -r, --recover                   To recover data from an image file\n -i, --input TEXT                Path to an bitmap (.bmp or .png) image\n -s, --secret TEXT               Path to a file to hide in the image\n -o, --output TEXT               Path to an output file\n --help                          Show this message and exit.\n```',
    'author': 'Sebastien Mascha',
    'author_email': 'sebastien.mascha@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sebastienmascha/data-science-package-steganography-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
