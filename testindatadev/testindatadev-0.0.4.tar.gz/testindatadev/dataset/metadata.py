import json

class MetaData():
    def __init__(self, metadata):
        # 数据格式检查
        if not type(metadata) is dict:
            raise Exception(f"box must be a dict, {type(metadata)} gavin")
        self.meta = metadata

    def ToString(self):
        return json.dumps(self.meta)
