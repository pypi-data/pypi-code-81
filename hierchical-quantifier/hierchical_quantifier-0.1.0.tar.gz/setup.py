import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hierchical_quantifier",
    version="0.1.0",
    author="Niroshan Vijayarasa",
    author_email="nirobnc@gmail.ch",
    description="computig hierarchical quantifier value from music pieces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DCMLab/hierarchicity-in-music",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)