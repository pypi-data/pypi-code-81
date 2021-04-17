from .core import main
from . import argument

if __name__ == '__main__':
    kind, name, kwargs = argument.get()
    main(kind, name, kwargs)
