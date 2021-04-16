import re
import json
from typing import Union, Dict, List
from requests import Response
from http import HTTPStatus

import pytest
import responses
from unittest import mock

from tests import MockResponse

from arthurai import ArthurAI
from arthurai.common.constants import InputType, OutputType
from arthurai.client.validation import validate_multistatus_response_and_get_failures, validate_response_status
from arthurai.common.exceptions import ResponseServerError, ResponseClientError, ResponseRedirectError, \
    InternalValueError
from tests.base_test import BaseTest


class TestClient(BaseTest):

    def _mock_get_user(self):
        self.mockPost(f"/api/v3/users/me", request_type=responses.GET, status=200,
                      dict_to_return={"organization_id": "65624ee6-9a73-4fe3-a7ff-8612f7d11c21", "role": "Model Owner"})

    @pytest.mark.usefixtures('mock_cred_env_vars')
    def test_client_init_env_vars(self):
        client = ArthurAI(offline=True)
        assert client.client.url == 'http://mock'
        assert client.client.access_key == 'access_key'

        client = ArthurAI(url="this is a url", access_key="this is an access key", offline=True)
        assert client.client.url == "https://this is a url"
        assert client.client.access_key == "this is an access key"

        client = ArthurAI(url="http://this is a url", access_key="this is an access key", offline=True)
        assert client.client.url == "http://this is a url"
        assert client.client.access_key == "this is an access key"

        client = ArthurAI(url="http://this is a url/apath", access_key="this is an access key", offline=True)
        assert client.client.url == "http://this is a url"
        assert client.client.access_key == "this is an access key"

        client = ArthurAI(url="http://this is a url?food=good", access_key="this is an access key", offline=True)
        assert client.client.url == "http://this is a url"
        assert client.client.access_key == "this is an access key"

        client = ArthurAI(url="fatfinger://this is a url", access_key="this is an access key", offline=True)
        assert client.client.url == "https://this is a url"
        assert client.client.access_key == "this is an access key"

        with pytest.raises(ValueError):
            ArthurAI(url="https:", access_key="this is an access key", offline=True)

    @responses.activate
    def test_client_init(self):
        self._mock_get_user()

        ArthurAI(access_key=self.access_key, url=self._base_url)
        self.assertEqual(len(responses.calls), 1)
        expectedResponse = {'organization_id': '65624ee6-9a73-4fe3-a7ff-8612f7d11c21', 'role': 'Model Owner'}
        self.assertEqual(expectedResponse, responses.calls[0].response.json())

    @responses.activate
    def test_client_init_offline(self):
        ArthurAI(access_key=self.access_key, url=self._base_url, offline=True)
        self.assertEqual(len(responses.calls), 0)

    @responses.activate
    def test_client_init_offlines(self):
        self.mockPost(f"/api/v3/models/1234", request_type=responses.GET, status=200,
                      dict_to_return={"organization_id": "65624ee6-9a73-4fe3-a7ff-8612f7d11c21", "role": "Model Owner"})
        ArthurAI(access_key=self.access_key, url=self._base_url, offline=True)
        self.assertEqual(len(responses.calls), 0)

    @responses.activate
    def test_client_user_agent_header(self):
        model_data = {
            "partner_model_id": "",
            "input_type": InputType.Tabular,
            "output_type": OutputType.Regression,
            "display_name": "",
            "description": "",
            "attributes": [],
        }
        self.mockPost("/api/v3/models/1234", request_type=responses.GET, status=200,
                      dict_to_return=model_data)

        self._mock_get_user()

        client = ArthurAI(access_key=self.access_key, url=self._base_url)
        client.get_model('1234')

        self.assertEqual(len(responses.calls), 2)
        if "models" in responses.calls[1].request.url:
            header = responses.calls[1].request.headers
        else:
            header = responses.calls[0].request.headers
        self.assertTrue('User-Agent' in header)
        print(header['User-Agent'])
        assert re.findall(r"^arthur-sdk\/\d.\d.\d* \(system=\w*, org=65624ee6-9a73-4fe3-a7ff-8612f7d11c21\)$",
                          header['User-Agent'])


class TestGetMultiStatusResponseFailures:
    # fixtures
    SUCCESS_RESULTS = [{"message": "ok", "status": HTTPStatus.OK}, {"message": "created", "status": HTTPStatus.CREATED}]
    USER_FAIL_RESULTS = [{"message": "not found", "status": HTTPStatus.NOT_FOUND}]
    INTERNAL_FAIL_RESULTS = [{"message": "failure", "status": HTTPStatus.INTERNAL_SERVER_ERROR},
                             {"message": "choose", "status": HTTPStatus.MULTIPLE_CHOICES}]
    SUCCESS_BODY = {"counts": {"success": len(SUCCESS_RESULTS), "failure": 0, "total": len(SUCCESS_RESULTS)},
                    "results": SUCCESS_RESULTS}
    FAILURES_BODY = {"counts": {"success": len(SUCCESS_RESULTS),
                                "failure": len(INTERNAL_FAIL_RESULTS) + len(USER_FAIL_RESULTS),
                                "total": len(SUCCESS_RESULTS) + len(INTERNAL_FAIL_RESULTS) + len(USER_FAIL_RESULTS)},
                     "results": SUCCESS_RESULTS + USER_FAIL_RESULTS + INTERNAL_FAIL_RESULTS}
    MISMATCHED_COUNTS_BODY = {"counts": {"success": len(SUCCESS_RESULTS), "failure": 0,
                                         "total": len(SUCCESS_RESULTS)},
                              "results": SUCCESS_RESULTS + USER_FAIL_RESULTS + INTERNAL_FAIL_RESULTS}

    def test_success(self):
        response = MockResponse(self.SUCCESS_BODY, HTTPStatus.MULTI_STATUS)
        actual_user_failures, actual_internal_failures = validate_multistatus_response_and_get_failures(response)
        assert actual_user_failures == []
        assert actual_internal_failures == []

    def test_failures(self):
        response = MockResponse(self.FAILURES_BODY, HTTPStatus.MULTI_STATUS)
        actual_user_failures, actual_internal_failures = validate_multistatus_response_and_get_failures(response)
        assert actual_user_failures == self.USER_FAIL_RESULTS
        assert actual_internal_failures == self.INTERNAL_FAIL_RESULTS

    def test_bad_status(self):
        response = MockResponse(self.SUCCESS_BODY, HTTPStatus.OK)
        with pytest.raises(ValueError):
            validate_multistatus_response_and_get_failures(response)

    def test_mismatched_counts(self):
        response = MockResponse(self.MISMATCHED_COUNTS_BODY, HTTPStatus.MULTI_STATUS)
        with pytest.raises(ValueError):
            validate_multistatus_response_and_get_failures(response)

# TODO: add testing around allowed exceptions and what gets raised first (e.g. expected 207 but 404 shouldn't raise InternalValueError)
class TestValidateResponse:
    # fixtures
    JSON_BODY = {"status": "somestatus"}
    BYTES_BODY = b"bodybytes"

    def test_server_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.INTERNAL_SERVER_ERROR)
        with pytest.raises(ResponseServerError):
            validate_response_status(response)

    def test_client_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.NOT_FOUND)
        with pytest.raises(ResponseClientError):
            validate_response_status(response)

    def test_expected_404_no_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.NOT_FOUND)
        validate_response_status(response, expected_status_code=HTTPStatus.NOT_FOUND)

    def test_redirect_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.MOVED_PERMANENTLY)
        with pytest.raises(ResponseRedirectError):
            validate_response_status(response)

    def test_redirect_no_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.MOVED_PERMANENTLY)
        validate_response_status(response, allow_redirects=True)

    def test_ok_no_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.OK)
        validate_response_status(response)

    def test_unexpected_ok_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.OK)
        with pytest.raises(InternalValueError):
            validate_response_status(response, expected_status_code=HTTPStatus.CREATED)

    def test_server_error(self):
        code = HTTPStatus.INTERNAL_SERVER_ERROR
        with pytest.raises(ResponseServerError):
            validate_response_status(code)

    def test_client_error(self):
        code = HTTPStatus.NOT_FOUND
        with pytest.raises(ResponseClientError):
            validate_response_status(code)

    def test_expected_404_no_error(self):
        code = HTTPStatus.NOT_FOUND
        validate_response_status(code, expected_status_code=HTTPStatus.NOT_FOUND)

    def test_redirect_error(self):
        code = HTTPStatus.MOVED_PERMANENTLY
        with pytest.raises(ResponseRedirectError):
            validate_response_status(code)

    def test_redirect_no_error(self):
        code = HTTPStatus.MOVED_PERMANENTLY
        validate_response_status(code, allow_redirects=True)

    def test_ok_no_error(self):
        code = HTTPStatus.OK
        validate_response_status(code)

    def test_unexpected_ok_error(self):
        code = HTTPStatus.OK
        with pytest.raises(InternalValueError):
            validate_response_status(code, expected_status_code=HTTPStatus.CREATED)
