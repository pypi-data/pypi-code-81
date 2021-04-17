import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ACStubeCode", # Replace with your own username
    version="0.0.1",
    author="NL",
    author_email="nelson.lopes@tecnico.ulisboa.pt",
    description="data analysis code for tube data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "extract"},
    packages=setuptools.find_packages(where="extract"),
    python_requires=">=3.6",
)
