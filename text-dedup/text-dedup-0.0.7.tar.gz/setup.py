# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_dedup', 'text_dedup.dedupers']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=1.6.2,<2.0.0',
 'coverage>=5.5,<6.0',
 'dask[bag]>=2021.4.0,<2022.0.0',
 'datasets>=1.5.0,<2.0.0',
 'datasketch[scipy]>=1.5.3,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'pytest-benchmark>=3.2.3,<4.0.0',
 'pytest>=6.2.2,<7.0.0',
 'sentence-transformers>=1.0.3,<2.0.0',
 'strsimpy>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'text-dedup',
    'version': '0.0.7',
    'description': 'Text deduplication with fuzzy match and more',
    'long_description': '![banner](./banner.png)\n[![PyPI version](https://badge.fury.io/py/text-dedup.svg)](https://badge.fury.io/py/text-dedup) ![Coverage](./coverage.svg)\n\n\nText de-duplication with edit distance, LSH or embeddings. (WIP)\n\n## Usage\n\n1. Group near duplicates with `EditDistanceSimilarityDeduper` or `LSHDeduper`\n```python\nimport pandas as pd\nfrom text_dedup.dedupers import EditDistanceSimilarityDeduper\nfrom text_dedup import group_duplicates\n\ndf = pd.read_csv(...)\ndf_groups = group_duplicates(\n    df, \n    deduper=EditDistanceSimilarityDeduper(\n        similarity_metric="cosine", \n        threshold=0.8, \n        k=3),\n    column="text",\n    target_column="__group_label__"\n    )\n\ndf["__group_label__"].value_counts(dropna=False)\n```\n\n2. Remove near duplicates\n```python\nimport pandas as pd\nfrom text_dedup.dedupers import EditDistanceSimilarityDeduper\nfrom text_dedup import drop_duplicates\n\ndf = pd.read_csv(...)\ndf_dedup = drop_duplicates(\n    df, \n    deduper=EditDistanceSimilarityDeduper(\n        similarity_metric="cosine", \n        threshold=0.8, \n        k=3),\n    column="text"\n    )\n\nassert df.shape != df_dedup.shape\n```\n\n3. Remove semantically similar duplicates using `PretrainedBERTEmbeddingDeduper`\n```python\nimport pandas as pd\nfrom text_dedup.dedupers import PretrainedBERTEmbeddingDeduper\nfrom text_dedup import drop_duplicates\n\ndf = pd.read_csv(...)\ndata_dedup = drop_duplicates(\n    df, \n    deduper=PretrainedBERTEmbeddingDeduper(\n        model=\'paraphrase-distilroberta-base-v1\',\n        threshold=threshold, \n    ),\n    column="text"\n)\n```\n\n## Installation\n```bash\npip install text-dedup\n```\n\n## Benchmarks\n\n- 400 samples\n```\n------------------------------------------------------------------------------------------- benchmark: 3 tests ------------------------------------------------------------------------------------------\nName (time in ms)              Min                    Max                   Mean              StdDev                 Median                 IQR            Outliers     OPS            Rounds  Iterations\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\ntest_lsh                  748.3384 (1.0)         752.1715 (1.0)         750.5136 (1.0)        1.7357 (1.0)         751.4906 (1.0)        2.9455 (1.0)           1;0  1.3324 (1.0)           5           5\ntest_bert               7,233.6232 (9.67)      8,480.0729 (11.27)     8,058.8376 (10.74)    513.7158 (295.97)    8,311.9608 (11.06)    681.7020 (231.44)        1;0  0.1241 (0.09)          5           5\ntest_edit_distance     10,040.8134 (13.42)    10,290.2110 (13.68)    10,165.0379 (13.54)    113.2858 (65.27)    10,111.8537 (13.46)    196.6889 (66.78)         3;0  0.0984 (0.07)          5           5\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n```\n\n- 40000 samples (`PretrainedBERTEmbeddingDeduper` and `EditDistanceSimilarityDeduper` might not be scaling well to large datasets)\n```\n----------------------------------------------- benchmark: 1 tests ----------------------------------------------\nName (time in s)          Min       Max      Mean  StdDev    Median     IQR  Outliers     OPS  Rounds  Iterations\n-----------------------------------------------------------------------------------------------------------------\ntest_lsh             714.5114  714.5114  714.5114  0.0000  714.5114  0.0000       0;0  0.0014       1           1\n-----------------------------------------------------------------------------------------------------------------\n```',
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
