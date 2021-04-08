from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pvoutput_publisher",
    version="0.20.0",
    package_dir={"": "src"},
    # packages=[""],
    packages=find_packages("src"),
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    url="https://bitbucket.org/clockworkcodeteam/pvoutput-publisher/src/master/",
    license="GNU General Public License V3 or later",
    author="dilbertau99",
    author_email="dilbertau99@gmail.com",
    description="read from solar inverters that implement the SunSpec interface, to simpler datastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="solar monitoring inverter communications reader pvoutput",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Topic :: Communications",
    ],
    install_requires=["retry", "requests", "urllib3"],
    tests_require=["responses"]

)
