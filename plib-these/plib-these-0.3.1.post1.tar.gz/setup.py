import setuptools

with open("README.md", "r") as fh :
    long_description = fh.read()


setuptools.setup(
     name='plib-these',  
     version='0.3.1-1',
     scripts=['plib/plib.py'] ,
     author="P. Delpierre / O. Irwin",
     author_email="<pauline.delpierre@univ-lille.fr>",
     description="Librairie générale pour la thèse",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/pdelpierre/plib",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
     install_requires = [
         "numpy", "matplotlib"
     ]
 )