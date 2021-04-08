import json


def json2dict(jsonStr="{\"a\": 1, \"b\": 2, \"c\": 3}"):
    return json.loads(jsonStr)


def dict2json(dict={"a": 1, "b": 2, "c": 3}):
    return json.dumps(dict)
