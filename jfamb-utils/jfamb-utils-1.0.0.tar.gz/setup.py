import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="jfamb-utils",
    version="1.0.0",
    author="Jonas Freire",
    author_email="jonasfreireperson@gmail.com",
    description="Test to understand PyPI packages dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['simple-sum'],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
