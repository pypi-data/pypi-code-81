from .new_rmsfact import _new_rmsfact

# `rmsfact()` is the only object exported from the package. We generate it here using
# `_new_rmsfact()` which handles parsing the input file containing the facts.
rmsfact = _new_rmsfact()
