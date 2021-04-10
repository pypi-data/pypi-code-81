# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['machine_learning_datasets', 'machine_learning_datasets.sources']

package_data = \
{'': ['*']}

install_requires = \
['aif360>=0.3.0,<0.4.0',
 'alibi>=0.5.5,<0.6.0',
 'matplotlib>=3.2.2,<4.0.0',
 'mlxtend>=0.14.0,<0.15.0',
 'numpy>=1.19.5,<2.0.0',
 'opencv-python>=4.5.1,<5.0.0',
 'pandas>=1.1.5,<2.0.0',
 'pathlib2>=2.3.5,<3.0.0',
 'pycebox>=0.0.1,<0.0.2',
 'scikit-learn>=0.22.2.post1,<0.23.0',
 'scipy>=1.4.1,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'statsmodels>=0.10.2,<0.11.0',
 'tqdm>=4.41.1,<5.0.0']

setup_kwargs = {
    'name': 'machine-learning-datasets',
    'version': '0.1.16.4',
    'description': 'A simple library for loading machine learning datasets and performing some common machine learning interpretation functions. Built for the book "Interpretable Machine Learning with Python".',
    'long_description': None,
    'author': 'Serg Masís',
    'author_email': 'smasis@hawk.iit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
