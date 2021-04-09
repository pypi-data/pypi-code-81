from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# any data files that match this pattern will be include in the build
data_files_to_include = ["*.png"]

setup(
    name='ez-icons',
    version='1.0.1',
    packages=find_packages(),
    package_data={
        "": data_files_to_include,
    },
    url='https://github.com/nielsvaes/ez_icons',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache 2.0',
    author='Niels Vaes',
    author_email='nielsvaes@gmail.com',
    description='Easily code complete your way to the Material Icons',
)
