# -*- coding: utf-8 -*-
import sys
import pathlib
import setuptools 

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="osmscigrid",
    version="1.0.1",
    description="Extracting gas transport pipelines OSM pbf-files and exporting to SciGRID_gas structure",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/osmscigrid",
    author="Adam Pluta",
    author_email="Adam.Pluta@dlr.de",
    package_dir={'':'src'},
    packages=setuptools.find_namespace_packages(where='src'),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
     python_requires='>=3.6',
     install_requires=['protobuf >= 3, < 4', 
                       'esy-osm-pbf >= 0',
                       'Unidecode==1.1.1', 
                       'pandas>=0.25.3',
                       'pathlib>=1.0.1',
                       'esy-osmfilter',
                       'quantulum3==0.7.6',
                       'mplcursors==0.4',
                       'descartes==1.1.0',
                       'adjustText==0.7.3',
                       'numpy==1.19.4',
                       'PyShp',
                       'geopy',
                       'scipy==1.6.2',
                       'Shapely==1.7.1']
            
)
