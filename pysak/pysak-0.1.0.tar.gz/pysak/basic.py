import json


# json转dict
def json2dict(jsonStr="{\"a\": 1, \"b\": 2, \"c\": 3}"):
    """
    json转dict
    @param jsonStr:
    @return:
    """
    return json.loads(jsonStr)


# dict转json
def dict2json(dict={"a": 1, "b": 2, "c": 3}):
    """
    dict转json
    @param dict:
    @return:
    """
    return json.dumps(dict)
