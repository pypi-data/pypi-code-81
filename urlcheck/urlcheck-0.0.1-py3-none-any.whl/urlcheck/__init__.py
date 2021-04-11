import urllib.request

from urllib.error import URLError


def http_status_code(url):
    x = urllib.request.urlopen(url)
    return x.getcode()


def check(codes, url):
    try:
        code = http_status_code(url)
    except URLError as e:
        print(f'Failed: {e}: {url}')
        return False

    if code not in codes:
        print(f'Failed: HTTP_STATUS_CODE({code}) not in {codes}: {url}')
        return False
    else:
        print(f'Succeed: HTTP_STATUS_CODE({code}) in {codes}: {url}')
        return True
