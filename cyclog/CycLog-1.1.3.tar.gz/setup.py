import setuptools


with open("README.md", encoding="u8") as readme:
    long_description = readme.read()

setuptools.setup(
    name="CycLog",
    version="1.1.3",
    author="Jonatan",
    author_email="pybots.il@gmail.com",
    description="A python module to handle cyclic logs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonatan1609/CycleLog",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: System :: Logging",
    ],
    python_requires=">=3"
)
