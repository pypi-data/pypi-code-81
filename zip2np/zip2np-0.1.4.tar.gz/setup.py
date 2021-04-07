import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

OFFICIAL_PACKAGE_NAME= "zip2np"
VERSION="0.1.4"
LICENSE="MIT"
LIBRARY_NAME = "zip2np"
AUTHOR="Borjakas"
URL="https://github.com/borjaeg/zip2np"
DEPENDENCIES=[
    "numpy",
    "tqdm",
    "opencv-python"
]

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name=OFFICIAL_PACKAGE_NAME, 
    packages=find_packages(include=[LIBRARY_NAME], 
                           exclude=['tests']),
    version=VERSION,
    url=URL,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ],
    description='Library for decompressing Zip files and put into Numpy Arrays',
    author=AUTHOR,
    author_email="hello@borjakas.com",
    license=LICENSE,
    long_description=README,
    include_package_data=True,
    long_description_content_type="text/markdown",
    install_requires=DEPENDENCIES,
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1"]
)