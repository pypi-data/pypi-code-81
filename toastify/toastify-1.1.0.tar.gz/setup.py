import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="toastify",
    version="1.1.0",
    description="Simple and Lighweight Windows 10 Toast Notifications.",
    long_description=README,
    long_description_content_type="text/markdown",
    #url="https://github.com/realpython/reader",
    author="Tanishq-Banyal",
    #author_email="banyaltanishq@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["toastify"],
    include_package_data=True,
    #install_requires=[],
)