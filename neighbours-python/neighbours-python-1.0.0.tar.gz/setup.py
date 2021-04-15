import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="neighbours-python",
    version="1.0.0",
    author="CHAI Ziqi",
    author_email="chaiziqi@sjtu.edu.cn",
    description="A modified package from NearPy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['future','numpy','scipy','bitarray'],
)
