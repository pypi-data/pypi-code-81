import copy
import json


class DictData:

    def __init__(self, data:dict=None, html:str=None):
        self.data = data if data else {}
        if html and html.strip():
            try:
                self.data = json.loads(html.strip())
            except Exception as e:
                print('__init__', e)

    def count(self, key):
        self.data[key] = self.data.get(key, 0) + 1

    def append_to_key(self, key, data):
        if key not in self.data:
            self.data[key] = []
        self.data.get(key).append(data)

    def append_unique_group_keys(self, key1, key2, key3=None):

        if key3:
            if key1 not in self.data:
                self.data[key1] = {}
            if key2 not in self.data.get(key1):
                self.data.get(key1)[key2] = {}
            self.data.get(key1).get(key2)[key3] = 1

        else:
            if key1 not in self.data:
                self.data[key1] = {}
            self.data.get(key1)[key2] = 1

    def keys(self):
        return list(self.data.keys())

    def items(self):
        return self.data.items()

    def values(self):
        return list(self.data.values())

    def get_data(self):
        return self.data

    def rename_key(self, old_val, new_val):
        self.data[new_val] = self.data.pop(old_val)

    def clone(self):
        data = copy.deepcopy(self.data)
        return DictData(data)

    def get(self, key):
        val = self.data.get(key)
        return val if val != None else ''

    def remove_item_if(self, value=10):
        tmp = {}
        for k, v in self.data.items():
            if v > value:
                tmp[k] = v
        return DictData(tmp)

    def add_if(self, key='', text=''):
        if key in text:
            self.data[key] = text,

    def get_list_values(self, obj_lst, headers=None): # type: (list[dict], list) -> list
        headers = self._get_headers(obj_lst, headers)
        _lst = [headers]
        for j in obj_lst:
            _lst.append(list(j.values()))
        return _lst

    def _get_headers(self, json_obj, headers=None): # type: (list[dict], list) -> list
        if isinstance(json_obj[0], dict):
            if not headers:
                headers = [header for header in json_obj[0].keys()]
        if not headers:
            headers = ['' for i in range(0, len(json_obj[0]))]
        return headers

    def is_empty(self, data=None):
        try:
            if not data:
                data = self.data

            if isinstance(data, dict):
                return len(data) == 0
            if data and isinstance(data, str):
                d = json.loads(data)
                return len(d) == 0

        except Exception as e:
            print(e)
            return True

    def sort(self, reverse=False, sort_by_key=False):
        sort_by = 0 if sort_by_key else 1
        return {k: v for k, v in sorted(self.items(), key=lambda item: item[sort_by], reverse=reverse)}

    def sort_asc(self, sort_by_key=False):
        return self.sort(reverse=True, sort_by_key=sort_by_key)

    def get_keys(self):
        return list(self.keys())

    def get_values(self):
        return list(self.values())

    def size(self):
        return len(self.data)


if __name__ == '__main__':
    d = DictData()
    d.count('test')
    d.count('test')
    print(d.items())