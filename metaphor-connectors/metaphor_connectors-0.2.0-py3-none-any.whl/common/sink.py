import json
import logging
from abc import ABC, abstractmethod
from typing import List

from .event_util import EventUtil
from .metadata_change_event import MetadataChangeEvent

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Sink(ABC):
    """Base class for metadata sinks"""

    def send_messages(self, events: List[MetadataChangeEvent]) -> None:
        """Send MCE messages to ingestion pipeline"""
        records = [EventUtil.trim_event(e) for e in events]
        valid_records = [r for r in records if EventUtil.validate_message(r)]
        logger.debug(f"Records: {json.dumps(valid_records)}")
        if valid_records:
            self._sink(valid_records)

    @abstractmethod
    async def _sink(self, messages: List[dict]) -> None:
        """Sink metadata records to ingestion pipeline, should be overridden"""
