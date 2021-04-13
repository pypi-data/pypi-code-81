"""
6.GreenDomain  удаляет все записи с субдоменами от указаного в парметрах
домена второго уровня. тоесть Greendomain amazon.com удалит server2.amazon.com
 и любые другие субдомены из списка до начала проверки на синтаксис.
"""
from typing import Type

from pydantic import BaseModel

from .baserule import BaseRule
from . import Rule


class Fields(BaseRule):
    domain_name: str


class GreenDomainRule(Rule):
    fields: Type[BaseModel] = Fields

    @property
    def calc_weight(self):
        if self.domain.name.endswith(self.domain_name):
            return -1 * self.bal
        return 0
