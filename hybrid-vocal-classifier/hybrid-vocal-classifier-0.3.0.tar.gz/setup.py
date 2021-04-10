# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hvc',
 'hvc.features',
 'hvc.neuralnet',
 'hvc.neuralnet.models',
 'hvc.parse',
 'hvc.plot',
 'hvc.utils']

package_data = \
{'': ['*']}

install_requires = \
['Keras>=2.4.3',
 'PyYAML>=5.4.1',
 'joblib>=1.0.1',
 'matplotlib>=3.4.1',
 'numpy>=1.19.2',
 'scikit-learn>=0.24.1',
 'scipy>=1.6.2',
 'tensorflow>=2.4.1']

setup_kwargs = {
    'name': 'hybrid-vocal-classifier',
    'version': '0.3.0',
    'description': 'a Python machine learning library for animal vocalizations and bioacoustics',
    'long_description': '[![DOI](https://zenodo.org/badge/78084425.svg)](https://zenodo.org/badge/latestdoi/78084425)\n[![Documentation Status](https://readthedocs.org/projects/hybrid-vocal-classifier/badge/?version=latest)](http://hybrid-vocal-classifier.readthedocs.io/en/latest/?badge=latest)\n[![CI](https://github.com/NickleDave/hybrid-vocal-classifier/actions/workflows/ci.yml/badge.svg)](https://github.com/NickleDave/hybrid-vocal-classifier/actions)\n[![codecov](https://codecov.io/gh/NickleDave/hybrid-vocal-classifier/branch/main/graph/badge.svg?token=9c27qf9WBf)](https://codecov.io/gh/NickleDave/hybrid-vocal-classifier)\n# hybrid-vocal-classifier\n## a Python machine learning library for animal vocalizations and bioacoustics \n![finch singing with annotated spectrogram of song](./docs/images/gr41rd41_song.png)\n\n### Getting Started\nYou can install with pip: `$ pip install hybrid-vocal-classifier`  \nFor more detail, please see: https://hybrid-vocal-classifier.readthedocs.io/en/latest/install.html#install\n\nTo learn how to use `hybrid-vocal-classifier`, please see the documentation at:  \nhttp://hybrid-vocal-classifier.readthedocs.io  \nYou can find a tutorial here: https://hybrid-vocal-classifier.readthedocs.io/en/latest/tutorial.html  \nA more interactive tutorial in Jupyter notebooks is here:  \nhttps://github.com/NickleDave/hybrid-vocal-classifier-tutorial  \n\n### Project Information\nthe `hybrid-vocal-classifier` library (`hvc` for short) \nmakes it easier for researchers studying\nanimal vocalizations and bioacoustics \nto apply machine learning algorithms to their data. \nThe focus on automating the sort of annotations  \noften used by researchers studying \n[vocal learning](https://www.sciencedirect.com/science/article/pii/S0896627319308396)  \nsets `hvc` apart from more general software tools for bioacoustics.\n \nIn addition to automating annotation of data, \n`hvc` aims to make it easy for you to compare different models people have proposed,  \nusing the data you have in your lab,\n so you can see for yourself which one works best for your needs. \nA related goal is to help you figure out \njust how much data you have to label to get "good enough" accuracy for your analyses.\n \nYou can think of `hvc` as a high-level wrapper around \nthe [`scikit-learn`](https://scikit-learn.org/stable/) library, \nplus built-in functionality for working with annotated animal sounds.\n\n### Support\nIf you are having issues, please let us know.\n- Issue Tracker: <https://github.com/NickleDave/hybrid-vocal-classifier/issues>\n\n### Contribute\n- Issue Tracker: <https://github.com/NickleDave/hybrid-vocal-classifier/issues>\n- Source Code: <https://github.com/NickleDave/hybrid-vocal-classifier>\n\n### CHANGELOG\nYou can see project history and work in progress in the [CHANGELOG](./doc/CHANGELOG.md)\n\n### License\nThe project is licensed under the [BSD license](./LICENSE).\n\n### Citation\nIf you use this library, please cite its DOI:  \n[![DOI](https://zenodo.org/badge/78084425.svg)](https://zenodo.org/badge/latestdoi/78084425)\n\n### Backstory\n`hvc` was originally developed in [the Sober lab](https://scholarblogs.emory.edu/soberlab/) \nas a tool to automate annotation of birdsong (as shown in the picture above). \nIt grew out of a submission to the \n[SciPy 2016 conference](https://conference.scipy.org/proceedings/scipy2016/david_nicholson.html) \nand later developed into a library, \nas presented in this talk: https://youtu.be/BwNeVNou9-s\n',
    'author': 'David Nicholson',
    'author_email': 'nickledave@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NickleDave/hybrid-vocal-classifier',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
