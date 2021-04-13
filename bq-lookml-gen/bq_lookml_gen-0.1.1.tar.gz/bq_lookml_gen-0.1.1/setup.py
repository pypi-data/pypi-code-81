import pathlib
from setuptools import setup,find_packages

here = pathlib.Path(__file__).parent

install_requires = [

    'attrs==20.3.0',
    'botocore==1.18.18',
    'cachetools==4.2.1',
    'certifi==2020.12.5',
    'cffi==1.14.5',
    'chardet==3.0.4',
    'google-auth==1.28.1',
    'idna==2.9',
    'importlib-metadata==3.9.0',
    'isodate==0.6.0',
    'jmespath==0.10.0',
    'lkml==1.1.0',
    'numpy==1.20.2',
    'oauthlib==3.1.0',
    'pandas==0.24.2',
    'protobuf==3.15.6',
    'pyasn1==0.4.8',
    'pyasn1-modules==0.2.8',
    'pycparser==2.20',
    'pyrsistent==0.17.3',
    'python-dateutil==2.8.1',
    'python-slugify==4.0.1',
    'pytimeparse==1.1.8',
    'pytz==2020.5',
    'requests==2.23.0',
    'requests-oauthlib==1.3.0',
    'rsa==4.7.2',
    's3transfer==0.3.6',
    'six==1.15.0',
    'text-unidecode==1.3',
    'typing-extensions==3.7.4.3',
    'urllib3==1.25.11',
    'zipp==3.4.1',
    'pandas_gbq',
    'tqdm'

]

setup (

    name='bq_lookml_gen',
    version='0.1.1',
    entry_points={
        'console_scripts': [
            'bq_lookml_gen=bq_lookml_gen:output'
        ],
        'target': [
        'view = run:output'
    ],

    },
)