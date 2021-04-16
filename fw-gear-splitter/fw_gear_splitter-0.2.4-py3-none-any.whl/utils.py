"""Splitter utilities."""
import typing as t

import pandas as pd
from fw_file.collection import FileCollection


def quote_val(val: t.Any) -> str:
    """Add quotes around a string value."""
    if isinstance(val, str):
        return f"'{val}'"
    return str(val)


def collection_to_df(  # pylint: disable=invalid-name
    collection: FileCollection, keys: t.Optional[t.List[str]] = None
) -> pd.DataFrame:
    """Populate splitting dataframe from FileCollection.

    Args:
        files (FileCollection): Collection from which to
            populate dataframe.
        keys (t.List[str]): List of file keys to
            include in the dataframe.

    Returns:
        pd.DataFrame: Pandas dataframe
    """
    if not keys:
        keys = []
    records = []
    for idx, file in enumerate(collection):
        record = {"idx": idx, "path": file.filepath}
        for key in keys:
            val = file.get(key)
            if isinstance(val, list):
                val = tuple(val)
            record[key] = val
        records.append(record)

    return pd.DataFrame.from_records(records).set_index("idx")


def collection_from_df(  # pyline: disable=invalid-name
    files: FileCollection, dataframe: pd.DataFrame
) -> FileCollection:
    """Create FileCollection from splitting dataframe.

    Args:
        files (FileCollection): Original FileCollection
        dataframe (pd.DataFrame): Pandas dataframe representation of a
            subset of `self.files`.

    Returns:
        FileCollection: New FileCollection containing files specified
            in `df`.
    """
    file_coll = files.__class__()
    for idx in list(dataframe.index):
        file = files[idx]
        file_coll.append(file)

    return file_coll
