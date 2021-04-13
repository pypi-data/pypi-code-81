
from setuptools import setup

__version__ = "0.0.6"
    
with open("README.md", "r") as fh:
    long_description = fh.read()
            
setup(name = 'pygomme',
      version = __version__,
      description = 'A simple package for calculating errors propagation',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author = 'Marc Albrecht',
      author_email = 'marc.albrecht@free.fr',
      packages = ['pygomme',],
      package_data = {'pygomme':['license.txt']},
      python_requires='>=3.6',
      install_requires=['numpy>=1.13','scipy','matplotlib'],
      zip_safe = True,
      classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Physics"
        ]   
      )


    
    
