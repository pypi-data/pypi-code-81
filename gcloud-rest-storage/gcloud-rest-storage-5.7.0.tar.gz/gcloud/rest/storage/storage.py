from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import next
from builtins import str
from builtins import object
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
import binascii
import enum
import io
import json
import logging
import mimetypes
import os
import sys
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import IO
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from six.moves.urllib.parse import quote

from gcloud.rest.auth import SyncSession  # pylint: disable=no-name-in-module
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.auth import Token  # pylint: disable=no-name-in-module
from gcloud.rest.storage.bucket import Bucket

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from time import sleep
    from requests import HTTPError as ResponseError
    from requests import Session
    from builtins import open as file_open
else:
    from aiofiles import open as file_open  # type: ignore[no-redef]
    from asyncio import sleep  # type: ignore[misc]
    from aiohttp import ClientResponseError as ResponseError  # type: ignore[no-redef]  # pylint: disable=line-too-long
    from aiohttp import ClientSession as Session  # type: ignore[no-redef]

API_ROOT = 'https://www.googleapis.com/storage/v1/b'
API_ROOT_UPLOAD = 'https://www.googleapis.com/upload/storage/v1/b'
VERIFY_SSL = True
SCOPES = [
    'https://www.googleapis.com/auth/devstorage.read_write',
]

MAX_CONTENT_LENGTH_SIMPLE_UPLOAD = 5 * 1024 * 1024  # 5 MB

STORAGE_EMULATOR_HOST = os.environ.get('STORAGE_EMULATOR_HOST')
if STORAGE_EMULATOR_HOST:
    API_ROOT = 'https://{}/storage/v1/b'.format((STORAGE_EMULATOR_HOST))
    API_ROOT_UPLOAD = 'https://{}/upload/storage/v1/b'.format((STORAGE_EMULATOR_HOST))
    VERIFY_SSL = False

log = logging.getLogger(__name__)


def choose_boundary()       :
    """Stolen from six.moves.urllib3.filepost.choose_boundary() as of v1.26.2."""
    boundary = binascii.hexlify(os.urandom(16))
    if sys.version_info.major == 2:
        return boundary  # type: ignore[return-value]
    return boundary.decode('ascii')


def encode_multipart_formdata(fields                                    ,
                              boundary     )                     :
    """
    Stolen from six.moves.urllib3.filepost.encode_multipart_formdata() as of v1.26.2.

    Very heavily modified to be compatible with our gcloud-rest converter and
    to avboid unnecessary six.moves.urllib3 dependencies (since that's only included with
    requests, not aiohttp).
    """
    body              = []
    for headers, data in fields:
        body.append('--{}\r\n'.format((boundary)).encode('utf-8'))

        # The below is from RequestFields.render_headers()
        # Since we only use Content-Type, we could simplify the below to a
        # single line... but probably best to be safe for future modifications.
        for field in ['Content-Disposition', 'Content-Type',
                      'Content-Location']:
            value = headers.pop(field, None)
            if value:
                body.append('{}: {}\r\n'.format((field), (value)).encode('utf-8'))
        for field, value in headers.items():
            # N.B. potential bug copied from six.moves.urllib3 code; zero values should
            # be sent! Keeping it for now, since Google libs use six.moves.urllib3 for
            # their examples.
            if value:
                body.append('{}: {}\r\n'.format((field), (value)).encode('utf-8'))

        body.append(b'\r\n')
        body.append(data)
        body.append(b'\r\n')

    body.append('--{}--\r\n'.format((boundary)).encode('utf-8'))

    # N.B. 'multipart/form-data' in upstream, but Google wants 'related'
    content_type = 'multipart/related; boundary={}'.format((boundary))

    return b''.join(body), content_type


class UploadType(enum.Enum):
    SIMPLE = 1
    RESUMABLE = 2
    MULTIPART = 3  # unused: SIMPLE upgrades to MULTIPART when metadata exists


class StreamResponse(object):
    """This class provides an abstraction between the slightly different
    recommended streaming implementations between requests and aiohttp.
    """
    def __init__(self, response     )        :
        self._response = response
        self._iter                            = None

    def read(self, size      = -1)         :
        #chunk: bytes
        if BUILD_GCLOUD_REST:
            if self._iter is None:
                self._iter = self._response.iter_content(chunk_size=size)
            chunk = next(self._iter, b'')
        else:
            chunk = self._response.content.read(size)
        return chunk


class Storage(object):
    def __init__(self, **_3to2kwargs)        :
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'token' in _3to2kwargs: token = _3to2kwargs['token']; del _3to2kwargs['token']
        else: token =  None
        if 'service_file' in _3to2kwargs: service_file = _3to2kwargs['service_file']; del _3to2kwargs['service_file']
        else: service_file =  None
        self.session = SyncSession(session, verify_ssl=VERIFY_SSL)
        self.token = token or Token(service_file=service_file, scopes=SCOPES,
                                    session=self.session.session)

    def _headers(self)                  :
        if STORAGE_EMULATOR_HOST:
            return {}

        token = self.token.get()
        return {
            'Authorization': 'Bearer {}'.format((token)),
        }

    def get_bucket(self, bucket_name     )          :
        return Bucket(self, bucket_name)

    def copy(self, bucket     , object_name     ,
                   destination_bucket     , **_3to2kwargs)                  :

        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  10
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        if 'params' in _3to2kwargs: params = _3to2kwargs['params']; del _3to2kwargs['params']
        else: params =  None
        if 'new_name' in _3to2kwargs: new_name = _3to2kwargs['new_name']; del _3to2kwargs['new_name']
        else: new_name =  None
        """
        When files are too large, multiple calls to `rewriteTo` are made. We
        refer to the same copy job by using the `rewriteToken` from the
        previous return payload in subsequent `rewriteTo` calls.

        Using the `rewriteTo` GCS API is preferred in part because it is able
        to make multiple calls to fully copy an object whereas the `copyTo` GCS
        API only calls `rewriteTo` once under the hood, and thus may fail if
        files are large.

        In the rare case you need to resume a copy operation, include the
        `rewriteToken` in the `params` dictionary. Once you begin a multi-part
        copy operation, you then have 1 week to complete the copy job.

        https://cloud.google.com/storage/docs/json_api/v1/objects/rewrite
        """
        if not new_name:
            new_name = object_name

        url = ("{}/{}/o/{}/rewriteTo"
               "/b/{}/o/{}".format((API_ROOT), (bucket), (quote(object_name, safe='')), (destination_bucket), (quote(new_name, safe=''))))

        # We may optionally supply metadata* to apply to the rewritten
        # object, which explains why `rewriteTo` is a POST endpoint; however,
        # we don't expose that here so we have to send an empty body. Therefore
        # the `Content-Length` and `Content-Type` indicate an empty body.
        #
        # * https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        headers = headers or {}
        headers.update(self._headers())
        headers.update({
            'Content-Length': '0',
            'Content-Type': '',
        })

        params = params or {}

        s = SyncSession(session) if session else self.session
        resp = s.post(url, headers=headers, params=params,
                            timeout=timeout)

        data                 = resp.json()

        while not data.get('done') and data.get('rewriteToken'):
            params['rewriteToken'] = data['rewriteToken']
            resp = s.post(url, headers=headers, params=params,
                                timeout=timeout)
            data = resp.json()

        return data

    def delete(self, bucket     , object_name     , **_3to2kwargs)       :
        # https://cloud.google.com/storage/docs/request-endpoints#encoding
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        if 'params' in _3to2kwargs: params = _3to2kwargs['params']; del _3to2kwargs['params']
        else: params =  None
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  10
        encoded_object_name = quote(object_name, safe='')
        url = '{}/{}/o/{}'.format((API_ROOT), (bucket), (encoded_object_name))
        headers = headers or {}
        headers.update(self._headers())

        s = SyncSession(session) if session else self.session
        resp = s.delete(url, headers=headers, params=params or {},
                              timeout=timeout)

        try:
            data      = resp.text()
        except (AttributeError, TypeError):
            data = str(resp.text)

        return data

    def download(self, bucket     , object_name     , **_3to2kwargs)         :
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  10
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        return self._download(bucket, object_name, headers=headers,
                                    timeout=timeout, params={'alt': 'media'},
                                    session=session)

    def download_to_filename(self, bucket     , object_name     ,
                                   filename     , **kwargs     )        :
        with file_open(  # type: ignore[attr-defined]
            filename,
            mode='wb+',
        ) as file_object:
            file_object.write(
                self.download(bucket, object_name, **kwargs)
            )

    def download_metadata(self, bucket     , object_name     , **_3to2kwargs)                  :
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  10
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        data = self._download(bucket, object_name, headers=headers,
                                    timeout=timeout, session=session)
        metadata                 = json.loads(data.decode())
        return metadata

    def download_stream(self, bucket     , object_name     , **_3to2kwargs
                              )                  :
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  10
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        """Download a GCS object in a buffered stream.

        Args:
            bucket (str): The bucket from which to download.
            object_name (str): The object within the bucket to download.
            headers (Optional[Dict[str, Any]], optional): Custom header values
                for the request, such as range. Defaults to None.
            timeout (int, optional): Timeout, in seconds, for the request. Note
                that with this function, this is the time to the beginning of
                the response data (TTFB). Defaults to 10.
            session (Optional[Session], optional): A specific session to
                (re)use. Defaults to None.

        Returns:
            StreamResponse: A object encapsulating the stream, similar to
            io.BufferedIOBase, but it only supports the read() function.
        """
        return self._download_stream(bucket, object_name,
                                           headers=headers, timeout=timeout,
                                           params={'alt': 'media'},
                                           session=session)

    def list_objects(self, bucket     , **_3to2kwargs)                  :
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  10
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        if 'params' in _3to2kwargs: params = _3to2kwargs['params']; del _3to2kwargs['params']
        else: params =  None
        url = '{}/{}/o'.format((API_ROOT), (bucket))
        headers = headers or {}
        headers.update(self._headers())

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, params=params or {},
                           timeout=timeout)
        data                 = resp.json()
        return data

    # https://cloud.google.com/storage/docs/json_api/v1/how-tos/upload
    # pylint: disable=too-many-locals
    def upload(self, bucket     , object_name     , file_data     , **_3to2kwargs)                  :
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  30
        if 'force_resumable_upload' in _3to2kwargs: force_resumable_upload = _3to2kwargs['force_resumable_upload']; del _3to2kwargs['force_resumable_upload']
        else: force_resumable_upload =  None
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'metadata' in _3to2kwargs: metadata = _3to2kwargs['metadata']; del _3to2kwargs['metadata']
        else: metadata =  None
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        if 'parameters' in _3to2kwargs: parameters = _3to2kwargs['parameters']; del _3to2kwargs['parameters']
        else: parameters =  None
        if 'content_type' in _3to2kwargs: content_type = _3to2kwargs['content_type']; del _3to2kwargs['content_type']
        else: content_type =  None
        url = '{}/{}/o'.format((API_ROOT_UPLOAD), (bucket))

        stream = self._preprocess_data(file_data)

        if BUILD_GCLOUD_REST and isinstance(stream, io.StringIO):
            # HACK: `requests` library does not accept `str` as `data` in `put`
            # HTTP request.
            stream = io.BytesIO(stream.getvalue().encode('utf-8'))

        content_length = self._get_stream_len(stream)

        # mime detection method same as in aiohttp 3.4.4
        content_type = content_type or mimetypes.guess_type(object_name)[0]

        parameters = parameters or {}

        headers = headers or {}
        headers.update(self._headers())
        headers.update({
            'Content-Length': str(content_length),
            'Content-Type': content_type or '',
        })

        upload_type = self._decide_upload_type(force_resumable_upload,
                                               content_length)
        log.debug('using %r gcloud storage upload method', upload_type)

        if upload_type == UploadType.RESUMABLE:
            return self._upload_resumable(
                url, object_name, stream, parameters, headers,
                metadata=metadata, session=session, timeout=timeout)
        if upload_type == UploadType.SIMPLE:
            if metadata:
                return self._upload_multipart(
                    url, object_name, stream, parameters, headers, metadata,
                    session=session, timeout=timeout)
            return self._upload_simple(
                url, object_name, stream, parameters, headers, session=session,
                timeout=timeout)

        raise TypeError('upload type {} not supported'.format((upload_type)))

    def upload_from_filename(self, bucket     , object_name     ,
                                   filename     ,
                                   **kwargs     )                  :
        with file_open(  # type: ignore[attr-defined]
            filename,
            mode='rb',
        ) as file_object:
            contents = file_object.read()
            return self.upload(bucket, object_name, contents,
                                     **kwargs)

    @staticmethod
    def _get_stream_len(stream            )       :
        current = stream.tell()
        try:
            return stream.seek(0, os.SEEK_END)
        finally:
            stream.seek(current)

    @staticmethod
    def _preprocess_data(data     )           :
        if data is None:
            return io.StringIO('')

        if isinstance(data, bytes):
            return io.BytesIO(data)
        if isinstance(data, str):
            return io.StringIO(data)
        if isinstance(data, io.IOBase):
            return data  # type: ignore[return-value]

        raise TypeError('unsupported upload type: "{}"'.format((type(data))))

    @staticmethod
    def _decide_upload_type(force_resumable_upload                ,
                            content_length     )              :
        # force resumable
        if force_resumable_upload is True:
            return UploadType.RESUMABLE

        # force simple
        if force_resumable_upload is False:
            return UploadType.SIMPLE

        # decide based on Content-Length
        if content_length > MAX_CONTENT_LENGTH_SIMPLE_UPLOAD:
            return UploadType.RESUMABLE

        return UploadType.SIMPLE

    @staticmethod
    def _split_content_type(content_type     )                             :
        content_type_and_encoding_split = content_type.split(';')
        content_type = content_type_and_encoding_split[0].lower().strip()

        encoding = None
        if len(content_type_and_encoding_split) > 1:
            encoding_str = content_type_and_encoding_split[1].lower().strip()
            encoding = encoding_str.split('=')[-1]

        return content_type, encoding

    @staticmethod
    def _format_metadata_key(key     )       :
        """
        Formats the fixed-key metadata keys as wanted by the multipart API.

        Ex: Content-Disposition --> contentDisposition
        """
        parts = key.split('-')
        parts = [parts[0].lower()] + [p.capitalize() for p in parts[1:]]
        return ''.join(parts)

    def _download(self, bucket     , object_name     , **_3to2kwargs)         :
        # https://cloud.google.com/storage/docs/request-endpoints#encoding
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  10
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        if 'params' in _3to2kwargs: params = _3to2kwargs['params']; del _3to2kwargs['params']
        else: params =  None
        encoded_object_name = quote(object_name, safe='')
        url = '{}/{}/o/{}'.format((API_ROOT), (bucket), (encoded_object_name))
        headers = headers or {}
        headers.update(self._headers())

        s = SyncSession(session) if session else self.session
        response = s.get(url, headers=headers, params=params or {},
                               timeout=timeout)

        # N.B. the GCS API sometimes returns 'application/octet-stream' when a
        # string was uploaded. To avoid potential weirdness, always return a
        # bytes object.
        try:
            data        = response.read()
        except (AttributeError, TypeError):
            data = response.content

        return data

    def _download_stream(self, bucket     , object_name     , **_3to2kwargs
                               )                  :
        # https://cloud.google.com/storage/docs/request-endpoints#encoding
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  10
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        if 'params' in _3to2kwargs: params = _3to2kwargs['params']; del _3to2kwargs['params']
        else: params =  None
        encoded_object_name = quote(object_name, safe='')
        url = '{}/{}/o/{}'.format((API_ROOT), (bucket), (encoded_object_name))
        headers = headers or {}
        headers.update(self._headers())

        s = SyncSession(session) if session else self.session

        if BUILD_GCLOUD_REST:
            # stream argument is only expected by requests.Session.
            # pylint: disable=unexpected-keyword-arg
            return StreamResponse(s.get(url, headers=headers,
                                        params=params or {},
                                        timeout=timeout, stream=True))
        return StreamResponse(s.get(url, headers=headers,
                                          params=params or {},
                                          timeout=timeout))

    def _upload_simple(self, url     , object_name     ,
                             stream            , params                ,
                             headers                , **_3to2kwargs)                  :
        # https://cloud.google.com/storage/docs/json_api/v1/how-tos/simple-upload
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  30
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        params['name'] = object_name
        params['uploadType'] = 'media'

        s = SyncSession(session) if session else self.session
        resp = s.post(url, data=stream, headers=headers, params=params,
                            timeout=timeout)
        data                 = resp.json()
        return data

    def _upload_multipart(self, url     , object_name     ,
                                stream            , params                ,
                                headers                ,
                                metadata                , **_3to2kwargs)                  :
        # https://cloud.google.com/storage/docs/json_api/v1/how-tos/multipart-upload
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  30
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        params['uploadType'] = 'multipart'

        metadata_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        metadata = {self._format_metadata_key(k): v
                    for k, v in metadata.items()}
        metadata['name'] = object_name

        raw_body         = stream.read()
        if isinstance(raw_body, str):
            bytes_body        = raw_body.encode('utf-8')
        else:
            bytes_body = raw_body

        parts = [
            (metadata_headers, json.dumps(metadata).encode('utf-8')),
            ({'Content-Type': headers['Content-Type']}, bytes_body),
        ]
        boundary = choose_boundary()
        body, content_type = encode_multipart_formdata(parts, boundary)
        headers.update({
            'Content-Type': content_type,
            'Content-Length': str(len(body)),
            'Accept': 'application/json'
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(url, data=body, headers=headers, params=params,
                            timeout=timeout)
        data                 = resp.json()
        return data

    def _upload_resumable(self, url     , object_name     ,
                                stream            , params                ,
                                headers                , **_3to2kwargs)                  :
        # https://cloud.google.com/storage/docs/json_api/v1/how-tos/resumable-upload
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  30
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'metadata' in _3to2kwargs: metadata = _3to2kwargs['metadata']; del _3to2kwargs['metadata']
        else: metadata =  None
        session_uri = self._initiate_upload(url, object_name, params,
                                                  headers, metadata=metadata,
                                                  session=session)
        return self._do_upload(session_uri, stream, headers=headers,
                                     session=session, timeout=timeout)

    def _initiate_upload(self, url     , object_name     ,
                               params                , headers                , **_3to2kwargs)       :
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'metadata' in _3to2kwargs: metadata = _3to2kwargs['metadata']; del _3to2kwargs['metadata']
        else: metadata =  None
        params['uploadType'] = 'resumable'

        metadict = (metadata or {}).copy()
        metadict.update({'name': object_name})
        metadata_ = json.dumps(metadict)

        post_headers = headers.copy()
        post_headers.update({
            'Content-Length': str(len(metadata_)),
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Upload-Content-Type': headers['Content-Type'],
            'X-Upload-Content-Length': headers['Content-Length']
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(url, headers=post_headers, params=params,
                            data=metadata_, timeout=10)
        session_uri      = resp.headers['Location']
        return session_uri

    def _do_upload(self, session_uri     , stream            ,
                         headers                , **_3to2kwargs)                  :
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  30
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'retries' in _3to2kwargs: retries = _3to2kwargs['retries']; del _3to2kwargs['retries']
        else: retries =  5
        s = SyncSession(session) if session else self.session

        for tries in range(retries):
            try:
                resp = s.put(session_uri, headers=headers,
                                   data=stream, timeout=timeout)
            except ResponseError:
                headers.update({'Content-Range': '*/*'})
                sleep(2. ** tries)  # type: ignore[func-returns-value]

                continue

            break

        data                 = resp.json()
        return data

    def patch_metadata(
            self, bucket     , object_name     , metadata                , **_3to2kwargs)                  :
        # https://cloud.google.com/storage/docs/json_api/v1/objects/patch
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  10
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        if 'params' in _3to2kwargs: params = _3to2kwargs['params']; del _3to2kwargs['params']
        else: params =  None
        url = '{}/{}/o/{}'.format((API_ROOT), (bucket), (object_name))
        params = params or {}
        headers = headers or {}
        headers.update(self._headers())
        headers['Content-Type'] = 'application/json'

        s = SyncSession(session) if session else self.session
        resp = s.patch(url, data=json.dumps(metadata).encode('utf-8'),
                             headers=headers, params=params, timeout=timeout)
        data                 = resp.json()
        return data

    def get_bucket_metadata(self, bucket     , **_3to2kwargs)                  :
        if 'timeout' in _3to2kwargs: timeout = _3to2kwargs['timeout']; del _3to2kwargs['timeout']
        else: timeout =  10
        if 'session' in _3to2kwargs: session = _3to2kwargs['session']; del _3to2kwargs['session']
        else: session =  None
        if 'headers' in _3to2kwargs: headers = _3to2kwargs['headers']; del _3to2kwargs['headers']
        else: headers =  None
        if 'params' in _3to2kwargs: params = _3to2kwargs['params']; del _3to2kwargs['params']
        else: params =  None
        url = '{}/{}'.format((API_ROOT), (bucket))
        headers = headers or {}
        headers.update(self._headers())

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, params=params or {},
                           timeout=timeout)
        data                 = resp.json()
        return data

    def close(self)        :
        self.session.close()

    def __enter__(self)             :
        return self

    def __exit__(self, *args     )        :
        self.close()
