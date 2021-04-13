from setuptools import setup

from domainrules import VERSION

setup(
    name='domainrules',
    version=VERSION,
    description='Rules give weight for different domains by some reason',
    install_requires=['pydantic', 'Levenshtein']
)