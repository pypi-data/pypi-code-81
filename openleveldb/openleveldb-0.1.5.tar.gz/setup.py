# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openleveldb', 'openleveldb.backend']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.1,<2.0.0',
 'numpy>=1.18.1,<2.0.0',
 'plyvel>=1.1.0,<2.0.0',
 'pytest>=5.4.1,<6.0.0',
 'python-dotenv>=0.10.3,<0.11.0',
 'python-rapidjson>=0.9.1,<0.10.0',
 'requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'openleveldb',
    'version': '0.1.5',
    'description': '',
    'long_description': '============================\nA pythonic leveldb wrapper\n============================\n|pypi| |docs| |license| |black|\n\n.. inclusion-marker-do-not-remove\n\n\n`Openleveldb <https://openleveldb.readthedocs.io/en/latest/index.html#>`_ is a small pythonic wrapper around Plyvel_\n\n\nFeatures\n========\n\n\nTransparent object store\n------------------------\n\nIt works with python objects:\n\n- Automatically **encodes objects** into bytes when saving to leveldb\n- Automatically **decodes bytes** into their original type when retrieving objects from leveldb\n\nSupported types include:\n\n- ``int``\n- ``str``\n- ``numpy.ndarray``\n- Anything that is serializable by orjson_\n\n>>> db[\'key\'] = {\'key\': [1, 2, 3]}\n>>> db[\'key\']\n{\'key\': [1, 2, 3]}\n\n\nPython dict-like protocol\n-------------------------\n\nIt offers dict-like interface to LevelDB_\n\n\n>>> db["prefix", "key"] = np.array([1, 2, 3], dtype=np.int8)\n>>> db["prefix", "key"]\narray([1, 2, 3], dtype=int8)\n\n>>> db = db["prefix", ...]\n>>> db["key"]\narray([1, 2, 3], dtype=int8)\n\n\n\nString-only keys\n----------------\n\nThe only possible type for the keys is ``str``.\nIt avoids several problems when working with prefixes.\n\n\n\nMultiprocessing support\n-----------------------\n\nExperimental **multiprocessing** support using a background flask server,\nexposing the same API of a direct connection::\n\n    db = LevelDB(db_path="path_to_db", server_address="http://127.0.0.1:5000")\n\n\n.. _Plyvel: https://github.com/wbolster/plyvel\n.. _LevelDB: http://code.google.com/p/leveldb/\n.. _orjson: https://github.com/ijl/orjson\n\n\n.. |docs| image:: https://readthedocs.org/projects/openleveldb/badge/?version=latest\n    :target: https://openleveldb.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. |license| image:: https://img.shields.io/github/license/lucmos/openleveldb\n    :target: https://github.com/lucmos/openleveldb/blob/master/LICENSE\n    :alt: Openleveldb license\n    \n.. |pypi| image:: https://img.shields.io/pypi/v/openleveldb\n    :target: https://pypi.org/project/openleveldb/\n    :alt: Openleveldb repo\n\n.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Black syntax\n',
    'author': 'Luca Moschella',
    'author_email': 'luca.moschella94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lucmos/openleveldb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.5,<4.0.0',
}


setup(**setup_kwargs)
