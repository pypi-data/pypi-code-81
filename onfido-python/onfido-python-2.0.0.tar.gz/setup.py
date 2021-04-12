# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onfido', 'onfido.resources']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'onfido-python',
    'version': '2.0.0',
    'description': 'The official wrapper for the Onfido API',
    'long_description': '# Onfido Python Client Library\n\n[onfido-python on PyPI](https://pypi.org/project/onfido-python/)\n\nVersion 2.0.0\n\nThe official wrapper for Onfido\'s API. Refer to the full [API documentation](https://documentation.onfido.com) for details of expected requests and responses for all resources.\n\nThis version uses Onfido API v3.1. Refer to our [API versioning guide](https://developers.onfido.com/guide/api-versioning-policy#client-libraries) for details of which client library versions use which versions of the API. \n\nThis project supersedes the automatically generated [api-python-client](https://github.com/onfido/api-python-client) library (`onfido` in PyPI).\n\n## Installation\n\n`pip install onfido-python`\n\n:warning: Having the old `onfido` package installed at the same time will cause errors.\n\n## Getting started\n\nMake API calls by using an instance of the `Api` class and providing your API\ntoken:\n\n```python\nimport onfido\n\napi = onfido.Api("<YOUR_API_TOKEN>")\n```\n\n### Regions\n\nSet the region in the API instance using the `region` parameter, which takes a value from the `Region` enum (currently `Region.EU`, `Region.US` or `Region.CA`).\n\nFor example, to specify the EU region:\n\n```python\nimport onfido\nfrom onfido.regions import Region\n\napi = onfido.Api("<YOUR_API_TOKEN>", region=Region.EU)\n```\n\n`region` does not take a default parameter. Failure to pass a correct region will raise an `OnfidoRegionError`.\n\nSee https://documentation.onfido.com/#regions for more information about our supported regions at a given time.\n\n### Timeouts\n\nYou can optionally set a global timeout for all requests in the API\nconstructor. This takes a floating number input and each whole integer\nincrement corresponds to a second. \n\nFor example, to set a timeout of 1 second:\n\n```python\napi = onfido.Api("<YOUR_API_TOKEN>", timeout=1)\n```\n\nThe default value for `timeout` is `None`, meaning no timeout will be set on\nthe client side.\n\n## Response format\n\nThe Python library will return JSON requests directly from the API. Each request corresponds to a resource. \n\nAll resources share the same interface when making API calls. For example, use `.create` to create a resource, `.find` to find one, and `.all` to fetch all resources. \n\nFor example, to create an applicant:\n\n```python\napplicant_details = {\n  "first_name": "Jane",\n  "last_name": "Doe",\n  "dob": "1984-01-01",\n  "address": {\n    "street": "Second Street",\n    "town": "London",\n    "postcode": "S2 2DF",\n    "country": "GBR"\n  }\n}\n\napi.applicant.create(applicant_details)\n```\n\n```python\n{\n  "id": "<APPLICANT_ID>",\n  "created_at": "2019-10-09T16:52:42Z",\n  "sandbox": true,\n  "first_name": "Jane",\n  "last_name": "Doe",\n  "email": null,\n  "dob": "1990-01-01",\n  "delete_at": null,\n  "href": "/v3.1/applicants/<APPLICANT_ID>",\n  "id_numbers": [],\n  "address": {\n    "flat_number": null,\n    "building_number": null,\n    "building_name": null,\n    "street": "Second Street",\n    "sub_street": null,\n    "town": "London",\n    "state": null,\n    "postcode": "S2 2DF",\n    "country": "GBR",\n    "line1": null,\n    "line2": null,\n    "line3": null\n  }\n}\n```\n\nSee https://documentation.onfido.com/#request,-response-format for more\ninformation.\n\n### Resources\n\nResource information and code examples can be found at https://documentation.onfido.com/.\n\n### Error Handling\n\n- `OnfidoServerError` is raised whenever Onfido returns a `5xx` response\n- `OnfidoRequestError` is raised whenever Onfido returns a `4xx` response\n- `OnfidoInvalidSignatureError` is raised whenever a signature from the header is not equal to the expected signature you compute for it\n- `OnfidoTimeoutError` is raised if a timeout occurs\n- `OnfidoConnectionError` is raised whenever any other network error occurs\n- `OnfidoUnknownError` is raised whenever something unexpected happens\n\n## Contributing\n\n1. Fork it ( https://github.com/onfido/onfido-python/fork )\n2. Create your feature branch (`git checkout -b my-new-feature`)\n3. Run the tests (`poetry run pytest tests/test_my_new_feature.py`)\n4. Commit your changes (`git commit -am \'Add some feature\'`)\n5. Push to the branch (`git push origin my-new-feature`)\n6. Create a new Pull Request\n',
    'author': 'Ben Ahmady',
    'author_email': 'ben.ahmady@onfido.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/onfido/onfido-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
