# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kt_pullback']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['pb = kt_pullback.cli:cli']}

setup_kwargs = {
    'name': 'kt-pullback',
    'version': '0.2.1',
    'description': '',
    'long_description': '# kt-pullback\nCalcula os preços de retração de uma pernada no gráfico\n\n## Pré-requisitos\nPython instalado e disponível no terminal de comandos.  \n  \n## Instalação\n```cmd\npip install kt-pullback\n```\n  \n## Uso\n```cmd\npb <PRECO_FINAL> <PRECO_INICIAL>\n```\nOnde:  \nPRECO_FINAL é o preço final da pernada.  \nPRECO_INICIAL é o preço inicial da pernada.  \nRetorna, de cima para baixo, as retrações de 1/3, 1/2 e 2/3 da pernada.  \n  \nExemplo:  \n```cmd\npb 100.09 93.40\n97.86\n96.85\n95.63\n```\n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vfranca/kt-pullback',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
