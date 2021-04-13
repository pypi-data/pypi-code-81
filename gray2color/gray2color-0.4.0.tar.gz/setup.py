# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.4.0'
DESCRIPTION = "Convert your grayscale semantic masks (vistas/cityscape style) to RGB colored masks wiht built-in or custom pallets"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
INSTALL_REQUIRES = []

setup(
        name="gray2color", 
        version=VERSION,
        author="Talha Ilyas",
        LICENSE = 'MIT License',
        author_email="mr.talhailyas@gmail.com",
        description=DESCRIPTION,
        long_description= long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES, 
        
        url = 'https://github.com/Mr-TalhaIlyas/Converting-Grayscale-Semantic-Masks-to-Color',
        
        keywords=['python', 'gray2rgb', 'gray2color', 
                  'grayscale to rgb', 'color pallets', 'cityscape'
                  'vistas','lip', 'ade20k', 'pannuke', 'pascal_voc'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
)