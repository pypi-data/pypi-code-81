# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robustnessgym',
 'robustnessgym.active',
 'robustnessgym.cachedops',
 'robustnessgym.cachedops.allen',
 'robustnessgym.core',
 'robustnessgym.core.dataformats',
 'robustnessgym.logging',
 'robustnessgym.slicebuilders',
 'robustnessgym.slicebuilders.attacks',
 'robustnessgym.slicebuilders.subpopulations',
 'robustnessgym.slicebuilders.transformations',
 'robustnessgym.tasks']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.21,<0.30.0',
 'cytoolz>=0.11.0,<0.12.0',
 'datasets>=1.1.3,<2.0.0',
 'dill>=0.3.3,<0.4.0',
 'fastBPE>=0.1.0,<0.2.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'ipywidgets>=7.6.2,<8.0.0',
 'jsonlines>=1.2.0,<2.0.0',
 'jupyterlab>=3.0.0,<4.0.0',
 'kaleido==0.1.0',
 'multiprocess>=0.70.11,<0.71.0',
 'numpy>=1.18.0,<2.0.0',
 'omegaconf>=2.0.5,<3.0.0',
 'plotly>=4.14.1,<5.0.0',
 'progressbar>=2.5,<3.0',
 'pyahocorasick>=1.4.0,<2.0.0',
 'python-Levenshtein>=0.12.0,<0.13.0',
 'pytorch-lightning>=1.1.2,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'semver>=2.13.0,<3.0.0',
 'tqdm>=4.27.0,<5.0.0',
 'transformers>=4.0.0,<5.0.0']

extras_require = \
{'adversarial': ['textattack>=0.2.15,<0.3.0'],
 'augmentation': ['nlpaug>=1.1.1,<2.0.0'],
 'summarization': ['rouge-score>=0.0.4,<0.0.5'],
 'text': ['nltk>=3.5,<4.0',
          'textblob>=0.15.3,<0.16.0',
          'spacy>=2.3.5,<3.0.0',
          'allennlp>=1.3.0,<2.0.0',
          'allennlp-models>=1.3.0,<2.0.0',
          'stanza>=1.1.1,<2.0.0'],
 'vision': ['torchvision>=0.8.0,<0.9.0']}

setup_kwargs = {
    'name': 'robustnessgym',
    'version': '0.0.4a1',
    'description': 'Robustness Gym is an evaluation toolkit for natural language processing.',
    'long_description': '\n\n<img src="docs/logo.png" width="50" height="50" alt="Robustness Gym logo"/> Robustness Gym\n================================\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/robustness-gym/robustness-gym/CI)\n![GitHub](https://img.shields.io/github/license/robustness-gym/robustness-gym)\n[![codecov](https://codecov.io/gh/robustness-gym/robustness-gym/branch/main/graph/badge.svg?token=MOLQYUSYQU)](https://codecov.io/gh/robustness-gym/robustness-gym)\n[![Documentation Status](https://readthedocs.org/projects/robustnessgym/badge/?version=latest)](https://robustnessgym.readthedocs.io/en/latest/?badge=latest)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![website](https://img.shields.io/badge/website-live-brightgreen)](https://robustnessgym.com)\n\nRobustness Gym is a Python evaluation toolkit for natural language processing. \n\n#### Coming Soon\n- Examples & tutorials\n- More documentation\n- Contributing guidelines\n\n\n### About\nRobustness Gym is being developed to address challenges in evaluating machine\n learning models today. You can read more about the ideas underlying Robustness Gym\n  in our paper on [arXiv](https://arxiv.org/pdf/2101.04840.pdf). We also have a\n   [website](https://robustnessgym.com).\n\nThe Robustness Gym project is an ongoing collaboration between [Stanford Hazy\n Research](https://hazyresearch.stanford.edu), [Salesforce Research](https://einstein.ai\n ) and [UNC Chapel-Hill](http://murgelab.cs.unc.edu/). \n\n_Note: Robustness Gym is in alpha, so expect frequent updates in the coming weeks and \nmonths. Reach out to kgoel [at] cs [dot] stanford [dot] edu if you\'d like to become an active contributor, \nor if you work on an interesting NLP task that you\'d like to see supported. \nFeel free to raise issues on GitHub for bugs/feature requests._\n\n### Installation\n```\npip install robustnessgym\n```\n\n### Robustness Gym in 5 minutes\n\n#### Datasets that extend Huggingface `datasets`\n```python\n# robustnessgym.Dataset wraps datasets.Dataset\nfrom robustnessgym import Dataset\n\n# Use Dataset.load_dataset(..) exactly like datasets.load_dataset(..) \ndataset = Dataset.load_dataset(\'boolq\')\ndataset = Dataset.load_dataset(\'boolq\', split=\'train[:10]\')\n```\n\n#### Cache information\n```python\n# Get a dataset\nfrom robustnessgym import Dataset\ndataset = Dataset.load_dataset(\'boolq\')\n\n# Run the Spacy pipeline\nfrom robustnessgym import Spacy\nspacy = Spacy()\n# .. on the \'question\' column of the dataset\ndataset = spacy(batch_or_dataset=dataset, \n                columns=[\'question\'])\n\n\n# Run the Stanza pipeline\nfrom robustnessgym import Stanza\nstanza = Stanza()\n# .. on both the question and passage columns of a batch\ndataset = stanza(batch_or_dataset=dataset[:32], \n                 columns=[\'question\', \'passage\'])\n\n# .. use any of the other built-in operations in Robustness Gym!\n\n\n# Or, create your own CachedOperation\nfrom robustnessgym import CachedOperation, Identifier\nfrom robustnessgym.core.decorators import singlecolumn\n\n# Write a silly function that operates on a single column of a batch\n@singlecolumn\ndef silly_fn(batch, columns):\n    """\n    Capitalize text in the specified column of the batch.\n    """\n    column_name = columns[0]\n    assert type(batch[column_name]) == str, "Must apply to text column."\n    return [text.capitalize() for text in batch[column_name]] \n\n# Wrap the silly function in a CachedOperation\nsilly_op = CachedOperation(apply_fn=silly_fn,\n                           identifier=Identifier(_name=\'SillyOp\'))\n\n# Apply it to a dataset\ndataset = silly_op(batch_or_dataset=dataset, \n                   columns=[\'question\'])\n```\n\n\n#### Retrieve cached information\n```python\nfrom robustnessgym import Spacy, Stanza, CachedOperation\n\n# Take a batch of data\nbatch = dataset[:32]\n\n# Retrieve the (cached) results of the Spacy CachedOperation \nspacy_information = Spacy.retrieve(batch, columns=[\'question\'])\n\n# Retrieve the tokens returned by the Spacy CachedOperation\ntokens = Spacy.retrieve(batch, columns=[\'question\'], proc_fns=Spacy.tokens)\n\n# Retrieve the entities found by the Stanza CachedOperation\nentities = Stanza.retrieve(batch, columns=[\'passage\'], proc_fns=Stanza.entities)\n\n# Retrieve the capitalized output of the silly_op\ncapitalizations = CachedOperation.retrieve(batch,\n                                           columns=[\'question\'],\n                                           identifier=silly_op.identifier)\n\n# Retrieve it directly using the silly_op\ncapitalizations = silly_op.retrieve(batch, columns=[\'question\'])\n\n# Retrieve the capitalized output and lower-case it during retrieval\ncapitalizations = silly_op.retrieve(\n    batch,\n    columns=[\'question\'],\n    proc_fns=lambda decoded_batch: [x.lower() for x in decoded_batch]\n)\n```\n\n#### Create subpopulations\n```python\nfrom robustnessgym import Spacy, ScoreSubpopulation\n\ndef length(batch, columns):\n    """\n    Length using cached Spacy tokenization.\n    """\n    column_name = columns[0]\n    # Take advantage of previously cached Spacy informations\n    tokens = Spacy.retrieve(batch, columns, proc_fns=Spacy.tokens)[column_name]\n    return [len(tokens_) for tokens_ in tokens]\n\n# Create a subpopulation that buckets examples based on length\nlength_subpopulation = ScoreSubpopulation(intervals=[(0, 10), (10, 20)],\n                                          score_fn=length)\n\ndataset, slices, membership = length_subpopulation(dataset, columns=[\'question\'])\n# dataset is updated with slice information\n# slices is a list of 2 Slice objects\n# membership is a matrix of shape (n x 2)\n```\n',
    'author': 'Robustness Gym',
    'author_email': 'kgoel@cs.stanford.edu',
    'maintainer': 'Karan Goel',
    'maintainer_email': 'kgoel@cs.stanford.edu',
    'url': 'https://robustnessgym.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
