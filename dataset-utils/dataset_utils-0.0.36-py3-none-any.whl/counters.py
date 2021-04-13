"""
Simple way to implement counters via sqlite

sample usage:
python3 -m dataset_utils.counters increment_cli counters.sqlite completed

"""
import dataset
from dataset_utils.sqlite import connect, get_or_create, ConnectMode
import fire
import time
from typing import Union


def get_or_create_counters(db: Union[str, dataset.Database], table_name: str):
    return get_or_create(
        db, table_name,
        columns=['epoch', 'value'],
        types={'epoch': 'float', 'value': 'integer'},
        index=['epoch']
    )


class SqliteCounters(object):
    def __init__(self, db, mode=ConnectMode.JOURNAL):
        if isinstance(db, str):
            self.db = connect(db, mode=mode)
        else:
            assert isinstance(db, dataset.Database)
            self.db = db
        self.table_cache = {}

    def increment(self, counter, value=1):
        if counter not in self.table_cache:
            _, table = get_or_create_counters(self.db, counter)
            self.table_cache[counter] = table
        table = self.table_cache[counter]
        table.insert({'ts': time.time(), 'value': value})

    def window_sum(self, counter, lookback):
        ts = time.time() - lookback
        out = self.db.query(f'select sum(value) from {counter} where ts >= {ts};')
        row = next(out)
        sum_val = row['sum(value)']
        return sum_val

    def prune(self):
        # TODO - implement later
        pass


def increment(dbpath: str, table_name: str, value=1):
    sc = SqliteCounters(dbpath)
    sc.increment(table_name, value=value)


def window_sum(db: str, table_name: str, lookback):
    sc = SqliteCounters(db, mode=ConnectMode.READ_ONLY)
    sum_val = sc.window_sum(table_name, lookback)
    if sum_val is None:
        return 0
    return sum_val


def window_sum_gte(db: str, table_name: str, lookback, value):
    sum_val = window_sum(db, table_name, lookback)
    assert sum_val >= value


if __name__ == '__main__':
    fire.Fire()
