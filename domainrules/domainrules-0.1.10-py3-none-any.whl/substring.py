from typing import List, Type

from .baserule import BaseRule
from . import Rule


class Fields(BaseRule):
    subwords: List[str]


class SubstringRule(Rule):
    """Правило"""

    fields: Type[BaseRule] = Fields

    @property
    def calc_weight(self):
        return (
            self.bal
            if self.subwords is not None
            and any([word in self.domain.name for word in self.subwords])
            else 0
        )
