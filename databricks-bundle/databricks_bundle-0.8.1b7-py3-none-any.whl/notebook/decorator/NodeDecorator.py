from injecta.container.ContainerInterface import ContainerInterface
from databricksbundle.notebook.decorator.BaseDecorator import BaseDecorator
from databricksbundle.notebook.decorator.DecoratedFunctionInjector import DecoratedFunctionInjector
from databricksbundle.notebook.function.ArgumentsResolver import ArgumentsResolver
from databricksbundle.notebook.function.function_inspector import inspect_function


class NodeDecorator(BaseDecorator, metaclass=DecoratedFunctionInjector):

    _result = None

    def set_result(self, result):
        self._result = result

    @property
    def result(self):
        return self._result

    def prepare_arguments(self, container: ContainerInterface):
        arguments_resolver: ArgumentsResolver = container.get(ArgumentsResolver)
        return arguments_resolver.resolve(inspect_function(self._function), self._args)

    def after_execution(self, container: ContainerInterface):
        pass
