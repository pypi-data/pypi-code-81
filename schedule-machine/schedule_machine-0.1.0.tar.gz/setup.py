#setup.py
'''
setup file for schedule_machine
'''

import setuptools
from setuptools import setup


with open("README.md") as file:
    read_me_description = file.read()

# This call to setup() does all the work
setup(
    name="schedule_machine",
    version="0.1.0",
    description="A simple python scheduler",
     long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BradKentAllen/schedule_machine",
    author="Brad Allen - AditNW LLC",
    author_email="brad.allen@aditnw.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["schedule_machine"],
    include_package_data=True,
    install_requires=["pytz"],
    python_requires='>=3.6',

)