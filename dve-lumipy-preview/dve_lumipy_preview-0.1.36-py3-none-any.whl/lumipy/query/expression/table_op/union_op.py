import lumipy.query.expression.table_op.group_aggregate_op
import lumipy.query.expression.table_op.limit_op
import lumipy.query.expression.table_op.order_by_op
import lumipy.query.expression.table_op.select_op
import lumipy.query.expression.table_op.where_op
from lumipy.query.expression.table_op.base_table_op import BaseTableExpression
from typing import Union


class UnionExpression(BaseTableExpression):
    """Class representing a union/union all statement applied to a pair of table expressions.

    """

    # noinspection PyUnresolvedReferences
    def __init__(
            self,
            top: Union['SelectTableExpression', 'WhereTableExpression', 'GroupByAggregation', 'UnionExpression'],
            bottom: Union['SelectTableExpression', 'WhereTableExpression', 'GroupByAggregation', 'UnionExpression'],
            union_all: bool
    ):
        """__init__ method of the UnionExpression class.

        Args:
            top (Union['SelectTableExpression', 'WhereTableExpression', 'GroupByAggregation']): table expression to be
            used in the top of the union expression. Only select, where, union, and groupby aggregates are valid.
            bottom (Union['SelectTableExpression', 'WhereTableExpression', 'GroupByAggregation']): table expression to
            be used in the bottom of the union expression. Only select, where, union and groupby aggregates are valid.
            union_all (bool): whether this is a union (False) or union all (True).
        """

        self._union_op_str = 'union'
        self._union_all = union_all
        if self._union_all:
            self._union_op_str += ' all'

        top_type = type(top)
        bottom_type = type(bottom)
        supported = [
            lumipy.query.expression.table_op.select_op.SelectTableExpression,
            lumipy.query.expression.table_op.where_op.WhereTableExpression,
            lumipy.query.expression.table_op.group_aggregate_op.GroupByAggregation,
            UnionExpression
        ]

        if top_type not in supported:
            supported_str = ", ".join([t.__name__ for t in supported])
            raise TypeError(
                f"Top input to {self._union_op_str} was not a supported type. Was {type(top).__name__} "
                f"but union expects one of the following: {supported_str}."
            )
        if bottom_type not in supported:
            supported_str = ", ".join([t.__name__ for t in supported])
            raise TypeError(
                f"Bottom input to {self._union_op_str} was not a supported type. Was {type(bottom).__name__} "
                f"but union expects one of the following: {supported_str}."
            )

        self._top = top
        self._bottom = bottom

        # Columns on the union are just the top input columns
        # HC will throw if they're different in number, otherwise will concat
        if len(top.get_columns()) != len(bottom.get_columns()):
            raise ValueError(
                f"Input tables to {self._union_op_str} must have the same number of columns. "
                f"Was {len(top.get_columns())} vs {len(bottom.get_columns())}."
            )

        super().__init__(
            top.get_columns(),
            top.get_client(),
            self._union_op_str,
            None,
            top.get_source_table(),
            top,
            bottom
        )

    def get_table_sql(self):
        return f"{self._top.get_table_sql()} {self._union_op_str} {self._bottom.get_table_sql()}"

    def order_by(self, *order_bys):
        """Apply an order by expression to this table expression given a collection of column ordering expressions.

        Sort a table's rows according to a collection of columns/functions of columns.

        Args:
            *order_bys:column ordering expression args in teh order they are to be applied.

        Returns:
            OrderedTableExpression: OrderedTableExpression instance representing the ordering applied to this table
            expression.
        """
        return lumipy.query.expression.table_op.order_by_op.OrderedTableExpression(self, *order_bys)

    def limit(self, limit):
        """Apply a limit expression to this table.

        Limit will take the first n-many rows of the table.

        Args:
            limit (int): the limit value

        Returns:
            LimitTableExpression: LimitTableExpression instance representing the limit expression applied to this table
            expression.
        """
        return lumipy.query.expression.table_op.limit_op.LimitTableExpression(self, limit)

    def union(self, other):
        """Apply a union expression to this table.

        Union works like a vertical concatenation of two table expressions that is then filtered for distinct rows.

        Args:
            other (BaseTableExpression): the other table expression to take the 'union' with.

        Returns:
            UnionExpression: a UnionExpression instance representing the union between this table expression and the
            argument table expression.

        """
        return UnionExpression(self, other, union_all=False)

    def union_all(self, other):
        """Apply a union all expressinon to this table.

        Union all works like a vertical concatenation of two tables. Unlike 'union' it doesn't filter duplicates rows
        out. The number of columns between the two table expressions must match.

        Args:
            other (BaseTableExpression): the other table expression to take the 'union all' with.

        Returns:
            UnionExpression: a UnionExpression instance representing the union all between this table expression and the
            argument table expression.

        """
        return UnionExpression(self, other, union_all=True)
