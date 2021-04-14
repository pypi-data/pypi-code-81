# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newrelic_logger']

package_data = \
{'': ['*']}

install_requires = \
['newrelic>=6.2.0,<7.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'new-relic-logger-for-python',
    'version': '0.1.6',
    'description': 'Push logs into New Relic using standard python logger asynchronously.',
    'long_description': '## New Relic APM Logger\nThis library enables the standard python logger to send its logs to New Relic using an async strategy.\nNote: These logs are linked to the application only in the context of a web transaction. \n\n## Configuration\nConfigure the APM agent according to the [documentation](https://docs.newrelic.com/docs/agents/python-agent/installation/standard-python-agent-install/). A `newrelic.ini` should be generated.\n\nTo enable the python logging module, include this line in your file. \n```python\nimport newrelic_logger\n```\n### Arguments\nNewRelicLogger constructor receives the following optional arguments:\n\n|Name|Type|Description|\n|---|---|---|\n|app_id|int|The app id for the newrelic APM\n|app_name|str|The app name for the newrelic APM\n|license_key|str|The license_key for comunicating with the new relic api\n|region|str|The region for newrelic, either "US" or "EU"\n|log_level|ENUM|The numeric level of the logging event (one of DEBUG, INFO etc.)\n\n### Environment Variables\nOptionaly, some arguments can be configured by environment variables. These are:\n\n|Name|Description|\n|---|---|\n|NEW_RELIC_APP_ID|The app id for the newrelic APM\n|NEW_RELIC_APP_NAME|he app name for the newrelic APM\n|NEW_RELIC_LICENSE_KEY|The license_key for comunicating with the new relic api\n|NEW_RELIC_REGION|The region for newrelic, either "US" or "EU"\n\n## Usage\nJust use the normal python logger, for example, to send an info message:\n```python\nimport logging\nlogging.info("This is an info message")\n```\n\n## Running the program\nRun the application using the new relic agent either by using the admin script integration, or the manual integration, as mentioned in the [documentation](https://docs.newrelic.com/docs/agents/python-agent/installation/python-agent-advanced-integration/). For example, for the admin script:\n```bash\nNEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program YOUR_COMMAND_OPTIONS\n```\nand for the manual integration:\n```python\nimport newrelic.agent\nnewrelic.agent.initialize(\'/some/path/newrelic.ini\')\n```',
    'author': 'Andrés Peñaloza',
    'author_email': 'andres.penaloza@xintec.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
