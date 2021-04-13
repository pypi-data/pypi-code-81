import json

from airworks_api.base_api import BaseApi


class CommonApi(BaseApi):
    base_url = "aw-airworks-frontend:30000"

    app_method = "GET"
    app_url = "api_gateway/api/1/baymax"
    access_key = "kB85aqPMFZs_14"
    access_value = "lh66YHfiE7qL6TcOOvbLTg"
    query_builder = """"""

    def api_response(
        self,
        country,
        id,
        page_size=100,
        page_num=1,
    ):
        return super(CommonApi, self).api_response(
            country=country,
            id=id,
            page_size=page_size,
            page_num=page_num,
            __query_builder__=self.query_builder,
        )


if __name__ == "__main__":
    api_result = CommonApi().api_response(
        country='中国',
        id=None,
        page_size=10,
    )
    print(json.dumps(api_result, indent=2, ensure_ascii=False))
