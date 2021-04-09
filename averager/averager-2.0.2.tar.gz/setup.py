import setuptools

with open("README.md") as file:
    long_description = file.read()

setuptools.setup(
    name="averager",
    version="2.0.2",
    author="Ben Soyka",
    author_email="bensoyka@icloud.com",
    description="Simple utilities for calculating averages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://averager.readthedocs.io/",
    packages=setuptools.find_packages(),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    project_urls={
        "Source": "https://github.com/bsoyka/averager",
        "Changelog": "https://github.com/bsoyka/averager/releases",
    },
)
