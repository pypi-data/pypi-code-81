
from setuptools import setup, find_packages

__version__ = "0.0.7"
    
with open("README.md", "r") as fh:
    long_description = fh.read()
            
setup(name = 'pygomme',
      version = __version__,
      description = 'A simple package for calculating errors propagation',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author = 'Marc Albrecht',
      author_email = 'marc.albrecht@free.fr',
      packages = ['pygomme','pygomme'],
      package_data={'pygomme': ['examples/*.py','examples/*.png']},
      python_requires='>=3.6',
      install_requires=['numpy>=1.13','scipy','matplotlib','functools'],
      zip_safe = True,
      classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Physics"
        ]   
      )


    
    
