
from dataclasses import dataclass, InitVar
from datetime import datetime
import re
import time


@dataclass
class AccountLineDetails:
    hash: str

    @classmethod
    def from_dict(cls, **kwargs):
        args = {k: kwargs.get(k) for k in cls.__annotations__.keys()}
        return cls(**args)


@dataclass
class AccountDetails:
    return_code: int
    return_text: str
    return_data: str

    def __post_init__(self):
        self._confirmed_lines = \
            [
                AccountLineDetails.from_dict(**i)
                for i in self.return_data['confirmedLines']
            ]

    @classmethod
    def from_dict(cls, **kwargs):
        args = {k: kwargs.get(k) for k in cls.__annotations__.keys()}
        return cls(**args)

    @property
    def confirmed_lines(self):
        return self._confirmed_lines


def string2date(redPocketDateString):
    return datetime.strptime(redPocketDateString, '%m/%d/%Y').date()


@dataclass
class LineDetails:
    return_code: InitVar[int]
    return_text: InitVar[str]
    return_data: InitVar[str]
    title: InitVar[str]
    phone_number: str = '0000000000'
    voice_balance: int = 0
    messaging_balance: int = 0
    data_balance: int = 0
    timestamp: int = 0
    start_date: datetime.date = None
    end_date: datetime.date = None
    hash: str = ''

    def __post_init__(self, return_code, return_text, return_data, title):
        self.timestamp = time.time()
        self.phone_number = return_data['mdn']

        self.voice_balance = self._cleanse_data(return_data['voice_balance'])
        self.messaging_balance = \
            self._cleanse_data(return_data['messaging_balance'])
        self.data_balance = self._cleanse_data(return_data['data_balance'])

        self.start_date = string2date(return_data['recurring']['last_date'])
        self.end_date = string2date(return_data['aed'])

        mat = re.findall(r'id (\w+)', title)
        try:
            self.hash = mat[0]
        except IndexError:
            raise Warning(f"Unable to parse 'hash' from title ('{title}')")

    @classmethod
    def from_dict(cls, **kwargs):
        args = {k: kwargs.get(k) for k in cls.__annotations__.keys()}
        return cls(**args)

    def _cleanse_data(self, value):
        if value in ['Unlimited', 'N/A']:
            return -1
        else:
            return int(value.replace(',', ''))

    @property
    def days_remaining(self):
        return (self.end_date - datetime.now().date()).days
