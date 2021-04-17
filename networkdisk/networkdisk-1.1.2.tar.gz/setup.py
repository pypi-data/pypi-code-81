import os
from setuptools import setup, find_packages
import networkdisk as nd

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()
packages = find_packages()
requires = list(read("requirements/default.txt").split("\n"))

setup(
    name = "networkdisk",
    version = nd.__version__,
    keywords = "graph, networkx, database",
    url = "https://networkdisk.inria.fr",
	project_urls = {
		"repository": "https://gitlab.inria.fr/guillonb/networkdisk",
		"documentation": "https://networkdisk.inria.fr/documentation"
	},
    install_requires = requires,
    packages=packages,
    include_package_data=True,
    long_description=read('README.rst'),
	description= "NetworkDisk: On disk graph manipulation",
	author= "Bruno Guillon, Charles Paperman",
	author_email= "bruno.guillon@uca.fr, charles.paperman@univ-lille.fr",
	licence= "3-clause BSD licence",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
