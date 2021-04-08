# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wakeonlan']
entry_points = \
{'console_scripts': ['wakeonlan = wakeonlan:main']}

setup_kwargs = {
    'name': 'wakeonlan',
    'version': '2.0.1',
    'description': 'A small python module for wake on lan.',
    'long_description': "#########\nwakeonlan\n#########\n\n.. image:: https://img.shields.io/pypi/v/wakeonlan.svg\n   :target: https://pypi.org/project/wakeonlan/\n   :alt: Pypi version\n\n.. image:: https://img.shields.io/pypi/pyversions/wakeonlan.svg\n   :target: https://pypi.org/project/wakeonlan/#files\n   :alt: Supported Python versions\n\n.. image:: https://github.com/remcohaszing/pywakeonlan/actions/workflows/ci.yaml/badge.svg\n   :target: https://github.com/remcohaszing/pywakeonlan/actions/workflows/ci.yaml\n   :alt: Build Status\n\n.. image:: https://readthedocs.org/projects/pywakeonlan/badge/?version=latest\n   :target: https://pywakeonlan.readthedocs.io/en/latest\n   :alt: Documentation Status\n\n.. image:: https://codecov.io/gh/remcohaszing/pywakeonlan/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/remcohaszing/pywakeonlan\n   :alt: Code coverage\n\nA small python module for wake on lan.\n\nFor more information on the wake on lan protocol please take a look at\nWikipedia_.\n\n\n*****\nUsage\n*****\n\nTo wake up a computer using wake on lan it must first be enabled in the BIOS\nsettings. Please note the computer you are trying to power on does not have an\nip address, but it does have a mac address. The package needs to be sent as a\nbroadcast package.\n\n\nAs a python module\n==================\n\nImport the module\n\n>>> from wakeonlan import send_magic_packet\n\n\nWake up a single computer by its mac address\n\n>>> send_magic_packet('ff.ff.ff.ff.ff.ff')\n\n\nWake up multiple computers by their mac addresses.\n\n>>> send_magic_packet('ff.ff.ff.ff.ff.ff', '00-00-00-00-00-00',\n...                   'FFFFFFFFFFFF')\n\n\nAn external host may be specified. Do note that port forwarding on that host is\nrequired. The default ip address is 255.255.255.255 and the default port is 9.\n\n>>> send_magic_packet('ff.ff.ff.ff.ff.ff',\n...                   ip_address='example.com',\n...                   port=1337)\n\n\nAs a standalone script\n======================\n\n::\n\n    usage: wakeonlan [-h] [-i ip] [-p port] mac address [mac address ...]\n\n    Wake one or more computers using the wake on lan protocol.\n\n    positional arguments:\n      mac address  The mac addresses or of the computers you are trying to wake.\n\n    optional arguments:\n      -h, --help   show this help message and exit\n      -i ip        The ip address of the host to send the magic packet to. (default 255.255.255.255)\n      -p port      The port of the host to send the magic packet to. (default 9)\n\n\n************\nDependencies\n************\n\n- Python3.x\n\n\n*******\nLicense\n*******\n\nMIT\n\n\n.. _GitHub: https://github.com/remcohaszing/pywakeonlan\n.. _Wikipedia: http://en.wikipedia.org/wiki/Wake-on-LAN\n",
    'author': 'Remco Haszing',
    'author_email': 'remcohaszing@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/remcohaszing/pywakeonlan',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
