import lru
import requests
import hashlib

from web3.utils.caching import (
    generate_cache_key,
)


def _remove_session(key, session):
    session.close()


_session_cache = lru.LRU(8, callback=_remove_session)


def _get_session(*args, **kwargs):
    cache_key = generate_cache_key((args, kwargs))
    if cache_key not in _session_cache:
        _session_cache[cache_key] = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        _session_cache[cache_key].mount('http://', adapter)

    return _session_cache[cache_key]


def make_post_request(endpoint_uri, json_payload, *args, **kwargs):
    kwargs.setdefault('timeout', 10)
    session = _get_session(endpoint_uri)
    response = session.post(endpoint_uri, json=json_payload, *args, **kwargs)
    response.raise_for_status()

    return response.content
