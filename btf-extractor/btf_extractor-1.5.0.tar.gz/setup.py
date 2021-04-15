# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['btf_extractor']

package_data = \
{'': ['*'], 'btf_extractor': ['c_ext/*']}

install_requires = \
['Cython>=0.29,<0.30',
 'imageio>=2.6,<3.0',
 'nptyping>=1,<2',
 'numpy>=1.19,<2.0',
 'simplejpeg>=1.3']

setup_kwargs = {
    'name': 'btf-extractor',
    'version': '1.5.0',
    'description': 'Extract UBO BTF archive format(UBO2003, ATRIUM, UBO2014).',
    'long_description': '# BTF Extractor\n[![PyPI version](https://img.shields.io/pypi/v/btf-extractor?style=flat-square)](https://pypi.org/project/btf-extractor/#history)\n[![GitHub version](https://img.shields.io/github/v/tag/2-propanol/BTF_extractor?style=flat-square)](https://github.com/2-propanol/BTF_extractor/releases)\n[![Python Versions](https://img.shields.io/pypi/pyversions/btf-extractor?style=flat-square)](https://pypi.org/project/btf-extractor/)\n\nExtract UBO BTF archive format([UBO2003](https://cg.cs.uni-bonn.de/en/projects/btfdbb/download/ubo2003/), [ATRIUM](https://cg.cs.uni-bonn.de/en/projects/btfdbb/download/atrium/), [UBO2014](https://cg.cs.uni-bonn.de/en/projects/btfdbb/download/ubo2014/)).\n\nThis repository uses [zeroeffects/btf](https://github.com/zeroeffects/btf)\'s [btf.hh](https://github.com/zeroeffects/btf/blob/master/btf.hh) (MIT License).\n\nExtract to ndarray compatible with openCV(BGR, channels-last).\n\n## Install\n```bash\npip install btf-extractor\n```\n\nThis package uses the [Python C API](https://docs.python.org/3/c-api/index.html).\nTo install this package, a C++ build environment is required.\n\n### Build is tested on\n- Windows 10 20H2 + MSVC v14.28 ([Build Tools for Visual Studio 2019](https://visualstudio.microsoft.com/downloads/))\n- MacOS 11(Big Sur) + clang 12.0.0 (Command line tools for Xcode (`xcode-select --install`))\n- Ubuntu 20.04 + GCC 9.3.0 ([build-essential](https://packages.ubuntu.com/focal/build-essential))\n\n## Example\n```python\n>>> from btf_extractor import Ubo2003, AtriumHdr, Ubo2014\n\n>>> btf = Ubo2003("UBO_CORDUROY256.zip")\n>>> angles_list = list(btf.angles_set)\n>>> print(angles_list[0])\n(0, 0, 0, 0)\n>>> image = btf.angles_to_image(*angles_list[0])\n>>> print(image.shape)\n(256, 256, 3)\n>>> print(image.dtype)\nuint8\n\n>>> btf = AtriumHdr("CEILING_HDR.zip")\n>>> angles_list = list(btf.angles_set)\n>>> print(angles_list[0])\n(0, 0, 0, 0)\n>>> image = btf.angles_to_image(*angles_list[0])\n>>> print(image.shape)\n(256, 256, 3)\n>>> print(image.dtype)\nfloat32\n\n>>> btf = Ubo2014("carpet01_resampled_W400xH400_L151xV151.btf")\n>>> print(btf.img_shape)\n(400, 400, 3)\n>>> angles_list = list(btf.angles_set)\n>>> print(angles_list[0])\n(60.0, 270.0, 60.0, 135.0)\n>>> image = btf.angles_to_image(*angles_list[0])\n>>> print(image.shape)\n(400, 400, 3)\n>>> print(image.dtype)\nfloat32\n```\n\n## Supported Datasets\n### UBO2003\n6561 images, 256x256 resolution, 81 view and 81 light directions. \n\n![ubo2003](https://user-images.githubusercontent.com/42978570/114306638-59518580-9b17-11eb-9961-baa775ab235f.jpg)\n> Mirko Sattler, Ralf Sarlette and Reinhard Klein "[Efficient and Realistic Visualization of Cloth](http://cg.cs.uni-bonn.de/de/publikationen/paper-details/sattler-2003-efficient/)", EGSR 2003.\n\n### ATRIUM (non-HDR and HDR)\n6561 images, 800x800 resolution, 81 view and 81 light directions.\n\n![atrium](https://user-images.githubusercontent.com/42978570/114306641-5c4c7600-9b17-11eb-8251-9a4a92a16b55.jpg)\n\n### UBO2014\n22,801 images, 512x512(400x400) resolution, 151 view and 151 light directions.\n\n![ubo2014](https://user-images.githubusercontent.com/42978570/114306647-5f476680-9b17-11eb-9fb6-5332e104f341.jpg)\n> [Michael Weinmann](https://cg.cs.uni-bonn.de/en/people/dr-michael-weinmann/), [Juergen Gall](http://www.iai.uni-bonn.de/~gall/) and [Reinhard Klein](https://cg.cs.uni-bonn.de/en/people/prof-dr-reinhard-klein/). "[Material Classification based on Training Data Synthesized Using a BTF Database](https://cg.cs.uni-bonn.de/de/publikationen/paper-details/weinmann-2014-materialclassification/)", accepted at ECCV 2014.\n',
    'author': '2-propanol',
    'author_email': 'nuclear.fusion.247@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/2-propanol/btf_extractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
