from lumipy.query.expression.column_op.common import get_expr_sql
from lumipy.query.expression.sql_value_type import numerics, numeric_priority, \
    SqlValType, fixed_type, \
    comparables
from lumipy.query.expression.column_op.base_scalar_op import BaseScalarOp
from lumipy.query.expression.column.column_base import BaseColumnExpression


class Add(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "add",
            lambda x, y: f"{get_expr_sql(x)} + {get_expr_sql(y)}",
            lambda x, y: x in numerics and y in numerics,
            numeric_priority,
            value1,
            value2
        )


class Sub(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "subtract",
            lambda x, y: f"{get_expr_sql(x)} - {get_expr_sql(y)}",
            lambda x, y: x in numerics and y in numerics,
            numeric_priority,
            value1,
            value2
        )


class Mul(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "multiply",
            lambda x, y: f"{get_expr_sql(x)} * {get_expr_sql(y)}",
            lambda x, y: x in numerics and y in numerics,
            numeric_priority,
            value1,
            value2
        )


class Div(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "divide",
            lambda x, y: f"{get_expr_sql(x)} / {get_expr_sql(y)}",
            lambda x, y: x in numerics and y in numerics,
            lambda x, y: y,
            value1,
            value2
        )


class Mod(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "modulus",
            lambda x, y: f"{get_expr_sql(x)} % {get_expr_sql(y)}",
            lambda x, y: x in numerics and y in numerics,
            lambda x, y: SqlValType.Int,
            value1,
            value2
        )


class BitwiseAnd(BaseScalarOp):
    # Todo: type checking is incorrect. Not boolean inputs.
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "bitwise and",
            lambda x, y: f"{get_expr_sql(x)} & {get_expr_sql(y)}",
            lambda x, y: x == SqlValType.Boolean and y == SqlValType.Boolean,
            lambda x, y: SqlValType.Boolean,
            value1,
            value2
        )


class BitwiseOr(BaseScalarOp):
    # Todo: type checking is incorrect. Not boolean inputs.
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "bitwise or",
            lambda x, y: f"{get_expr_sql(x)} | {get_expr_sql(y)}",
            lambda x, y: x == SqlValType.Boolean and y == SqlValType.Boolean,
            lambda x, y: SqlValType.Boolean,
            value1,
            value2
        )


class BitwiseXor(BaseScalarOp):
    # Todo: type checking is incorrect. Not boolean inputs.
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "bitwise xor",
            lambda x, y: f"{get_expr_sql(x)} ^ {get_expr_sql(y)}",
            lambda x, y: x == SqlValType.Boolean and y == SqlValType.Boolean,
            lambda x, y: SqlValType.Boolean,
            value1,
            value2
        )


class StringConcat(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "string concat",
            lambda x, y: f"{get_expr_sql(x)} || {get_expr_sql(y)}",
            lambda x, y: x == SqlValType.Text and y == SqlValType.Text,
            fixed_type(SqlValType.Text),
            value1,
            value2
        )


class Equals(BaseScalarOp):
    # todo: change comparables -> equatable
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "equal",
            lambda x, y: f"{get_expr_sql(x)} = {get_expr_sql(y)}",
            lambda x, y: {x, y} in comparables,
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class NotEquals(BaseScalarOp):
    # todo: change comparables -> equatable
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "not equal",
            lambda x, y: f"{get_expr_sql(x)} != {get_expr_sql(y)}",
            lambda x, y: {x, y} in comparables,
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class GreaterThan(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "greater than",
            lambda x, y: f"{get_expr_sql(x)} > {get_expr_sql(y)}",
            lambda x, y: {x, y} in comparables,
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class LessThan(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "less than",
            lambda x, y: f"{get_expr_sql(x)} < {get_expr_sql(y)}",
            lambda x, y: {x, y} in comparables,
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class GreaterThanOrEqual(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "greater or equal",
            lambda x, y: f"{get_expr_sql(x)} >= {get_expr_sql(y)}",
            lambda x, y: {x, y} in comparables,
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class LessThanOrEqual(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super().__init__(
            "less or equal",
            lambda x, y: f"{get_expr_sql(x)} <= {get_expr_sql(y)}",
            lambda x, y: {x, y} in comparables,
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class And(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super(And, self).__init__(
            "and",
            lambda x, y: f"{get_expr_sql(x)} and {get_expr_sql(y)}",
            lambda x, y: {x, y} == {SqlValType.Boolean},
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class Or(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super(Or, self).__init__(
            "or",
            lambda x, y: f"{get_expr_sql(x)} or {get_expr_sql(y)}",
            lambda x, y: {x, y} == {SqlValType.Boolean},
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class IsIn(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):

        from lumipy.query.expression.column.collection import CollectionExpression
        if not isinstance(value2, CollectionExpression):
            raise TypeError("Second arg to IN/NOT IN expression must be a CollectionExpression.")

        super(IsIn, self).__init__(
            "is in",
            lambda x, y: f"{get_expr_sql(x)} in {y.get_sql()}",
            lambda x, y: True,
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class NotIn(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):

        from lumipy.query.expression.column.collection import CollectionExpression
        if not isinstance(value2, CollectionExpression):
            raise TypeError("Second arg to IN/NOT IN expression must be a CollectionExpression.")

        super(NotIn, self).__init__(
            "is not in",
            lambda x, y: f"{get_expr_sql(x)} not in {y.get_sql()}",
            lambda x, y: True,
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class Like(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super(Like, self).__init__(
            "like",
            lambda x, y: f"{get_expr_sql(x)} like {get_expr_sql(y)}",
            lambda x, y: {x, y} == {SqlValType.Text},
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class NotLike(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super(NotLike, self).__init__(
            "not like",
            lambda x, y: f"{get_expr_sql(x)} not like {get_expr_sql(y)}",
            lambda x, y: {x, y} == {SqlValType.Text},
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class Glob(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super(Glob, self).__init__(
            "glob",
            lambda x, y: f"{get_expr_sql(x)} glob {get_expr_sql(y)}",
            lambda x, y: {x, y} == {SqlValType.Text},
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )


class NotGlob(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super(NotGlob, self).__init__(
            "not glob",
            lambda x, y: f"{get_expr_sql(x)} not glob {get_expr_sql(y)}",
            lambda x, y: {x, y} == {SqlValType.Text},
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )

class Regexp(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super(Regexp, self).__init__(
            "regexp",
            lambda x, y: f"{get_expr_sql(x)} regexp {get_expr_sql(y)}",
            lambda x, y: {x, y} == {SqlValType.Text},
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )

class NotRegexp(BaseScalarOp):
    def __init__(self, value1: BaseColumnExpression, value2: BaseColumnExpression):
        super(NotRegexp, self).__init__(
            "not regexp",
            lambda x, y: f"{get_expr_sql(x)} not regexp {get_expr_sql(y)}",
            lambda x, y: {x, y} == {SqlValType.Text},
            fixed_type(SqlValType.Boolean),
            value1,
            value2
        )
