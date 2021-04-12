import os
import tempfile
from typing import TYPE_CHECKING

import google.cloud.storage

from forecastflow import DataSource
from forecastflow.api import v3
from forecastflow.enums import FileType
from forecastflow.firebase_api import storage
from forecastflow.firebase_api.storage import upload_files_to_data_source

if TYPE_CHECKING:
    from typing import IO, Iterator, List, Optional, Union

    import forecastflow


__all__ = ['import_data_source', 'export_prediction']


__filetype_to_suffix = {
    FileType.CSV: '.csv',
    FileType.TSV: '.tsv',
    FileType.PARQUET: '.parquet',
}


def __generate_fileobjs_from_uris(
    uris: 'List[str]',
    client: 'google.cloud.storage.Client',
) -> 'Iterator[IO]':
    for uri in uris:
        with tempfile.TemporaryFile() as f:
            client.download_blob_to_file(uri, f)
            f.flush()
            os.fsync(f.fileno())
            f.seek(0)
            yield f


def import_data_source(
    uri: 'Union[str, List[str]]',
    project: 'forecastflow.Project',
    name: 'str',
    label: 'forecastflow.DataSourceLabel',
    filetype: 'forecastflow.FileType',
    description: 'Optional[str]' = None,
    skip_profile: bool = True,
    client: 'Optional[google.cloud.storage.Client]' = None,
) -> 'forecastflow.DataSource':
    """
    Import data-source from given Cloud Storage URIs.

    Args:
        uri:
            Cloud Storage URIs.
            e.g.) gs://bucket-name/foo/bar.parquet

        project:
            ForecastFlow Project object.

        name:
            Name of data source.

        label:
            Label of data.

        filetype:
            Data file format.

        description:
            Description of data source.

        skip_profile:
            If True, skip profiling.

        client:
            Cloud Storage client to access URI. \
            If not passed, use default credential.

    Returns:
        New data source imported.
    """
    _client = client or google.cloud.storage.Client()
    uris = [uri] if isinstance(uri, str) else uri
    if len(uris) > 999:
        raise ValueError('Too many files to create datasource.')
    did = v3.create_data_source(
        id_token=project.user.id_token,
        pid=project.pid,
        name=name,
        label=label,
        filetype=filetype,
        description=description,
    )
    upload_files_to_data_source(
        files=__generate_fileobjs_from_uris(uris, _client),
        filetype=filetype,
        id_token=project.user.id_token,
        uid=project.user.uid,
        did=did,
    )
    data_source = DataSource(project=project, data_source_id=did)
    if not skip_profile:
        data_source.profile()
    project._data_sources[did] = data_source
    return data_source


def export_prediction(
    prediction: 'forecastflow.Prediction',
    uri_prefix: str,
    client: 'Optional[google.cloud.storage.Client]' = None,
):
    """
    Export prediction to given Cloud Storage URI.

    Args:
        prediction:
            ForecastFlow Prediction object.

        uri_prefix:
            Prefix of Cloud Storage URIs. If uri_prefix is \
            "gs://bucket-name/foo/", upload parquet filetype prediction to \
            "gs://bucket-name/foo/000000000000.parquet", \
            "gs://bucket-name/foo/000000000001.parquet", ...

        client:
            Cloud Storage client to export prediction. \
            If not passed, use default credential.
    """
    prediction.wait_until_done()
    _client = client or google.cloud.storage.Client()
    src_uris = v3.get_predict(
        id_token=prediction.user.id_token,
        uid=prediction.user.uid,
        pid=prediction.project.pid,
        rid=prediction.rid,
    )
    dest_uris = []
    for i, src_uri in enumerate(src_uris):
        with tempfile.TemporaryFile() as f:
            storage.download(path=src_uri, file=f, id_token=prediction.user.id_token)
            f.flush()
            os.fsync(f.fileno())
            f.seek(0)
            dest_uri = f'{uri_prefix}{i:012}{__filetype_to_suffix[prediction.filetype]}'
            dest_uris.append(dest_uri)
            (
                google.cloud.storage.Blob.from_string(
                    dest_uri,
                    client=_client,
                ).upload_from_file(file_obj=f, content_type=prediction.filetype.value)
            )
    return dest_uris


def __dir__() -> 'List[str]':
    return __all__
