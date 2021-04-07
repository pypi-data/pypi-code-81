# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_slackeventsapi']

package_data = \
{'': ['*']}

install_requires = \
['aiojobs>=0.3.0,<0.4.0',
 'async-timeout>=3.0.1,<4.0.0',
 'fastapi>=0.63.0,<0.64.0']

setup_kwargs = {
    'name': 'fastapi-slackeventsapi',
    'version': '0.1.0',
    'description': 'FastAPI Implementation of slackeventsapi',
    'long_description': "# Slack Events API adapter for Python with FastAPI  \n\nSlackEventManager is a Python-based solution to recieve and parse events from Slack's Events API\n\nThis is simple add to fastapi server SLack Events API  \n\n## Installation\n```bash\npip install fastapi-slackeventsapi\n```\n\n## Work Setup \n* [App Setup](https://github.com/slackapi/python-slack-events-api/blob/main/README.rst#--app-setup)\n* [Development Workflow](https://github.com/slackapi/python-slack-events-api/blob/main/README.rst#--development-workflow)  \n\n## Usage  \n\nCreate simple FastAPI app and add SlackEventManager event handler\n\n```python\nimport os\n\nimport uvicorn\nfrom fastapi import FastAPI\nfrom fastapi_slackeventsapi import SlackEventManager\n\nsigning_secret = os.environ.get('SLACK_BOT_SIGNING_SECRET')\n\napp = FastAPI()\n\nslack_event_manger = SlackEventManager(singing_secret=signing_secret,\n                                       endpoint='/slack/events/',\n                                       app=app)\n\n\n@slack_event_manger.on('reaction_added')\nasync def reaction_added(event_data):\n    emoji = event_data['event']['reaction']\n    print(emoji)\n\n\nuvicorn.run(app, host='0.0.0.0')\n\n```\n\n",
    'author': 'Phygitalism',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/und3v3l0p3d/fastapi_slackeventsapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
