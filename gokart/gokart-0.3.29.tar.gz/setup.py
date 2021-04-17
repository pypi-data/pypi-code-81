# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gokart', 'gokart.slack', 'gokart.testing']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler',
 'boto3',
 'google-api-python-client',
 'google-auth',
 'luigi',
 'matplotlib',
 'numpy',
 'pandas<1.2',
 'pyarrow',
 'redis',
 'slack-sdk>=3.0,<4.0',
 'tqdm',
 'uritemplate']

setup_kwargs = {
    'name': 'gokart',
    'version': '0.3.29',
    'description': 'A wrapper of luigi. This make it easy to define tasks.',
    'long_description': '# gokart\n\n[![Test](https://github.com/m3dev/gokart/workflows/Test/badge.svg)](https://github.com/m3dev/gokart/actions?query=workflow%3ATest)\n[![](https://readthedocs.org/projects/gokart/badge/?version=latest)](https://gokart.readthedocs.io/en/latest/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/gokart.svg)](https://pypi.org/project/gokart/)\n[![](https://img.shields.io/pypi/v/gokart)](https://pypi.org/project/gokart/)\n![](https://img.shields.io/pypi/l/gokart)\n\nA wrapper of the data pipeline library "luigi".\n\n\n## Getting Started\nRun `pip install gokart` to install the latest version from PyPI. [Documentation](https://gokart.readthedocs.io/en/latest/) for the latest release is hosted on readthedocs.\n\n## How to Use\nPlease use gokart.TaskOnKart instead of luigi.Task to define your tasks.\n\n\n### Basic Task with gokart.TaskOnKart\n```python\nimport gokart\n\nclass BasicTask(gokart.TaskOnKart):\n    def requires(self):\n        return TaskA()\n\n    def output(self):\n        # please use TaskOnKart.make_target to make Target.\n        return self.make_target(\'basic_task.csv\')\n\n    def run(self):\n        # load data which TaskA output\n        texts = self.load()\n\n        # do something with texts, and make results.\n\n        # save results with the file path {self.workspace_directory}/basic_task_{unique_id}.csv\n        self.dump(results)\n```\n\n### Details of base functions\n#### Make Target with TaskOnKart\n`TaskOnKart.make_target` judge `Target` type by the passed path extension. The following extensions are supported.\n\n - pkl\n - txt\n - csv\n - tsv\n - gz\n - json\n - xml\n\n#### Make Target for models which generate multiple files in saving.\n`TaskOnKart.make_model_target` and `TaskOnKart.dump` are designed to save and load models like gensim.model.Word2vec.\n```python\nclass TrainWord2Vec(TaskOnKart):\n    def output(self):\n        # please use \'zip\'.\n        return self.make_model_target(\n            \'model.zip\',\n            save_function=gensim.model.Word2Vec.save,\n            load_function=gensim.model.Word2Vec.load)\n\n    def run(self):\n        # make word2vec\n        self.dump(word2vec)\n```\n\n#### Load input data\n##### Pattern 1: Load input data individually.\n```python\ndef requires(self):\n    return dict(data=LoadItemData(), model=LoadModel())\n\ndef run(self):\n    # pass a key in the dictionary `self.requires()`\n    data = self.load(\'data\')\n    model = self.load(\'model\')\n```\n\n##### Pattern 2: Load input data at once\n```python\ndef run(self):\n    input_data = self.load()\n    """\n    The above line is equivalent to the following:\n    input_data = dict(data=self.load(\'data\'), model=self.load(\'model\'))\n    """\n```\n\n\n#### Load input data as pd.DataFrame\n```python\ndef requires(self):\n    return LoadDataFrame()\n\ndef run(self):\n    data = self.load_data_frame(required_columns={\'id\', \'name\'})\n```\n\n## Advanced\n### Inherit task parameters with decorator\n#### Description\n```python\nclass MasterConfig(luigi.Config):\n    param: str = luigi.Parameter()\n    param2: str = luigi.Parameter()\n\n@inherits_config_params(MasterConfig)\nclass SomeTask(gokart.TaskOnKart):\n    param: str = luigi.Parameter()\n```\n\nThis is useful when multiple tasks has same parameter, since parameter settings of `MasterConfig`  will be inherited to all tasks decorated with `@inherits_config_params(MasterConfig)`.\n\nNote that parameters which exists in both `MasterConfig` and `SomeTask` will be inherited.\nIn the above example, `param2` will not be available in `SomeTask`, since `SomeTask` does not have `param2` parameter.\n',
    'author': 'M3, inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m3dev/gokart',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
