import os

_jax_enable_x64 = os.getenv("JAX_ENABLE_X64")
if _jax_enable_x64 is None or "true" in _jax_enable_x64.lower():
    from jax.config import config as _jax_config

    if not _jax_config.read("jax_enable_x64"):
        _jax_config.update("jax_enable_x64", True)
    del _jax_config

del _jax_enable_x64
del os

from .array import (
    ndarray,
    array,
    asarray,
    JAXArraySliceBlock,
    set_default_dtype,
    get_default_dtype,
)
from .jax import overload_jax, JAXBlock
import jax.numpy as np
