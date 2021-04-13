from pydantic import BaseModel, validator

from .validators import gt0


class BaseRule(BaseModel):
    bal: int = 0
    _gt0_bal = validator("bal", allow_reuse=True)(gt0)


class NullRuleFields(BaseModel):
    bal: int = 0
