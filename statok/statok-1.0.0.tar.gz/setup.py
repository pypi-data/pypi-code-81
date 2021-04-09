import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="statok",
    version="1.0.0",
    description="A simple module to get statistics of a tiktok account",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ProgrammingMyLife/statstok",
    author="Classified",
    author_email="futuredd10@gmail.com",
    packages=["statok"],
    include_package_data=True,
    install_requires=["bs4", "requests"]
    
)