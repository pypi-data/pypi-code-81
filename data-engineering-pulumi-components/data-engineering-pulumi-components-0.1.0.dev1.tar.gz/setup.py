# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_engineering_pulumi_components',
 'data_engineering_pulumi_components.aws',
 'data_engineering_pulumi_components.aws.lambdas.move',
 'data_engineering_pulumi_components.pipelines']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.50,<2.0.0', 'pulumi-aws>=3.29.0,<4.0.0', 'pulumi>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'data-engineering-pulumi-components',
    'version': '0.1.0.dev1',
    'description': 'Reusable components for use in Pulumi Python projects',
    'long_description': None,
    'author': 'MoJ Data Engineering Team',
    'author_email': 'data-engineering@digital.justice.gov.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
