from typing import Union

from .continuous import Continuous
from .discrete import Discrete

Continuity = Union[Continuous, Discrete]
