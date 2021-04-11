# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pillaralgos_dev']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.49,<2.0.0',
 'matplotlib>=3.4.1,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'seaborn>=0.11.1,<0.12.0']

setup_kwargs = {
    'name': 'pillaralgos-dev',
    'version': '0.1.0',
    'description': 'Library containing some basic, commonly used functions during the creation and analysis of algorithms for Pillar',
    'long_description': '# Dev Tools\n\nCommon functions to help in developing `pillaralgos` library. Includes \n* `dev_helpers.awsBucketAPI` to connect to aws (assuming AWS Cli is installed locally), download files.\n* `dev_helpers.plot_with_time` to create a time series plot with conveniently formatted xaxis\n* `sanity_checks` future site of error catchers\n\n# How To\nConnect to AWS bucket, download random files.\n```\nfrom pillaralgos_dev import dev_helpers as dev\naws = dev.awsBucketAPI()\nnames = aws.get_random_file_names(n=5)\naws.save_files(names)\n```\nCheck sanity:\n```\nfrom pillaralgos_dev import sanity_checks as sane\n```',
    'author': 'Peter Gates',
    'author_email': 'pgate89@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
