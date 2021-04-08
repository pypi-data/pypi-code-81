# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scalarstop']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.5,<2.0.0',
 'cloudpickle>=1.6.0,<2.0.0',
 'numpy',
 'pandas',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'tensorflow>=2.3.0']

setup_kwargs = {
    'name': 'scalarstop',
    'version': '0.1.1',
    'description': 'A framework for managing machine learning experiments.',
    'long_description': 'Organize your machine learning experiments with ScalarStop\n==========================================================\n\nScalarStop is a framework written in Python that helps you keep track of datasets, models, hyperparameters, and training metrics in machine learning experiments.\n\nInstallation\n------------\n\nScalarStop is available on PyPI. You can install by running the command ``pip3 install scalarstop``.\n\nUsage\n-----\n\nRead the `ScalarStop Tutorial <https://github.com/scalarstop/scalarstop/blob/main/notebooks/tutorial.ipynb>`_ to learn the core concepts behind ScalarStop and how to structure your datasets and models.\n\nAfterwards, you might want to dig deeper into the `ScalarStop Documentation <https://docs.scalarstop.com>`_. In general, a typical ScalarStop workflow involves four steps:\n\n1. Organize your datasets with `scalarstop.datablob <https://www.scalarstop.com/en/latest/autoapi/scalarstop/datablob/#module-scalarstop.datablob>`_.\n2. Describe your machine learning model architectures using `scalarstop.model_template <https://www.scalarstop.com/en/latest/autoapi/scalarstop/model_template/#module-scalarstop.model_template>`_.\n3. Load, train, and save machine learning models with `scalarstop.model <https://www.scalarstop.com/en/latest/autoapi/scalarstop/model/#module-scalarstop.model>`_.\n4. Save hyperparameters and training metrics to a SQLite or PostgreSQL database using `scalarstop.train_store <https://www.scalarstop.com/en/latest/autoapi/scalarstop/train_store/#module-scalarstop.train_store>`_.\n',
    'author': 'Neocrym Records Inc',
    'author_email': 'engineering@neocrym.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.scalarstop.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
