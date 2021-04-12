from xml.etree.ElementTree import ElementTree, Element

class DynamicElement(Element):
    def __init__(self, tag, attrib={}, attr_prefix='attr_', **extra):
        self.attr_prefix = attr_prefix
        super().__init__(tag=tag, attrib=attrib, **extra)

    def __getattr__(self, key:str):

        # caller is trying to get an attribute
        if key.startswith(self.attr_prefix):
            key = key.replace(self.attr_prefix, '')

            # key is invalid
            if key not in self.attrib:
                raise AttributeError(key)

            return self.attrib[key]
        # caller is trying to get child elements, return as a list
        else:
            return self.findall(key)

    def __setattr__(self, key:str, value):

        # defer to super if it's a predefined member
        if key in self.__dict__ or key in ['attr_prefix', 'tag', 'attrib', 'text', 'tail', '_children']:
            super().__setattr__(key, value)
            return

        # only attr_prefix lookups are allowed
        if not key.startswith(self.attr_prefix):
            raise AttributeError(key)

        key = key.replace(self.attr_prefix, '')

        # invalid key
        if key not in self.attrib:
            raise AttributeError(key)

        self.attrib[key] = value