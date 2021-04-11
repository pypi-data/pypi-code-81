from .column import Column


class ColumnarFrame:
    def __init__(self, data=None):
        self.rows = 0
        self.data = {}
        if data is not None:
            for k, v in data.items():
                if self.rows == 0:
                    self.rows = len(v)
                self.data[k] = Column(self, k, v)

    @property
    def columns(self):
        return list(self.data.keys())

    def __getitem__(self, name):
        if isinstance(name, tuple):
            return tuple(self.data[key] for key in name)
        return self.data[name]

    def __setitem__(self, name, value):
        if isinstance(value, Column):
            self.data[name] = value
        else:
            self.data[name] = Column(self, name, value)
