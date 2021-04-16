import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import dataclass_json
from smart_open import open

from .api import IngestionApi, IngestionApiConfig
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

    kinesis: Optional[KinesisConfig]
    api: Optional[IngestionApiConfig]

    @classmethod
    def from_json_file(cls, path: str) -> "RunConfig":
        with open(path, encoding="utf8") as fin:
            # Ignored due to https://github.com/lidatong/dataclasses-json/issues/23
            return cls.from_json(fin.read())  # type: ignore


class BaseExtractor(ABC):
    """Base class for metadata extractors"""

    def run(self, config: RunConfig) -> None:
        """Callable function to extract metadata and send/post messages"""
        logger.info("Starting extractor {}".format(self.__class__.__name__))

        events: List[MetadataChangeEvent] = asyncio.run(self.extract(config))

        logger.info("Fetched {} entities".format(len(events)))

        if config.kinesis is not None:
            Kinesis(config.kinesis).send_messages(events)

        if config.api is not None:
            IngestionApi(config.api).send_messages(events)

        logger.info("Execution finished")

    @abstractmethod
    async def extract(self, config: RunConfig) -> List[MetadataChangeEvent]:
        """Extract metadata and build messages, should be overridden"""
