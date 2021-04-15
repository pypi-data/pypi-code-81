# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['tfworker',
 'tfworker.authenticators',
 'tfworker.backends',
 'tfworker.commands',
 'tfworker.providers',
 'tfworker.util']

package_data = \
{'': ['*']}

install_requires = \
['awscli>=1.18.152,<2.0.0',
 'boto3>=1.15.8,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'google-cloud-storage>=1.37.1,<2.0.0',
 'jinja2>=2.11.2,<3.0.0',
 'requests>=2.25,<3.0',
 'tenacity>=6.2.0,<7.0.0']

entry_points = \
{'console_scripts': ['worker = tfworker.cli:cli']}

setup_kwargs = {
    'name': 'terraform-worker',
    'version': '0.9.0',
    'description': 'An orchestration tool for Terraform',
    'long_description': '# terraform-worker\n\n`terraform-worker` is a command line tool for pipelining terraform operations while sharing state between them. The worker consumese a yaml configuration file which is broken up into two sections, definitions (which were really just top level modules) and sub-modules. The definitions are put into a worker config in order, with the terraform variables, and remote state variables.  Following is a sample configuration file and command:\n\n*./worker.yaml*\n```yaml\nterraform:\n  providers:\n    aws:\n      vars:\n        region: //aws-region//\n        version: "~> 2.61"\n\n  # global level variables\n  terraform_vars:\n    region: //aws-region//\n    environment: dev\n\n  definitions:\n    # Either setup a VPC and resources, or deploy into an existing one\n    network:\n      path: /definitions/aws/network-existing\n\n    database:\n      path: /definitions/aws/rds\n```\n\n```sh\n% worker --aws-profile default --backend s3 terraform --show-output example1\n```\n\n**NOTE:** When adding a provider from a non-hashicorp source, use a `source` field, as follows\n(_the `source` field is only valid for terraform 13+ and is not emitted when using 12_):\n\n```yaml\nproviders:\n...\n  kubectl:\n    vars:\n      version: "~> 1.9"\n    source: "gavinbunney/kubectl"\n```\n\n## Development\n\n```sh\n # virtualenv setup stuff... and then:\n % pip install poetry && make init\n```\n\n## Releasing\n\nPublishing a release to PYPI is done locally through poetry. Instructions on how to configure credentials for poetry can be found [here](https://python-poetry.org/docs/repositories/#configuring-credentials).\n\nBump the version of the worker and commit the change:\n```sh\n % poetry version <semver_version_number>\n```\n\nBuild and publish the package to PYPI:\n```sh\n % poetry publish --build\n```\n\n## Configuration\n\nA project is configured through a worker config, a yaml file that specifies the definitions, inputs, outputs, providers and all other necessary configuration. The worker config is what specifies how state is shared among your definitions. The config support jinja templating that can be used to conditionally pass state or pass in env variables through the command line via the `--config-var` option.\n\n*./worker.yaml*\n```yaml\nterraform:\n  providers:\n    aws:\n      vars:\n        region: {{ aws-region }}\n        version: "~> 2.61"\n\n  # global level variables\n  terraform_vars:\n    region: {{ aws-region }}\n    environment: dev\n\n  definitions:\n    # Either setup a VPC and resources, or deploy into an existing one\n    network:\n      path: /definitions/aws/network-existing\n\n    database:\n      path: /definitions/aws/rds\n      remote_vars:\n        subnet: network.outputs.subnet_id\n```\n\nIn this config, the worker manages two separate terraform modules, a `network` and a `database` definition, and shares an output from the network definition with the database definition. This is made available inside of the `database` definition through the `local.subnet` value.\n\n`aws-region` is substituted at runtime for the value of `--aws-region` passed through the command line.\n\n## Troubleshooting\n\nRunning the worker with the `--no-clean` option will keep around the terraform files that the worker generates. You can use these generated files to directly run terraform commands for that definition. This is useful for when you need to do things like troubleshoot or delete items from the remote state. After running the worker with --no-clean, cd into the definition directory where the terraform-worker generates it\'s tf files. The worker should tell you where it\'s putting these for example:\n\n```\n...\nbuilding deployment mfaitest\nusing temporary Directory: /tmp/tmpew44uopp\n...\n```\n\nIn order to troubleshoot this definition, you would cd /tmp/tmpew44uopp/definitions/my_definition/ and then perform any terraform commands from there.\n\n## Background\n\nThe terraform worker was a weekend project to run terraform against a series of definitions (modules). The idea was the configuration vars, provider configuration, remote state, and variables from remote state would all be dynamically generated. The purpose was for building kubernetes deployments, and allowing all of the configuration information to be stored as either yamnl files in github, or have the worker configuration generated by an API which stored all of the deployment configurations in a database.\n',
    'author': 'Richard Maynard',
    'author_email': 'richard.maynard@objectrocket.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ephur/terraform-worker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
