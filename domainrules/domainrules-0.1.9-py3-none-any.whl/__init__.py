"""Let's describe alowed rules!"""
VERSION = "0.1.9"
__version__ = VERSION

from typing import Type

from pydantic import BaseModel
from .baserule import NullRuleFields


class Domain:
    name: str = ""

    def __init__(self, name: str):
        self.name = name

    @property
    def weight(self):
        return 0

    def __repr__(self):
        return f"<Domain> {self.name}"


class Rule(Domain):
    fields: Type[BaseModel] = NullRuleFields
    _rules_set = False

    def __init__(self, domain: Domain):
        self.domain = domain

    def __repr__(self):
        if self._rules_set:
            values = [
                f + ":" + str(getattr(self, f))
                for f in self.fields.schema()["properties"]
            ]
            values_str = "\t".join(values)
            return f"<{self.__class__.__name__}> {values_str} {self.domain}"
        return f"<{self.__class__.__name__}> for {self.domain}"

    @property
    def name(self):
        return self.domain.name

    @classmethod
    def validate(cls, **kwargs):
        return cls.fields.validate(kwargs)

    def set_rules(self, **kwargs):
        for k in self.validate(**kwargs).dict():
            setattr(self, k, kwargs[k])
        self._rules_set = True
        return self

    @property
    def calc_weight(self):
        # Зная домен и правила можно рассчитать добавляемый штрафной вес
        return self.bal

    @property
    def weight(self):
        return self.domain.weight + self.calc_weight


__all__ = [
    "Domain",
    "Rule",
]
