import os
import json


def json_to_string(j: dict, indent: int = -1, sort_keys: bool = False) -> str:
    """
    :param j: dict
    :param indent: how many indents
    :param sort_keys: sort dict keys
    :return: string rep of j
    e.g.
    cfg = {'x': 3, 'a': 'dx'}
    print('one liner:')
    print(json_to_string(cfg, indent=-1, sort_keys=False))  # 1 liner
    print('pretty print - 4 indentations:')
    print(json_to_string(cfg, indent=4, sort_keys=False))  # pretty print - 4 indentations
    print('pretty print - 0 indentations:')
    print(json_to_string(cfg, indent=0, sort_keys=False))  # pretty print - 0 indentations
    print('one liner sorted keys:')
    print(json_to_string(cfg, indent=-1, sort_keys=True))  # 1 liner
    """
    if indent == -1:
        indent = None
    return json.dumps(j, indent=indent, sort_keys=sort_keys)


def string_to_json(j_str: str) -> json:
    """
    e.g.
    j_str = '{"x": 3, "a": "dx"}'
    j = string_to_json(j_str)
    print(type(j))
    """
    return json.loads(j_str)


def load_json(file_path: str, ack: bool = True) -> dict:
    """ loads a dict in json format from path """
    ret_dict = {}
    if os.path.exists(file_path):
        ret_dict = json.load(open(file_path))
        if ack:
            print('{} loaded (type {})'.format(file_path, type(ret_dict)))
            print(json_to_string(ret_dict, indent=4))
    else:
        print('file {} doesnt exists'.format(file_path))
    return ret_dict


def load_jsons(files_path: list, ack: bool = True) -> dict:
    """
    loads several of json files format from paths and concat to one dict
    asserts if a key found on 2 of the files
    """
    all_in_one_dict = {}
    len_keys_json = 0
    for file_path in files_path:
        j = load_json(file_path, ack=False)
        len_keys_json += len(j)
        all_in_one_dict.update(j)
    if ack:
        print('{} loaded (type {})'.format(files_path, type(all_in_one_dict)))
        print(json_to_string(all_in_one_dict, indent=4))
    assert len_keys_json == len(all_in_one_dict), 'Duplicated keys found: {}'.format(files_path)
    return all_in_one_dict


def save_json(file_path: str, j: dict, indent: int = -1, sort_keys: bool = False, ack: bool = True) -> None:
    json.dump(j, open(file_path, 'w'), indent=indent, sort_keys=sort_keys)
    if ack:
        print('{} saved successfully'.format(file_path))
        print(json_to_string(j, indent=indent, sort_keys=sort_keys))
    return


def get_key_by_value(d: dict, value) -> str:
    """
    :param d: dict
    :param value:
    Notice that it will return the first key of the value given. if value not unique...
    :return: the key of the value
    e.g.
    j = {"x": 3, "a": "dx"}
    print(get_key_by_value(j, value="dx"))
    print(get_key_by_value(j, value=3))
    """
    key = None
    for k, v in d.items():
        if v == value:
            key = k
            break
    return key


def main():
    return


if __name__ == '__main__':
    main()
