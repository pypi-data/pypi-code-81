import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="antp",
    version="0.0.1",
    author="anttin",
    author_email="muut.py@antion.fi",
    description="Python Template Processor for Jinja templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anttin/antp",
    packages=setuptools.find_packages(),
    install_requires=
    [
      "Jinja2",
      "anoptions"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
