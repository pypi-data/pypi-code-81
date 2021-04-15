from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from future import standard_library
standard_library.install_aliases()
import io
import os
import random
import string
import uuid

import pytest
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.storage import Storage

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session

# TODO: use hypothesis
RANDOM_BINARY = os.urandom(2045)

# Updated statement to make it compatible with python2
rand_str_list = [random.choice(string.ascii_letters) for r in range(0, 1054)]
RANDOM_STRING = ''.join(rand_str_list)


#@pytest.mark.asyncio
@pytest.mark.parametrize('uploaded_data,expected_data', [
    (io.BytesIO(RANDOM_BINARY), RANDOM_BINARY),
    (io.StringIO(RANDOM_STRING), RANDOM_STRING.encode('utf-8')),
])
def test_download_stream(bucket_name, creds, uploaded_data,
                               expected_data):
    object_name = '{}/{}'.format((uuid.uuid4().hex), (uuid.uuid4().hex))

    with Session() as session:
        storage = Storage(service_file=creds, session=session)
        res = storage.upload(bucket_name, object_name, uploaded_data)

        with io.BytesIO(b'') as downloaded_data:
            download_stream = storage.download_stream(
                bucket_name, res['name'])
            while True:
                chunk = download_stream.read(4096)
                if not chunk:
                    break
                downloaded_data.write(chunk)

            assert expected_data == downloaded_data.getvalue()

        storage.delete(bucket_name, res['name'])
