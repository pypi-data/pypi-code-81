# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chem_kit', 'chem_kit.transformation']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.21.0,<8.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'chem-kit',
    'version': '0.1.2',
    'description': 'A chemical toolbox based on RDKit',
    'long_description': '# ChemKit\n\n<p align="center">\n<a href="https://pypi.org/project/chem-kit" target="_blank">\n    <img src="https://img.shields.io/pypi/v/chem-kit?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n</p>\n\n---\n\n**Documentation**: <a href="http://chem-kit.metwork.science/" target="_blank">http://chem-kit.metwork.science/</a>\n\n**Source Code**: <a href="https://github.com/YannBeauxis/chem-kit" target="_blank">https://github.com/YannBeauxis/chem-kit</a>\n\n---\n\nChemKit is a chemical toolbox based on [RDKit](https://www.rdkit.org/) with currently 2 main purposes :\n\n- Facilitate the usage of the [RDKIt Python API](https://www.rdkit.org/docs/api-docs.html)\n with some more easy to use classes that can occasionally fix some bug (especially with Jupyter rendering).\n\n- Provide tailored methods for the [MetWork](http://www.metwork.science) project\n\n## Usage\n\n### Manipulate Molecules\n\n```python\n    from chem_kit import Molecule\n    mol = Molecule("CCO")\n```\n\n### Manipulate Transformation\n\n```python\n    from chem_kit import Transformation\n    tsf = Transformation("[#6:1]-[#8:2]-[#1:3]>>[#6:1]-[#8:2]-[#6:3](-[#1])(-[#1])-[#1]")\n```\n\nMore examples with [Jupyter notebook](http://chem-kit.metwork.science/jupyter_example/)\n\n## Install\n\nLike RDKit, ChemKit needs [Conda](https://docs.conda.io) :\n\n```bash\nconda env install -f conda-env.yml\nconda activate chem_kit\n```\n\nTo manage other required Python packages, \nthe better way is to use [Poetry](https://python-poetry.org) on top of Conda :\n\n```bash\ncd /path/to/chem_kit\npoetry install\n```\n\n> Poetry manipulate Python packages directly on Conda env.\n',
    'author': 'Yann Beauxis',
    'author_email': 'dev@yannbeauxis.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/YannBeauxis/chem-kit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
