from typing import Type

from Levenshtein._levenshtein import distance
from pydantic import validator

from .validators import gt0
from .baserule import BaseRule
from . import Rule


class Fields(BaseRule):
    possible: int
    base_name: str
    _gt0_possible = validator("possible", allow_reuse=True)(gt0)


class LevensteinRule(Rule):
    fields: Type[BaseRule] = Fields

    @property
    def calc_weight(self):
        domain_name = self.domain.name.replace(".", "").replace("-", "")
        base_name = self.base_name.replace(".", "").replace("-", "")
        if distance(domain_name, base_name) < self.possible:
            return self.bal
        return 0
