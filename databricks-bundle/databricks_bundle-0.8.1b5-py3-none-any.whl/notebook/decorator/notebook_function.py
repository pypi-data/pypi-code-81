from databricksbundle.notebook.decorator.NodeDecorator import NodeDecorator
from databricksbundle.notebook.decorator.DecoratedDecorator import DecoratedDecorator


@DecoratedDecorator
class notebook_function(NodeDecorator):  # noqa: N801
    def __init__(self, *args):
        self._args = args
