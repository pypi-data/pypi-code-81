
import psycopg2
from psycopg2 import extensions

from dbwrapper.postgresql._table import Table

from dbwrapper._util import Navigator, Literal, Function

_TYPE_QUERY = """
WITH types AS (
SELECT
-- 	n.nspname as "Schema",
-- 	pg_catalog.obj_description(t.oid, 'pg_type') as "Description",
	pg_catalog.format_type(t.oid, NULL) AS "Name",
	typname
FROM pg_catalog.pg_type t
     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
WHERE (t.typrelid = 0 OR (SELECT c.relkind = 'c' FROM pg_catalog.pg_class c WHERE c.oid = t.typrelid))
  AND NOT EXISTS(SELECT 1 FROM pg_catalog.pg_type el WHERE el.oid = t.typelem AND el.typarray = t.oid)
  AND pg_catalog.pg_type_is_visible(t.oid)
),
types2 AS (
	SELECT typname AS "Name", typname FROM types
	UNION
	SELECT REPLACE(REPLACE("Name", ' ', '_'), '"', '') AS "Name", typname FROM types
)
SELECT * FROM types2 ORDER BY "Name";
"""

_FN_QUERY = """
SELECT routines.routine_name
FROM information_schema.routines
WHERE routines.specific_schema=%s
"""

class DType(Literal):
    pass

TYPE_ALIASES = {
    "serial": "serial",
    "blob": "bytea"
}

class Database:
    def __init__(self, target, name: str):
        self.target = target
        self.name = name
        self.conn = psycopg2.connect(*target[0], **target[1])
        self.conn.isolation_level = extensions.ISOLATION_LEVEL_READ_UNCOMMITTED
        self.pg_schema = "public"
        self.transactions = []
    
    def get_raw(self):
        return self.conn
        
    def open(self):
        if self.conn is None:
            self.conn = psycopg2.connect(*target[0], **target[1])
            self.conn.isolation_level = extensions.ISOLATION_LEVEL_READ_UNCOMMITTED
            return True
        else:
            return False

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            return True
        else:
            return False

    def __str__(self):
        return "Database[%s]" % self.name

    def exists(self):
        return self.conn is not None

    @property
    def schema(self):
        if self.pg_schema is not None:
            return [(x[0], x[1]) for x in self._ex(
                "SELECT schemaname, tablename FROM pg_catalog.pg_tables WHERE schemaname = %s;", [
                    self.pg_schema
                ]
            )]
        else:
            return [(x[0], x[1]) for x in self._ex("SELECT schemaname, tablename FROM pg_catalog.pg_tables;")]
    
    @property
    def tables(self):
        return Navigator(self, "TableList",
            lambda: self.schema,
            lambda x: self.table(x[1], pg_schema=x[0]),
            lambda x: x[1]
        )

    def table(self, name, pg_schema=None):
        return Table(self.conn, self.name, pg_schema or self.pg_schema, name)

    def get_functions(self):
        return [tuple(x) for x in self._ex(_FN_QUERY % self.pg_schema)]

    @property
    def functions(self):
        return Navigator(self, "Functions",
            lambda: self.get_functions(),
            lambda x: Function(pg_schema + "." + x),
            lambda x: x
        )

    def start_transaction(self):
        if self.conn:
            if len(self.transactions) == 0:
                self._ex("BEGIN;")

            tname = "transaction%d" % len(self.transactions)
            self.transactions.append(tname)
            self._ex("SAVEPOINT %s;" % tname)

            return Transaction(self, tname)
    
    def get_current_transaction(self):
        if self.conn and len(self.transactions) > 0:
            return self.transactions[-1]
        else:
            return None

    def commit(self, tname=None):
        if isinstance(tname, Transaction):
            tname = tname.name

        if self.conn and len(self.transactions) > 0 and (self.transactions[-1] == tname or tname is None):
            self._ex("RELEASE SAVEPOINT %s;" % self.transactions[-1])
            self.transactions.pop()

            if len(self.transactions) == 0:
                self._ex("COMMIT;")
            return True
        else:
            return False
        
    def rollback(self, tname=None):
        if isinstance(tname, Transaction):
            tname = tname.name

        if self.conn and len(self.transactions) > 0 and (self.transactions[-1] == tname or tname is None):
            self._ex("ROLLBACK TO SAVEPOINT %s;" % self.transactions[-1])
            self.transactions.pop()

            if len(self.transactions) == 0:
                self._ex("COMMIT;")
            return True
        else:
            return False

    def __enter__(self):
        self.start_transaction()
        return self

    def __exit__(self, et, ev, tb):
        if et:
            self.rollback()
        else:
            self.commit()

    def get_dtypes(self):
        return [tuple(x) for x in self._ex(_TYPE_QUERY)] + list(TYPE_ALIASES.items())

    @property
    def dtypes(self):
        return Navigator(self, "DTypeList",
            lambda: self.get_dtypes(),
            lambda x: DType(x[1]),
            lambda x: x[0]
        )

    def _ex(self, sql_str, params=[]):
        cursor = self.conn.cursor()
        cursor.execute(sql_str, params)
        lst = list(cursor.fetchall()) if cursor.rowcount > 0 else []
        cursor.close()
        return lst

class Transaction:
    def __init__(self, db, name):
        self.db = db
        self.name = name
    
    def rollback(self):
        return self.db.rollback(self.name)
    
    def commit(self):
        return self.db.commit(self.name)

    def __enter__(self):
        return self

    def __exit__(self, et, ev, tb):
        if et:
            self.rollback()
        else:
            self.commit()
