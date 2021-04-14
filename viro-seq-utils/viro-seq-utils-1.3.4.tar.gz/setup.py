#! /usr/bin/env python

"""
author: Nicolas JEANNE
email: jeanne.n@chu-toulouse.fr
Created on 22 jan. 2020
"""

import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="viro-seq-utils",
    version="1.3.4",
    author="Nicolas Jeanne",
    author_email="jeanne.n@chu-toulouse.fr",
    description="Utilities modules for sequences, alignments and phylogeny from Toulouse virology laboratory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://srvhpccode.icr.local/njeanne/viro-seq-utils",
    project_urls={
        "Bug Tracker": "http://srvhpccode.icr.local/njeanne/viro-seq-utils/-/issues",
    },
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Science/Research"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    keywords="alignment sequence phylogeny",
    license="GNU General Public License",
    install_requires=[
        "biopython",
        "numpy"
    ]
)
