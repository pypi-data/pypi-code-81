class Document:
    def __init__(self, index, nodes):
        self.index = str(index).zfill(3)
        self.nodes = nodes