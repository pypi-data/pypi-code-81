from setuptools import find_packages, setup
import snakewrap.__version__ as vers
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name='snakewrap',
    packages=find_packages(),
    version=vers.VERSION,
    description='Snakemake Wrapper for NGS Pipelines',
    long_description=README,
    long_description_content_type="text/markdown",
    tests_require=["pytest","PyYAML", "pandas"],
    install_requires=[
        "snakemake>5.26",
        "PyYAML",
        "pandas"],
    entry_points={
        "console_scripts":[
            'swrap-quicksetup = scripts.swrap_quicksetup:main' 
        ]},
    #scripts=["scripts/swrap-quicksetup"],
    author='René Kmiecinski',
    author_email="r.w.kmiecinski@gmail.com",
    license='GPL-v3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
        ]
)


