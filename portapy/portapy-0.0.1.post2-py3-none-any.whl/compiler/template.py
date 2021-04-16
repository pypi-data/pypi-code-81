import typing
import re
import datetime
from jinja2 import Environment
from jinja2 import FileSystemLoader

from portapy.core import API
from portapy.core import Endpoint
from portapy.core import EndpointInfo
from portapy.core import Model
from portapy.core import Path
from portapy.core import Method
from portapy.core import Parameter
from portapy.core import RequestMapping
from portapy.core import ResponseMapping


class Filters():
    """
    This collection contains a collection of template filters.
    """

    @classmethod
    def as_dict(cls) -> typing.Dict[str, typing.Callable]:
        """
        Get the filters as a dictionary.
        """
        items = {k: getattr(cls, k) for k, v in cls.__dict__.items() if isinstance(v, staticmethod)}
        return items

    @staticmethod
    def to_pascal_case(data: str) -> str:
        """
        Convert a string to pascal case.
        """
        data = re.sub('([A-Z])', ' \\1', data)
        data = re.sub('[^a-zA-Z0-9]', ' ', data)
        return data.title().replace(' ', '')

    @staticmethod
    def to_snake_case(data: str) -> str:
        """
        Convert a string to snake case.
        """
        data = Filters.to_pascal_case(data)
        data = re.sub('([A-Z])', '_\\1', data).lower()
        return data.strip('_')

    @staticmethod
    def to_camel_case(data: str) -> str:
        """
        Convert a string to camel case.
        """
        data = Filters.to_pascal_case(data)
        return data[0:1].lower() + data[1:]

    @staticmethod
    def to_kebab_case(data: str) -> str:
        """
        Convert a string to kebab case.
        """
        return Filters.to_snake_case(data).replace('_', '-')

    @staticmethod
    def is_dict(data: typing.Any) -> bool:
        """
        Check if a value is a dict.
        """
        return isinstance(data, dict)


class Renderer():
    def __init__(self, api: API, data: dict = None, filters: dict = None,
                 *args, **kwargs) -> None:
        self.api = api
        self.data = data
        self.env = Environment(loader=FileSystemLoader('.'), *args, **kwargs)
        self.env.filters.update(Filters.as_dict())
        self.env.filters.update(filters or {})

    def get_api_tree(self) -> dict:
        """
        Get the tree for the API.
        """
        result = {
            'endpoints': [],
            'children': {},
        }

        for endpoint in self.api.get(Endpoint):
            info = endpoint.get(EndpointInfo)
            name = info.name if info and info.name else None
            desc = info.desc if info and info.desc else ''
            paths = endpoint.get(Path)
            methods = endpoint.get(Method)
            params = endpoint.get(Parameter)
            request = endpoint.get(RequestMapping)
            responses = endpoint.get(ResponseMapping)

            ref = result
            if info and info.tags:
                for tag in info.tags:
                    if tag not in ref['children']:
                        ref['children'][tag] = {
                            'endpoints': [],
                            'children': {},
                        }
                    ref = ref['children'][tag]

            if not name:
                name = 'temp'  # FIXME

            ref['endpoints'].append({
                'object': endpoint,
                'info': info,
                'name': name,
                'desc': desc,
                'paths': paths,
                'methods': methods,
                'params': params,
                'request': request,
                'success_responses': [x for x in responses if x.status_code < 300],
                'error_responses': [x for x in responses if x.status_code >= 400],
            })

        return result

    def get_vars(self) -> dict:
        """
        Get the variables to pass to the template.
        """
        self.api.get_spec()  # FIXME: shouldn't have to call this
        data = {
            'api': self.api,
            'tree': self.get_api_tree(),
            'models': {x.name: x for x in reversed(self.api.get(Model))},
        }
        data.update(self.data)
        return data

    def render(self, filename: str) -> str:
        template = self.env.get_template(filename)
        tpl_vars = self.get_vars()
        return template.render(**tpl_vars)
