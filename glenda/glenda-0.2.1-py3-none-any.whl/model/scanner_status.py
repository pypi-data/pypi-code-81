from enum import Enum


class ScannerStatus(Enum):
    WAITING = 1
    PROGRESS = 2
    DONE = 3
    SKIPPED = 4
    ERROR = 5
