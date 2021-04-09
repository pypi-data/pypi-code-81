"""
Numbers добавляет балы если вместе с ключевым словом используютса номера
amazon0055.com,amazon8855.com,paypal-ticketid567759.com,paypal ,
paypal-ticketid489572.com,
paypal-ticketid98412.com  и тд

Пример Numbers amazon 5;
"""
import re
from typing import Type

from pydantic import validator, BaseModel

from .validators import gt0
from .baserule import BaseRule
from . import Rule


class Fields(BaseRule):
    keyword: str
    min_numbers_qty: int
    max_numbers_qty: int

    _gt0_min_numbers_qty = validator("min_numbers_qty", allow_reuse=True)(gt0)
    _gt0_max_numbers_qty = validator("max_numbers_qty", allow_reuse=True)(gt0)


class NumbersRule(Rule):
    fields: Type[BaseModel] = Fields

    def set_rules(self, **kwargs):
        super().set_rules(**kwargs)
        self.reg = re.compile(
            "[0-9]{%d, %d}" % (self.min_numbers_qty, self.max_numbers_qty)
        )
        return self

    @property
    def calc_weight(self):
        return (
            self.bal
            if self.domain.name.find(self.keyword) >= 0
            and re.match(self.reg, self.domain.name)
            else 0
        )
