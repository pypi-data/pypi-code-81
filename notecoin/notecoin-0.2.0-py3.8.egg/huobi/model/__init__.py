class Response:
    def __init__(self, code=None, data=None, dict_data=None):
        self.code = code
        self.data = data
        self.dict_data = dict_data

    def __str__(self):
        return self.code + " " + len(self.data)
