import os
# TODO - should finish this sometime
from typing import List, Union, Dict, Tuple, Any, Set
from dataset_utils.sqlite import get_or_create, ConnectMode, connect
from dataset_utils.buffered_writer import BufferedTableWriter, ConflictChecker
import os
import dataset
from collections import defaultdict
from pypika import Table, Query


def chunks(lst, n):
    # https://stackoverflow.com/a/312464
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class ScoreCache(object):
    def __init__(self, dbpath, table_name: str, rel_from: str):
        # model id is model_name + model version
        assert os.path.abspath(dbpath) == dbpath, f'error: please pass in an absolute path: {dbpath} vs {os.path.abspath(dbpath)}'
        dne = not os.path.exists(dbpath)
        self.dbpath = dbpath
        self.table_name = table_name
        self.rel_from = rel_from
        self.db, self.table = get_or_create(
            self.dbpath, self.table_name, primary_id='path', types={'path': 'string'},
            mode=ConnectMode.WAL)
        # assert self.table_name in self.db

    def create_indicies(self):
        assert isinstance(self.table, dataset.Table)
        for col in self.table.columns:
            # NOTE: the below code only creates the index if it doesn't already exist
            self.table.create_index([col])

    def set_multiple(self, d: Dict[str, Dict[str, float]]):
        b = BufferedTableWriter(self.table, key_column='path', key_conflicts=ConflictChecker.OVERWRITE)
        for path, scores in d.items():
            assert isinstance(scores, dict)
            assert isinstance(path, str)
            assert os.path.isabs(path), f'error: {path} is not an abs path'
            row: Dict[str, Any] = scores.copy()
            max_all = 0.0
            max_per = defaultdict(float)
            for label, score in scores.items():
                assert isinstance(score, float), f'Error contains non-floats: {str(scores)}'
                max_all = max(max_all, score)
                label_prefix = 'max_' + label.split('_')[0]
                max_per[label_prefix] = max(max_per[label_prefix], score)

            for label, score in max_per.items():
                row[label] = score

            row['max_all'] = max_all
            relpath = os.path.relpath(path, self.rel_from)
            row['path'] = relpath
            row['parent_folder'] = relpath.split('/')[0]
            b.insert(row)
        b.force_flush()
        self.create_indicies()

    def top_predictions(self, target_class: str, path_prefix=None, folders=None, not_folders=None, order_by='default', order='desc', page=0, limit=10000) -> List[Dict[str, Any]]:
        if order_by in ('default', None):
            order_by = target_class
        if isinstance(folders, str):
            folders = [folders]
        assert order in ('desc', 'asc')
        results = []
        offset = page * limit
        import logging
        logging.error(f'order_by: {order_by}')
        logging.error(f'limit: {limit}')
        logging.error(f'offset: {offset}')
        from pypika import Table, Query, Order
        ctable = Table(self.table_name)
        q = Query.from_(ctable).select(ctable.star)
        assert folders or not_folders, 'at least one needs to be set'
        assert not (folders and not_folders), 'folders and not_folders cannot be set'
        if folders:
            q = q.where(ctable.parent_folder.isin(folders))
        else:
            assert not_folders
            q = q.where(ctable.parent_folder.notin(not_folders))
        if path_prefix:
            q = q.where(ctable.path.glob(path_prefix + '*'))
        q = q.orderby(getattr(ctable, order_by), order=getattr(Order, order))
        # after the score, order by the path
        q = q.orderby(ctable.path)
        q = q.offset(offset)
        q = q.limit(limit)
        logging.error('should run: ' + str(q))
        #for row in self.table.find(parent_folder={'in': folders}, order_by=order_by, _offset=offset, _limit=limit):
        for row in self.db.query(str(q)):
            row['path'] = os.path.join(self.rel_from, row['path'])
            results.append(row)
        return results

    def table_counts(self):
        tmp_results = self.db.query(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}';")
        existing_tables = set()
        for row in tmp_results:
            existing_tables.add(row['name'])
        return existing_tables

    def get_multiple(self, paths: Union[List[str], str], order_by=None, limit=None) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
        existing_tables = self.table_counts()
        if self.table_name not in existing_tables:
            return {}, paths
        if isinstance(paths, str):
            paths = [paths]
        for path in paths:
            assert os.path.isabs(path)
        # we convert to relpath because we use it for everything
        relpaths = [os.path.relpath(path, self.rel_from) for path in paths]
        #import logging
        #logging.error('new paths: ' + str(paths))
        assert isinstance(relpaths, list)
        keys_set = set(paths)
        assert len(relpaths) == len(keys_set), 'Error: there are duplicate keys in your request'
        results = {}
        score_table = Table('scores')

        for relpaths_chunk in chunks(relpaths, 10000):
            # we chunk the reads b/c there's a limit for how big a query can be
            q = Query.from_(score_table).select(
                score_table.star,
            )
            q = q.where(score_table.path.isin(relpaths_chunk))
            if order_by:
                q = q.orderby(order_by)
            q = q.limit(limit)
            for row in self.db.query(str(q)):
                relpath = row.pop('path')
                # row['path'] = relpath
                path = os.path.join(self.rel_from, relpath)
                parent_folder = row.pop('parent_folder')
                for label, score in row.items():
                    assert isinstance(score, float)
                assert isinstance(row, dict)
                row['parent_folder'] = parent_folder
                row['path'] = relpath
                results[path] = row
        remaining = keys_set - set(results.keys())
        remaining = [os.path.join(self.rel_from, p) for p in remaining]
        assert len(results) + len(remaining) == len(relpaths)
        return results, remaining

