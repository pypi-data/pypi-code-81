
from setuptools import find_packages, setup

# create setup to be used by pip
setup(
    name='mfp',
    packages=find_packages(include=["mfp", "mfp.*"]),
    version='0.1.0',
    install_requires=['numpy', 'pandas'],
    description='my first package',
    author='Ben van Vliet',
    author_email='benvliet@icloud.com',
    license=''
)
