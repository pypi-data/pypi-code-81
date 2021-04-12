from typing import Type

from .baserule import BaseRule
from . import Rule


class Fileds(BaseRule):
    min_qty: int


class SubdomainRule(Rule):
    fields: Type[BaseRule] = Fileds

    @property
    def calc_weight(self):
        return self.bal if self.domain.name.count(".") > self.min_qty else 0
