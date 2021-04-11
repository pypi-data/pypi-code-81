
import psycopg2

import re
number_regex = re.compile(r"\d+\.?\d*")

import logging

from dbwrapper._query import Query, Update, Delete, Condition, Column
from dbwrapper._util import (
    sql, escape_value, execute, executemany,
    cached_property, Navigator, computeIfAbsent,
    Literal
)

_LOGGER = logging.getLogger("Table")

class Table:
    def __init__(self, conn, db: str, pg_schema: str, name: str, alias: str = None):
        self.conn = conn
        self.db = db
        self.pg_schema = pg_schema.lower()
        self.name = name.lower()
        self.alias = alias.lower() if alias else alias
    
    def __str__(self):
        return "Table[%s]" % sql(self, usage="table-like")
    
    def __sql__(self, usage=None):
        if not self.alias or usage == "table-noalias":
            return self.pg_schema + "." + self.name

        if usage in ("table-like", "table"):
            return self.pg_schema + "." + self.name + " AS " + self.alias
        else:
            return self.alias

    def _ex(self, sql_str, params=[]):
        return execute(_LOGGER, self.conn, sql_str, params)

    def _exmany(self, sql_str, rows=[]):
        return executemany(_LOGGER, self.conn, sql_str, rows)

    def exists(self):
        cursor = self._ex("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = %s AND tablename = %s;", (
            self.pg_schema,
            self.name
        ))
        nfound = len(cursor.fetchall())
        cursor.close()
        if nfound > 1:
            _LOGGER.warn("Found more than one existing table with the name %s", sql(self))
        return nfound > 0
    
    def drop(self):
        self._ex("DROP TABLE %s;", (sql(self),)).close()
    
    def builder(self):
        return TableFactory(self)
    
    def select(self, *columns):
        if len(columns) == 0:
            return Query(self, "*")
        else:
            return Query(self, columns)
    
    def update(self, updates):
        return Update(self, updates)

    def delete(self):
        return Delete(self)
    
    def insert_one(self, values):
        if hasattr(values, "items"):
            cols = []
            lst = []
            for (k, v) in values.items():
                cols.append(k)
                lst.append(v)
            
            return self.insert_many(cols, [lst])
        else:
            return self.insert_many([], [values])

    def insert_many(self, columns, rows):
        ncols = 0
        if columns is not None and len(columns) > 0:
            ncols = len(columns)
            for col in columns:
                if not self.has_column(col):
                    raise ValueError("No column [%s] in table %s" % (col, sql(self)))
        else:
            ncols = max(len(row) for row in rows)

        colnames = []
        for col in columns:
            col = (col if isinstance(col, str) else sql(col)).split(".")

            if len(col) == 3 and col[0] == self.pg_schema and col[1] == (self.alias or self.name):
                colnames.append(col[2])
            elif len(col) == 2 and col[1] == (self.alias or self.name):
                colnames.append(col[1])
            elif len(col) == 1:
                colnames.append(col[0])
            else:
                raise ValueError("Cannot parse column: %s" % col)

        sql_str = "INSERT INTO %s%s VALUES (%s);" % (
            sql(self),
            " (%s)" % (",".join(colnames)) if len(colnames) > 0 else "",
            ",".join("%s" for i in range(ncols))
        )

        cursor = self._exmany(sql_str, rows) if len(rows) > 1 else self._ex(sql_str, next(iter(rows)))
        rc = cursor.rowcount
        cursor.close()
        return rc

    def column(self, name):
        if not self.has_column(name):
            raise RuntimeError("No column [%s] in table %s" % (name, sql(self)))

        return Column(self, name)

    def has_column(self, col):

        if isinstance(col, Column):
            if sql(col.table) == sql(self):
                return col.colname in self.schema
        else:
            col = str(col).split(".")

            if len(col) == 3 and col[0] == self.pg_schema and col[1] == (self.alias or self.name):
                return col[2] in self.schema
            elif len(col) == 2 and col[1] == (self.alias or self.name):
                return col[1] in self.schema
            elif len(col) == 1:
                return col[0] in self.schema
            else:
                raise ValueError("Cannot parse column: %s" % col)

    @cached_property
    def schema(self):
        cursor = self._ex("SELECT ordinal_position,column_name,data_type FROM information_schema.columns WHERE table_schema = %s AND table_name = %s;", [
            self.pg_schema,
            self.name,
        ])
        cols = cursor.fetchall()
        cursor.close()

        return {row[1]: (row[0], row[2]) for row in cols}

    @property
    def columns(self):
        return Navigator(self, "ColumnList",
            lambda: list(self.schema.keys()),
            lambda x: self.column(x)
        )

    def with_alias(self, alias):
        return Table(self.conn, self.db, self.pg_schema, self.name, alias)

class TableFactory:
    def __init__(self, table: Table):
        self._table = table
        self._columns = {}
    
    def column(self, name, type_):
        self._columns[name] = {"type": type_}
        return self
    
    def primary_key(self, column, name=None):
        self._columns[column]["pk"] = {"name": name}
        return self

    def foreign_key(self, column, table: Table, name=None, tcolumns=None):
        if not isinstance(column, (set, list)):
            column = [column]

        if isinstance(table, Table):
            if table.db != self._table.db:
                raise RuntimeError("Must be in the same database")

            table = sql(table, usage="table-noalias")

        for col in column:
            self._columns[col]["fk"] = {
                "name": name,
                "table": table,
                "tcols": list(tcolumns) if tcolumns else None
            }

        return self
    
    def unique(self, column):
        self._columns[column]["unique"] = True
        return self
    
    def not_null(self, name):
        self._columns[column]["nullable"] = False
        return self
    
    def nullable(self, name):
        self._columns[column]["nullable"] = True
        return self
    
    def __sql__(self, **kwargs):
        s = "CREATE SCHEMA IF NOT EXISTS %s; CREATE TABLE %s (" % (
            self._table.pg_schema,
            sql(self._table, usage="table-noalias")
        )
        chunks = []
        constraints = {}
        for (name, col) in self._columns.items():
            constraint = ""

            if "pk" in col:
                pkname = col["pk"]["name"]

                if pkname is None:
                    pkname = "%s_%s_pk" % (self._table.pg_schema, self._table.name)

                c = computeIfAbsent(constraints, pkname, lambda k: {
                    "type": "pk",
                    "params": [],
                    "sql": lambda name, self: "CONSTRAINT \"%s\" PRIMARY KEY (%s)" % (name, ",".join(self["params"]))
                })

                if c["type"] != "pk":
                    raise ValueError("Constraint %s is not a primary key" % pkname)

                c["params"].append(name)

            if "fk" in col:
                fk = col["fk"]
                fkname = fk["name"]

                if fkname is None:
                    x = 1
                    while True:
                        fkname = ("%s_%s_fk_%d" % (self._table.pg_schema, self._table.name, x))
                        if fkname not in constraints:
                            break
                        x += 1

                c = computeIfAbsent(constraints, fkname, lambda k: {
                    "type": "fk",
                    "table": fk["table"],
                    "tcols": fk["tcols"],
                    "params": [],
                    "sql": lambda name, self: "CONSTRAINT \"%s\" FOREIGN KEY (%s) REFERENCES %s%s" % (
                        name,
                        ",".join(self["params"]),
                        self["table"],
                        ("(%s)" % (",".join(self["tcols"]))) if bool(self["tcols"]) else ""
                    )
                })

                if c["type"] != "fk":
                    raise ValueError("Constraint %s is not a foreign key" % pkname)

                c["params"].append(name)
            
            if col.get("unique", False):
                constraint += " UNIQUE"

            if col.get("nullable") == True:
                constraint += " NULL"
            
            if col.get("nullable") == False:
                constraint += " NOT NULL"
            
            chunks.append("%s %s%s" % (name, sql(col["type"]), constraint))
        
        for name, c in constraints.items():
            chunks.append(c["sql"](name, c))

        s += ", ".join(chunks)
        s += ");"

        return s
    
    def create(self):
        execute(_LOGGER, self._table.conn, sql(self)).close()
        del self._table.schema
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        if not value:
            self.create()
