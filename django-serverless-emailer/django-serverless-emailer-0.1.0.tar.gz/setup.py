# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_serverless_emailer']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2,<4.0']

setup_kwargs = {
    'name': 'django-serverless-emailer',
    'version': '0.1.0',
    'description': 'Provides a Django app and a lambda handler for sending emails concerning errors in AWS',
    'long_description': 'Currently only supports failed step functions. This is half-baked so far\n\n# Usage\n\n```python\n# settings.py\n\nINSTALLED_APPS = [\n    "django_serverless_emailer",\n    # ...\n]\n\nAWS_REGION = "us-west-2"  # your region\n\nDEFAULT_FROM_EMAIL = "an-email@email.com"  # your sender\nEMAIL_HOST = "smtp.gmail.com"  # your host\nEMAIL_PORT = 465  # your port\nEMAIL_HOST_USER = "an-email@email.com"  # your user\nEMAIL_HOST_PASSWORD = os.getenv["EMAIL_PASSWORD"]\nEMAIL_USE_SSL = True  # if you\'re using SSL\n\nEMAIL_RECEPIENTS = "a@b.com,c@d.com"  # comma delimited list or a plain list\n```\n\n```yml\n# serverless.yml\n\nfunctions:\n  notify:\n    handler: django_serverless_emailer/handler.notify\n    description: Send an email when there\'s something in the queue\n    layers:\n      - { Ref: PythonRequirementsLambdaLayer }\n    timeout: 10\n    environment:\n      DJANGO_SETTINGS_MODULE: setup.settings # path to your settings module\n    events:\n      - sqs:\n          arn:\n            Fn::GetAtt:\n              - ErrorNotificationDlq\n              - Arn\n```\n',
    'author': 'Alex Drozd',
    'author_email': 'drozdster@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kicksaw-Consulting/django-serverless-emailer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
