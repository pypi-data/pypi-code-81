import asyncio
import logging
from typing import Any, List

from metaphor.common.kinesis import Kinesis
from metaphor.common.metadata_change_event import MetadataChangeEvent

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RunConfig:
    """Base class for runtime parameters"""

    @staticmethod
    def parameters() -> List[str]:
        return []

    @staticmethod
    def build(obj: Any) -> "RunConfig":
        return RunConfig()


class BaseExtractor:
    """Base class for metadata extractors"""

    def run(self, config: RunConfig) -> None:
        """Callable function to extract metadata and send messages, should be overridden"""
        logger.info("Starting extractor {}".format(self.__class__.__name__))

        events: List[MetadataChangeEvent] = asyncio.run(self.extract(config))

        logger.info("Fetched {} entities".format(len(events)))
        Kinesis.send_messages(events)
        logger.info("Execution finished")

    async def extract(self, config: RunConfig) -> List[MetadataChangeEvent]:
        """Extract metadata and build messages, should be overridden"""
