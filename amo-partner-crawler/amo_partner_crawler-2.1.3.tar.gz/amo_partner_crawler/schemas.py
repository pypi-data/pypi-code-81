import re
import time
import datedelta
from datetime import datetime, timedelta

from pydantic import BaseModel, validator


class BillingSchema(BaseModel):
    price: int = 0
    users_count: int = 0
    tariff: str = 'Неопределен'
    pay_period_in_months: int = 12
    pay_period: int = int(time.time())
    is_paid: bool = False
    is_unrecognized: bool = False

    @validator('price', pre=True)
    def _price_validator(cls, value):
        value = int(value)
        if value != 0:
            value *= 2
        return value

    @validator('users_count', pre=True)
    def _users_count_validator(cls, value):
        return int(value)

    @validator('pay_period', pre=True)
    def _pay_period_validator(cls, value, values):
        match = re.search(r'(\d{2}.\d{2}.\d{4})', value).group(1)
        parsed = datetime.strptime(match, "%d.%m.%Y")
        pay_period_in_months = values.get('pay_period_in_months')
        sub_thirteen_months = parsed - datedelta.datedelta(months=pay_period_in_months+1) - timedelta(days=1)
        correct_pay_period = time.mktime(sub_thirteen_months.timetuple())
        return correct_pay_period
