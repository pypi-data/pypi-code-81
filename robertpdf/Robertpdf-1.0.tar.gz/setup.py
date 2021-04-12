import setuptools
from pathlib import Path

setuptools.setup(
    name="Robertpdf",
    version=1.0,
    long_dcription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
