# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.1.7'
DESCRIPTION = "Tensorflow/Keras Model Profiler: Tells you model's memory requirement, no. of parameters, flops etc."

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
INSTALL_REQUIRES = [
                    'numpy',
                    'tabulate'
                    ]
# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="model_profiler", 
        version=VERSION,
        author="Talha Ilyas",
        LICENSE = 'MIT License',
        author_email="mr.talhailyas@gmail.com",
        description=DESCRIPTION,
        long_description= long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES, 
        
        url = 'https://github.com/Mr-TalhaIlyas/Tensorflow-Keras-Model-Profiler',
        
        keywords=['python', 'model_profile', 'gpu memory usage', 
                  'model flops', 'model parameters', 'gpu availability'
                  'mdoel memory requirement','weights memory requirement'],
        classifiers= [
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
)