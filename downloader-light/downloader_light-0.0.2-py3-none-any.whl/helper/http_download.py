from requests import session as RequestSession
from requests.exceptions import RequestException
from io import BytesIO
import tempfile
import os


def download(url, local_path=None):
    filename = os.path.basename(url)
    local_file_path = os.path.join(tempfile.gettempdir(), filename)
    if local_path is not None and os.path.isdir(local_path):
        local_file_path = os.path.join(local_path, filename)

    session = RequestSession()
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3' }
    request = session.get(url, headers=headers)

    if not request.ok:
        return False

    with open(local_file_path, 'wb') as fh:
        fh.write(request.content)

    return local_file_path


def retrieve(url):
    session = RequestSession()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    request = session.get(url, headers=headers)

    if not request.ok:
        return False

    res = BytesIO()
    res.write(request.content)

    return res
