import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION.txt", "r") as fh:
    version = fh.read().strip()

setuptools.setup(
     name='matrixb',
     version=version,
     author="Kevin Crouse",
     author_email="krcrouse@gmail.com",
     description="An extensible package to automate and enhance the manipulation of tabular/matrix data without giving up performance.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://gitlab.com/krcrouse/matrixb",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3.7",
         "License :: OSI Approved :: Apache Software License",
         "Operating System :: OS Independent",
         "Development Status :: 3 - Alpha"
     ],
     #
     # List the modules recommended for certain types of exports.
     #
     extra_require={
             'dataframe': ['pandas'],
             'xls': ['xlrd', 'xlwt'],
             'xlsx': ['openpyxl'],
             #'googleapps': not ready yet
             #'ods': not mature yet
     }
 )
