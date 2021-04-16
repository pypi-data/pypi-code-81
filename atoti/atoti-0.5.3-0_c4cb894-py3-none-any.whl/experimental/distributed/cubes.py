from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from ..._local_cubes import LocalCubes
from .cube import DistributedCube

if TYPE_CHECKING:
    from .session import DistributedSession


@dataclass(frozen=True)
class DistributedCubes(LocalCubes[DistributedCube]):
    """Manage the distributed cubes."""

    _session: DistributedSession = field(repr=False)
