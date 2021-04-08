# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kt_line']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['l = kt_line.cli:cli']}

setup_kwargs = {
    'name': 'kt-line',
    'version': '0.3.1',
    'description': 'Ferramenta de linha de comando para calcular linha de tendencia e linha de canal',
    'long_description': '# kt-line\nCalcula o próximo preço das linhas de canal.  \n\n## Pré-requisitos\nPython instalado e disponível no terminal de comandos.  \n\n## Instalação\n```cmd\n> pip install kt-line\n```\n\n## Uso\n```cmd\n> l <PRECO1> <PRECO2>\n```\n\nOnde:  \nPRECO1 e PRECO2 são dois topos ou dois fundos.  \nExemplo:  \n```cmd\n> l 26.00 27.00  \n28.00\n```\nDois fundos mais altos 26.00 e 27.00 desenham uma linha cujo próximo ponto está em 28.00.  \n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vfranca/kt-line',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
