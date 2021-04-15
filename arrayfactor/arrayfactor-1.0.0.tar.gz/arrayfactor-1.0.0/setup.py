# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 13:35:32 2021

@author: Merve Tascioglu
"""


from setuptools import setup, find_packages


VERSION = '1.0.0'
DESCRIPTION = 'Array Factor Pattern'
LONG_DESCRIPTION = ''''A package that allows to observe the array factor pattern with respect to required inputs: 
                                                                                                                Array Layout
                                                                                                                Inter-element spacing,
                                                                                                                frequency
                                                                                                                steering_angle,
                                                                                                                number of element
                                                                                                                increase_rate
                                                                                                               plane.'''

# Setting up
setup(
    name="arrayfactor",
    version=VERSION,
    author="Merve Tascioglu",
    author_email="<merve.tascioglu@barkhauseninstitut.org>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'antenna array', 'array factor'],
    
    classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: Microsoft :: Windows",
        ]    
    
)