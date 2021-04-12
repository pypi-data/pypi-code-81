""" module not found exception """

class ModuleNotImportedError(ModuleNotFoundError):
    """ Extends ModuleNotFoundError. Because a Module can also
    available but not imported """
