# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cool']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cool',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Cool.py\n\nMake Python code cooler. 100% coverage. Use and enjoy this code!\n\n## Install\n\n```\npip install cool\n```\n\nOr fetch from github\n\n```\npip install git+https://github.com/abersheeran/cool@setup.py\n```\n\n## Usage\n\n### Pipe\n\nUse pipeline to pass data as a positional parameter to the next function:\n\n```python\nfrom cool import F\n\nrange(10) | F(filter, lambda x: x % 2) | F(sum) == 25\n```\n\nOr you need to pass multiple parameters through the pipeline:\n\n```python\nfrom cool import FF\n\n\ndef get_data():\n    return 1, 2\n\n\nget_data() | FF(lambda x, y: x + y) == 3\n```\n\nUse alias like follow code, you can use `map`/`filter`/`reduce` more conveniently:\n\n```python\nfrom functools import reduce\nfrom cool import F\n\nFilter = F(F, filter)\nMap = F(F, map)\nReduce = F(F, reduce)\n\nrange(100) | Filter(lambda x: x % 2) | Map(lambda x: x * x) | Reduce(lambda x, y: x + y)\n```\n\n### Redirect\n\nJust like the redirection symbol in `Shell`, you can redirect the output to a specified file or `TextIO` object through `>` or `>>`.\n\n*Note: `R` inherits from `functools.partial`.*\n\n```python\nfrom pathlib import PurePath\nfrom cool import R\n\n# Redirect output to specified filepath\nR(print, "hello") > PurePath("your-filepath")\n\n# Append mode\nR(print, "world") >> PurePath("your-filepath")\n```\n\nRedirect to opened file or other streams.\n\n```python\nfrom io import StringIO\nfrom cool import R\n\nwith open("filepath", "a+", encoding="utf8") as file:\n    R(print, "hello") >> file\n\nout = StringIO("")\n\nR(print, "hello") > out\n\nout.seek(0, 0)\nout.read() == "hello\\n"\n```\n\nMaybe you also want to block the output, just like `> /dev/null`.\n\n```python\nfrom cool import R\n\nR(print, "hello") > None\n# Or\nR(print, "hello") >> None\n```\n\nNote that after the calculation is over, `R` will faithfully return the return value of your function. Try the following example.\n\n```python\nfrom pathlib import PurePath\nfrom cool import F, R\n\n\ndef func(num):\n    return range(num) | F(map, lambda x: print(x) or x) | F(sum)\n\n\nprint(R(func, 10) > PurePath("filepath"))\n```\n\n### Set Global\n\nMaybe you don\'t want to use `from cool import F` in every file of the entire project, you can use the following code to set it as a global function, just like `min`/`max`/`sum`.\n\n```python\nimport cool\n\ncool.set_global(cool.F, cool.FF)\n```\n\nMaybe you also want to expose `functools.reduce` to the world, just like `map`/`filter`.\n\n```python\nimport functools\nimport cool\n\ncool.set_global(cool.F, cool.FF, functools.reduce)\n```\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/cool',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
