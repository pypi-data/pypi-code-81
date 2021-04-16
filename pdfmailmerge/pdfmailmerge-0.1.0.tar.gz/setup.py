# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdfmailmerge']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'argparse>=1.4.0,<2.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pdfkit>=0.6.1,<0.7.0',
 'tqdm>=4.59.0,<5.0.0']

setup_kwargs = {
    'name': 'pdfmailmerge',
    'version': '0.1.0',
    'description': 'Easy command line mailmerge csv -> pdf tool.',
    'long_description': '# pdf-mailmerge\n\n\nMailmerge to a pdf or html file. Adds csv data to an html jinja template.\nCan be configured to generate filenames and subdirectories as well as sort order from columns in the csv.\n\n## Install\n\n```\npip install pdf-mailmerge\n```\n\n## Usage\n\nRequires a `config.yml` file in your directory containing:\n\n```\ndata: Some.csv\n\ntemplate: "Some_jinja.html"\n\nidentifier_columns:\n  - "col1"\n  - "col2"\n\nfilename_columns:\n  - "col3"\n  - "col4"\n\noutput_folders:\n  - "col1"\n  - "col5"\n\nsort:\n  - "col2"\n  - "col3"\n```\n\n#### Required Configuration Fields\n\n`data`: csv file with the data you wish to mailmerge\n\n`template`: jinja template being used for the mailmerge\n\n`identifier_columns`: columns used to construct a primary key for the data. If a column already contains the primary key, list it but only it. A mailmerge document will be created for every unique value or unique value combination of the identifier columns.\n\n`filename_columns`: columns used to construct the filename for the document. Name will be "col1_col2_" etc.\n\n#### Optional Configuration Fields\n\n`output_folders`: columns used to construct output subdirectories. All files placed in either `html` or `pdf` directory. Additional folder nesting levels based on order of output folders. Sample file path `pdf/col1/col5`. \n\n`sort`: columns used to sort documents within their output folder. If multiple options, sort precedence given in order of list.\n',
    'author': 'Joshua',
    'author_email': 'joshua.flies.planes@gmail.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
