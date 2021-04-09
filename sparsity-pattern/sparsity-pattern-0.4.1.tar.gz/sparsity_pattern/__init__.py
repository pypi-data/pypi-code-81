__version__ = '0.4.1'

from .generators import (
    get, diag, dense_quadratic, dense_pythonic, nodiag_quadratic,
    nodiag_pythonic, blockflex, circledet)
from .utils import get_matrix_dims_circle
from .experimental import blockdiag
