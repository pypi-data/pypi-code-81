# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kt_osc']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['osc = kt_osc.cli:cli']}

setup_kwargs = {
    'name': 'kt-osc',
    'version': '0.2.1',
    'description': 'Calcula oscilacao de preco',
    'long_description': '# kt-osc\nCalcula oscilação percentual do preço.  \n\n## Pré-requisitos\nPython instalado e disponível no terminal de comandos.  \n\n## Instalação\n```cmd\n> pip install kt-osc\n```\n\n## Uso\n```cmd\n> osc <PRECO-FINAL> <PRECO-INICIAL>\n```\nOnde:  \nPRECO-FINAL é o preço final da oscilação.  \nPRECO-INICIAL é o preço inicial da oscilação.  \nExemplo:  \n```cmd\n> osc 99.81 94.89\n5.2%\n```\nA oscilação percentual entre 94.89 e 99.81 é 5.2%.  \n\n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vfranca/kt-osc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
