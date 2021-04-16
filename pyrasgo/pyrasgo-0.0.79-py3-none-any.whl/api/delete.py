from typing import List, Optional

from .connection import Connection
from .error import APIError
from pyrasgo.utils.monitoring import track_usage

class Delete(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def collection(self, id: int):
        raise NotImplementedError('Not avaliable yet.')

    def data_source(self, id: int):
        raise NotImplementedError('Not avaliable yet.')

    def dimension(self, id: int):
        raise NotImplementedError('Not available yet.')

    def feature(self, id: int):
        raise NotImplementedError('Not available yet.')

    def feature_set(self, id: int):
        raise NotImplementedError('Not available yet.')