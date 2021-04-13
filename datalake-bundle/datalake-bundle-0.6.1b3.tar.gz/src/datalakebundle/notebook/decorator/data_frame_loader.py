from databricksbundle.notebook.decorator.DecoratedDecorator import DecoratedDecorator
from injecta.container.ContainerInterface import ContainerInterface
from databricksbundle.display import display as display_function
from datalakebundle.notebook.decorator.DataFrameReturningDecorator import DataFrameReturningDecorator


@DecoratedDecorator
class data_frame_loader(DataFrameReturningDecorator):  # noqa: N801
    def __init__(self, *args, display=False):
        self._args = args
        self._display = display

    def after_execution(self, container: ContainerInterface):
        self._set_global_dataframe()

        if self._display and container.get_parameters().datalakebundle.notebook.display.enabled is True:
            display_function(self._result)
