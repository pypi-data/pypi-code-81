import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amxtelnet", # Replace with your own username
    version="0.0.4",
    author="Logan Vaughn",
    author_email="logantv@gmail.com",
    description="xlsx to amx dict list",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/amxtelnet",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/amxtelnet/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "amxtelnetlib"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)