import importlib
from argparse import Namespace, ArgumentParser
from logging import Logger
from box import Box
from consolebundle.ConsoleCommand import ConsoleCommand
from sqlalchemy.schema import CreateTable
from consolebundle.StrToBool import str2_bool
from sqlalchemy import text as sql_alchemy_text
from sqlalchemybundle.command.connection_aware_command import connection_aware_command
from sqlalchemybundle.engine.EngineFactoryResolver import EngineFactoryResolver


@connection_aware_command
class TableCreatorCommand(ConsoleCommand):
    def __init__(
        self,
        connections: Box,
        logger: Logger,
        engine_factory_resolver: EngineFactoryResolver,
    ):
        self._connections = connections
        self.__logger = logger
        self.__engine_factory_resolver = engine_factory_resolver

    def get_command(self) -> str:
        return "sqlalchemy:table:create"

    def get_description(self):
        return "Creates new table for given table entity"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument(dest="entity_class", help="Entity class (example: myproject.client.ClientEntity)")
        argument_parser.add_argument(
            "-c", "--connection", dest="connection_name", required=False, default="default", help="Connection name"
        )
        argument_parser.add_argument(
            "-f", "--force", required=False, default=False, nargs="?", const=True, type=str2_bool, help="Execute table creation query"
        )

    def run(self, input_args: Namespace):
        entity_name = input_args.entity_class[input_args.entity_class.rfind(".") + 1 :]  # noqa: E203
        entity = getattr(importlib.import_module(input_args.entity_class), entity_name)

        statement = CreateTable(getattr(entity, "__table__"))

        db_config = self._connections[input_args.connection_name]
        engine_factory = self.__engine_factory_resolver.resolve(db_config)
        engine = engine_factory.create(db_config)

        query = str(statement.compile(engine, dialect=engine.dialect))

        if input_args.force is True:
            engine.execute(sql_alchemy_text(query))

            self.__logger.warning("Table successfully created")
        else:
            print(query)
            self.__logger.warning("Add --force option to execute the table creation query")
