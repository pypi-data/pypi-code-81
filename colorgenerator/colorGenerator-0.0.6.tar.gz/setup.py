import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colorGenerator", # Replace with your own username
    version="0.0.6",
    author="tttienthinh",
    author_email="tranthuongtienthinh@gmail.com",
    description="This package help you find complementary colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tttienthinh/colorGenerator.git",
    project_urls={
        "Download": "https://pypi.org/project/colorGenerator/",
        "Source Code": "https://github.com/tttienthinh/colorGenerator.git",
        "Documentation": "https://colorgenerator.readthedocs.io",
        "Bug Tracker": "https://github.com/tttienthinh/colorGenerator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)