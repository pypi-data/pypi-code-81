import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="tpjl",
    version="2021.04.03",
    author="TechGeeks",
    author_email="PJSONLang@tgeeks.cf",
    maintainer="Rajdeep Malakar",
    maintainer_email="Rajdeep@tgeeks.cf",
    description="a free & OpenSource Portable version of JSON.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TechGeeks-Dev/PJSONLang",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)