import logging
from pathlib import Path
from typing import Optional, Dict, Union

import pandas as pd

from oncoboxlib.quant.database.interfaces import PathwayDatabaseCsvReader, PathwayDatabaseXlsxReader

logger = logging.getLogger(__name__)


class Database:
    def __init__(
            self,
            gp: pd.DataFrame,
            arr: pd.DataFrame,
            components: pd.DataFrame,
            edges: pd.DataFrame,
            pathway_db: Optional[Dict[str, str]] = None
    ) -> None:

        Database._check_pathways_data(gp, arr)
        self.gp = gp
        self.arr = arr
        self.components = components
        self.edges = edges

        exists_nodes = self.components.reset_index().set_index(
            ['pathway', 'component']
        ).index.drop_duplicates().to_list()

        gp_long = self.gp.unstack()
        gp_long = gp_long[gp_long != 0]

        fake_nodes = [{
            'pathway': node[0],
            'node': node[1],
            'component': node[1]
        } for node in set(gp_long.index.to_list()) - set(exists_nodes)]

        if fake_nodes:
            self.components = self.components.reset_index().append(
                fake_nodes, ignore_index=True
            ).set_index('pathway')

        self.components = self.components[self.components['component'].notnull()]

        self.pathway_db = pathway_db

    ACTIVATOR_VALUE = 'activator'

    @staticmethod
    def _check_pathways_data(gp: pd.DataFrame, arr: pd.DataFrame) -> None:

        if gp.index.name != 'gene':
            raise ValueError(
                'Gene to pathway indicator dataframe must have index with name "gene".')

        if gp.columns.name != 'pathway':
            raise ValueError(
                'Gene to pathway indicator dataframe must have columns index with name "pathway".')

        if arr.index.name != 'gene':
            raise ValueError(
                'Arr dataframe must have index with name "gene".')

        if arr.columns.name != 'pathway':
            raise ValueError(
                'Arr dataframe must have columns index with name "pathway".')

        if gp.columns.tolist() != arr.columns.tolist():
            raise ValueError('Inconsistent gp and arr columns.')

        if gp.index.tolist() != arr.index.tolist():
            raise ValueError('Inconsistent gp and arr index.')


def adjust_samples_for_db(samples: pd.DataFrame, db: Database, na_fill_value: float) -> pd.DataFrame:
    """
    Make samples file compatible with database:
    remove missing genes, add genes from database, fill NaNs with na_fill_value.
    """
    db_genes = db.gp.index

    # if a gene is in DB but not in samples: fill the value with NaN
    samples_joined = samples.reindex(db_genes)
    samples_joined.fillna(na_fill_value, inplace=True)

    return samples_joined


def load_database(path: Union[str, Path], database_format: str) -> Database:

    if database_format == 'csv':
        database_reader = PathwayDatabaseCsvReader
    elif database_format == 'xlsx':
        database_reader = PathwayDatabaseXlsxReader
    else:
        raise ValueError(
            f'Unsupported database format "{database_format}". Choices: "csv" or "xlsx".')

    return Database(**database_reader(path).read())
