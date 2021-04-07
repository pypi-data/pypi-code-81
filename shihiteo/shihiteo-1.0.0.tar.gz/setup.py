# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['shihiteo']
setup_kwargs = {
    'name': 'shihiteo',
    'version': '1.0.0',
    'description': '1000-7',
    'long_description': '#ENG\n## How to use\nIMPORT Shihiteo module\n```sh\nfrom shihiteo import Shihiteo\n```\nghoul module\n```sh\nprint(Shihiteo.ghoul())\n```\nand ghoul with massive\n```sh\nprint(Shihiteo.letmedie())\n```sh\n',
    'author': 'perfecto',
    'author_email': 'rektnpc@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
