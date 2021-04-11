
try:
    import psycopg2
except ImportError:
    raise ImportError("psycopg2 must be installed to use the postgresql wrapper.")

from dbwrapper.postgresql._conn import Connection, MASTER_DB, TEMP_DB
from dbwrapper._query import Condition

__all__ = [
    "Connection",
    "Condition",
    "MASTER_DB",
    "TEMP_DB"
]
