from setuptools import find_packages, setup
from Cython.Build import cythonize
from distutils.extension import Extension

import numpy as np


with open("README.md", 'r') as f:
    long_description = f.read()

ext_modules = [
    Extension(
        name="disparity_interpolation",
        sources=["disparity_interpolation/disparity_interpolation.pyx"],
        include_dirs=["/usr/local/include/", np.get_include()],
        libraries=["opencv_core", "opencv_imgproc"],
        language="c++",
        extra_compile_args=["-w", "-O3"],
    )
]

setup(
    name="disparity_interpolation",
    version="1.0.3",
    packages=find_packages(),
    author="Jhony Kaesemodel Pontes",
    description="Nearest neighbor interpolation for disparity images with missing parts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhonykaesemodel/disparity_interpolation",
    ext_modules=cythonize(ext_modules),
    install_requires=["numpy==1.19"],
)
