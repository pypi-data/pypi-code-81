from unittest.mock import MagicMock
from mock_server.mocks import MockNewsHeadlinesResponse, MockNewsStoryResponse, MockRequestResponse, MockHistoricalPricingResponseError


class MockResponseUniversal(MagicMock):
    expires_in_5_min = 5 * 60

    status_code = 200

    headers = {'content-type': '/json'}

    def json(self):
        return {
            'refresh_token': MagicMock(),
            'access_token': MagicMock(),
            'expires_in': MockAuthResponse.expires_in_5_min,
            'service': MagicMock(),
            'headers': MagicMock(),
            'data': [MagicMock()]
            }


class MockAuthResponse(MagicMock):
    expires_in_5_min = 5 * 60

    status_code = 200

    headers = {'content-type': '/json'}

    def json(self):
        return {
            'refresh_token': MagicMock(),
            'access_token': MagicMock(),
            'expires_in': MockAuthResponse.expires_in_5_min,
            'service': MagicMock(),
            }


class MockSession(MagicMock):
    response = MagicMock()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def send(self, request, **kwargs):
        return MockSession.response
