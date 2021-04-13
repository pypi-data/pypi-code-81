import json
import logging
from dataclasses import dataclass
from typing import List, Optional

import boto3
from aws_assume_role_lib import assume_role
from botocore.config import Config
from botocore.exceptions import ClientError
from dataclasses_json import dataclass_json

from metaphor.common.event_util import EventUtil
from metaphor.common.metadata_change_event import MetadataChangeEvent

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass_json
@dataclass
class KinesisConfig:

    stream_name: str = "mce"
    region_name: str = "us-west-2"
    assume_role_arn: Optional[str] = None

    retry_mode: str = "standard"
    retry_max_attempts: int = 3


class Kinesis:
    """Kinesis client functions"""

    # TODO: Replace with proper partition key
    _partition_key = "123"

    def __init__(self, config: KinesisConfig):
        self._stream_name = config.stream_name

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

    def send_messages(self, events: List[MetadataChangeEvent]) -> None:
        """Send MCE message to Kinesis Stream"""
        records = [EventUtil.trim_event(e) for e in events]
        valid_records = [r for r in records if EventUtil.validate_message(r)]
        logger.debug("Records: {}".format(json.dumps(valid_records)))
        if valid_records:
            self._send_records(valid_records)

    def _send_records(self, messages: List) -> None:
        """Send records to Kinesis Stream"""
        records = [
            {
                "Data": json.dumps(msg),
                "PartitionKey": Kinesis._partition_key,
            }
            for msg in messages
        ]

        try:
            response = self._client.put_records(
                StreamName=self._stream_name, Records=records
            )
            logger.info(f"Sent {len(messages)} records. Response {response}")
        except ClientError:
            logger.error("Error putting Kinesis records.")
            raise
        else:
            # TODO: error handling of some records failure within batch
            return response
