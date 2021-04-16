# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['udft']
install_requires = \
['numpy>=1.20.2,<2.0.0']

setup_kwargs = {
    'name': 'udft',
    'version': '2.0.0',
    'description': 'Unitary discrete Fourier Transform (and related)',
    'long_description': '# UDFT: Unitary Discrete Fourier Transform (and related)\n\nThis module implements unitary discrete Fourier transform, that is orthonormal.\nThis module existed before the introduction of the `norm="ortho"` keyword and is\nnow a very thin wrapper around Numpy or pyFFTW (maybe others in the future),\nmainly done for my personal usage. There is also functions related to Fourier\nand convolution like `ir2fr`.\n\nIt is useful for convolution [1]: they respect the Perceval equality, e.g., the\nvalue of the null frequency is equal to `1/√N * ∑ₙ xₙ`.\n\n```\n[1] B. R. Hunt "A matrix theory proof of the discrete convolution theorem", IEEE\nTrans. on Audio and Electroacoustics, vol. au-19, no. 4, pp. 285-288, dec. 1971\n```\n\nIf you are having issues, please let me know\n\nfrancois.orieux AT l2s.centralesupelec.fr\n\n## Installation and documentation\n\nUDFT is just the file `udft.py` and depends on `numpy` and Python 3.7 only. We\nrecommend using poetry for installation\n\n```\n   poetry add qmm\n```\n\nbut the package is available with pip also. For a quick and dirty installation,\njust copy the `udft.py` file: it is quite stable, follow the [Semantic\nVersioning](https://semver.org/spec/v2.0.0.html), and major changes are\nunlikely.\n\n## License\n\nThe project is licensed under the DO WHAT THE FUCK YOU WANT license.\n',
    'author': 'François Orieux',
    'author_email': 'francois.orieux@universite-paris-saclay.fr',
    'maintainer': 'François Orieux',
    'maintainer_email': 'francois.orieux@universite-paris-saclay.fr',
    'url': 'https://github.com/forieux/udft/',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
