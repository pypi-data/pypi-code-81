import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="inkebase", 
    version="1.6.0",                       
    author="inke-bigdata",              
    author_email="majiankun@inke.cn",    
    description="Common tools", 
    long_description=long_description,              
    long_description_content_type="text/markdown",  
    packages=setuptools.find_packages(),    
    classifiers=[                    
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
