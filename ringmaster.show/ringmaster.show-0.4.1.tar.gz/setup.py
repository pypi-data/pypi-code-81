# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ringmaster']

package_data = \
{'': ['*'], 'ringmaster': ['res/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'boto3>=1.17.24,<2.0.0',
 'cfn-flip>=1.2.3,<2.0.0',
 'docopt>=0.6.2,<0.7.0',
 'halo>=0.0.31,<0.0.32',
 'loguru>=0.5.3,<0.6.0',
 'python-cloudflare>=1.0.1,<2.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'snakecase>=1.0.1,<2.0.0',
 'snowflake-connector-python>=2.4.1,<3.0.0']

entry_points = \
{'console_scripts': ['ringmaster = ringmaster.cli:main']}

setup_kwargs = {
    'name': 'ringmaster.show',
    'version': '0.4.1',
    'description': 'The world is a circus and you are the ringmaster!',
    'long_description': "# Ringmaster\n```\n         _\n       _[_]_\n       _(_)______.-'`-.\n      /, >< ,----'     `-._.-'*\n      \\\\|::|  Welcome to the Circus\n        |/\\|  We already got enough Clowns,\n        ||||  You got any experiance with\n        ||||  Being shot from a canon??\n     __(_/\\_)\n    /`-..__.,-'\\\n   /   __/\\__   \\\n   `._ \\    / _.'MJP\n      ``|/\\|-'\n```\n\nRingmaster organises a bunch of other tools on your behalf so that you don't\nhave to. The aim is you can create, updated and delete entire stacks crossing\ncloudformation, EKS, kubectl, helm and random Python/BASH scripts with a single\ncommand.\n\nRingmaster helps you create and share your automation scripts with others, so\nyou can get up and running as quick as possible. There are no agents, hubs, \ngits or daemons - unless you add them yourself. \n\nThere is also no custom DSL or new programming language to learn, although\n[jinja2](https://jinja.palletsprojects.com/) is used for templating.\n\nRingmaster is just files on a disk and calls to other systems made in an order\nyou decide.\n\n## How does it work?\n\nYou create a directory of scripts to process, like this:\n\n```\nstack/\n├── 0010-iam\n│     ├── AWSLoadBalancerController.iam_policy.json\n│     ├── Certbot.iam_policy.json\n│     ├── EksDeploy.iam_policy.json\n│     ├── EksExternalSecrets.iam_policy.json\n│     ├── ExternalDns.iam_policy.json\n│     └── metadata.yaml\n├── 0020-efs\n│     ├── efs.cloudformation.yaml\n│     └── metadata.yaml\n├── 0030-vpc\n│     ├── metadata.yaml\n│     ├── vpc.remote_cloudformation.yaml\n│     └── vpc.yaml\n...\n```\n\nThen you run `ringmaster` like this:\n\n`ringmaster stack up`\n\nRingmaster will carry out the _create_ action of each script, running each \nscript in alphabetical order by _directory_ and then _file_\n\n`ringmaster stack down`\n\nRingmaster will carry out the delete action of each script, in _reverse_\nalphabetical order\n\n**The `up` and `down` actions are \n[idempotent](https://en.wikipedia.org/wiki/Idempotence#Computer_science_examples)\nso you can run them as many times as you like**\n\n\n## What's in the scripts? do I have to learn a new language?\n\nNo! The scripts use the languages and tools you already know and love, eg:\n\n* Cloudformation\n* Bash\n* Python\n* Kubernetes deployment descriptors\n* ...etc\n\nRingmaster uses a [databag](doc/concepts.md#databag) to give each script the\nright inputs and collects outputs that may be required later. Combined with a\nsimple built-in variable substitution system, this makes gluing completely \ndifferent systems together easy, eg:\n\n```\ncloudformation -> ekscl -> more cloudformation -> heml -> kubectl -> ...\n```\n\nTo reduce dependency on ringmaster and allow easy debugging and repeatable\ndeployments, substitution results are stored adjacent to their input files, so\nthey can be added to git or use directly by tools such as `kubectl`.\n\n## Reference\n\n1. [Concepts](doc/concepts.md)\n2. [Setup](doc/setup.md)\n3. [Authentication](doc/authentication.md)\n4. [Handlers](doc/handlers.md)\n5. [Scripts](doc/scripts.md)\n6. [Variables](doc/variables.md)   \n7. [Worked Example](doc/worked_example.md)\n",
    'author': 'Geoff Williams',
    'author_email': 'geoff@declarativesystems.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://ringmaster.show',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
