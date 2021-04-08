import logging
from dataclasses import dataclass

logger = logging.getLogger()


@dataclass
class GlobalConstants:
    loggerName: str = "Franzi"
    dateFormat: str = "%d-%m-%Y"