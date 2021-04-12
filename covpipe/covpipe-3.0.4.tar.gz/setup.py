from setuptools import find_packages, setup
import covpipe.__version__ as vers
import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
    name='covpipe',
    packages=find_packages(include=["covpipe", "covpipe_tools"]),
    version=vers.VERSION,
    description='Sars-Cov-2 NGS Pipline for generating consensus sequences',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/RKIBioinformaticsPipelines/ncov_minipipe",
    tests_require=["pytest","PyYAML", "pandas"],
    install_requires=[
        "snakemake >5.26, <6.1.0",
        "strictyaml",
        "PyYAML",
        "biopython",
        "pysam",
        "pandas",
        "numpy"],
    entry_points={
        "console_scripts":[
            'covpipe = covpipe.ncov_minipipe:main',
            'ncov_minipipe = covpipe.ncov_minipipe:main', 
            'create_bedpe = covpipe_tools.create_bedpe:main',
            'update_pangolin = covpipe_tools.update_pangolin:main'
        ]},
    include_package_data = True,
    package_data={
        "covpipe":[
            "covpipe/ncov_minipipe.snake",
            "covpipe/ncov_minipipe.Rmd",
            "covpipe/ncov_minipipe.config",
            "covpipe/rules/*.smk",
            "covpipe/scripts/*",
            "covpipe_tools/*.py",
            "covpipe/data/*"]
        },
    author='Oliver Drechsel, Stephan Fuchs, Martin Hölzer, René Kmiecinski',
    author_email="r.w.kmiecinski@gmail.com",
    license='GPLv3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)


