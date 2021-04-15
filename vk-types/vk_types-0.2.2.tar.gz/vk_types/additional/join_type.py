from enum import Enum


class JoinType(str, Enum):
    join = "join"
    unsure = "unsure"
    accepted = "accepted"
    approved = "approved"
    request = "request"
