import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="baarutil",
    version="1.0.0",
    author="Zhaoyu Xu, Souvik Roy",
    author_email="zhaoyu.xu@alliedmedia.com, souvik.roy@alliedmedia.com",
    description="Utility functions for BAAR developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Allied-Media/baarutil",
    project_urls={
        "Bug Tracker": "https://github.com/Allied-Media/baarutil/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    instrall_requires=[
        "numpy >=1.18.4",
        "pandas >=1.0.3"
    ],
    python_requires=">=3.6.8",
)