from setuptools import find_packages, setup
from my_pip_pkg import __version__
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='cs253_demo_pip34',
    version="1.0.2",

    description="A demo peoject for CS253 presentation",
    url='https://github.com/arka19das/cs253_package_upload.git',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Arka Das',
    author_email='dasarka@iitk.ac.in',
    install_requires=["numpy"],
    packages=find_packages(),
)
