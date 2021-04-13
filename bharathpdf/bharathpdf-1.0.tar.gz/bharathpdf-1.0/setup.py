import setuptools
from pathlib import Path


setuptools.setup(
    name="bharathpdf",
    version='1.0',
    description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests","data"])
)