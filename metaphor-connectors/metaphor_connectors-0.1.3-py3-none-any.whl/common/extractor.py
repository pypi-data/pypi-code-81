import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json
from smart_open import open

from .kinesis import Kinesis, KinesisConfig
from .metadata_change_event import MetadataChangeEvent

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass_json
@dataclass
class RunConfig:
    """Base class for runtime parameters

    All subclasses should add the @dataclass_json & @dataclass decorators
    """

    kinesis: KinesisConfig = field(default=KinesisConfig(), init=False)

    @classmethod
    def from_json_file(cls, path: str) -> "RunConfig":
        with open(path, encoding="utf8") as fin:
            # Ignored due to https://github.com/lidatong/dataclasses-json/issues/23
            return cls.from_json(fin.read())  # type: ignore


class BaseExtractor(ABC):
    """Base class for metadata extractors"""

    def run(self, config: RunConfig) -> None:
        """Callable function to extract metadata and send messages, should be overridden"""
        logger.info("Starting extractor {}".format(self.__class__.__name__))

        events: List[MetadataChangeEvent] = asyncio.run(self.extract(config))

        logger.info("Fetched {} entities".format(len(events)))
        Kinesis(config.kinesis).send_messages(events)
        logger.info("Execution finished")

    @abstractmethod
    async def extract(self, config: RunConfig) -> List[MetadataChangeEvent]:
        """Extract metadata and build messages, should be overridden"""
