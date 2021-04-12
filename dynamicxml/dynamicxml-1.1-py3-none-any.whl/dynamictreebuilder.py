from xml.etree.ElementTree import TreeBuilder
from .dynamicelement import DynamicElement

class DynamicTreeBuilder(TreeBuilder):
    def __init__(self, *args, **kwargs):
        super().__init__(element_factory=DynamicElement, *args, **kwargs)
