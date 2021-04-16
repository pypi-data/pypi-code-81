# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rest_framework_money_field']

package_data = \
{'': ['*']}

install_requires = \
['djangorestframework>3.7.0,<4.0.0', 'py-moneyed>1.0,<2.0']

setup_kwargs = {
    'name': 'rest-framework-money-field',
    'version': '1.1.1',
    'description': 'A DRF serializer for monetary values.',
    'long_description': '# Money field for Django REST framework\n\n[![pipeline status][pipeline-image]][pipeline-url]\n[![coverage report][coverage-image]][coverage-url]\n[![pypi][pypi-image]][pypi-url]\n\nAn serializer field implementation for [Django REST framework] that serializes\nmonetary types provided by [py-moneyed] library. Serialized data is compatible\nwith [Dinero.js] JavaScript library.\n\n## Usage example\n\nFor example, if you would have an serializer like this:\n\n```python\nfrom rest_framework.serializers import Serializer\nfrom rest_framework_money_field import MoneyField\n\n\nclass ProductSerializer(Serializer):\n    price = MoneyField()\n```\n\nAnd you would use the serializer with data like this:\n\n```python\nfrom moneyed import Money\nfrom rest_framework.renderers import JSONRenderer\n\nserializer = ProductSerializer({"price": Money(50, "EUR")})\njson = JSONRenderer().render(serializer.data)\n```\n\nYou would end up with JSON like this:\n\n```json\n{\n    "price": {\n        "amount": 5000,\n        "currency": "EUR"\n    }\n}\n```\n\n[django rest framework]: https://www.django-rest-framework.org/\n[py-moneyed]: https://github.com/py-moneyed/py-moneyed\n[dinero.js]: https://dinerojs.com/\n[pipeline-url]: https://gitlab.com/treet/rest-framework-money-field/commits/master\n[pipeline-image]: https://gitlab.com/treet/rest-framework-money-field/badges/master/pipeline.svg\n[coverage-url]: https://gitlab.com/treet/rest-framework-money-field/commits/master\n[coverage-image]: https://gitlab.com/treet/rest-framework-money-field/badges/master/coverage.svg\n[pypi-url]: https://pypi.org/project/rest-framework-money-field\n[pypi-image]: https://badge.fury.io/py/rest-framework-money-field.svg\n',
    'author': 'Rauli Laine',
    'author_email': 'rauli.laine@treet.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
