from jijmodeling.expression.expression import from_serializable
from http import HTTPStatus
from requests.models import Response
import json
import io

# mock for requests.post
def mock_request_post(*args, **kwargs):

    response = Response()
    response.status_code = HTTPStatus.ACCEPTED

    response_dict = {}

    headers = kwargs['headers']

    endpoint = args[0]


    # /instance/upload in InstancePost
    if 'jijcloudpostinstance/instance/upload' in endpoint:
        assert headers['Content-Type'] == 'application/zstd'
        response_dict = {'instance_data_id': 'abcd1234'}

    # /instance in InstancePost
    elif 'jijcloudpostinstance/instance' in endpoint:
        assert headers['Content-Type'] == 'application/json'
        data = json.loads(kwargs['data'])
        assert 'instance_type' in data
        assert 'instance_data_id' in data

        response_dict = {'instance_id': '1234abcd'}

    # /solution in Query
    elif 'jijcloudquery/solution' in endpoint:
        assert headers['Content-Type'] == 'application/json'
        data = json.loads(kwargs['data'])
        assert 'instance_id' in data
        assert 'solver_params' in data
        assert 'solver' in data

        response_dict = {
                'solution_id': 'hogefuga'
                }


    response.raw = io.BytesIO(json.dumps(response_dict).encode())

    return response

# mock for requests.post (BAD REQUEST)
def mock_request_post_query_err_bad_request(response_dict, *args, **kwargs):
    response = Response()
    response.status_code = HTTPStatus.BAD_REQUEST

    headers = kwargs['headers']

    endpoint = args[0]

    if 'jijcloudquery/solution' in endpoint:
        assert headers['Content-Type'] == 'application/json'
        data = json.loads(kwargs['data'])
        assert 'instance_id' in data
        assert 'solver_params' in data
        assert 'solver' in data

        response.raw = io.BytesIO(json.dumps(response_dict).encode())
        return response
    else:
        return mock_request_post(*args, **kwargs)

# mock for requests.post (INTERNAL SERVER ERROR)
def mock_request_post_query_err_internal_server_error(response_dict, *args, **kwargs):
    response = Response()
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    headers = kwargs['headers']

    endpoint = args[0]

    if 'jijcloudquery/solution' in endpoint:
        assert headers['Content-Type'] == 'application/json'
        data = json.loads(kwargs['data'])
        assert 'instance_id' in data
        assert 'solver_params' in data
        assert 'solver' in data

        response.raw = io.BytesIO(json.dumps(response_dict).encode())
        return response
    else:
        return mock_request_post(*args, **kwargs)


# mock for requests.get
def mock_request_get(solution_object, *args, **kwargs):

    # mock for requests.get
    response = Response()
    response.status_code = HTTPStatus.ACCEPTED

    response_dict = {}

    headers = kwargs['headers']
    params = kwargs['params']

    endpoint = args[0]

    # /solution in Query
    if 'jijcloudquery/solution' in endpoint:
        assert 'solution_id' in params
        response_dict = {
                'solution_id': params['solution_id'],
                'status': 'SUCCESS',
                'solution': dict(solution_object)}

    response.raw = io.BytesIO(json.dumps(response_dict).encode())

    return response

# mock for requests.get (invalid id)
def mock_request_get_invalid_id(*args, **kwargs):

    # mock for requests.get
    response = Response()
    response.status_code = HTTPStatus.BAD_REQUEST

    response_dict = {}

    headers = kwargs['headers']
    params = kwargs['params']

    endpoint = args[0]

    # /solution in Query
    if 'jijcloudquery/solution' in endpoint:
        assert 'solution_id' in params
        response_dict = {'detail': 'invalid_id'}

    response.raw = io.BytesIO(json.dumps(response_dict).encode())

    return response

# mock for requests.get (PENDING)
def mock_request_get_pending(*args, **kwargs):

    # mock for requests.get
    response = Response()
    response.status_code = HTTPStatus.ACCEPTED

    response_dict = {}

    headers = kwargs['headers']
    params = kwargs['params']

    endpoint = args[0]

    # /solution in Query
    if 'jijcloudquery/solution' in endpoint:
        assert 'solution_id' in params
        response_dict = {
                'solution_id': params['solution_id'],
                'status': 'PENDING',
                'solution': {}}

    response.raw = io.BytesIO(json.dumps(response_dict).encode())

    return response

# mock for requests.get (RUNNING)
def mock_request_get_running(*args, **kwargs):

    # mock for requests.get
    response = Response()
    response.status_code = HTTPStatus.ACCEPTED

    response_dict = {}

    headers = kwargs['headers']
    params = kwargs['params']

    endpoint = args[0]

    # /solution in Query
    if 'jijcloudquery/solution' in endpoint:
        assert 'solution_id' in params
        response_dict = {
                'solution_id': params['solution_id'],
                'status': 'RUNNING',
                'solution': {}}

    response.raw = io.BytesIO(json.dumps(response_dict).encode())

    return response

# mock for requests.get (FAILED)
def mock_request_get_failed(message_dict, *args, **kwargs):

    # mock for requests.get
    response = Response()
    response.status_code = HTTPStatus.ACCEPTED

    response_dict = {}

    headers = kwargs['headers']
    params = kwargs['params']

    endpoint = args[0]

    # /solution in Query
    if 'jijcloudquery/solution' in endpoint:
        assert 'solution_id' in params
        response_dict = {
                'solution_id': params['solution_id'],
                'status': 'FAILED',
                'solution': message_dict}

    response.raw = io.BytesIO(json.dumps(response_dict).encode())

    return response

# mock for requests.get (UNKNOWNERROR)
def mock_request_get_unknownerror(*args, **kwargs):

    # mock for requests.get
    response = Response()
    response.status_code = HTTPStatus.ACCEPTED

    response_dict = {}

    headers = kwargs['headers']
    params = kwargs['params']

    endpoint = args[0]

    # /solution in Query
    if 'jijcloudquery/solution' in endpoint:
        assert 'solution_id' in params
        response_dict = {
                'solution_id': params['solution_id'],
                'status': 'UNKNOWNERROR',
                'solution': {}}

    response.raw = io.BytesIO(json.dumps(response_dict).encode())

    return response


