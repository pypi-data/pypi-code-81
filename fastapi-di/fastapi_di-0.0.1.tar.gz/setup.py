# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_di']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0', 'pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'fastapi-di',
    'version': '0.0.1',
    'description': 'Extracted the dependency injection process from fastapi.',
    'long_description': '# fastapi_di\nExtracted the dependency injection process from fastapi.\nDependency injection by fastapi_di is only available in the async environment.\n\n# Requirement\n\n- Python 3.8+\n\n# Installation\n``` shell\npoetry install fastapi_di\n```\n\n# Getting started\nDependency injection is done by decorating the function and calling do as follows.\n\n\n``` Python\nimport asyncio\nfrom fastapi import Depends\nfrom fastapi_di import DI\n\ndi = DI()\n\n\ndef get_db():\n    yield {1: {"id": 1, "name": "bob", "memo": ""}}\n\n\n@di.task()\nasync def update_user(db=Depends(get_db), *, user_id: int, memo: str):\n    record = db[user_id]\n    record["memo"] = memo\n    return record\n\n\nasync def main():\n    return await update_user.do(user_id=1, memo="test")\n\n\nresult = asyncio.run(main())\nprint(result)\n# => {\'id\': 1, \'name\': \'bob\', \'memo\': \'test\'}}\n```\n\n# warning\nThis library is in the experimental stage.\n\n',
    'author': 'sasano8',
    'author_email': 'y-sasahara@ys-method.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sasano8/fastapi_di',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
