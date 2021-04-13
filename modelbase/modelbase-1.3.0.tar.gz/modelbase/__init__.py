"""Write me."""

__version__ = "1.3.0"

# Local code
from . import core, ode, utils

try:
    # Third party
    import modelbase_pde as pde
except ImportError:
    pass
