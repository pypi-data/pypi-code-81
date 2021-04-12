import logging
from typing import IO, Iterable, Union
from urllib.parse import quote

import requests

from .. import config
from ..enums import FileType
from .exceptions import APIFailed, NotFound, PermissionDenied

_api_base_url = "https://firebasestorage.googleapis.com/v0/b/"
logger = logging.getLogger(__name__)


def download(path: str, file: IO, id_token: str):
    """
    Download object at <path> on Firebase Storage and write it to <file>.

    Args:
        path:
            Path on Firebase Storage

        file:
            IO object

        id_token:
            Firebase Auth ID token

    Raises:
        PermissionDenied:

        NotFound:

        APIFailed:
            Other Firebase API error
    """
    url = get_url(path)
    res = requests.get(
        url, stream=True, headers={'Authorization': f"Bearer {id_token}"}
    )

    if res.status_code != 200:
        if res.status_code == 403:
            raise PermissionDenied(res.text)
        elif res.status_code == 404:
            raise NotFound(res.text)
        else:
            raise APIFailed(res.text)

    file.write(res.content)


def get_url(path):
    if path.startswith('gs://'):
        bucket_name = path.split('/')[2]
        path = path.replace(f'gs://{bucket_name}', '')
    else:
        bucket_name = config.firebase['storageBucket']
    if path.startswith('/'):
        path = path[1:]
    api_url = _api_base_url + bucket_name
    return "{0}/o/{1}?alt=media".format(api_url, quote(path, safe=''))


def upload(file: Union[IO, str], path: str, filetype: 'FileType', id_token: str):
    """
    Upload <file> to <path> on Firebase Storage

    Args:
        file:
            IO object or path to file

        path:
            Path on Firebase Storage

        id_token:
            Firebase Auth ID token

    Raises:
        PermissionDenied:

        APIFailed:
            Other Firebase API error
    """
    file_object: IO
    if path.startswith('/'):
        path = path[1:]
    if isinstance(file, str):
        file_object = open(file, 'rb')
    else:
        file_object = file
    request_ref = (
        _api_base_url + config.firebase['storageBucket'] + "/o?name={0}".format(path)
    )
    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": filetype.value,
    }
    res = requests.post(request_ref, headers=headers, data=file_object)
    if res.status_code != 200:
        if res.status_code == 403:
            raise PermissionDenied(res.text)
        else:
            raise APIFailed(res.text)
    return res.json()


def upload_files_to_data_source(
    files: Union[Iterable[IO], Iterable[str]],
    filetype: 'FileType',
    id_token: str,
    uid: str,
    did: str,
):
    """
    Upload files to data source

    Args:
        file:
            IO object or path to file

        filetype:
            filetype of data

        id_token:
            Firebase Auth ID token

        uid:
            User id

        did:
            Data-source id

    Raises:
        PermissionDenied:

        APIFailed:
            Other Firebase API error
    """
    for i, file in enumerate(files):
        upload(
            file=file,
            path=f"{uid}/rawData/{did}/{i:012}",
            filetype=filetype,
            id_token=id_token,
        )
    logger.info('Successfully uploaded the data')
