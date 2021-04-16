import json
import os
import sys

import random

from string import ascii_uppercase as letters


def docopt_parse_argv(doc):
    from docopt import docopt

    argv = sys.argv
    args = docopt(doc, argv[1:] if len(argv) > 1 else {})
    return args


def generate_fake_rics(rics, limit):
    count = len(rics)

    if count >= limit:
        return rics

    numbers = [str(i) for i in range(0, 10)]

    d = dict.fromkeys(rics, None)
    while len(d) < limit:
        d[f"{random.sample(letters, 2)}.{random.sample(numbers, 3)}"] = None

    assert len(d) == limit, f"length of rics not equal limit, {len(d)}"

    return list(d.keys())


def load_rics(count=None, path="./rics.txt", is_add_fake_if_not_enough=False):
    with open(path) as f:
        rics = [line.rstrip('\n') for line in f.readlines()]

    if is_add_fake_if_not_enough:
        rics = generate_fake_rics(rics, limit=count or 0)

    return rics if count is None else rics[:count]


class FieldsType(object):
    SMALL = 'small'
    SMALL_1 = 'small_1'
    MEDIUM = 'medium'
    MEDIUM_20 = 'medium_20'
    LARGE = 'large'
    LARGE_100 = 'large_100'
    ALL = 'all'


def load_fields(fields_type, path="./fields.json"):
    """
    [{
        "type": "small",
        "fields": {
            "BID": 155.31,
            "ASK": 155.5,
            ... }
    }, ... ]
    """

    with open(path) as f:
        json_data = json.loads(f.read())

    types = json_data

    for t in types:
        if fields_type == t.get('type'):
            return t.get('fields')

    return None


def create_platform_session(rdp):
    platform_session = rdp.CoreFactory.create_platform_session(
        app_key=os.environ.get('DESKTOP_APP_KEY'),
        oauth_grant_type=rdp.GrantPassword(
            username=os.environ.get('EDP_USERNAME'),
            password=os.environ.get('EDP_PASSWORD')
            )
        )
    return platform_session


def create_desktop_session(rdp, app_key):
    desktop_session = rdp.CoreFactory.create_desktop_session(app_key)
    return desktop_session


def create_session(**kwargs):
    session_type = kwargs.get('session_type')
    rdp = kwargs.get('rdp')
    app_key = kwargs.get('app_key', '')
    deployed_platform_host = kwargs.get('deployed_platform_host', '')
    is_logging = kwargs.get('is_logging', False)

    session = None
    if session_type == 'platform':
        session = create_platform_session(rdp)
    elif session_type == 'desktop':
        session = create_desktop_session(rdp, app_key)

    if not session:
        raise Exception(f'Incorrect session_type: {session_type}')

    if is_logging:
        session.set_log_level(1)

    return session


def write_json_file(filename, d):
    with open(filename, 'w') as f:
        f.write(json.dumps(d))

    import time
    time.sleep(3)
