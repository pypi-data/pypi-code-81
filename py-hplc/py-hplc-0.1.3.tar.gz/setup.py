# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_hplc']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'py-hplc',
    'version': '0.1.3',
    'description': 'An unoffical Python wrapper for the SSI-Teledyne Next Generation class HPLC pumps.',
    'long_description': '===============================================\npy-hplc |build-status| |docs| |pylint| |style| \n===============================================\n\nOverview\n==========\nAn unoffical Python wrapper for the SSI-Teledyne Next Generation class HPLC pumps.\n\n- `Download page`_ \n- `API Documentation`_\n- `Official pump documentation`_\n\nMIT license, (C) 2021 Alex Whittington <alex@southsun.tech>\n\nInstallation\n=============\nThe package is available on PyPI.\n\n``pip install py-hplc``\n\n.. _`Download page`: https://pypi.org/project/py-hplc/\n.. _`API Documentation`: https://py-hplc.readthedocs.io/en/latest/\n.. _`Official pump documentation`: https://www.teledynessi.com/Manuals%20%20Guides/Product%20Guides%20and%20Resources/Serial%20Pump%20Control%20for%20Next%20Generation%20SSI%20Pumps.pdf\n\n\n.. |build-status| image:: https://github.com/teauxfu/py-hplc/actions/workflows/build.yml/badge.svg\n  :target: https://github.com/teauxfu/py-hplc/actions/workflows/build.yml\n  :alt: Build Status\n\n.. |docs| image:: https://readthedocs.org/projects/pip/badge/?version=stable\n  :target: https://pip.pypa.io/en/stable/?badge=stable\n  :alt: Documentation Status\n\n.. |style| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :target: https://github.com/psf/black\n  :alt: Style\n  \n.. |pylint| image:: https://mperlet.github.io/pybadge/badges/9.86.svg\n  :target: https://github.com/mperlet/pybadge\n  :alt: Vanilla Pylint Score\n',
    'author': 'Alex W',
    'author_email': 'alex@southsun.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/teauxfu/py-hplc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
