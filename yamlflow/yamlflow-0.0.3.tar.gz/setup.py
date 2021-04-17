# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yamlflow', 'yamlflow.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0,<8.0.0', 'docker>=5.0.0,<6.0.0', 'pyyaml>=5.4.1,<6.0.0']

entry_points = \
{'console_scripts': ['yamlflow = yamlflow.cli:main']}

setup_kwargs = {
    'name': 'yamlflow',
    'version': '0.0.3',
    'description': 'Yet Another ML flow',
    'long_description': '# yamlflow\nYet Another ML flow\n\n## STATUS NOT READY\n\n```\nexamle-project\n    ...\n    ...\n    .yamlflow\n        flow.yaml\n        predictor.py\n        requirements.txt\n```\n\n### User guide\n```bash\npip install yamlflow\nyamlflow apply -f flow.yaml\n```\n\n### Developer guide\n```\npoetry env use <path/to/python3.8.6/executable>\npoetry shell\npoetry install\n```',
    'author': 'Sevak Harutyunyan',
    'author_email': 'sevak.g.harutyunyan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sevakharutyunyan/aida',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
