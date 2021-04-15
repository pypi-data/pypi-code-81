from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext
import glob


ext_modules = [
    Pybind11Extension(
        "kpLib.lib",
        ["python/kpLib/interface.cpp"] + glob.glob("./src/*.cpp"),
        include_dirs=[
            "./src/",
        ],
    )
]


if __name__ == "__main__":
    setup(
        name="kpLib",
        use_scm_version=True,
        description="Library for generating highly-efficient generalized Monkhorst-Pack k-point grids.",
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
    )
