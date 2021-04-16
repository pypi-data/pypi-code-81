import json
import logging
from dataclasses import dataclass
from typing import List, Optional

import boto3
from aws_assume_role_lib import assume_role
from botocore.config import Config
from botocore.exceptions import ClientError
from dataclasses_json import dataclass_json

from .sink import Sink

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass_json
@dataclass
class KinesisConfig:
    stream_name: str = "mce"
    region_name: str = "us-west-2"
    assume_role_arn: Optional[str] = None

    batch_size: int = 20
    retry_mode: str = "standard"
    retry_max_attempts: int = 3


class Kinesis(Sink):
    """Kinesis sink functions"""

    # TODO: Replace with proper partition key
    _partition_key = "123"

    def __init__(self, config: KinesisConfig):
        self._stream_name = config.stream_name
        self._batch_size = config.batch_size

        session = boto3.Session()
        if config.assume_role_arn is not None:
            session = assume_role(session, config.assume_role_arn)

        self._client = session.client(
            "kinesis",
            config=Config(
                region_name=config.region_name,
                signature_version="v4",
                retries={
                    "mode": config.retry_mode,
                    "max_attempts": config.retry_max_attempts,
                },
            ),
        )

    def _sink(self, messages: List[dict]) -> None:
        """Send records to Kinesis Stream"""
        records = [
            {
                "Data": json.dumps(msg),
                "PartitionKey": Kinesis._partition_key,
            }
            for msg in messages
        ]

        for chunk in self._chunks(records, self._batch_size):
            try:
                response = self._client.put_records(
                    StreamName=self._stream_name, Records=chunk
                )
            except ClientError as error:
                logger.error(f"Error putting Kinesis records, error: {error}")
                raise
            else:
                # TODO: error handling of some records failure within batch
                logger.info(f"Sent {len(chunk)} records. Response {response}")

    @staticmethod
    def _chunks(records: List, n: int) -> List[List]:
        """Yield successive n-sized chunks from list."""
        for i in range(0, len(records), n):
            yield records[i : i + n]
