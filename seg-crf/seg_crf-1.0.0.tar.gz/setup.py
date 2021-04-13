# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = "Conditional Random Field Implementation for segmentation models as used in Deeplab-v2"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
INSTALL_REQUIRES = ['gray2color',
                    'pydensecrf']

setup(
        name="seg_crf", 
        version=VERSION,
        author="Talha Ilyas",
        LICENSE = 'MIT License',
        author_email="mr.talhailyas@gmail.com",
        description=DESCRIPTION,
        long_description= long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES, 
        
        url = 'https://github.com/Mr-TalhaIlyas/Conditional-Random-Fields-CRF',
        
        keywords=['python', 'conditional random fields', 'segmentation', 
                  'crf', 'semantic segmentation', 'fully connected crf'
                  'dense crf','deeplabv2', ],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3.6",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
)