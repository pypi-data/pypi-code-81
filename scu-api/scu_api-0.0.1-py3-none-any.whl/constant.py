# -*- coding: utf-8 -*-

from enum import Enum, auto

#  Start-> INIT -> OFFLINE -> ONLINE
#                    |    <-     |


class ClientStatus(Enum):
    INIT = auto()      # init state
    OFFLINE = auto()   # set baseinfo and without login
    # after login, MAYBE cache outdate in SCU website, need get_status() to check
    ONLINE = auto()
