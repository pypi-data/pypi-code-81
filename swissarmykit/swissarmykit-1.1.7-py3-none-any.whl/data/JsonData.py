import json
import pprint
import ast

from swissarmykit.conf import *

from swissarmykit.utils.fileutils import FileUtils
from swissarmykit.utils.stringutils import StringUtils


class JsonData:

    def __init__(self, data=None, json_html='', json_path='', single_quote=False):
        self.data = data

        if json_html:
            self.data = self._parse_json(json_html, single_quote=single_quote)

        if json_path:
            json_html = FileUtils.load_html_file(json_path)
            self.data = self._parse_json(json_html, single_quote=single_quote)

    def _parse_json(self, data, single_quote=False):
        return ast.literal_eval(data) if single_quote else json.loads(data)


    def get_list(self, key, debug=False):
        return self.get(key, as_list=True, debug=debug)

    def get(self, key, as_list=False, debug=False):
        if not self.data:
            return JsonData() if not as_list else []

        if '.' in key:
            re = self
            keys = key.split('.')
            total = len(keys)
            for i, k in enumerate(keys):
                re = re.get(k, as_list) if (total - 1) == i else re.get(k)
                if debug and not re:
                    print('DEBUG: Empty at key ', k)
            return re

        if key.endswith(']'):
            try:
                key, idx = key[:-1].split('[')
                d = self.data.get(key)
                d = d[int(idx)] if d else None
                return JsonData(data=d)
            except Exception as e:
                print('WARN: json.get error ', e)
            return JsonData()

        d = self.data.get(key)
        if isinstance(d, list):
            lst = []
            for d_ in d:
                lst.append(JsonData(data=d_))
            return lst

        if as_list:
            return [JsonData(data=d)] if self.data else []

        return JsonData(data=d)

    def get_data(self):
        return self.data

    @property
    def val(self):
        return self.data

    def is_null(self):
        return self.data == None
    
    def get_value(self, default=None):
        if self.val: return self.val
        return default

    def to_json(self):
        return json.dumps(self.data)

    def __contains__(self, key):
        return key in self.data

    def __bool__(self):
        return bool(self.data)

    def __str__(self):
        return self.to_json()

    @staticmethod
    def is_json(obj):
        try:
            return json.loads(obj)
        except Exception as e:
            pass
        return False

if __name__ == '__main__':
    single = "{'test': 1}"
    js = JsonData(single_quote=True, json_html=single)
    print(js)

    print('test' in js, 's' in js)
