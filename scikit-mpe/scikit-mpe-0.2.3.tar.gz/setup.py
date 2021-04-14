# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skmpe']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=1.6.0,<2.0.0',
 'numpy>=1.18.1,<2.0.0',
 'pydantic>=1.4,<2.0',
 'scikit-fmm>=2021.1.21,<2021.2',
 'scipy>=1.4.1,<2.0.0']

extras_require = \
{'docs': ['sphinx>=2.3.1,<3.0.0',
          'numpydoc>=0.9.2,<0.10.0',
          'm2r>=0.2.1,<0.3.0',
          'matplotlib>=3.1.3,<4.0.0',
          'scikit-image>=0.16.2,<0.17.0']}

setup_kwargs = {
    'name': 'scikit-mpe',
    'version': '0.2.3',
    'description': 'Minimal path extraction using the fast marching method',
    'long_description': "# scikit-mpe\n\n[![PyPI version](https://img.shields.io/pypi/v/scikit-mpe.svg)](https://pypi.python.org/pypi/scikit-mpe)\n[![Build status](https://travis-ci.org/espdev/scikit-mpe.svg?branch=master)](https://travis-ci.org/espdev/scikit-mpe)\n[![Documentation Status](https://readthedocs.org/projects/scikit-mpe/badge/?version=latest)](https://scikit-mpe.readthedocs.io/en/latest/?badge=latest)\n[![Coverage Status](https://coveralls.io/repos/github/espdev/scikit-mpe/badge.svg?branch=master)](https://coveralls.io/github/espdev/scikit-mpe?branch=master)\n![Supported Python versions](https://img.shields.io/pypi/pyversions/scikit-mpe.svg)\n[![License](https://img.shields.io/pypi/l/scikit-mpe.svg)](LICENSE)\n\n**scikit-mpe** is a package for extracting a minimal path in N-dimensional Euclidean space (on regular Cartesian grids) \nusing [the fast marching method](https://math.berkeley.edu/~sethian/2006/Explanations/fast_marching_explain.html).\n\n\n## Quickstart\n\n### Installing\n\n```\npip install -U scikit-mpe\n```\n\n### Usage\n\nHere is a simple example that demonstrates how to extract the path passing through the retina vessels.\n\n```python\nfrom matplotlib import pyplot as plt\n\nfrom skimage.data import retina\nfrom skimage.color import rgb2gray\nfrom skimage.transform import rescale\nfrom skimage.filters import sato\n\nfrom skmpe import mpe\n\nimage = rescale(rgb2gray(retina()), 0.5)\nspeed_image = sato(image)\n\nstart_point = (76, 388)\nend_point = (611, 442)\nway_points = [(330, 98), (554, 203)]\n\npath_info = mpe(speed_image, start_point, end_point, way_points)\n\npx, py = path_info.path[:, 1], path_info.path[:, 0]\n\nplt.imshow(image, cmap='gray')\nplt.plot(px, py, '-r')\n\nplt.plot(*start_point[::-1], 'oy')\nplt.plot(*end_point[::-1], 'og')\nfor p in way_points:\n    plt.plot(*p[::-1], 'ob')\n\nplt.show()\n```\n\n![retina_vessel_path](https://user-images.githubusercontent.com/1299189/73838143-0d74c380-4824-11ea-946a-667c8236ed75.png)\n\n## Documentation\n\nThe full documentation can be found at [scikit-mpe.readthedocs.io](https://scikit-mpe.readthedocs.io/en/latest)\n\n## References\n\n- [Fast Marching Methods: A boundary value formulation](https://math.berkeley.edu/~sethian/2006/Explanations/fast_marching_explain.html)\n- [Level Set Methods and Fast Marching Methods](https://math.berkeley.edu/~sethian/2006/History/Menu_Expanded_History.html)\n- [scikit-fmm](https://github.com/scikit-fmm/scikit-fmm) - Python implementation of the fast marching method\n- [ITKMinimalPathExtraction](https://github.com/InsightSoftwareConsortium/ITKMinimalPathExtraction) - ITK based C++ implementation of MPE\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n",
    'author': 'Eugene Prilepin',
    'author_email': 'esp.home@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/espdev/scikit-mpe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
