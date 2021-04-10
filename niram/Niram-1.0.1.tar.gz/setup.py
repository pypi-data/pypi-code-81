import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Niram", # Replace with your own username
    version="1.0.1",
    author="Aswanth Vc",
    author_email="no-mail@mail.no",
    description="Simple python module to colour text",
    keywords=["colours","change coloure","terminal colour","python colours","pip colours","change colour in terminal","vhange text colour in python"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aswanthabam/Colours",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)