import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyecodevices_rt2",
    version="1.0.0",
    author="pcourbin",
    author_email="pierre.courbin@gmail.com",
    description="Get information from GCE Ecodevices RT2.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pcourbin/pyecodevices_rt2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)