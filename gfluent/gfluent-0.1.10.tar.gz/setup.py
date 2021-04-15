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
    'version': '0.1.10',
    'description': 'A fluent API for Google Cloud Python Client',
    'long_description': '# Google Cloud Fluent Client\n\nThis is a wrapper on Google Cloud Platform Python SDK client library. It provides a fluent-style to\ncall the methods. The idea is, there are too many parameters for Google `Storage` and `BigQuery`,\nhowever, most of them are ok to be set as default value. \n\nThis library is good for Data Engineer to create data pipeline based on `BigQuery`, here is an example\nof a end to end user case.\n\nYou are asked to\n\n1 - load multiple files from your local drive to GCS\n2 - load those files to a BigQuery table\n3 - run another query on that table by joining other tables, store the result to another table\n\n\n```python\n\nfrom gfluent import BQ, GCS\n\nproject_id = "here-is-you-project-id"\nbucket_name = "my-bucket"\ndataset = "sales"\ntable_name = "products"\nprefix = "import"\nlocal_path = "/user/tom/products/" # there are many *.json files in this directory\n\n# uplaod files to GCS bucket\n(\n    GCS(project_id)\n    .local(path=local_path, suffix=".json" )\n    .bucket(bucket_name)\n    .prefix(prefix)\n    .upload()\n)\n\n# if you need to create the dataset\nBQ(project_id).create_dataset(dataset, location="US")\n\n# load data to BigQuery table\n\nuri = f"gs://{bucket_name}/{prefix}/*.json"\nnumber_of_rows = (\n    BQ(project_id)\n    .table(f"{dataset}.{table_name}")\n    .mode("WRITE_APPEND")               # don\'t have to, default mode\n    .create_mode("CREATE_IF_NEEDED")    # don\'t have to, default mode\n    .format("NEWLINE_DELIMITED_JSON")   # don\'t have to, default format\n    .gcs(uri).load(location="US")\n)\n\nprint(f"{number_of_rows} rows are loaded")\n\n\n# run a query\n\nfinal_table = "sales_summary"\n\nsql = """\n    select t1.col1, t2.col2, t2.col3\n    FROM\n        sales.products t1\n    JOIN\n        other.category t2\n    ON  t1.prod_id = t2.prod_id\n"""\n\nnumber_of_rows = (\n    BQ(product_id)\n    .table(f"{dataset}.{final_table}")\n    .sql(sql)\n    .create_mode("CREATE_NEVER")    # have to, don\'t want to create new table\n    .query()\n)\n\nprint(f"{number_of_rows} rows are appended")\n\n\n# now let\'s query the new table\n\nrows = (\n    BQ(product_id)\n    .sql(f"select col1, col2 from {dataset}.{final_table} limit 10")\n    .query()\n)\n\nfor row in rows:\n    print(row.col1, row.col2)\n```\n\n\nHere is the [document](https://gfluent.readthedocs.io/en/latest/#), and please refer\nto the test cases to see more real examples.\n\nThis project is in the inital phase.\n\n\n## Installation\n\n\nInstall from PyPi,\n\n```bash\npip install -U gfluent\n```\n\nOr build and install from source code,\n\n```bash\npip install -r requirements-dev.txt\npoetry build\npip install dist/gfluent-<versoin>.tar.gz\n```\n\n\n## Testing\n\nThe unit test and integration test are actually using the real GCP project, so you\ncannot execute the integration test if you don\'t have the GCP project setup.\n\nIf you really want to run the test cases, you need to set up a free tier project, and\nset the project ID as `PROJECT_ID` enviroment, you also need to expose the GCP JSON key\nof the service account with correct permission of read/write `BigQuery` and `GCS`.\n\n',
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
