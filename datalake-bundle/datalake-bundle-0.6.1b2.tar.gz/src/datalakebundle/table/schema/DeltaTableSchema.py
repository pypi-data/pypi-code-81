from pyspark.sql.types import StructType


class DeltaTableSchema(StructType):
    def __init__(self, fields: list, primary_key, constraints: list = None):
        super().__init__(fields)
        self.__primary_key_columns = [primary_key] if isinstance(primary_key, str) else primary_key
        self.__constraints = constraints or []

    @property
    def primary_key_columns(self) -> list:
        return self.__primary_key_columns

    @property
    def constraints(self):
        return self.__constraints
