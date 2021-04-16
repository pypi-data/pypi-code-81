from collections import defaultdict

import pandas as pd

from jutest.utils.choise import choice
from jutest.utils.display import display


def show_duplicates(dataframe: pd.DataFrame, column_names: list, limit_groups: int = 5, **kwargs):
    column_indexes = [dataframe.columns.get_loc(name) for name in column_names]
    buckets = defaultdict(list)
    for row in dataframe.itertuples():
        hashes = tuple(
            hash(row[i + 1])
            for i in column_indexes
        )
        bucket_id = hash(hashes)
        buckets[bucket_id].append(row)
    buckets = dict(sorted(buckets.items(), key=lambda bucket: len(bucket[1]), reverse=True))

    count_groups = 0
    for bucket_id, values in buckets.items():
        count = len(values)
        if count > 1:
            display(f'Count of duplicates: {count}', html=True)
            duplicates = pd.DataFrame(values)
            duplicates = choice(duplicates, **kwargs)
            duplicates.index = duplicates.pop(duplicates.columns[0])
            duplicates.columns = dataframe.columns
            display(duplicates, **kwargs)
            count_groups += 1
            if count_groups >= limit_groups:
                break
