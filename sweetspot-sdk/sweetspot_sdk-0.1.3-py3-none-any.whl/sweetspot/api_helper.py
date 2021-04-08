import jsonpickle 
import re

from requests.utils import quote

class ApiHelper(object):

    @staticmethod
    def merge_dicts(dict1, dict2):
        temp = dict1.copy()
        temp.update(dict2)
        return temp

    @staticmethod
    def clean_url(url):
        regex = "^http?://[^/]+"
        match = re.match(regex, url)
        if match is None:
            raise ValueError('Invalid Url format.')

        protocol = match.group(0)
        index = url.find('?')
        query_url = url[len(protocol): index if index != -1 else None]
        query_url = re.sub("//+", "/", query_url)
        parameters = url[index:] if index != -1 else ""

        return protocol + query_url + parameters

    @staticmethod 
    def json_serialize(obj):
        return jsonpickle.encode(obj)

    @staticmethod 
    def json_deserialize(json):
        if not json: 
            return json 
        try:
            decoded = jsonpickle.decode(json)
            return decoded 
        except ValueError: 
            return json 

    @staticmethod
    def append_url_with_query_parameters(url,
                                        parameters,
                                        array_serialization="indexed"):
        if url is None:
            raise ValueError("URL is None.")
        if parameters is None:
            return url

        for key, value in parameters.items():
            seperator = '&' if '?' in url else '?'
            if value is not None:
                if isinstance(value, list):
                    value = [element for element in value if element]
                    if array_serialization == "csv":
                        url += "{0}{1}={2}".format(
                            seperator,
                            key,
                            ",".join(quote(str(x), safe='') for x in value)
                        )
                    elif array_serialization == "psv":
                        url += "{0}{1}={2}".format(
                            seperator,
                            key,
                            "|".join(quote(str(x), safe='') for x in value)
                        )
                    elif array_serialization == "tsv":
                        url += "{0}{1}={2}".format(
                            seperator,
                            key,
                            "\t".join(quote(str(x), safe='') for x in value)
                        )
                    else:
                        url += "{0}{1}".format(
                            seperator,
                            "&".join(("{0}={1}".format(k, quote(str(v), safe='')))
                                        for k, v in APIHelper.serialize_array(key, value, array_serialization))
                        )
                else:
                    url += "{0}{1}={2}".format(seperator, key, quote(str(value), safe=''))

        return url



         
