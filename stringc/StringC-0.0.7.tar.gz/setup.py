from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Persian",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
        "Topic :: Text Editors :: Text Processing",

    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="StringC",
    version="0.0.7",
    description='This Package Convert numeric date in the string to the datetime object',
    py_modules=['StringC', 'conf'],
    package_dir={'': 'src'},
    url="https://bitbucket.org/mvahid/stringc.git",
    author="Mohammad Vahid",
    author_email="m.vahid.da@gmail.com",
    install_requires=["persiantools ~= 2.1.1",
                      "python-dateutil ~= 2.8.1",
                      "regex ~= 2021.3.17",
                      "Unidecode ~= 1.2.0",
                      ],
    extras_require={
        "dev": [
            "pytest>=3.7",
            "twine>=3.4.1",
            "check-manifest>=0.46",
        ],
    }
)
