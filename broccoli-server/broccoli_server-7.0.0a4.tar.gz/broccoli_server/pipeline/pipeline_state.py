import dataclasses
from typing import Dict


@dataclasses.dataclass
class PipelineState:
    name: str
    migrate_q: Dict
