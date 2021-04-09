from setuptools import setup, find_packages

setup(
    name = "downloadbook",
    version = "0.0.1",
    keywords = ["pip", "download", "book", "zerenl"],
    description = "download books",
    long_description = "download books from a website",
    license = "MIT Licence",

    url = "https://github.com/zerenlu/downloadbook",
    author = "zerenlu",
    author_email = "zeren.lu@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests", "bs4"]

)
