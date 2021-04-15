from setuptools import setup


with open('README.md','r') as f:
    long_description = f.read()



setup(name="constant_nums"
,version="0.4"
,description="A final function for your constant variables"
,long_description = long_description
,long_description_content_type='text/markdown'
,author = "Ashutosh Joshi"
,packages = ['constant_nums'],
install_requires = [])
