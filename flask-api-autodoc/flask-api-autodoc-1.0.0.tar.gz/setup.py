# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flask_api_autodoc']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'flask-api-autodoc',
    'version': '1.0.0',
    'description': 'A Python module to generate a page documenting the API of a Flask application.',
    'long_description': "# Flask API Auto-documentation\n\nA Python module to generate a page documenting the API of a Flask application.\n\n## Installation\n\npip install flask-audo-doc\n\n## Usage\n\n```\nimport flask\nfrom flask_api_autodoc.view import render_page\n\napp = flask.Flask('demo')\napp.route('/info')(render_something)\napp.route('/api/this')(render_something)\napp.route('/api/that')(render_something)\n\n@app.route('/doc')\ndef _():\n  return render_page(path_prefixes=['/api'])\n```\n\n## Support\n\nPlease [open an issue](https://github.com/lsiden/flask-api-autodoc/issues/new) for support.\n\n## Contributing\n\nClone, edit, and submit pull requests.\n\n## Dev Automation\n\n- `make clean`\n- `make test`\n- `make tox`\n- `make install-local`\n- `make build`\n\n## Author\n\nLawrence Siden\n<br>Westside Consulting LLC\n<br>Ann Arbor, MI  USA\n<br>lsiden@gmail.com\n\n## License\n\nMIT\n",
    'author': 'Lawrence Siden',
    'author_email': 'lsiden@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lsiden/flask-api-autodoc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
