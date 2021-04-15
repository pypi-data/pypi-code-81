from setuptools import setup, find_packages

VERSION = "1.0"
DESCRIPTION = 'Basic Math Package'
LONG_DESCRIPTION = 'Basic math operators.'

setup(
       # the name must match the folder name 'verysimplemodule'
        name="basicmath", 
        version=VERSION,
        author="Balaguru",
        author_email="<balagurudmanickam@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
