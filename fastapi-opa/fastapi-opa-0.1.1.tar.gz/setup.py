# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_opa', 'fastapi_opa.auth', 'fastapi_opa.opa']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT[crypto]>=2.0.1,<3.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'requests>=2.25.1,<3.0.0',
 'uvicorn>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'fastapi-opa',
    'version': '0.1.1',
    'description': 'Fastapi OPA middleware incl. auth flow.',
    'long_description': '# Open Policy Agent Middleware for FastAPI\n\n`fastapi-opa` is an extension to FastAPI that allows you to add a login flow\nto your application within minutes using open policy agent and your favourite\nidentity provider.\n\n```bash\n─▄████▄▄░\n▄▀█▀▐└─┐░░         FastAPI App\n█▄▐▌▄█▄┘██  ---->  @app.get("/")\n└▄▄▄▄▄┘███         async def root():  \n██▒█▒███▀              return {}\n   User                   |                   Identity Provider\n    |       ------------------------------>    (e.g. Keycloak)\n    |       <------------------------------           |\n    |       ---->         |                           |\n    |                     |           ---->           |\n    |                     |           <----           |\n    |                     |           ---------------------------------->  Open Policy Agent\n    |                     |           <---------------------------------- \n    |       <-----        |\n```\n\nWhen a user tries to get a response from an endpoint he/she will be redirected\nto the identity provider for authorization.\nAfter the authentication the app validates the token provided. Once it was\nvalidated the user information is used to get an OPA decision whether\nthe user is allowed to get any information from the endpoint.\n\n## Installation\n\n```bash\npoetry add fastapi-opa\n```\n\n## How to get started\n\nThe package provides a very easy way to integrate authentication and\nauthorization. We can decide what authentication flow we inject into the\nOPAMiddleware to be able choosing between different flows.\n\n```python\nfrom typing import Dict\n\nfrom fastapi import FastAPI\n\nfrom fastapi_opa import OPAConfig\nfrom fastapi_opa import OPAMiddleware\nfrom fastapi_opa.auth import OIDCAuthentication\nfrom fastapi_opa.auth import OIDCConfig\n\n# The hostname of your Open Policy Agent instance\nopa_host = "http://localhost:8181"\n# In this example we use OIDC authentication flow (using Keycloak)\noidc_config = OIDCConfig(\n    host="http://localhost:8080",  # host of your identity provider\n    realm="example-realm",  # realm id of your identity provider\n    app_uri="http://localhost:4000",  # host where this app is running\n    client_id="example-client",  # client id of your app configured in the identity provider\n    client_secret="bbb4857c-21ba-44a3-8843-1364984a36906",  # the client secret retrieved from your identity provider\n)\noidc_auth = OIDCAuthentication(oidc_config)\nopa_config = OPAConfig(authentication=oidc_auth, opa_host=opa_host)\n\napp = FastAPI()\n# Add OPAMiddleware to the fastapi app\napp.add_middleware(OPAMiddleware, config=opa_config)\n\n\n@app.get("/")\nasync def root() -> Dict:\n    return {\n        "msg": "success",\n    }\n```\n\n## Open Policy Agent\n\nThe (validated/authenticated) user token is sent to the Open Policy Agent\nwith the additional attributes `request_method` and `request_path`.\n\n```json\n{\n    "input": {\n        "exp": 1617466243,\n        "iat": 1617465943,\n        "auth_time": 1617465663,\n        "jti": "9aacb638-70c6-4f0a-b0c8-dbc67f92e3d1",\n        "iss": "http://localhost:8080/auth/realms/example-realm",\n        "aud": "example-client",\n        "sub": "ccf78dc0-e1d6-4606-99d4-9009e74e3ab4",\n        "typ": "ID",\n        "azp": "david",\n        "session_state": "41640fe7-39d2-44bc-818c-a3360b36fb87",\n        "at_hash": "2IGw-B9f5910Sll1tnfQRg",\n        "acr": "0",\n        "email_verified": false,\n        "hr": "true",\n        "preferred_username": "david",\n        "user": "david",\n        "subordinates": [],\n        "request_method": "GET",\n        "request_path": ["finance", "salary", "david"]\n    }\n}\n```\n\nIn open policy agent you can now easily create policies using user roles,\nroutes, or request methods etc.\n\nAn example policy (from [the official OPA docs](https://www.openpolicyagent.org/docs/v0.11.0/http-api-authorization/))\nfor this setup could be like:\n\n```rego\npackage httpapi.authz\n\n# bob is alice\'s manager, and betty is charlie\'s.\nsubordinates = {"alice": [], "charlie": [], "bob": ["alice"], "betty": ["charlie"]}\n\n# HTTP API request\nimport input\n\ndefault allow = false\n\n# Allow users to get their own salaries.\nallow {\n  some username\n  input.request_method == "GET"\n  input.request_path = ["finance", "salary", username]\n  input.user == username\n}\n\n# Allow managers to get their subordinates\' salaries.\nallow {\n  some username\n  input.request_method == "GET"\n  input.request_path = ["finance", "salary", username]\n  subordinates[input.user][_] == username\n}\n```\n\n## Authentication Flow\n\nThese flows are implemented:\n\n- OpenID Connect\n\nIf your favourite flow is not provided yet, there is an interface provided to\neasily implement it and inject it into OPAMiddleware\n(`fastapi_opa.auth.auth_interface.AuthInterface`), or you can open a pull\nrequest if you would like to contribute to the package.\n\n## Roadmap\n\n- Document quick-start environment to empower users\n- Add other authentication flows\n- Allow more flexible way of opa jwt enrichment\n',
    'author': 'Matthias Osswald',
    'author_email': 'm@osswald.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/busykoala/fastapi-opa',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
