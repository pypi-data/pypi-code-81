from enum import Enum


class Status(Enum):
    pending = 'pending'
    computing = 'computing'
    done = 'done'
    failed = 'failed'
    stopped = 'stopped'
