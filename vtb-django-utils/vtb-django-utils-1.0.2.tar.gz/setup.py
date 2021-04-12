"""
Описание установки
"""
from setuptools import setup, find_packages

"""
python -m pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python -m twine upload dist/*
"""

REQUIRED = [
    'vtb-http-interaction>=0.0.4',
    'django>=3.0.0',
    'djangorestframework>=3.12.2'
]

setup(
    name='vtb-django-utils',
    version='1.0.2',
    packages=find_packages(exclude=['tests']),
    url='https://bitbucket.region.vtb.ru/projects/PUOS/repos/vtb-django-utils',
    license='',
    author='VTB',
    author_email='',
    description='django utils for VTB projects',
    install_requires=REQUIRED,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Framework :: Django :: 3.0",
        "Operating System :: OS Independent",
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-env',
            'pylint',
            'pytest-asyncio'
        ]
    }
)
