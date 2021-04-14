import dataset
from dataset.types import Types
from enum import Enum
from urllib.parse import urlparse
from sqlalchemy import event
import sqlite3
import os
from dataset.database import Database
from typing import Tuple


class ConnectMode(Enum):
    # Rollback journal (the default mode)
    JOURNAL = 1
    # Write-Ahead-Log:
    # https://www.sqlite.org/wal.html
    WAL = 2
    READ_ONLY = 3


def connect(path, mode=ConnectMode.JOURNAL, ensure_exists=False):
    # NOTE: if you open in read-only mode, we always check to see it exists
    # otherwise, if ensure_exists is False, we might create it if it doesn't exist
    if ensure_exists:
        assert os.path.exists(path)
    if mode == ConnectMode.JOURNAL:
        return connect_journal(path)
    elif mode == ConnectMode.WAL:
        return connect_wal(path)
    else:
        assert mode == ConnectMode.READ_ONLY
        return connect_ro(path)


def connect_journal(path):
    return dataset.connect('sqlite:///' + path, sqlite_wal_mode=False)


def connect_ro(path):
    # https://github.com/pudo/dataset/issues/136
    # https://stackoverflow.com/questions/27910829/sqlalchemy-and-sqlite-shared-cache
    # https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
    # See "URI Connections":
    # https://docs.sqlalchemy.org/en/14/dialects/sqlite.html
    assert os.path.exists(path)
    creator = lambda: sqlite3.connect('file:' + path + '?mode=ro&check_same_thread=false', uri=True)
    return dataset.connect('sqlite:///', engine_kwargs={'creator': creator}, sqlite_wal_mode=False)


def connect_wal(path) -> dataset.Database:
    assert not path.startswith('sqlite:')
    url = 'sqlite:///' + path
    db = dataset.connect(url, sqlite_wal_mode=True)
    return db


def get_or_create(path_or_db, table_name, mode=ConnectMode.JOURNAL, primary_id=None, columns=None, types=None, index=None) -> Tuple[dataset.Database, dataset.Table]:
    # by default, types are all string (text or string - they're the same in sqlite)
    # more readable than calling get_or_create_from_dict
    generated_dict = {}
    if types is None:
        types = dict()
    if columns is not None:
        assert isinstance(columns, list) or isinstance(columns, tuple)

    def get_type(column, default='text'):
        type_ = types.get(column)
        if type_ is None:
            type_ = default
        if isinstance(type_, str):
            return getattr(dataset.types.Types, type_)
        assert not isinstance(type_, str)
        return type_

    if primary_id:
        generated_dict['primary'] = (primary_id, get_type(primary_id))
    generated_dict['columns'] = []
    if columns:
        for column in columns:
            generated_dict['columns'].append((column, get_type(column)))
    if index:
        generated_dict['index'] = index

    db = get_or_create_from_dict(path_or_db, {table_name: generated_dict}, mode=mode)
    table = db.load_table(table_name)
    return db, table


def get_or_create_from_dict(path_or_db, table_info: dict, mode=ConnectMode.JOURNAL) -> dataset.Database:
    if not isinstance(path_or_db, dataset.Database):
        assert isinstance(path_or_db, str)
        db = connect(path_or_db, mode)
    else:
        db = path_or_db

    def get_type(type_):
        if isinstance(type_, str):
            return getattr(db.types, type_)
        return type_

    for table_name in table_info.keys():
        ct = table_info[table_name]
        if table_name not in db:
            # create column if it doesn't exist
            # Create table_name
            #assert 'primary' in ct
            #assert 'columns' in ct
            if 'primary' in ct:
                primary_id, primary_key = ct['primary']
                table = db.create_table(table_name, primary_id=primary_id, primary_type=get_type(primary_key))
            else:
                table = db.create_table(table_name)
        else:
            table = db[table_name]
        assert isinstance(table, dataset.Table)
        assert isinstance(ct['columns'], list)
        for col in ct['columns']:
            col_name, col_type = col
            if not table.has_column(col_name):
                table.create_column(col_name, get_type(col_type))
        if 'index' in ct:
            for cc in ct['index']:
                idxcols = cc
                if not isinstance(cc, list):
                    idxcols = [cc]
                if not table.has_index(idxcols):
                    table.create_index(idxcols)
        # NOTE: we have to do this to ensure the table is created by the time we return,
        #       esp for WAL mode
        #tmp_table = db.load_table(table_name)
        # even this line below
        #assert len(tmp_table.columns) >= 0
        # assert table_name in db
    return db


class RamCache():
    # TODO - in the middle of implementing

    @classmethod
    def from_path(cls, path):
        pass

    # For now, read-only
    def __init__(self, path, cache_dir='/dev/shm/'):
        assert os.path.isdir(cache_dir)
        assert os.path.exists(path)
        import shutil
        shutil.copy(path, cache_dir)
        from pathlib import Path
        self.cached_path = os.path.join(cache_dir, Path(path).name)
        assert os.path.isfile(self.cached_path)
        self.db = connect_ro(self.cached_path)
        self.closed = False

    def close(self):
        self.closed = True
        import shutil
        os.remove(self.cached_path)

