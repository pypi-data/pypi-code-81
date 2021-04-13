import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dollarN",                     # This is the name of the package
    version="1.2.4",                        # The initial release version
    author="Michael Ortega",                     # Full name of the author
    author_email='michael.ortega@imag.fr',
    url='https://github.com/mikefromlig/dollarN',
    description="Implementation of the $N 2D gesture recognizer",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["dollarN"],                # Name of the python package
    package_dir={'':'dollarN/src'},        # Directory of the source code of the package
    install_requires=['numpy',]              # Install other dependencies if any
)
