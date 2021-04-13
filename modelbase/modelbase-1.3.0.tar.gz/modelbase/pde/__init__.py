"""Write me."""

# Standard Library
import warnings

try:
    # Third party
    from modelbase_pde import *
except ImportError:  # pragma: no cover
    warnings.warn("Could not find pde subpackage. Did you install modelbase_pde?")
except ModuleNotFoundError:  # pragma: no cover
    warnings.warn("Could not find pde subpackage. Did you install modelbase_pde?")
