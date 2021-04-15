# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt', 'dbt.adapters.ibmdb2', 'dbt.include.ibmdb2']

package_data = \
{'': ['*'],
 'dbt.include.ibmdb2': ['macros/*',
                        'macros/materializations/incremental/*',
                        'macros/materializations/seed/*',
                        'macros/materializations/snapshot/*']}

install_requires = \
['dbt-core>=0.19,<0.20', 'ibm-db>=3.0.2,<4.0.0']

setup_kwargs = {
    'name': 'dbt-ibmdb2',
    'version': '0.1.2',
    'description': 'The db2 adapter plugin for dbt (data build tool)',
    'long_description': '[![pypi](https://badge.fury.io/py/dbt-ibmdb2.svg)](https://pypi.org/project/dbt-ibmdb2/)\n[![python](https://img.shields.io/pypi/pyversions/dbt-ibmdb2)](https://pypi.org/project/dbt-ibmdb2/)\n\n# dbt-ibmdb2\n\nThis plugin ports [dbt](https://getdbt.com) functionality to IBM DB2.\n\nThis is an experimental plugin:\n- We have not tested it extensively\n- Only tested with DB2 LUW on Mac OS\n- Only tested with [dbt-adapter-tests](https://github.com/fishtown-analytics/dbt-adapter-tests)\n- Compatiblity with other [dbt packages](https://hub.getdbt.com/) (like [dbt_utils](https://hub.getdbt.com/fishtown-analytics/dbt_utils/latest/)) is also untested\n\nPlease read these docs carefully and use at your own risk. [Issues](https://github.com/aurany/dbt-ibmdb2/issues/new) welcome!\n\n**TODO**\n- [ ] Implement incremental strategy if necessary\n- [ ] Find better way to rename/copy views\n- [ ] Check compatibility with DB2 for z/OS\n\nTable of Contents\n=================\n\n   * [Installation](#installation)\n   * [Supported features](#supported-features)\n   * [Configuring your profile](#configuring-your-profile)\n   * [Notes](#notes)\n   * [Running Tests](#running-tests)\n   * [Reporting bugs](#reporting-bugs)\n\n### Installation\nThis plugin can be installed via pip:\n\n```bash\n$ pip install dbt-ibmdb2\n```\n\n### Supported features\n\n| DB2 LUW | DB2 z/OS | Feature |\n|:---------:|:---:|---------------------|\n| ✅ | 🤷 | Table materialization       |\n| ✅ | 🤷 | View materialization        |\n| ✅ | 🤷 | Incremental materialization |\n| ✅ | 🤷 | Ephemeral materialization   |\n| ✅ | 🤷 | Seeds                       |\n| ✅ | 🤷 | Sources                     |\n| ✅ | 🤷 | Custom data tests           |\n| ✅ | 🤷 | Docs generate               |\n| ✅ | 🤷 | Snapshots                   |\n\nNotes:\n- dbt-ibmdb2 is built on the ibm_db python package and there are some known encoding issues related to z/OS.\n\n### Configuring your profile\n\nA dbt profile can be configured to run against DB2 using the following configuration example:\n\n**Example entry for profiles.yml:**\n\n```\nyour_profile_name:\n  target: dev\n  outputs:\n    dev:\n      type: ibmdb2\n      schema: analytics\n      database: test\n      host: localhost\n      port: 50000\n      protocol: TCPIP\n      username: my_username\n      password: my_password\n```\n\n| Option          | Description                                                                         | Required?                                                          | Example                                        |\n| --------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------- |\n| type            | The specific adapter to use                                                         | Required                                                           | `ibmdb2`                                       |\n| schema          | Specify the schema (database) to build models into                                  | Required                                                           | `analytics`                                    |\n| database        | Specify the database you want to connect to                                         | Required                                                           | `testdb`                                         |\n| host            | Hostname or IP-adress                                                               | Required                                                           | `localhost`                                    |\n| port            | The port to use                                                                     | Optional                                                           | `50000`                                        |\n| protocol        | Protocol to use                                                                     | Optional                                                           | `TCPIP`                                        |\n| username        | The username to use to connect to the server                                        | Required                                                           | `my-username`                                  |\n| password        | The password to use for authenticating to the server                                | Required                                                           | `my-password`                                  |\n\n### Running Tests\n\nSee [test/README.md](test/README.md) for details on running the integration tests.\n\n### Reporting bugs\n\nWant to report a bug or request a feature? Open [an issue](https://github.com/aurany/dbt-ibmdb2/issues/new).\n\n### Credits\n\ndbt-ibmdb2 is heavily inspired by and borrows from [dbt-mysql](https://github.com/dbeatty10/dbt-mysql) and [dbt-oracle](https://github.com/techindicium/dbt-oracle).\n',
    'author': 'aurany',
    'author_email': 'rasmus.nyberg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aurany/dbt-ibmdb2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
