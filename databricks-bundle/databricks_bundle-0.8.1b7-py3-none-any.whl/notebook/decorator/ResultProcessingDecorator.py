from injecta.container.ContainerInterface import ContainerInterface
from databricksbundle.notebook.decorator.BaseDecorator import BaseDecorator
from databricksbundle.notebook.decorator.DecoratedFunctionInjector import DecoratedFunctionInjector


class ResultProcessingDecorator(BaseDecorator, metaclass=DecoratedFunctionInjector):
    def process_result(self, result, container: ContainerInterface):
        pass
