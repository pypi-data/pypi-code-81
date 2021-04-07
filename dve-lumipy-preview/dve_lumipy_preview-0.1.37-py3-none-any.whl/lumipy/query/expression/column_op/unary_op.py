from lumipy.query.expression.column_op.base_scalar_op import BaseScalarOp
from lumipy.query.expression.column_op.common import get_expr_sql
from lumipy.query.expression.sql_value_type import numerics, SqlValType, fixed_type, all_types
from lumipy.query.expression.column.column_base import BaseColumnExpression


class Not(BaseScalarOp):
    def __init__(self, value: BaseColumnExpression):
        super(Not, self).__init__(
            "not",
            lambda x: f"not {get_expr_sql(x)}",
            lambda x: x == SqlValType.Boolean,
            fixed_type(SqlValType.Boolean),
            value
        )


class IsNull(BaseScalarOp):
    def __init__(self, value: BaseColumnExpression):
        super(IsNull, self).__init__(
            "is null",
            lambda x: f"{get_expr_sql(x)} is null",
            lambda x: x in all_types,
            fixed_type(SqlValType.Boolean),
            value
        )


class IsNotNull(BaseScalarOp):
    def __init__(self, value: BaseColumnExpression):
        super(IsNotNull, self).__init__(
            "is null",
            lambda x: f"{get_expr_sql(x)} is not null",
            lambda x: x in all_types,
            fixed_type(SqlValType.Boolean),
            value
        )


class Negative(BaseScalarOp):
    def __init__(self, value: BaseColumnExpression):
        super(Negative, self).__init__(
            "negative",
            lambda x: f"-{get_expr_sql(x)}",
            lambda x: x in numerics,
            lambda x: x,
            value
        )


class LowerCase(BaseScalarOp):
    def __init__(self, value: BaseColumnExpression):
        super(LowerCase, self).__init__(
            "lower case",
            lambda x: f"Lower({x.get_sql()})",
            lambda x: x == SqlValType.Text,
            lambda x: SqlValType.Text,
            value
        )


class UpperCase(BaseScalarOp):
    def __init__(self, value: BaseColumnExpression):
        super(UpperCase, self).__init__(
            "upper case",
            lambda x: f"Upper({x.get_sql()})",
            lambda x: x == SqlValType.Text,
            lambda x: SqlValType.Text,
            value
        )
