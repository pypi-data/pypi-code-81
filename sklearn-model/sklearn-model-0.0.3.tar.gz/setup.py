from os import path, walk
from setuptools import setup

import sklearn_model.version

### To run the tests:
# python setup.py test

### To install on a machine:
# sudo python setup.py install

### To install in a home directory (~/lib):
# python setup.py install --home=~
LONG_DESCRIPTION = open(path.join(path.dirname(__file__), 'README.md')).read()

setup(name="sklearn-model",
      version=sklearn_model.version.__version__,
      author="Ankit Mahato",
      author_email="ankit@realworldpython.guide",
      keywords='scikit-learn json scoring inference engine deployment machine learning data mining',
      packages=['sklearn_model'],
      description="Export scikit-learn models into JSON for Inference.",
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/markdown",
      url="https://github.com/animator/sklearn-model",
      project_urls={
            "Source Code": "https://github.com/animator/sklearn-model",
            "Bug Tracker": "https://github.com/animator/sklearn-model/issues",
            "Documentation": "https://realworldpython.guide/sklearn-model/",
      },
      test_suite="test",
      install_requires=["scikit-learn>=0.22", "pandas"],
      tests_require=["scikit-learn>=0.22", "pandas"],
      python_requires='>=3.4',
      classifiers=[  
            'Development Status :: 5 - Production/Stable', 
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Information Technology',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Natural Language :: English',
      ],      
      )