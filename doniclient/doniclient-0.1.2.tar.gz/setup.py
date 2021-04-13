# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doniclient', 'doniclient.osc', 'doniclient.tests', 'doniclient.v1']

package_data = \
{'': ['*']}

install_requires = \
['osc-lib>=1.14.1,<2.0.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'python-openstackclient[cli]>=4.0.2,<5.0.0']

entry_points = \
{'openstack.cli.extension': ['inventory = doniclient.osc.plugin'],
 'openstack.inventory.v1': ['hardware_create = '
                            'doniclient.osc.cli:CreateHardware',
                            'hardware_delete = '
                            'doniclient.osc.cli:DeleteHardware',
                            'hardware_export = '
                            'doniclient.osc.cli:ExportHardware',
                            'hardware_list = doniclient.osc.cli:ListHardware',
                            'hardware_set = doniclient.osc.cli:UpdateHardware',
                            'hardware_show = doniclient.osc.cli:GetHardware',
                            'hardware_sync = doniclient.osc.cli:SyncHardware']}

setup_kwargs = {
    'name': 'doniclient',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Michael Sherman',
    'author_email': 'shermanm@uchicago.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
