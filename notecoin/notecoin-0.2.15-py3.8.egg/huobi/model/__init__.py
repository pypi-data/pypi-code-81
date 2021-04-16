import pandas as pd


class Response:
    def __init__(self, dict_data, code=None, data=None):
        self.code = dict_data.get('code', -1)
        self.data = dict_data.get('data', [])
        self.dict_data = dict_data
        if self.data is not None and len(self.data)>0:
            self.data=pd.DataFrame(self.data)

    def __str__(self):
        return "{} {}".format(self.code, len(self.data))
