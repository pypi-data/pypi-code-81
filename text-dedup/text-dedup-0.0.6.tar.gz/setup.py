# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_dedup', 'text_dedup.dedupers']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=1.6.2,<2.0.0',
 'datasets>=1.5.0,<2.0.0',
 'datasketch[scipy]>=1.5.3,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pytest-benchmark>=3.2.3,<4.0.0',
 'pytest>=6.2.2,<7.0.0',
 'sentence-transformers>=1.0.3,<2.0.0',
 'strsimpy>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'text-dedup',
    'version': '0.0.6',
    'description': 'Text deduplication with fuzzy match and more',
    'long_description': '# text-dedup\n![PyPI](https://img.shields.io/pypi/v/text-dedup?style=plastic)\n\nText de-duplication with edit distance, LSH or embeddings. (WIP)\n\n## Usage\n\n1. Group near duplicates\n```python\nimport pandas as pd\nfrom text_dedup.dedupers import EditDistanceSimilarityDeduper\nfrom text_dedup import group_duplicates\n\ndf = pd.read_csv(...)\ndf_groups = group_duplicates(\n    df, \n    deduper=EditDistanceSimilarityDeduper(\n        similarity_metric="cosine", \n        threshold=0.8, \n        k=3),\n    column="text",\n    target_column="__group_label__"\n    )\n\ndf["__group_label__"].value_counts(dropna=False)\n```\n\n2. Remove near duplicates\n```python\nimport pandas as pd\nfrom text_dedup.dedupers import EditDistanceSimilarityDeduper\nfrom text_dedup import drop_duplicates\n\ndf = pd.read_csv(...)\ndf_dedup = drop_duplicates(\n    df, \n    deduper=EditDistanceSimilarityDeduper(\n        similarity_metric="cosine", \n        threshold=0.8, \n        k=3),\n    column="text"\n    )\n\nassert df.shape != df_dedup.shape\n```\n\n3. Remove semantically similar duplicates\n```python\nimport pandas as pd\nfrom text_dedup.dedupers import PretrainedBERTEmbeddingDeduper\nfrom text_dedup import drop_duplicates\n\ndf = pd.read_csv(...)\ndata_dedup = drop_duplicates(\n    df, \n    deduper=PretrainedBERTEmbeddingDeduper(\n        model=\'paraphrase-distilroberta-base-v1\',\n        threshold=threshold, \n    ),\n    column="text"\n)\n```\n\n## Installation\n```bash\npip install text-dedup\n```\n\n## Benchmarks\n\n```\nLSH\n------------------------------------------------ benchmark: 1 tests ------------------------------------------------\nName (time in ms)          Min       Max      Mean   StdDev    Median      IQR  Outliers     OPS  Rounds  Iterations\n--------------------------------------------------------------------------------------------------------------------\ntest_performance3     767.0355  846.3728  803.1992  31.7007  798.3628  50.2480       2;0  1.2450       5           5\n--------------------------------------------------------------------------------------------------------------------\n\nEditDistance\n--------------------------------------------- benchmark: 1 tests ---------------------------------------------\nName (time in s)          Min      Max     Mean  StdDev   Median     IQR  Outliers     OPS  Rounds  Iterations\n--------------------------------------------------------------------------------------------------------------\ntest_performance2     10.7813  11.7912  11.2641  0.3861  11.1549  0.5356       2;0  0.0888       5           5\n--------------------------------------------------------------------------------------------------------------\n\nBERT\n-------------------------------------------- benchmark: 1 tests -------------------------------------------\nName (time in s)         Min      Max    Mean  StdDev  Median     IQR  Outliers     OPS  Rounds  Iterations\n-----------------------------------------------------------------------------------------------------------\ntest_performance1     8.0105  10.8614  9.4974  1.2967  9.1050  2.3446       3;0  0.1053       5           5\n-----------------------------------------------------------------------------------------------------------\n```',
    'author': 'Chenghao Mou',
    'author_email': 'mouchenghao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
