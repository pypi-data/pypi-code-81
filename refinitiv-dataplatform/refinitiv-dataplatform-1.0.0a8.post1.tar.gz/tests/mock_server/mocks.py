from unittest.mock import MagicMock


class MockRequestResponse(MagicMock):
    status_code = 200
    reason = 'OK'
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


class MockNewsHeadlinesResponse(MockRequestResponse):
    import json
    import pathlib

    data_json_path = pathlib.Path(__file__).parent.absolute() / 'news_headlines_data.json'

    with open(data_json_path, 'r', encoding="utf8") as f:
        data = json.load(f)

    def json(self):
        return {
            'headers': MagicMock(),
            'data': self.data.get('data')
            }


class MockNewsStoryResponse(MockNewsHeadlinesResponse):
    import json
    import pathlib

    data_json_path = pathlib.Path(__file__).parent.absolute() / 'news_story_data.json'

    with open(data_json_path, 'r', encoding="utf8") as f:
        data = json.load(f)

    def json(self):
        return self.data
