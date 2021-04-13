from databricksbundle.notebook.lineage.OutputDecoratorInterface import OutputDecoratorInterface


class TableWriter(OutputDecoratorInterface):
    def __init__(self, table_name: str, mode: str):
        self.__table_name = table_name
        self.__mode = mode

    @property
    def table_name(self):
        return self.__table_name

    @property
    def mode(self):
        return self.__mode
