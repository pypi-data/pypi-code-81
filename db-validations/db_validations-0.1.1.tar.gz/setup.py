from setuptools import setup, find_packages

PKG_NAME = 'db_validations'
with open(f'{PKG_NAME}/_version.py') as f:
    __version__ = '0.0.0'
    exec(f.read())

setup(
    name=PKG_NAME,
    version=__version__,
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'pydantic',
    ],
)
