from databricksbundle.notebook.lineage.argument.DecoratorInputFunctionInterface import DecoratorInputFunctionInterface


class ReadTable(DecoratorInputFunctionInterface):
    def __init__(self, table_name: str):
        self.__table_name = table_name

    @property
    def table_name(self):
        return self.__table_name
