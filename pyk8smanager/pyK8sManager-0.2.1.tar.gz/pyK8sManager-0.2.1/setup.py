from setuptools import setup, find_packages

VERSION = '0.2.1' 
DESCRIPTION = 'pyK8sManager'
LONG_DESCRIPTION = 'pyK8sManager'

setup(
        name="pyK8sManager", 
        version=VERSION,
        author="Lucian Tin Udovicic",
        author_email="luciantin@protonmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["kubernetes"], 
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
        ]
)
