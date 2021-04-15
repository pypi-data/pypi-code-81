
def copy_docstring_of(original):
    def wrapper(target):
        if type(target.__doc__) != str:
            target.__doc__ = "N.A."
        if type(original.__doc__) != str:
            original.__doc__ = ""

        if "NOTE:" not in original.__doc__:
            target.__doc__ = original.__doc__ + "\n\n NOTE: \n" + target.__doc__
        else:
            original.__doc__ = original.__doc__.replace("N.A.", "")
            original.__doc__ = original.__doc__.rstrip()
            target.__doc__ = original.__doc__ + "\n" + target.__doc__

        return target

    return wrapper
