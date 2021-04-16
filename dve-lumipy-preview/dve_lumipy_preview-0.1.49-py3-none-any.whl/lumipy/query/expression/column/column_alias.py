from lumipy.common.string_utils import sql_str_to_name
from lumipy.query.expression.column.column_base import BaseColumnExpression
from lumipy.query.expression.column.column_literal import LiteralColumn, python_to_expression
from typing import Dict, Union


# noinspection PyArgumentList
class AliasedColumn(BaseColumnExpression):
    """Column expression class that represents the operation of aliasing a column or function of column(s).

    """

    def __init__(self, column: BaseColumnExpression, alias: Union[str, LiteralColumn]):
        """__init__ method for AliasedColumn class.

        Args:
            column (BaseColumnExpression): column/function of columns to be aliased.
            alias (str): the name the column/function of columns is to be aliased as.
        """
        if isinstance(column, AliasedColumn):
            raise TypeError(
                f"Can't alias a a column that's already aliased:\n{column.get_sql()}."
            )
        if not issubclass(type(column), BaseColumnExpression):
            raise TypeError(
                f"Object to apply column alias to must inherit from BaseColumnExpression. Was {type(column).__name__}"
            )
        if not isinstance(alias, str) and not isinstance(alias, LiteralColumn):
            raise TypeError(
                f"Alias must be a non-empty string. Was a {type(alias).__name__}, value: {alias}."
            )

        alias_expr = python_to_expression(alias)
        self._alias = alias_expr.get_py_value()
        self._original = column
        super().__init__(
            sql_str_to_name(alias_expr.get_py_value()),
            column.is_main(),
            column.source_table_hash(),
            lambda x, y: f"{x.get_sql()} as [{y.get_py_value()}]",
            lambda x, y: True,
            lambda x, y: x,
            'alias',
            column,
            alias_expr
        )

    def get_alias(self) -> str:
        """Get the alias string

        Returns:
            str: the alias
        """
        return self._alias

    def get_original(self) -> BaseColumnExpression:
        """Get the original column expression

        Returns:
            BaseColumnExpression: the original column expression
        """
        return self._original

    def with_alias(self, alias) -> 'AliasedColumn':
        raise TypeError(f"Can't alias a column that's already aliased: \n{self.get_sql()}.")

    def with_prefixes(self, table_prefixes: Dict[int, str]):
        # Because the alias of a column has the same hash as the column we need to apply the prefixing to the original
        # col and then re-apply the alias op.
        prefixed = self.get_original().with_prefixes(table_prefixes)
        re_aliased = prefixed.with_alias(self._alias)
        return re_aliased

    def __hash__(self):
        # Hash must be the same as the non-prefixed column for expression
        # decomposition, prefixing, and reconstruction to work.
        return hash(self._alias) + hash(self._original) + hash('alias')

    # noinspection PyUnresolvedReferences
    def as_col_on_new_table(self, new_table_name: str, new_table_hash: int) -> 'SourceColumn':

        from lumipy.navigation.field_definition import FieldDefinition
        from lumipy.query.expression.column.source_column import SourceColumn

        new_field_description = FieldDefinition(
            field_name=self.get_alias(),
            field_type='Column',
            table_name=new_table_name,
            data_type=self.get_type(),
            description=f"Alias of {self.get_sql()}",
            is_main=self.is_main(),
            is_primary_key=False,  # todo: implement in base. This is missing.
            param_default_value=None,
            table_param_columns=None
        )
        return SourceColumn(new_field_description, new_table_hash, with_brackets=True)

    # noinspection PyUnresolvedReferences
    def ascending(self) -> 'AscendingOrder':
        # Ordering expects the original SQL piece as an arg
        return self.get_original().ascending()

    # noinspection PyUnresolvedReferences
    def descending(self) -> 'DescendingOrder':
        # Ordering expects the original SQL piece as an arg
        return self.get_original().descending()
