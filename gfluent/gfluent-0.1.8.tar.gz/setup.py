# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gfluent']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=2.13.1,<3.0.0', 'google-cloud-storage>=1.37.1,<2.0.0']

setup_kwargs = {
    'name': 'gfluent',
    'version': '0.1.8',
    'description': 'A fluent API for Google Cloud Python Client',
    'long_description': '# Google Cloud Fluent Client\n\nThis is a wrapper on Google Cloud Platform Python SDK client library. It provides a fluent-style to\ncall the methods, here is an example,\n\n```python\n\nfrom gfluent import BQ\n\nproject_id = "here-is-you-project-id"\nbq = BQ(project_id, table="mydataset.table")\n\nresult = bq.mode("WRITE_APPEND").sql("SELECT name, age from dataset.tabble").query()\n\nprint(f"The query has inserted {result} rows to table mydataset.table")\n\n```\n\n\n```python\n\nfrom gfluent import GCS\n\nproject_id = "here-is-you-project-id"\n\n# upload single local `file.txt` to `gs://bucket-name/import/file.txt`\nGCS(project_id).bucket("bucket-name").local("/tmp/file.txt").prefix("import").upload()\n\n# upload many local files to GCS\n# if you have /tmp/abc.txt, /tmp/111.txt, /tmp/abc.csv\n# two GCS objects will be created\n# gs://bucket-name/import/abc.txt\n# gs://bucket-name/import/111.txt\n(\n    GCS(project_id)\n    .bucket("bucket-name")\n    .local(path="/tmp", suffix=".txt").prefix("import").upload()\n)\n\n```\n\n## Installation\n\n\nInstall from PyPi,\n\n```bash\npip install -U gfluent\n```\n\nOr build and install from source code,\n\n```bash\npip install -r requirements-dev.txt\npoetry build\npip install dist/gfluent-<versoin>.tar.gz\n```\n\n\n## Testing\n\nThe unit test and integration test are actually using the real GCP project, so you\ncannot execute the integration test if you don\'t have the GCP project setup.\n\nIf you really want to run the test cases, you need to set up a free tier project, and\nset the project ID as `PROJECT_ID` enviroment, you also need to expose the GCP JSON key\nof the service account with correct permission of read/write `BigQuery` and `GCS`.\n\n',
    'author': 'Zhong Dai',
    'author_email': 'zhongdai.au@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zhongdai/gfluent/releases',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
