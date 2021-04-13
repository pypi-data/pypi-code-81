import json
from airworks_api.base_api import BaseApi


class AirWorksApi:

    def __init__(self, base_url, app_method, access_key, access_secret, app_url):
        self.base_api = BaseApi()
        BaseApi.base_url = base_url
        self.base_api.app_method = app_method
        self.base_api.access_key = access_key
        self.base_api.access_secret = access_secret
        self.base_api.app_url = app_url

    def call(self, **kwargs):
        return self.base_api.api_response(**kwargs)


if __name__ == "__main__":
    awp = AirWorksApi(
        base_url="aw-airworks-frontend:30000",
        app_method="GET",
        app_url="api_gateway/api/1/baymax",
        access_key="kB85aqPMFZs_14",
        access_secret="lh66YHfiE7qL6TcOOvbLTg"
    )

    res = awp.call(page_size=100, page_num=1, country='中国', id=None)
    print(json.dumps(res, indent=2, ensure_ascii=False))
