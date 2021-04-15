import hashlib
import json


def api_collection_id(collection_id):
    return collection_id if collection_id != "root" else None


def uuid(item):
    """
    Returns an UUID that is a function of item id.
    """
    return hashlib.md5(str(item["id"]).encode()).hexdigest()


def content_hash(item):
    return hashlib.md5(json.dumps(item, sort_keys=True).encode()).hexdigest()

def get_in(dictionary, key_list):
    p = dictionary
    found = True
    for a in key_list:
        if a in p:
            p = p[a]
        else:
            found = False
    if found:
        return p
