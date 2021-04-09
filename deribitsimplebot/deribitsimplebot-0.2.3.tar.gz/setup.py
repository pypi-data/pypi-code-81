# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deribitsimplebot']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'anyio>=2.1.0,<3.0.0',
 'json5>=0.9.5,<0.10.0',
 'mysql-connector-python>=8.0.23,<9.0.0',
 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'deribitsimplebot',
    'version': '0.2.3',
    'description': 'Class set for the implementation of a simple bot working with the Deribit crypto exchange',
    'long_description': '.. _header-n246:\n\nDeribitSimpleBot\n================\n\n| Реализация простого бота для криптобиржи Deribit.\\\\\n| Реализация для websockets JSON-RPC v.2\n  (`Документация <https://docs.deribit.com/>`__)\n\n.. _header-n249:\n\nВозможности\n-----------\n\n1. Возможность работы с несколькими инструментами одновременно\n\n2. Возобновление работы после остановки\n\n3. Возможность использвоать разные системы хранения ордеров\n\n.. _header-n257:\n\nАлгоримт работы\n---------------\n\n1. Робот выставляет ордер #1 на покупку по цене **buy price = current\n   price - gap / 2**.\n\n2. | **(a)** Если цена уменьшается до **buy price**, то ордер #1, скорее\n     всего, будет исполнен. В этом случае перейти к пункту 3.\\\\\n   | **(b)** Если цена увеличивается до такого значения, что становится\n     истинным условие **current price > buy price + gap + gap ignore**,\n     то робот должен отменить ордер #1. Далее, вернуться к пункту 1.\n\n3. Робот выставляет ордер #2 на продажу по цене **sell price = current\n   price + gap**.\n\n4. | **(a)** Если цена увеличивается до sell price, то ордер #2, скорее\n     всего, будет исполнен. В этом случае вернуться к пункту 1.\\\\\n   | **(b)** Если цена уменьшается до такого значения, что становится\n     истинным условие **current price < sell price - gap - gap ignore**,\n     то робот должен отменить ордер #2. После этого следует вернуться к\n     пункту 3.\n\n.. _header-n267:\n\nРабочий пример\n--------------\n\n`Пример\nприложение <https://github.com/n-eliseev/deribitsimplebot/tree/master/example-app>`__\n(`описание к нему <https://github.com/n-eliseev/deribitsimplebot/>`__)\n',
    'author': 'Eliseev Nikolay',
    'author_email': 'n.a.eliseev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/n-eliseev/deribitsimplebot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
