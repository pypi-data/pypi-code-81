from lumipy.query.expression.column.column_base import BaseColumnExpression
from lumipy.query.expression.column.source_column import SourceColumn
from lumipy.navigation.field_definition import FieldDefinition


class PrefixedColumn(BaseColumnExpression):
    """Expression representing the addition of a prefix to a source column.

    For example ('LHS', [ExampleCol]) -> LHS.[ExampleCol].

    """

    def __init__(self, column: SourceColumn, prefix: str):
        """__init__ method of the PrefixedColumn class.

        Args:
            column (SourceColumn): source column expression to prefix.
            prefix (str): prefix string to use.
        """

        if type(prefix) != str:
            raise TypeError(f"Prefix value must be a str. Was {type(prefix).__name__}.")
        if type(column) != SourceColumn:
            raise TypeError(f"Can only prefix SourceColumn types. Was {type(column).__name__}.")

        self._prefix = prefix
        self._original = column
        super().__init__(
            column.get_name(),
            column.is_main(),
            column.source_table_hash(),
            lambda x: f"{prefix}.{x.get_sql()}",
            lambda x: True,
            lambda x: x,
            'prefix',
            column
        )

    def __hash__(self):
        return hash(hash(self._prefix) + hash(self._original))

    def get_prefix(self) -> str:
        """Get prefix string this expression adds.

        Returns:
            str: the prefix string
        """
        return self._prefix

    def get_without_prefix(self):
        """Get the original source column expression.

        Returns:
            SourceColumn: the original un-prefixed column.
        """
        return self._original

    def as_col_on_new_table(self, new_table_name, new_table_hash):

        new_field_description = FieldDefinition(
            field_name=self._original.get_sql(),
            field_type='Column',
            table_name=new_table_name,
            data_type=self._original.get_type(),
            description=self._original.get_definition().description,
            is_main=self._original.is_main(),
            is_primary_key=False,
            param_default_value=None,
            table_param_columns=None
        )
        return SourceColumn(new_field_description, new_table_hash)
