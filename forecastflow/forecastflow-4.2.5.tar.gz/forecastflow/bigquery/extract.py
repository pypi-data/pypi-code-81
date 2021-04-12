from typing import Sequence, TYPE_CHECKING, Optional, Union

from google.cloud.bigquery import (
    DEFAULT_RETRY,
    Client,
    Compression,
    DestinationFormat,
    ExtractJobConfig,
)

if TYPE_CHECKING:
    from google.api_core.retry import Retry
    from google.cloud.bigquery import Model, ModelReference, Table, TableReference


def _extract_table(
    source: Union['Table', 'TableReference', 'Model', 'ModelReference', str],
    destination_uris: Union[str, Sequence[str]],
    client: Optional['Client'] = None,
    retry: Optional['Retry'] = None,
    timeout: Optional[float] = None,
):
    """
    Extract data from BigQuery source to Cloud Storage.

    Args:
        source:
            Table or Model to be extracted.
        destination_uris:
            URIs of Cloud Storage.
        client:
            BigQuery client to run extact job.
        retry:
            How to retry the RPC.
        timeout:
            The number of seconds to wait for the underlying HTTP transport
    """
    if client is None:
        client = Client()
    if retry is None:
        retry = DEFAULT_RETRY

    job_config = ExtractJobConfig(
        compression=Compression.SNAPPY, destination_format=DestinationFormat.PARQUET
    )
    extract_job = client.extract_table(
        source=source,
        destination_uris=destination_uris,
        location='asia-northeast1',
        job_config=job_config,
    )
    extract_job.result(retry=retry, timeout=timeout)
