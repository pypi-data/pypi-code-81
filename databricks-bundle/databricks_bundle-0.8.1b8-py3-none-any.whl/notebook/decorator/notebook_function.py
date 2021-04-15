from databricksbundle.notebook.decorator.InputDecorator import InputDecorator
from databricksbundle.notebook.decorator.DecoratedDecorator import DecoratedDecorator


@DecoratedDecorator
class notebook_function(InputDecorator):  # noqa: N801
    def __init__(self, *args):
        self._args = args
