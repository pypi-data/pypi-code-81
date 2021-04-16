#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from setuptools import Extension, setup

cmd = sys.argv[1]

VERSION = "0.2.3"


requires_numpy_headers = any(cmd.startswith(c) for c in ("install", "build", "bdist"))


if requires_numpy_headers:
    try:
        import numpy.distutils.misc_util

        include_dirs = numpy.distutils.misc_util.get_numpy_include_dirs()
    except ImportError:
        print("please install numpy first")
        sys.exit(1)
else:
    # happens at install time when fetching meta data and when setting up on ci server
    # no compilation will happen for "sdist" sub command and it is not sure at this
    # stage if numpy is already installed by tox.
    include_dirs = []

if requires_numpy_headers or "dist" in cmd:  # sdist, bdist, bdist_wheel etc.
    # run script to call cython to create _recfast.cpp
    here = os.path.dirname(os.path.abspath(__file__))
    os.system(os.path.join(here, "update_wrapper.sh"))

ext = Extension(
    "recfast4py._recfast",
    sources=[
        "recfast4py/_recfast.cpp",
        "recfast4py/cosmology.Recfast.cpp",
        "recfast4py/evalode.Recfast.cpp",
        "recfast4py/recombination.Recfast.cpp",
        "recfast4py/ODE_solver.Recfast.cpp",
        "recfast4py/DM_annihilation.Recfast.cpp",
        "recfast4py/Rec_corrs_CT.Recfast.cpp",
    ],
    extra_compile_args=["-stdlib=libc++",] if sys.platform == "darwin" else [],
)


try:
    desc = open("README.rst").read()
except IOError:
    desc = ""

required = ["numpy"]

setup(
    name="recfast4py",
    version=VERSION,
    author="Joel Akeret, Uwe Schmitt",
    author_email="jakeret@phys.ethz.ch",
    url="http://refreweb.phys.ethz.ch/software/recfast4py/0.1.3",
    packages=["recfast4py"],
    description=(
        "A slightly modified version of Recfast++ to do the "
        "recombination computation"
    ),
    long_description=desc,
    install_requires=required,
    ext_modules=[ext],
    include_dirs=include_dirs,
    package_data={"recfast4py": ["data/*.dat"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    zip_safe=False,
)
