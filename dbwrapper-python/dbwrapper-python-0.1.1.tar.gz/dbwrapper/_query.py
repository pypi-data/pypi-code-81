
import logging

from dbwrapper._util import (
    sql, execute as sqlexec, skip_empty_join,
    Literal, Navigator
)

__all__ = [
    "Query",
    "Update",
    "Delete",
    "Operator",
    "Condition",
]

class Query:
    _LOGGER = logging.getLogger("Query")
    def __init__(self, src, columns):
        self._src = src
        self._cols = [(Literal(col) if isinstance(col, str) else col) for col in columns]
        self._joins = []
        self._constraint = None
        self._group_by = None
        self._order_by = None
        self._order_dir = None
        self._having = None
        self._offset = None
        self._size = None
        self._join_alias = None

    def __sql__(self, usage=None, **kwargs):
        stmt = "SELECT " \
            + ",".join(sql(c, usage="value") for c in self._cols) \
            + " FROM " \
            + sql(self._src, usage="table-like")
            
        for join in self._joins:
            stmt += " " + sql(join) + " "
        if self._constraint is not None:
            stmt += " WHERE "
            stmt += sql(self._constraint)
        if self._group_by is not None:
            stmt += " GROUP BY "
            stmt += sql(self._group_by)
        if self._having is not None:
            stmt += " HAVING "
            stmt += sql(self._having)
        if self._order_by is not None:
            stmt += " ORDER BY "
            stmt += sql(self._order_by)
            if self._order_dir is not None:
                stmt += " " + self._order_dir
        if self._size is not None:
            stmt += " LIMIT %s" % sql(self._size)
        elif self._offset is not None:
            stmt += " LIMIT -1"
        if self._offset is not None:
            stmt += " OFFSET %s" % sql(self._offset)
        
        if usage  == "value":
            return "(%s)" % stmt
        elif usage == 'table-like':
            return "(%s)%s" % (
                stmt,
                " AS %s" % sql(self._join_alias) if self._join_alias else ""
            )
        else:
            if self._join_alias is not None:
                return self._join_alias
            else:
                return stmt

    @property
    def columns(self):
        return Navigator(self, "ColumnList",
            lambda: [sql(x, usage="column-like") for x in self._cols],
            lambda x: self.column(x)
        )

    def column(self, colname):
        if self._join_alias is None:
            logging.warn("Referencing query column without query alias - this will be EXTREMELY slow (if it works at all)")

        return Column(Literal(sql(self)), colname)

    def where(self, condition):
        self._constraint = condition
        return self

    def group_by(self, condition):
        self._group_by = condition
        return self

    def order_by(self, condition):
        self._order_by = condition
        return self

    def order_ascending(self):
        self._order_dir = "ASC"
        return self

    def order_descending(self):
        self._order_dir = "DESC"
        return self

    def having(self, condition):
        self._having = condition
        return self

    def inner_join(self, table):
        join = Join("inner", table, self)
        self._joins.append(join)
        return join

    def left_join(self, table):
        join = Join("left", table, self)
        self._joins.append(join)
        return join

    def left_outer_join(self, table):
        join = Join("left outer", table, self)
        self._joins.append(join)
        return join

    def right_outer_join(self, table):
        join = Join("right outer", table, self)
        self._joins.append(join)
        return join

    def full_outer_join(self, table):
        join = Join("full outer", table, self)
        self._joins.append(join)
        return join

    def cross_join(self, table):
        join = Join("cross", table, self)
        self._joins.append(join)
        return join

    def join(self, join_type, table):
        join = Join(join_type, table, self)
        self._joins.append(join)
        return join

    def offset(self, offset):
        self._offset = offset
        return self
    
    def size(self, size):
        self._size = size
        return self

    def with_alias(self, alias):
        self._join_alias = alias
        return self

    def execute(self, asdict=False):
        cursor = sqlexec(Query._LOGGER, self._src.conn, sql(self))
        if asdict:
            lst = [{k[0]: v for k, v in zip(cursor.description, x)} for x in cursor.fetchall()]
        else:
            lst = [x if len(x) > 1 else x[0] for x in cursor.fetchall()]
        cursor.close()
        return lst

class Update:
    _LOGGER = logging.getLogger("Update")
    def __init__(self, src, updates):
        self._src = src
        self._updates = list(updates.items()) if isinstance(updates, dict) else updates
        self._joins = []
        self._constraint = None
        self._having = None

    def __sql__(self, **kwargs):
        stmt = "UPDATE %s SET " % sql(self._src, usage="table")
        
        stmt += " %s " % (
            ", ".join("%s = %s" % (
                sql(dst, usage="column"),
                sql(src, usage="value")
            ) for (dst, src) in self._updates)
        )

        for join in self._joins:
            stmt += " %s " % sql(join)
        if self._constraint is not None:
            stmt += " WHERE "
            stmt += sql(self._constraint)
        if self._having is not None:
            stmt += " HAVING "
            stmt += sql(self._having)
        return stmt

    def where(self, condition):
        self._constraint = condition
        return self

    def having(self, condition):
        self._having = condition
        return self

    def inner_join(self, table):
        join = Join("inner", table, self)
        self._joins.append(join)
        return join

    def left_join(self, table):
        join = Join("left", table, self)
        self._joins.append(join)
        return join

    def left_outer_join(self, table):
        join = Join("left outer", table, self)
        self._joins.append(join)
        return join

    def right_outer_join(self, table):
        join = Join("right outer", table, self)
        self._joins.append(join)
        return join

    def full_outer_join(self, table):
        join = Join("full outer", table, self)
        self._joins.append(join)
        return join

    def cross_join(self, table):
        join = Join("cross", table, self)
        self._joins.append(join)
        return join

    def join(self, join_type, table):
        join = Join(join_type, table, self)
        self._joins.append(join)
        return join

    def execute(self):
        cursor = sqlexec(Update._LOGGER, self._src.conn, sql(self))
        rc = cursor.rowcount
        cursor.close()
        return rc

class Delete:
    _LOGGER = logging.getLogger("Delete")
    def __init__(self, src):
        self._src = src
        self._joins = []
        self._constraint = None
        self._having = None

    def __sql__(self, **kwargs):
        stmt = "DELETE FROM " + sql(self._src, usage="table")
        for join in self._joins:
            stmt += " " + sql(join) + " "
        if self._constraint is not None:
            stmt += " WHERE "
            stmt += sql(self._constraint)
        if self._having is not None:
            stmt += " HAVING "
            stmt += sql(self._having)
        return stmt

    def where(self, condition):
        self._constraint = condition
        return self

    def having(self, condition):
        self._having = condition
        return self

    def inner_join(self, table):
        join = Join("inner", table, self)
        self._joins.append(join)
        return join

    def left_join(self, table):
        join = Join("left", table, self)
        self._joins.append(join)
        return join

    def left_outer_join(self, table):
        join = Join("left outer", table, self)
        self._joins.append(join)
        return join

    def right_outer_join(self, table):
        join = Join("right outer", table, self)
        self._joins.append(join)
        return join

    def full_outer_join(self, table):
        join = Join("full outer", table, self)
        self._joins.append(join)
        return join

    def cross_join(self, table):
        join = Join("cross", table, self)
        self._joins.append(join)
        return join

    def join(self, join_type, table):
        join = Join(join_type, table, self)
        self._joins.append(join)
        return join

    def execute(self):
        cursor = sqlexec(Delete._LOGGER, self._src.conn, sql(self))
        rc = cursor.rowcount
        cursor.close()
        return rc

class Operator:
    def __init__(self, s):
        self._sql = s

    def __sql__(self, **kwargs):
        return self._sql

Operator.AND = Operator("AND")
Operator.OR = Operator("OR")
Operator.EQ = Operator("=")
Operator.NE = Operator("!=")
Operator.GT = Operator(">")
Operator.LT = Operator("<")
Operator.GE = Operator(">=")
Operator.LE = Operator("<=")

class Condition:
    def __init__(self, lhs, operator=None, rhs=None):
        self.lhs = lhs
        self.op = operator
        self.rhs = rhs

    def __repr__(self):
        return "Condition[%s]" % skip_empty_join(" ", sql(self.lhs), sql(self.op), sql(self.rhs))

    def __sql__(self, **kwargs):
        return "(%s)" % skip_empty_join(" ", sql(self.lhs, usage="value"), sql(self.op), sql(self.rhs, usage="value"))

    def __and__(self, rhs):
        return Condition(self, Operator.AND, rhs)

    def __or__(self, rhs):
        return Condition(self, Operator.OR, rhs)
    
    def __eq__(self, rhs):
        return Condition(self, Operator.EQ, rhs)

    def __ne__(self, rhs):
        return Condition(self, Operator.NE, rhs)

    def __gt__(self, rhs):
        return Condition(self, Operator.GT, rhs)

    def __lt__(self, rhs):
        return Condition(self, Operator.LT, rhs)

    def __ge__(self, rhs):
        return Condition(self, Operator.GE, rhs)

    def __le__(self, rhs):
        return Condition(self, Operator.LE, rhs)

class Join:
    def __init__(self, join_type, tbl, condition):
        self.join_type = join_type
        self.tbl = tbl
        self.join_condition = None
        self.condition = condition

    def on(self, join_condition: Condition):
        self.join_condition = join_condition
        return self.condition

    def __sql__(self, **kwargs):
        return "%s JOIN %s ON %s" % (self.join_type.upper(), sql(self.tbl, usage="table-like"), sql(self.join_condition))

class Column(Condition):
    def __init__(self, table, colname):
        self.table = table
        self.colname = colname
    
    def __repr__(self):
        return "Column[%s.%s]" % (sql(self.table), self.colname)

    def __sql__(self, usage=None):
        if usage in ("column", "column-like"):
            return self.colname
        else:
            return "%s.%s" % (sql(self.table), self.colname)

    def __hash__(self):
        return hash(self.__sql__())
        
    def is_in(self, values):
        return Condition(
            self,
            Literal("IN"),
            Literal("(%s)" % (",".join(sql(x) for x in values)))
        )
