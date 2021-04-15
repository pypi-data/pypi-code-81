import _ast
from databricksbundle.notebook.lineage.DecoratorParserInterface import DecoratorParserInterface
from datalakebundle.notebook.lineage.TableWriter import TableWriter


class TableWriterParser(DecoratorParserInterface):
    def __init__(self, name: str, mode: str):
        self.__name = name
        self.__mode = mode

    def parse(self, decorator: _ast.Call):
        return TableWriter(decorator.args[0].s, self.__mode)

    def get_name(self) -> str:
        return self.__name
