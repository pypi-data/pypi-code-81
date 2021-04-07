from lumipy.query.expression.column_op.base_scalar_op import BaseScalarOp
from lumipy.query.expression.column_op.common import get_expr_sql
from lumipy.query.expression.sql_value_type import SqlValType, fixed_type, comparables
from lumipy.query.expression.column.column_base import BaseColumnExpression


class Between(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression, value3: BaseColumnExpression):
        super(Between, self).__init__(
            "between values",
            lambda x, y, z: f"{get_expr_sql(x)} between {get_expr_sql(y)} and {get_expr_sql(z)}",
            lambda x, y, z: {x, y} in comparables and {x, z} in comparables,
            fixed_type(SqlValType.Boolean),
            value1,
            value2,
            value3
        )


class NotBetween(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression, value3: BaseColumnExpression):
        super(NotBetween, self).__init__(
            "not between values",
            lambda x, y, z: f"{get_expr_sql(x)} not between {get_expr_sql(y)} and {get_expr_sql(z)}",
            lambda x, y, z: {x, y} in comparables and {x, z} in comparables,
            fixed_type(SqlValType.Boolean),
            value1,
            value2,
            value3
        )


class StrReplace(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression, value3: BaseColumnExpression):
        super(StrReplace, self).__init__(
            "str replace",
            lambda x, y, z: f"Replace({x.get_sql()}, {y.get_sql()}, {z.get_sql()})",
            lambda *args: all(a == SqlValType.Text for a in args),
            fixed_type(SqlValType.Text),
            value1,
            value2,
            value3
        )
