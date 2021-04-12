# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['panimg', 'panimg.image_builders', 'panimg.post_processors']

package_data = \
{'': ['*']}

install_requires = \
['Pillow',
 'SimpleITK',
 'numpy',
 'openslide-python',
 'pydantic',
 'pydicom',
 'pyvips',
 'tifffile']

setup_kwargs = {
    'name': 'panimg',
    'version': '0.2.1',
    'description': 'Conversion of medical images to MHA and TIFF.',
    'long_description': '# panimg\n\n[![CI](https://github.com/DIAGNijmegen/rse-panimg/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/DIAGNijmegen/rse-panimg/actions/workflows/ci.yml?query=branch%3Amain)\n[![PyPI](https://img.shields.io/pypi/v/panimg)](https://pypi.org/project/panimg/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/panimg)](https://pypi.org/project/panimg/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**NOT FOR CLINICAL USE**\n\nConversion of medical images to MHA and TIFF. \nRequires Python 3.7, 3.8 or 3.9.\n`libvips-dev` and `libopenslide-dev` must be installed on your system.\nFor compressed DICOM support ensure that `gdcm` is installed.\n\nUnder the hood we use:\n\n* `SimpleITK`\n* `pydicom`\n* `Pillow`\n* `openslide-python`\n* `pyvips`\n\n## Usage\n\n`panimg` takes a folder full of files and tries to covert them to MHA or TIFF.\nFor each subdirectory of files it will try several strategies for loading the contained files, and if an image is found it will output it to the output folder.\nIt will return a structure containing information about what images were produced, what images were used to form the new images, image metadata, and any errors from any of the strategies.\n\n**NOTE: Alpha software, do not run this on folders you do not have a backup of.**\n\n```python\nfrom pathlib import Path\nfrom panimg import convert\n\nresult = convert(\n    input_directory=Path("/path/to/files/"),\n    output_directory=Path("/where/files/will/go/"),\n)\n```\n\n### Supported Formats\n\n| Input                               | Output  | Strategy   | Notes                      |\n| ----------------------------------- | --------| ---------- | -------------------------- |\n| `.mha`                              | `.mha`  | `metaio`   |                            |\n| `.mhd` with `.raw` or `.zraw`       | `.mha`  | `metaio`   |                            |\n| `.dcm`                              | `.mha`  | `dicom`    | <sup>[1](#footnote1)</sup> |\n| `.nii`                              | `.mha`  | `nifti`    |                            |\n| `.nii.gz`                           | `.mha`  | `nifti`    |                            |\n| `.png`                              | `.mha`  | `fallback` | <sup>[2](#footnote2)</sup> |\n| `.jpeg`                             | `.mha`  | `fallback` | <sup>[2](#footnote2)</sup> |\n| `.tiff`                             | `.tiff` | `tiff`     |                            |\n| `.svs` (Aperio)                     | `.tiff` | `tiff`     |                            |\n| `.vms`, `.vmu`, `.ndpi` (Hamamatsu) | `.tiff` | `tiff`     |                            |\n| `.scn` (Leica)                      | `.tiff` | `tiff`     |                            |\n| `.mrxs` (MIRAX)                     | `.tiff` | `tiff`     |                            |\n| `.biff` (Ventana)                   | `.tiff` | `tiff`     |                            |\n\n<a name="footnote1">1</a>: Compressed DICOM requires `gdcm`\n\n<a name="footnote2">2</a>: 2D only, unitary dimensions\n\n#### Post Processors\n\nYou can also define a set of post processors that will operate on each output file.\nWe provide a `dzi_to_tiff` post processor that is enabled by default, which will produce a DZI file if it is able to.\nTo customise the post processors that run you can do this with\n\n```python\nresult = convert(..., post_processors=[...])\n```\n\n#### Using Strategies Directly\n\nIf you want to run a particular strategy directly which returns a generator of images for a set of files you can do this with\n\n```python\nfiles = {f for f in Path("/foo/").glob("*.dcm") if f.is_file()}\n\ntry:\n    for result in image_builder_dicom(files=files):\n        sitk_image = result.image\n        process(sitk_image)  # etc. you can also look at result.name for the name of the file,\n                             # and result.consumed_files to see what files were used for this image\nexcept UnconsumedFilesException as e:\n    # e.errors is keyed with a Path to a file that could not be consumed,\n    # with a list of all the errors found with loading it,\n    # the user can then choose what to do with that information\n    ...\n```\n',
    'author': 'James Meakin',
    'author_email': '12661555+jmsmkn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DIAGNijmegen/rse-panimg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
