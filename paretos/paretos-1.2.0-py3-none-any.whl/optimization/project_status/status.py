from typing import Union

from .done import Done
from .ready import Ready

ProjectStatus = Union[Done, Ready]
