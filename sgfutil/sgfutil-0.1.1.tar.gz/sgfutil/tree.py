class GameNode(object):
    def __init__(self, parent, children=None, prop=None, val=None, nodetype=None, branch=0, **kwargs):
        """If root node, set parent=None."""
        self.parent = parent
        self.id = self.parent.id + 1 if parent else 0
        self.children = children if children else []
        self.prop = prop
        self.val = val
        self.nodetype = nodetype
        self.branch = branch
        self.__dict__.update(kwargs)
    
    def __repr__(self):
        s = f"{self.branch}-{self.id:0>3d} ~ {self.prop}: {self.val} ({self.nodetype})"
        return s

    def add_children(self, node):
        self.children.append(node)
