#import pathlib
from setuptools import setup

# The directory containing this file
#HERE = pathlib.Path(__file__).parent

# The text of the README file
#README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="riboloco",
    version="0.3.5",
    description="Riboseq analysis",
    #long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Delayed-Gitification/riboloco.git",
    author="Oscar Wilkins",
    author_email="oscar.wilkins@crick.ac.uk",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["riboloco"],
    include_package_data=True,
    install_requires=["pandas", "scipy", "pysam", "matplotlib", "seaborn", "gffutils", "sklearn"],
    entry_points={
        "console_scripts": [
            "riboloco=riboloco.__main__:main",
            "riboloco_convert_gff=riboloco.convert_gff:main",
            "riboloco_find_orfs=riboloco.find_orfs:main"
        ]
    },
)

"""
to install on cluster I used conda skeleton, then conda-build -c bioconda riboloco, then conda install /camp/.../riboloco.tar.bz2. Had to downgrade to python 3.7
"""
