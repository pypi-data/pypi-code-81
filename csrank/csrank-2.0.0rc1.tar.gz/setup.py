# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csrank',
 'csrank.choicefunction',
 'csrank.core',
 'csrank.dataset_reader',
 'csrank.dataset_reader.choicefunctions',
 'csrank.dataset_reader.discretechoice',
 'csrank.dataset_reader.dyadranking',
 'csrank.dataset_reader.labelranking',
 'csrank.dataset_reader.objectranking',
 'csrank.deprecated',
 'csrank.discretechoice',
 'csrank.dyadranking',
 'csrank.modules',
 'csrank.modules.scoring',
 'csrank.objectranking',
 'csrank.tests']

package_data = \
{'': ['*'], 'csrank.deprecated': ['hotel_dataset/*', 'university_dataset/*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'h5py>=2.7,<3.0',
 'joblib>=0.16.0,<0.17.0',
 'numpy>=1.12.1,<2.0.0',
 'pandas>=1.1.1,<2.0.0',
 'psycopg2-binary>=2.7,<3.0',
 'pygmo>=2.7,<3.0',
 'pymc3>=3.8,<4.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'scipy>=1.5.2,<2.0.0',
 'skorch>=0.9.0,<0.10.0',
 'torch>=1.8.0,<2.0.0',
 'tqdm>=4.11.2,<5.0.0']

extras_require = \
{'docs': ['Sphinx>=3.2.1,<4.0.0',
          'sphinx_rtd_theme>=0.5.0,<0.6.0',
          'sphinxcontrib-bibtex>=1.0.0,<2.0.0',
          'nbsphinx>=0.7.1,<0.8.0',
          'IPython>=7.18.1,<8.0.0']}

setup_kwargs = {
    'name': 'csrank',
    'version': '2.0.0rc1',
    'description': 'Context-sensitive ranking and choice',
    'long_description': None,
    'author': 'Karlson Pfannschmidt',
    'author_email': 'kiudee@mail.upb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kiudee/cs-ranking',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
