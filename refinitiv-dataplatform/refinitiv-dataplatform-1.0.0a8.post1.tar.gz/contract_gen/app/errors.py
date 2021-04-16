class UnsolvableCollision(Exception):
    def __init__(self, name, *args):
        super().__init__()
        self.name = name
        self.args = args


class CantFindCommonName(Exception):
    def __init__(self, *args):
        super().__init__()
        self.args = args
