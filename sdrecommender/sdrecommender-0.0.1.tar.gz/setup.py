from setuptools import setup, find_packages

DESCRIPTION = ''
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
    
REQUIREMENTS = ["pandas>=1.0.3", "numpy>=1.20.0", "scikit-learn>=0.24.1", "scipy>=1.6.2"]

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name = "sdrecommender", 
        version = "0.0.1",
        author = "Rani Prake",
        author_email = "<pranavpathare1111@email.com>",
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        packages = find_packages(exclude=("tests",)),
        install_requires = REQUIREMENTS,
        python_requires ='>=3.6',
        keywords =['python', 'recommend', "recommender", "models", "machine learning", "similarity"],
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)