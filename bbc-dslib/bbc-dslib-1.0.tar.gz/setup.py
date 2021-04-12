import os

import setuptools

from version import __version__

CURRENT_FILEPATH = os.path.abspath(os.path.dirname(__file__))
VERSION_FILENAME = 'version.py'


setuptools.setup(
    name='bbc-dslib',
    version=__version__,
    author='Raphaël Berly',
    author_email='raphael.berly@blablacar.com',
    description='A lib for the Data Science team at Blablacar',
    license='closed',
    url="https://github.com/blablacar/data-dslib",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['humanfriendly', 'pyyaml', 'jinja2'],
    extras_require={
        'database': ['sqlalchemy', 'psycopg2-binary', 'PyMySQL', 'pandas==1.1.3'],
        'facebook': ['fbprophet'],
        'google': [
            'google-cloud-bigquery==1.28.0',
            'google-cloud-bigquery-storage==0.8.0',
            'google-cloud-storage==1.31.2',
            'google-api-python-client==1.12.3',
            'pyarrow==1.0.1',
            'oauth2client==4.1.3',
            'grpcio==1.32.0',
            'pandas==1.1.3',
            'pandas-gbq==0.14.0',
            'tqdm==4.50.2',
            'gspread==3.6.0',
            'gspread-dataframe==3.0.6'
        ],
        'science': [
            'scikit-learn==0.23.2',
            'numpy==1.19.3',
            'matplotlib==3.2.1',
            'dill==0.3.1.1',
            'pandas==1.1.3'
        ],
        'testing': ['pytest', 'pytest-cov', 'coverage', 'mock', 'testfixtures'],
    }
)
