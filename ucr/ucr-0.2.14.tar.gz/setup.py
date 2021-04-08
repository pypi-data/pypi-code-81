# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ucr',
 'ucr.core',
 'ucr.core.architecture',
 'ucr.core.architecture.backbone',
 'ucr.core.architecture.head',
 'ucr.core.architecture.neck',
 'ucr.core.architecture.transform',
 'ucr.core.dataloader',
 'ucr.core.postprocess',
 'ucr.core.preprocess',
 'ucr.core.preprocess.text_image_aug',
 'ucr.inference',
 'ucr.utils']

package_data = \
{'': ['*'],
 'ucr': ['conf/*',
         'conf/architecture/*',
         'conf/hydra/job_logging/*',
         'conf/hydra/output/*',
         'conf/postprocess/*',
         'conf/preprocess/*'],
 'ucr.utils': ['dict/*', 'fonts/*', 'imgs/*']}

install_requires = \
['PyMuPDF>=1.18.10,<2.0.0',
 'hydra-core>=1.0.6,<2.0.0',
 'imgaug>=0.4.0,<0.5.0',
 'numpy<1.20.0',
 'opencv-python>=4.1.0,<5.0.0',
 'pandas>=1.1,<1.2',
 'pyclipper>=1.2.1,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.40,<5.0']

entry_points = \
{'console_scripts': ['ucr = ucr.ucr:main']}

setup_kwargs = {
    'name': 'ucr',
    'version': '0.2.14',
    'description': 'Universal Character Recognizer (UCR): Simple, Intuitive, Extensible, Multi-Lingual OCR engine',
    'long_description': '<br> <br> <br>\n<p align="center"><img src="docs/static/images/VectorU.svg" alt="Github Runner Covergae Status" height="100">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="docs/static/images/VectorC.svg" alt="Github Runner Covergae Status" height="100">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="docs/static/images/VectorR.svg" alt="Github Runner Covergae Status" height="100"></p>\n<br> <br>\n<p align="center">Universal Character Recognizer (UCR) is an <u>Open Source</u>, <u>Easy to use</u> Python library to build <u>Production Ready</u> OCR applications with its highly Intuitive,  Modular & Extensible API design and off-the-shelf <a href="docs/modelzoo.md">Pretrained Models</a> for over <b>25 languages</b>.</p>\n<p align="center">\n  Read UCR Documentation on <u><a href="https://ucr.docyard.ai/">ucr.docyard.ai</a></u>\n  <br> <br>\n  <a href="#about">Features</a> •\n  <a href="#setup">Setup</a> •\n  <a href="#usage">Usage</a> •\n  <a href="#acknowledgement">Acknowledgement</a>\n  <br> <br>\n  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/ucr">\n  <a href="https://badge.fury.io/py/ucr"><img src="https://badge.fury.io/py/ucr.svg" alt="PyPI version"></a>\n</p>\n\n\n## Features\n\n- Supports SOTA Text Detection and Recognition models\n- Built on top of Pytorch and Pytorch Lightning\n- Supports over 25 languages\n- Model Zoo contains 27 Pretrained Models across 25 languages\n- Modular Design Language allows Pick and Choose of different components\n- Easily extensible with Custom Components and attributes\n- Hydra config enables Rapid Prototyping with multiple configurations\n- Support for Packaging, Logging and Deployment tools straight out of the box\n\n\n## Setup\n\n### Installation\n\n**Require python version >= 3.6.2, install with `pip` (recommended)**\n\n1. <b>Prerequisites:</b> Install compatible version of Pytorch and torchvision from [official repository](https://pytorch.org/get-started/locally/).\n2. <b>Installation:</b> Install the latest stable version of UCR:\n```shell\npip install -U ucr\n```\n\n#### <span style="color:#FF8856">[Optional]</span> Test Installation\n\nRun dummy tests!\n```python\nucr test\n# Optional: Add -l/--lang=\'language_id\' to test on particular language!\nucr test -l=\'en_number\'\n```  \n\n\n## Usage\n### Workflow\n\n\n<p align="center"><img src="docs/static/images/workflow.png"/></p>\n\nExecution flow of UCR is displayed above. Broadly it can be divided into 4 sub-parts.\n\n1. Input(img path/folder path/web address) goes into the <u>Detection</u> model which outputs bounding box coordinates of all the text boxes.\n2. The detected boxes are then checked for <u>Orientation</u> and corrected accordingly.\n3. Next, <u>Recognition</u> model runs on the corrected text boxes. It returns bounding box information and OCR output.\n4. Lastly, an optional <u>Post Processing</u> module is executed to improve/modify the results.\n\n### Quick Start\n\nThe following code snippet shows how to get started with UCR library.\n\n```python\nfrom ucr import UCR\n\n# initialization\nocr = UCR(lang="en_number", device="cpu")\n\n# run prediction\nresult = ocr.predict(\'input_path\', output=\'output_path\')\n\n# for saving annotated image\nresult = ocr.predict(\'input_path\', output=\'output_path\', save_image=True)\n```\nFor complete list of arguments, refer <a href="docs/tldr.md/#argument-list">Argument List</a>\n\n## Model Zoo\n\nA collection of pretrained models for detection, classification and recognition processes is present <a href="docs/modelzoo.md">here</a> !  \nThese models can be useful for out-of-the-box inference on over 25 languages.\n\n\n## Acknowledgement\n\nSubstantial part of the UCR library is either inspired or inherited from the [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) library. Wherever possible the repository has been ported from PaddlePaddle to PyTorch framework including the direct translation of model parameters.\nAlso, a big thanks to [Clova AI](https://clova.ai/en/research/research-areas.html), for open sourcing their testing script and pretrained models ([CRAFT](https://github.com/clovaai/CRAFT-pytorch)).  \n\n## License\n\n[Apache License 2.0](LICENSE)\n',
    'author': 'Abhigyan Raman',
    'author_email': 'abhigyan@docyard.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
