__all__ = ["TrueChecker"]

import os

from .api import TrueChecker

# install uvloop if exists and not disabled
try:
    import uvloop  # noqa
except ImportError:  # pragma: no cover
    pass
else:
    if "DISABLE_UVLOOP" not in os.environ:
        uvloop.install()
