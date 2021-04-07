import requests


class API(object):

    def __init__(self):
        pass

    def query_exchange(self, key):
        """返回常用汇率"""
        url = "http://op.juhe.cn/onebox/exchange/query"
        res = requests.get(
            url,
            params={
                "key": key,
            },
        )
        res.raise_for_status()
        assert res.json()["error_code"] == 0, res.text
        data = res.json()["result"]["list"]
        return data
