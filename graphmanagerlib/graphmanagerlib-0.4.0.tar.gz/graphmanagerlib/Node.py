class Node:
    def __init__(self, XMin, YMin, XMax,YMax,Tag):
        self.XMin = XMin
        self.YMin = YMin
        self.XMax = XMax
        self.YMax = YMax
        self.Tag = Tag

    def to_string(self):
        return ','.join([str(self.XMin), str(self.YMin), str(self.XMax), str(self.YMax), self.Tag])


