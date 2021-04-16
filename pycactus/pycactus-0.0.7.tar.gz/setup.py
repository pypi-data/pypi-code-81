from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


NAME = "pycactus"
VERSION = "0.0.7"

REQUIRES = ["azure-functions"]


setup(
    name=NAME,
    version=VERSION,
    description="Adapter to run an Azure Function Application with a WSGI Web Server.",
    author="Claudjos",
    author_email="claudjosmail@gmail.com",
    url="https://github.com/Claudjos/cactus",
    keywords=["Azure Function", "Web App"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={},
    include_package_data=False,
    long_description_content_type='text/markdown',
    long_description=long_description
)
