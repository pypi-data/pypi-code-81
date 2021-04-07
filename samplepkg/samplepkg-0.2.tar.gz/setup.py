## The setup file.

from setuptools import setup

setup(name="samplepkg",
    version="0.2",
    description="Not much to see here.",
    author="Rick Astley",
    ##data_files=[
    ##    ("data", ["samplepkg/data/dogetext.txt"])
    ##],
    include_package_data=True,
    zip_safe=False)
