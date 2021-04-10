
from typing import List, Union, Dict, Tuple, Any, Set
from dataset_utils.sqlite import get_or_create
from .buffered_writer import BufferedTableWriter, ConflictChecker
import os


class DictCache(object):
    def __init__(self, dbpath, table_name='default', key_column='key', value_column='value'):
        # model id is model_name + model version
        assert os.path.abspath(dbpath) == dbpath, f'error: please pass in an absolute path: {dbpath} vs {os.path.abspath(dbpath)}'
        self.dbpath = dbpath
        self.table_name = table_name
        self.key_column = key_column
        self.value_column = value_column
        self.db, self.table = get_or_create(
            self.dbpath, self.table_name, primary_id=self.key_column, columns=[self.value_column],
            types={self.key_column: 'string', self.value_column: 'string'})

    def set_multiple(self, d: Dict[str, Dict[str, str]]):
        b = BufferedTableWriter(self.table, key_column=self.key_column, key_conflicts=ConflictChecker.OVERWRITE)
        for k, v in d.items():
            assert isinstance(k, str)
            assert isinstance(v, str)
            b.insert({self.key_column: k, self.value_column: v})
        b.force_flush()

    def get_multiple(self, keys: Union[List[str], str]) -> Tuple[Dict[str, str], Set[str]]:
        if isinstance(keys, str):
            keys = [keys]
        assert isinstance(keys, list)
        keys_set = set(keys)
        assert len(keys) == len(keys_set), 'Error: there are duplicate keys in your request'
        results = {}
        for e in self.table.find(key=keys):
            k, v = e[self.key_column], e[self.value_column]
            assert isinstance(k, str)
            assert isinstance(v, str)
            results[k] = v
        remaining = keys_set - set(results.keys())
        assert len(results) + len(remaining) == len(keys)
        return results, remaining

