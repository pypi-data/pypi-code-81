
from setuptools import setup, find_packages

with open("README.md", "r") as infile:
    readme = infile.read()

setup(
    name = "dbwrapper-python",
    version = "0.1.1",
    url = "https://github.com/azalac/dbwrapper",
    author = "azalac",
    description = ("Wraps SQL Syntax into a python API."),
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=readme,
    extras_require={
        "postgres": ["psycopg2"]
    }
)
