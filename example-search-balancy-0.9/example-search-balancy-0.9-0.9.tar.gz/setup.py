from setuptools import setup

with open("README_package.md", "r") as file:
    long_description = file.read()

setup(
    name="example-search-balancy-0.9",
    version="0.9",
    author="balancy",
    author_email="balancy@gmail.com",
    install_requires=["beautifulsoup4", "lxml", "requests", "terminaltables"],
    packages=["search"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
