import pytest
import requests

from d8s_networking import (
    get,
    head,
    post,
    put,
    delete,
    headers_update,
    urllib3_backoff_factor_executions,
    headers_update,
    url_hash,
    requests_basic_auth,
)
from d8s_networking.networking import _update_header_for_json


def test_requests_basic_auth_1():
    result = requests_basic_auth('foo', 'bar')
    assert isinstance(result, requests.auth.HTTPBasicAuth)


def test_url_hash_1():
    result = url_hash('https://example.com/')
    assert result == 'ea8fac7c65fb589b0d53560f5251f74f9e9b243478dcb6b3ea79b5e36449c8d9'


@pytest.mark.network
def test_head():
    response = head('https://jsonplaceholder.typicode.com/posts/1')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8'

    response = head('https://jsonplaceholder.typicode.com/posts/1', process_response=True)
    assert response == ''


@pytest.mark.network
def test_post_docs_1():
    url = 'https://jsonplaceholder.typicode.com/posts'
    data = {'title': 'foo', 'body': 'bar', 'userId': 1}
    response = post(url, data=data, process_response=True)
    assert response == {'title': 'foo', 'body': 'bar', 'userId': 1, 'id': 101}

    response = post(url, data=data)
    assert response.status_code == 201


@pytest.mark.network
def test_put_docs_1():
    url = 'https://jsonplaceholder.typicode.com/posts/1'
    data = {'id': 1, 'title': 'foo', 'body': 'bar', 'userId': 1}
    response = put(url, data=data, process_response=True)
    assert response == {'id': 1, 'title': 'foo', 'body': 'bar', 'userId': 1}

    response = put(url, data=data)
    assert response.status_code == 200


@pytest.mark.network
def test_get_docs_1():
    response = get('http://hightower.space/projects', process_response=True)
    assert 'Floyd' in response

    response = get('http://hightower.space/projects')
    assert response.status_code == 200

    response = get('http://hightower.space/projects', process_response_as_bytes=True)
    assert isinstance(response, bytes)
    assert response.startswith(b'<!DOCTYPE html>')

    response = get('http://example.com/bar')
    assert response.status_code == 404

    response = get(
        'http://example.com',
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        },
        process_response=True,
    )
    assert response.startswith('<!doctype html>')


@pytest.mark.network
def test_get_odds_and_ends():
    response = get('http://example.com', headers={'Foo': 'Bar'}, process_response=True)
    assert response.startswith('<!doctype html>')


@pytest.mark.network
def test_delete():
    response = delete('https://jsonplaceholder.typicode.com/posts/1', process_response=True)
    assert response == {}

    response = delete('https://jsonplaceholder.typicode.com/posts/1')
    assert response.status_code == 200


def test_urllib3_backoff_factor_executions_1():
    results = tuple(urllib3_backoff_factor_executions(0.1, 10))
    assert len(results) == 10
    assert results[0] == 0.0
    assert results[1] == 0.2
    assert results[2] == 0.4
    assert results[9] == 51.2

    results = tuple(urllib3_backoff_factor_executions(0.5, 3))
    assert len(results) == 3
    assert results[0] == 0.0
    assert results[1] == 1.0
    assert results[2] == 2.0


def test_headers_update_1():
    results = headers_update({'Content-Type': 'foo'}, 'Content-Type', 'bar')
    assert results == {'Content-Type': 'bar'}

    results = headers_update({'Content-Type': 'foo'}, 'Content-Type', 'bar', overwrite=False)
    assert results == {'Content-Type': 'foo'}

    results = headers_update({'a': 'b'}, 'Content-Type', 'foo')
    assert results == {'a': 'b', 'Content-Type': 'foo'}


def test__update_header_for_json_1():
    kwargs = {'a': 'b'}
    results = _update_header_for_json(**kwargs)
    assert results == {'a': 'b', 'headers': {'Content-Type': 'application/json'}}

    kwargs = {'headers': {'a': 'b'}}
    results = _update_header_for_json(**kwargs)
    assert results == {'headers': {'a': 'b', 'Content-Type': 'application/json'}}

    kwargs = {'headers': {'a': 'b', 'Content-Type': 'foo bar'}}
    results = _update_header_for_json(**kwargs)
    assert results == {'headers': {'a': 'b', 'Content-Type': 'foo bar'}}
