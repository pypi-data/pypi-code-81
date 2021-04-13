from setuptools import find_packages, setup

import numpy as np
from Cython.Build import cythonize


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name="disparity_interpolation",
    version="1.0.1",
    packages=find_packages(),
    author="Jhony Kaesemodel Pontes",
    description="Nearest neighbor interpolation for disparity images with missing parts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhonykaesemodel/disparity_interpolation",
    ext_modules=cythonize(["disparity_interpolation/disparity_interpolation.pyx"]),
    include_dirs=["/usr/local/include/", np.get_include()],
    install_requires=["numpy==1.19"],
    language="c++",
    extra_compile_args=["-w", "-O3", "std=c++11"],
)
