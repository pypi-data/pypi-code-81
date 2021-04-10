import datetime
import json
import os
import re
import requests
from .. import config
from .. exceptions import InvalidVideoIdException


PATTERN_VID = re.compile(r"((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)")
PATTERN_DIR = re.compile(r"(.*)\(([0-9]+)\)$")

YT_VIDEO_ID_LENGTH = 11



def extract(url):
    _session = requests.Session()
    html = _session.get(url, headers=config.headers)
    with open(str(datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                  ) + 'test.json', mode='w', encoding='utf-8') as f:
        json.dump(html.json(), f, ensure_ascii=False)


def save(data, filename, extention):
    with open(filename + "_" + (datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')) + extention,
              mode='w', encoding='utf-8') as f:
        f.writelines(data)


def checkpath(filepath):
    splitter = os.path.splitext(os.path.basename(filepath))
    body = splitter[0]
    extention = splitter[1]
    newpath = filepath
    counter = 1
    while os.path.exists(newpath):
        match = re.search(PATTERN_DIR, body)
        if match:
            counter = int(match[2]) + 1
            num_with_bracket = f'({str(counter)})'
            body = f'{match[1]}{num_with_bracket}'
        else:
            body = f'{body}({str(counter)})'
        newpath = os.path.join(os.path.dirname(filepath), body + extention)
    return newpath



def extract_video_id(url_or_id: str) -> str:
    ret = ''
    if type(url_or_id) != str:
        raise TypeError(f"{url_or_id}: URL or VideoID must be str, but {type(url_or_id)} is passed.")
    if len(url_or_id) == YT_VIDEO_ID_LENGTH:
        return url_or_id
    match = re.search(PATTERN_VID, url_or_id)
    if match is None:
        raise InvalidVideoIdException(url_or_id)
    try:
        ret = match.group(4)
    except IndexError:
        raise InvalidVideoIdException(url_or_id)

    if ret is None or len(ret) != YT_VIDEO_ID_LENGTH:
        raise InvalidVideoIdException(url_or_id)
    # print(ret)
    return ret
