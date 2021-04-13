from logging import Logger
from databricksbundle.notebook.decorator.DecoratedDecorator import DecoratedDecorator
from databricksbundle.notebook.decorator.ResultProcessingDecorator import ResultProcessingDecorator
from injecta.container.ContainerInterface import ContainerInterface


class TestingStorage:
    result: None


@DecoratedDecorator
class dummy_saver(ResultProcessingDecorator):  # noqa: N801
    def __init__(self, table_identifier: str):
        self._table_identifier = table_identifier

    def process_result(self, result, container: ContainerInterface):
        logger: Logger = container.get("datalakebundle.logger")

        logger.info(f"Saving into {self._table_identifier}")

        TestingStorage.result = result
