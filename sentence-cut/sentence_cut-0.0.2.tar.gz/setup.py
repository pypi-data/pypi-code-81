import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sentence_cut",
    version="0.0.2",
    author="Yu",
    author_email="t-yhan@microsoft.com",
    description="sentence cut.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/xxx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
