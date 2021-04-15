import re
from collections import OrderedDict
from pathlib import Path
from typing import Union

import pandas as pd


def _is_sequence(obj):
    return hasattr(obj, '__iter__') and not isinstance(obj, str)


CLEANUPS = (
    lambda s: s.strip(),
    lambda s: s.replace('\t', ' '),
    lambda s: re.sub(' +', ' ', s),
    lambda s: s.replace(' ;', ';'),
    lambda s: s.replace(' ,', ','),
    lambda s: s.replace(' .', '.'),
)


def _cleanup_atom(s, cleanups):
    for f in cleanups:
        s = f(s)
    return s


def _cleanup_block(block, cleanups=CLEANUPS):
    if _is_sequence(block):
        return [_cleanup_block(elem) for elem in block]
    else:
        return _cleanup_atom(block, cleanups)


class BaseDatabaseByPathReader:

    def __init__(self, src_path: Union[str, Path]) -> None:

        self.path = Path(src_path)

        if not self.path.exists() or not self.path.is_dir():
            raise ValueError(f'Path not found: {self.path}')

        db_name_chunks = self.path.name.split()
        name, version = ' '.join(db_name_chunks[:-1]), db_name_chunks[-1]

        assert name and version

        self.name, self.version = name, version


class PathwayDatabaseCsvReader(BaseDatabaseByPathReader):

    def read(self) -> OrderedDict:

        gp_path = self.path / 'gp.csv'
        arr_path = self.path / 'arr.csv'
        components_path = self.path / 'components.csv'
        edges_path = self.path / 'edges.csv'

        for file_path in (gp_path, arr_path, components_path, edges_path):
            if not file_path.is_file():
                raise ValueError('File "{}" not found.'.format(file_path))

        arr = pd.read_csv(arr_path, index_col=0)
        arr.index.name = 'gene'
        arr.columns.name = 'pathway'

        gp = pd.read_csv(gp_path, index_col=0).astype(int)
        gp.index.name = 'gene'
        gp.columns.name = 'pathway'

        components = pd.read_csv(components_path, index_col=0)
        edges = pd.read_csv(edges_path, index_col=0)

        return OrderedDict((
            ('pathway_db', {'name': self.name, 'version': self.version}),
            ('arr', arr),
            ('gp', gp),
            ('components', components),
            ('edges', edges)
        ))


class PathwayDatabaseXlsxReader(BaseDatabaseByPathReader):

    def read(self) -> OrderedDict:

        arr = pd.DataFrame()
        edges = pd.DataFrame()
        long_pathway_components = list()

        for pathway_file in self.path.iterdir():
            if pathway_file.is_file() and pathway_file.suffix == ".xlsx":

                try:
                    xls = pd.ExcelFile(pathway_file, engine='openpyxl')
                    pathway_arrs = pd.read_excel(xls, 'genes', header=None, names=['gene', 'arr'])
                    pathway_arrs.insert(0, 'pathway', pathway_file.stem, True)

                    pathway_edges = pd.read_excel(
                        xls, 'edges', header=None, names=['from_node', 'to_node', 'relation_type'])
                    pathway_edges.insert(0, 'pathway', pathway_file.stem, True)

                    pathway_components = pd.read_excel(
                        xls, 'nodes', header=None, names=['node', 'blank_col', 'components'])
                except Exception:
                    raise RuntimeError('Error when read pathway: {}'.format(self.path))

                if arr.empty:
                    arr = pathway_arrs
                else:
                    arr = arr.append(pathway_arrs)

                if edges.empty:
                    edges = pathway_edges
                else:
                    edges = edges.append(pathway_edges)

                for _, row in pathway_components.iterrows():
                    node_comp = list()

                    if not pd.isna(row.components):
                        for comp in _cleanup_block(row.components.split(',')):
                            node_comp.append([pathway_file.stem, row.node, comp])

                    if node_comp:
                        long_pathway_components.extend(node_comp)
                    else:
                        long_pathway_components.append([pathway_file.stem, row.node, None])

        gp = arr.copy()
        gp['arr'] = 1
        gp = gp.pivot(index='gene', columns='pathway', values='arr').fillna(0)
        gp = gp.astype(int)

        arr = arr.pivot(index='gene', columns='pathway', values='arr').fillna(0)

        edges = edges[
            ['pathway', 'from_node', 'to_node', 'relation_type']
        ].sort_values(['pathway', 'from_node', 'to_node', 'relation_type'])
        edges = edges.set_index('pathway')

        components = pd.DataFrame(
            long_pathway_components, columns=['pathway', 'node', 'component']
        ).sort_values(
            by=['pathway', 'node', 'component']
        ).set_index('pathway')

        return OrderedDict((
            ('pathway_db', {'name': self.name, 'version': self.version}),
            ('arr', arr),
            ('gp', gp),
            ('components', components),
            ('edges', edges)
        ))
