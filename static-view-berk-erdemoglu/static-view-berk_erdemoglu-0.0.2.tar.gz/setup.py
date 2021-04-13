import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="static-view-berk_erdemoglu", # Replace with your own username
    version="0.0.2",
    author="Berk Erdemoglu",
    author_email="berkerdemoglu1120@gmail.com",
    description="A package for opening HTML files on a local server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/berkerdemoglu/static_view",
    project_urls={
        "Bug Tracker": "https://github.com/berkerdemoglu/static_view/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
