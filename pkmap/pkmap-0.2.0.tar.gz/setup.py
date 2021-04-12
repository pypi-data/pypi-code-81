
import codecs
import os

from setuptools import setup, find_packages

from pkmap.__init__ import __version__


THENAME = "pkmap"
DESCRIPTION = "xxx"
MAINTAINER = "ZJ Lewous"
MAINTAINER_EMAIL = "zj.lewous@gmail.com"
URL = "https://github.com/pkmap/pkmap"
LICENSE = "Mozilla"
DOWNLOAD_URL = "https://github.com/pkmap/pkmap/tarball/master"
VERSION = __version__
# CLASSIFIERS = [
#     "Intended Audience :: Science/Research",
#     "Intended Audience :: Developers",
#     "License :: OSI Approved",
#     "Programming Language :: C",
#     "Programming Language :: Python",
#     "Topic :: Software Development",
#     "Topic :: Scientific/Engineering",
#     "Operating System :: Microsoft :: Windows",
#     "Operating System :: POSIX",
#     "Operating System :: Unix",
#     "Operating System :: MacOS",
#     "Programming Language :: Python :: 3.6",
#     "Programming Language :: Python :: 3.7",
#     "Programming Language :: Python :: 3.8",
#     "Programming Language :: Python :: 3.9",
# ]
# INSTALL_REQUIRES = [
#     "numpy>=1.13.3",
#     "scipy>=0.19.1",
#     "scikit-learn>=0.24",
#     "joblib>=0.11",
# ]
# EXTRAS_REQUIRE = {
#     "optional": [
#         "keras",
#         "tensorflow",
#     ],
#     "dev": [
#         "black",
#         "flake8",
#     ],
#     "tests": [
#         "pytest",
#         "pytest-cov",
#     ],
#     "docs": [
#         "sphinx",
#         "sphinx-gallery",
#         "pydata-sphinx-theme",
#         "sphinxcontrib-bibtex",
#         "numpydoc",
#         "matplotlib",
#         "pandas",
#         "seaborn",
#     ],
# }



setup(
    name = THENAME,
    version = __version__,
    packages = find_packages(),
    # package_data = {"": ["*.yaml"]},
    install_requires = [
        "numpy", 
        "pandas", 
        "matplotlib==3.1.3", 
        "seaborn", 
        "scikit-learn>=0.21.2", 
        "jupyter", 
        "tqdm", 
    ],
    extras_require = {
        "optional": [
            "nilmtk",
        ]
    },
    description = DESCRIPTION,
    author = MAINTAINER,
    author_email = MAINTAINER_EMAIL,
    url = URL,
    download_url = DOWNLOAD_URL,
    # long_description = open("README.md", encoding="utf-8").read(),
    long_description = "see in " + URL, 
    license = LICENSE,
    # classifiers=[
    #     "Development Status :: 3 - Alpha",
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: Apache 2.0",
    #     "Programming Language :: Python",
    #     "Topic :: Scientific/Engineering :: Mathematics",
    # ],
    # keywords="smartmeters power electricity energy analytics redd "
    # "disaggregation nilm nialm",
)
