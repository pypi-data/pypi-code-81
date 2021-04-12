from setuptools import find_packages, setup
#from my_pip_pkg import __version__
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="demo_pip",
    version="1.0.1",
    description="demo project",
    long_description= README,
    long_description_content_type="text/markdown",
    author="shubham",
    install_requires=["numpy"],
    packages=find_packages(),
)