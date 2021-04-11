import dataclasses
from typing import List, Optional, Dict
from broccoli_server.mod_view import NamedModViewColumn


@dataclasses.dataclass
class PipelineModViewToState:
    name: str
    to_state: str
    update_set_doc: Optional[Dict] = None


@dataclasses.dataclass
class PipelineModView:
    name: str
    from_state: str
    to_states: List[PipelineModViewToState]
    projections: List[NamedModViewColumn]
    filter_q_key: str
    limit: Optional[int] = None
    sort: Optional[Dict] = None

    def to_state_names(self) -> List[str]:
        return list(set(map(lambda s: s.to_state, self.to_states)))
