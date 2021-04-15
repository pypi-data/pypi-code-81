import json
import os
import sys
from typing import Any, Dict

import requests


def requests_basic_auth(user, password):
    """Return an instance of request's basic auth."""
    from requests.auth import HTTPBasicAuth

    return HTTPBasicAuth(user, password)


def _process_response(
    response,
    url,
    *,
    process_response_as_bytes: bool = False,
):
    """Handle the responses from requests."""
    from d8s_json import json_read

    if response.ok:
        if process_response_as_bytes:
            return response.content

        try:
            return json_read(response.text)
        except json.JSONDecodeError:
            return response.text
    else:
        message = f'{response.status_code} error from {response.request.method} {url}: {response.text}'
        print(message)
        return response


def get(
    url,
    *,
    use_common_user_agent: bool = True,
    process_response: bool = False,
    process_response_as_bytes: bool = False,
    **request_kwargs,
):
    """Make a GET request to the given URL."""
    from d8s_user_agents import user_agent_common

    if use_common_user_agent:
        user_agent = user_agent_common()
        if request_kwargs.get('headers'):
            if not request_kwargs['headers'].get('User-Agent'):
                request_kwargs['headers']['User-Agent'] = user_agent
            # if there is already a user agent provided, use that
        else:
            headers = {'User-Agent': user_agent}
            request_kwargs['headers'] = headers

    response = requests.get(url, **request_kwargs)

    if process_response or process_response_as_bytes:
        result = _process_response(
            response,
            url,
            process_response_as_bytes=process_response_as_bytes,
        )
    else:
        result = response

    return result


def head(url, *, process_response: bool = False, **kwargs):
    """Make a head request."""
    response = requests.head(url, **kwargs)

    if process_response:
        return _process_response(response, url)
    else:
        return response


def _data_is_json(data: Any) -> bool:
    """."""
    JSON_DATATYPES = (dict, list)
    if isinstance(data, JSON_DATATYPES):
        return True
    return False


def post(
    url,
    *,
    update_headers_for_datatype: bool = True,
    process_response: bool = False,
    process_response_as_bytes: bool = False,
    **request_kwargs,
):
    """Make a POST request to the given URL with the given data."""
    has_data = request_kwargs.get('data')
    if update_headers_for_datatype and has_data:
        data = request_kwargs['data']
        if _data_is_json(data):
            request_kwargs['data'] = json.dumps(data)
            request_kwargs = _update_header_for_json(**request_kwargs)

    response = requests.post(url, **request_kwargs)

    if process_response or process_response_as_bytes:
        result = _process_response(
            response,
            url,
            process_response_as_bytes=process_response_as_bytes,
        )
    else:
        result = response

    return result


def headers_update(headers: Dict[str, str], new_header_key: str, new_header_value: Any, *, overwrite: bool = True):
    """."""
    if headers.get(new_header_key):
        if overwrite:
            headers[new_header_key] = new_header_value
    else:
        headers[new_header_key] = new_header_value

    return headers


def _update_header_for_json(**kwargs):
    """Given the keyword arguments for a request, check to see if there is already a header, if there is a "Content-Type" header, don't change it; if there is not a "Content-Type" header, add one."""
    if kwargs.get('headers'):
        kwargs['headers'] = headers_update(kwargs['headers'], 'Content-Type', 'application/json', overwrite=False)
    else:
        kwargs['headers'] = {'Content-Type': 'application/json'}

    return kwargs


def put(
    url,
    *,
    update_headers_for_datatype: bool = True,
    process_response: bool = False,
    process_response_as_bytes: bool = False,
    **request_kwargs,
):
    """Make a PUT request to the given URL with the given data."""
    has_data = request_kwargs.get('data')
    if update_headers_for_datatype and has_data:
        data = request_kwargs['data']
        if _data_is_json(data):
            request_kwargs['data'] = json.dumps(data)
            request_kwargs = _update_header_for_json(**request_kwargs)

    response = requests.put(url, **request_kwargs)

    if process_response or process_response_as_bytes:
        result = _process_response(
            response,
            url,
            process_response_as_bytes=process_response_as_bytes,
        )
    else:
        result = response

    return result


def delete(
    url,
    *,
    process_response: bool = False,
    process_response_as_bytes: bool = False,
    **request_kwargs,
):
    """Make a DELETE request to the given URL with the given data."""
    response = requests.delete(url, **request_kwargs)

    if process_response or process_response_as_bytes:
        return _process_response(
            response,
            url,
            process_response_as_bytes=process_response_as_bytes,
        )
    else:
        return response


def url_hash(url, hash_type='sha256'):
    """Return the hash of the url."""
    from d8s_hashes.hashes import _string_hash

    return _string_hash(get(url, process_response=True), hash_type)


def urllib3_backoff_factor_executions(backoff_factor: float, number_of_requests: int):
    """Return the times (in seconds) of the first n requests with the given backoff_factor. See https://urllib3.readthedocs.io/en/latest/reference/index.html#urllib3.Retry under the "backoff_factor" argument."""
    # the end of the range through which we iterate is number_of_requests plus one because we start the iteration at one and we want to have n items in the execution_times array
    range_end = number_of_requests + 1

    if range_end > 1:
        # if the original request (which can be considered the zeroth request) fails, the first re-request is made immediately by urllib3
        yield 0.0

    for i in range(2, range_end):
        yield backoff_factor * (2 ** (i - 1))
