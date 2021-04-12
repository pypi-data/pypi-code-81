from databricksbundle.notebook.decorator.NodeDecorator import NodeDecorator


class DataFrameReturningDecorator(NodeDecorator):
    def _set_global_dataframe(self):
        self._function.__globals__[self._function.__name__ + "_df"] = self._result
