# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_serverless_oauth_session']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=0.15.3,<0.16.0', 'pynamodb>=5.0.3,<6.0.0']

setup_kwargs = {
    'name': 'django-serverless-oauth-session',
    'version': '0.2.2',
    'description': "Provides a Django app for storing tokens in AWS's DynamoDB, and providing a convenient requests session which uses the token. This is a use-case-specific library, and is intended for backend integrations that must authenticate with an API which only supports OAuth2 for its authentication protocol.",
    'long_description': '# Don\'t Use\n\nThis is in super-duper early development. Stay away!\n\n# Introduction\n\nThis is a use-case specific library, enabling you to quickly get up and running with a backend integration where OAuth2 is necessary.\n\nThis package assumes you\'re not using Django\'s ORM (a SQL database) and that you are using AWS. If so, the point is to spin up\na DynamoDB table with which your application can store an OAuth token from an authenticating user. This table will only have\none active token at a time, which is the token of the most recent user to authenticate. Past tokens are kept around for up to\none month.\n\nThis package is certainly not intended for a user-facing web-application.\n\n# Usage\n\nTaking a looking at the example project will probably tell you everything you need to know, but here are the explicit details.\n\n## settings.py\n\nIn your `settings.py`, add `django_serverless_oauth_session` to your `INSTALLED_APPS`\n\n```python\n# settings.py\n\nINSTALLED_APPS = [\n    # ...\n    "django_serverless_oauth_session",\n]\n```\n\n---\n\n**NOTE**\n\nBy registering this app, the DynamoDB table will be created in AWS on the start-up of the app if it doesn\'t already exist.\nTo turn this off, set `OAUTH_TOKEN_TABLE_CREATE = False` in `settings.py`. This might be useful if you need to add KMS keys\nto your table, or you\'d rather provision in some other way.\n\nAlso, your environment must have your AWS credentials ready to go, just like you would have them set-up for boto3.\n\n---\n\nSet a `LOGIN_REDIRECT_URL`\n\n```python\n# settings.py\n\nLOGIN_REDIRECT_URL = "/"\n```\n\nAnd finally, fill in your OAuth provider\'s details, as well as some info for AWS\n\n```python\n# settings.py\n\n# AWS stuff\nOAUTH_TOKEN_TABLE_NAME = "some-table-name"\nAWS_REGION = "us-west-2"\n\n# OAuth app stuff\nOAUTH_CLIENT_ID = os.getenv(\'GITHUB_CLIENT_ID\')\nOAUTH_CLIENT_SECRET = os.getenv(\'GITHUB_CLIENT_SECRET\')\nOAUTH_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"\nOAUTH_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"\nOAUTH_USER_INFO_URL = "https://api.github.com/user"\nOAUTH_SCOPE = "user:email"\n```\n\n## urls\n\nRegister the following urls in your root url conf\n\n```python\n# urls.py\n\npath(\n    "oauth/",\n    include("django_serverless_oauth_session.urls"),\n),\n```\n\nSupport for custom URL callbacks will be worked on in a future version.\n\n## Getting the token\n\nSomewhere in your site, you\'ll need a view with a button with which users can click to get started. Put\nthis in your template to kick off the OAuth process.\n\n```html\n<a href="{% url \'sls-login\' %}" class="btn btn-primary">Click to OAuth</a>\n```\n\n## Using it!\n\nAfter all that set-up, you probably want to use it. The above enables to you grab an authenticated `requests` session\nthat handles authenticated and token refreshing for you.\n\n```python\nfrom django_serverless_oauth_session import get_oauth_session\n\ndef repos(request):\n    session = get_oauth_session()\n    response = session.get("https://api.github.com/user/repos")\n    repos = response.json()\n    return render(request, "repos.html", {"repos": repos})\n```\n\nThis allows you to simply import this function and start making calls to your API in backend scripts and the like.\n\nPlease refer to the documentation for [requests](https://docs.python-requests.org/en/master/) for more info on how to use\nthe session.\n',
    'author': 'Alex Drozd',
    'author_email': 'drozdster@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brno32/django-serverless-oauth-session',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
