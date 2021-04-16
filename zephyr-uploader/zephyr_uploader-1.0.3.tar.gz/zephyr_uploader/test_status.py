from enum import Enum


class TestStatus(Enum):
    NOT_EXECUTED = -1
    PASSED = 1
    FAILED = 2
