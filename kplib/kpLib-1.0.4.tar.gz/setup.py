import glob
from pathlib import Path

from setuptools import find_packages, setup

try:
    from pybind11.setup_helpers import Pybind11Extension, build_ext
except ImportError:
    from setuptools import Extension as Pybind11Extension
    from setuptools.command.build_ext import build_ext

ext_modules = [
    Pybind11Extension(
        "kpLib.lib",
        ["python/kpLib/interface.cpp"] + glob.glob("./src/*.cpp"),
        include_dirs=[
            "./src/",
        ],
    )
]


with open(Path(__file__).parent.joinpath("README.md").resolve()) as f:
    long_description = f.read()

if __name__ == "__main__":
    setup(
        name="kpLib",
        use_scm_version=True,
        description="Library for generating highly-efficient generalized Monkhorst-Pack k-point grids.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages("python"),
        package_dir={"": "python"},
        ext_modules=ext_modules,
        install_requires=["pybind11~=2.6", "pymatgen~=2021.3", "click~=7.1"],
        setup_requires=["pybind11", "setuptools_scm"],
        tests_require=["pytest"],
        python_requires=">=3.7",
        cmdclass={"build_ext": build_ext},
        zip_safe=False,
        entry_points={
            "console_scripts": [
                "kpgen = kpLib.cli:generate [cmd]",
            ],
        },
        keywords=[
            "VASP",
            "ABINIT",
            "materials science",
            "electronic structure",
            "crystal",
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Scientific/Engineering :: Physics",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    )
