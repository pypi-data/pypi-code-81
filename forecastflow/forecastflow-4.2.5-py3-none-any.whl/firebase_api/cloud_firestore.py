import json
from typing import Union

import requests

from .. import config
from .exceptions import APIFailed, NotFound, PermissionDenied


def _parse(type_and_value: dict) -> Union[bool, int, float, str, dict, list, None]:
    """
    Parse json from cloud firestore.

    Types are here https://firebase.google.com/docs/firestore/reference/rest/v1beta1/Value

    Args:
        type_and_value:
            {type: value}

    Returns:
        parsed value
    """
    type_ = list(type_and_value.keys())[0]
    value = type_and_value[type_]

    if type_ == 'stringValue':
        return value

    elif type_ == 'nullValue':
        return None

    elif type_ == 'booleanValue':
        return value == 'true'

    elif type_ == 'integerValue':
        return int(value)

    elif type_ == 'doubleValue':
        return float(value)

    elif type_ == 'timestampValue':
        # TODO: Implement TimestampValue parser
        return None

    elif type_ == 'mapValue':
        fields = value['fields']
        res = {k: _parse(fields[k]) for k in fields}
        return res

    elif type_ == 'arrayValue':
        if len(value) > 0:
            values = value['values']
            res = [_parse(value) for value in values]
            return res
        else:
            return []
    else:
        raise ValueError(f"Unsupported type '{type_}'.")


def _parse_collection(collection):
    """
    Args:
        collection:
            API response for collection.
            'documents' property is list of document.
            {'documents':
                [{'name': <name>, 'fields':{<field name>: {<type>: <value>}},...}, ...]
            }

    Returns:
        List of parsed document
    """
    documents = [_parse_document(d) for d in collection['documents']]
    return documents


def _parse_document(document):
    # document is like
    # {'name': <path to document>,
    #  'fields': {
    #    <some filed name>: {<type>: <value>},
    #  }
    name = document['name']
    fields = {
        field_name: _parse(document['fields'][field_name])
        for field_name in document['fields']
    }
    return {'name': name, 'fields': fields}


def get(path: str, id_token: str):
    """
    API Document is here
    https://firebase.google.com/docs/firestore/reference/rest/v1beta2/projects.databases.collectionGroups.fields/get

    Args:
        path:
            Path on Cloud Firestore

        id_token:
            Firebase Auth ID token

    Returns:
        parsed document if path is to document.
        list of parsed document if path is to collection.

    Raises:
        PermissionDenied
            Path does not exist or permission of token is insufficient

        APIFailed
            Other API Error

    Notes:
        parsed document is dictionary like below.
        { 'name': <path to document on firebase>,
          'fields': { <field 1>: value, <field 2>: value, ...}
        }
    """
    api_base_url = (
        f"https://firestore.googleapis.com/v1/projects/"
        f"{config.gcp['project_name']}/databases/(default)/documents"
    )
    if path.startswith('/'):
        path = path[1:]
    request_url = f"{api_base_url}/{path}"
    res = requests.get(request_url, headers={'Authorization': f"Bearer {id_token}"})

    if res.status_code != 200:
        if res.status_code == 403:
            raise PermissionDenied(res.text)
        if res.status_code == 404:
            raise NotFound(res.text)
        else:
            raise APIFailed(res.text)

    j = json.loads(res.text)
    if 'documents' in j:
        return _parse_collection(j)
    elif 'fields' in j:
        return _parse_document(j)
    else:
        raise Exception("Response cannot be parsed")
