# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cutout']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0']

setup_kwargs = {
    'name': 'cut-out-cookies',
    'version': '0.1.2',
    'description': 'Jinja extension for optionally including files and directories',
    'long_description': '# A jinja2 extension for optionally including files in cookiecutter templates\n\nIt\'s a well known and documented issue that cookiecutter does not support\nconditionally included files and directories. See\n[this post on github](https://github.com/cookiecutter/cookiecutter/issues/723).\n\nThis package unlocks that feature with simple jinja2 filters that can be\napplied to:\n* optional file inclusion\n* optional directory inclusion\n* optional inclusion of blocks within templates\n* optional inclusion of in-line text\n\n\n## Setup\n\nThis assumes that you have cookiecutter installed already and have a project\nthat you are building into a template. This also assumes you are managing\nyour environment in your preferred way.\n\nFirst, install `cut-out-cookies`:\n```bash\n$ pip install cut-out-cookies\n```\nIf you are using poetry, pipenv, flit, etc you will need to convert the\ncommand for your setup.\n\nAdd the extension to your `cookiecutter.json` file like so:\n```json\n{\n    "full_name": "Tucker Beck",\n    "email": "tucker.beck@gmail.com",\n    "project_name": "Sugar Cookies Project",\n    "version": "0.1.0",\n    "_extensions": ["cutout.Stencil"]\n}\n```\nThe only important line here is where the extension is being added. The\nreset is just for example context.\n\nNext, you should add some \'patterns\' to your `cookiecutter.json` that you\nwill use to \'decorate\' your optional cookies with:\n```json\n{\n    "full_name": "Tucker Beck",\n    "email": "tucker.beck@gmail.com",\n    "project_name": "Sugar Cookies Project",\n    "version": "0.1.0",\n    "_extensions": ["cutout.Stencil"],\n    "include_sprinkles": false,\n    "include_frosting": false\n}\n```\nThis indicates that, by default, any cookies decorated with \'sprinkles\' or\n\'frosting\' should not be included in the generated project. The user will\nnow be prompted if they want to include the optional features \'sprinkles\'\nand \'frosting\'\n\nFinally, due to [this issue on the cookiecutter github repo](https://github.com/cookiecutter/cookiecutter/issues/1518)\nyou will need to install a post-gen project hook to cleanup the directories\nthat you intend to omit. Add a `hooks` directory in your template with a\nfile called `post_gen_project.py`. That file needs to contain this:\n```python\nfrom cutout import cleanup\n\ncleanup()\n```\n\nThat\'s it. You should be ready to make some cookies now!\n\n\n## Using cut-out-cookies stencils\n\nFor a case study, let\'s suppose you are building a project stencil called\n\'Sugar Cookies\' that starts out looking like this:\n```\nsugar-cookies/\n├── cookiecutter.json\n└── {{cookiecutter.project_name}}\n    └── README.md\n```\n\n\n### Optionally including a file\n\nTo indicate that a file should only be included if a certain pattern is\nincluded, you use the `stencil_path` filter in its template filename.\n\nLet\'s create a file called \'tasty.py\' that should only be included if the\n\'sprinkles\' pattern is applied. To do that, we\'ll apply the `stencil_path`\nfilter like so:\n```\nexamples/\n├── cookiecutter.json\n└── {{cookiecutter.project_name}}\n    ├── README.md\n    └── {{\'tasty.py\'|stencil_path(\'sprinkles\')}}\n```\n\nNow if the `include_sprinkles` setting is enabled in cookiecutter, the rendered\nproject will have a file called `tasty.py`. If it is not enabled, the `tasty.py`\nsource file will be omitted altogether\n\n\n### Optionally including a directory\n\nTo indicate that a directory should only be included if a certain pattern is\nincluded, you use the `stencil_path` filter in its name just like for files.\n\nLet\'s create a diretory called \'batch\' that should only be included if the\n\'frosting\' pattern is included. To do that, we\'ll apply the `stencil_path` filter\nlike so:\n```\nexamples/\n├── cookiecutter.json\n└── {{cookiecutter.project_name}}\n    ├── README.md\n    └── {{\'batch\'|stencil_path(\'frosting\')}}\n        ├── star_shaped.py\n        └── heart_shaped.py\n```\n\nNow if the `include_frosting` setting is enabled in cookiecutter, the rendered\nproject will have a directory called `batch` that includes two file called\n`star_shaped.py` and `heart_shaped.py`. If it is not enabled, the entire directory\nwill not be included.\n\n\n### Optionally include a block of text\n\nTo indicate that a block of text should only be included if a cerain pattern\nis included, you use the `stencil` filter block like so:\n```\nThis text will always be included\n{%- filter stencil(\'glitter\') }\nThis text will only be inlcuded if the glitter pattern is included in the\ncookiecutter config\n{% endfilter %}\n```\n\n\n### Optionally include text inline\n\nTo indicate that a bit  of in-line text should only be included if a cerain pattern\nis included, you use the `stencil` filter like so:\n```\nThis text includes {{ \'whipped cream\' | stencil(\'creamy\') }} frosting\n```\nThe text above will only include \'whipped cream\' if the `creamy` pattern in included\n',
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dusktreader/cut-out-cookies',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
