import pandas as pd


def test_response(response):
    assert response


def test_success_response_is_success(response):
    success = response.is_success
    assert success
    assert isinstance(success, bool)


def test_not_success_response_is_success(response):
    success = response.is_success
    assert not success
    assert isinstance(success, bool)


def test_success_response_data(response):
    data = response.data
    assert data
    assert isinstance(data.raw, dict)
    assert isinstance(data.df, pd.DataFrame)
    assert not data.df.empty


def test_success_response_data_empty(response):
    data = response.data
    assert data
    assert isinstance(data.raw, dict)
    assert isinstance(data.df, pd.DataFrame)
    assert data.df.empty


def test_not_success_response_data(response):
    data = response.data
    assert data
    assert data.raw
    assert data.df is None or data.df.empty


def test_success_response_status(response):
    status = response.status
    assert status
    assert isinstance(status, dict)
    assert status['http_status_code'] == 200
    assert status['http_reason'] == 'OK'
    has_content = status.get('content', False)
    assert not has_content or 'error' not in status['content']


def test_not_success_response_status(response):
    status = response.status
    assert status
    assert isinstance(status, dict)
    has_content = status.get('content', False)
    assert has_content
    assert 'error' in status['content']


def test_response_headers(response):
    headers = response.headers
    assert headers


def test_response_request_message(response):
    request_message = response.request_message
    assert request_message


def test_response_closure(response):
    closure = response.closure
    assert closure is None


def success_response_tests(response):
    test_response(response)
    test_response_closure(response)
    test_response_request_message(response)
    test_response_headers(response)
    test_success_response_status(response)
    test_success_response_data(response)
    test_success_response_is_success(response)


def success_response_without_data_tests(response):
    test_response(response)
    test_response_closure(response)
    test_response_request_message(response)
    test_response_headers(response)
    test_success_response_status(response)
    test_success_response_data_empty(response)
    test_success_response_is_success(response)


def not_success_response_tests(response, check_status=True):
    test_response(response)
    test_response_closure(response)
    test_response_request_message(response)
    test_response_headers(response)
    check_status and test_not_success_response_status(response)
    test_not_success_response_data(response)
    test_not_success_response_is_success(response)
