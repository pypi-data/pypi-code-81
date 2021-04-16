from unittest.mock import MagicMock


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


class MockRequestResponse(MagicMock):
    status_code = 200

    headers = {'content-type': '/json'}

    def json(self):
        return {
            'headers': MagicMock(),
            'data': MagicMock()
        }


class MockHistoricalPricingResponseError(MockRequestResponse):
    def json(self):
        return [{
            "universe": {"ric": "VOD.Lasd"},
            "status": {"code": "TS.Intraday.UserRequestError.90001", "message": "The universe is not found."}
        }]


class MockSession(MagicMock):
    response = MagicMock()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def send(self, request, **kwargs):
        return MockSession.response
