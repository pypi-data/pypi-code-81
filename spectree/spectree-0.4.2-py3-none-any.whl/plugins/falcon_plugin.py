import inspect
import re
from functools import partial

from pydantic import ValidationError

from .base import BasePlugin
from .page import PAGES


class OpenAPI:
    def __init__(self, spec):
        self.spec = spec

    def on_get(self, req, resp):
        resp.media = self.spec


class DocPage:
    def __init__(self, html, spec_url):
        self.page = html.format(spec_url)

    def on_get(self, req, resp):
        resp.content_type = "text/html"
        resp.body = self.page


DOC_CLASS = [x.__name__ for x in (DocPage, OpenAPI)]


class FalconPlugin(BasePlugin):
    def __init__(self, spectree):
        super().__init__(spectree)
        from falcon import HTTPUnsupportedMediaType
        from falcon.routing.compiled import _FIELD_PATTERN

        self.UnsupportedMediaType = HTTPUnsupportedMediaType
        self.FIELD_PATTERN = _FIELD_PATTERN
        # NOTE from `falcon.routing.compiled.CompiledRouterNode`
        self.ESCAPE = r"[\.\(\)\[\]\?\$\*\+\^\|]"
        self.ESCAPE_TO = r"\\\g<0>"
        self.EXTRACT = r"{\2}"
        # NOTE this regex is copied from werkzeug.routing._converter_args_re and
        # modified to support only int args
        self.INT_ARGS = re.compile(
            r"""
            ((?P<name>\w+)\s*=\s*)?
            (?P<value>\d+)\s*
        """,
            re.VERBOSE,
        )
        self.INT_ARGS_NAMES = ("num_digits", "min", "max")

    def register_route(self, app):
        self.app = app
        self.app.add_route(self.config.spec_url, OpenAPI(self.spectree.spec))
        for ui in PAGES:
            self.app.add_route(
                f"/{self.config.PATH}/{ui}",
                DocPage(PAGES[ui], self.config.spec_url),
            )

    def find_routes(self):
        routes = []

        def find_node(node):
            if node.resource and node.resource.__class__.__name__ not in DOC_CLASS:
                routes.append(node)

            for child in node.children:
                find_node(child)

        for route in self.app._router._roots:
            find_node(route)

        return routes

    def parse_func(self, route):
        return route.method_map.items()

    def parse_path(self, route):
        subs, parameters = [], []
        for segment in route.uri_template.strip("/").split("/"):
            matches = self.FIELD_PATTERN.finditer(segment)
            if not matches:
                subs.append(segment)
                continue

            escaped = re.sub(self.ESCAPE, self.ESCAPE_TO, segment)
            subs.append(self.FIELD_PATTERN.sub(self.EXTRACT, escaped))

            for field in matches:
                variable, converter, argstr = [
                    field.group(name) for name in ("fname", "cname", "argstr")
                ]

                if converter == "int":
                    if argstr is None:
                        argstr = ""

                    arg_values = [None, None, None]
                    for index, match in enumerate(self.INT_ARGS.finditer(argstr)):
                        name, value = match.group("name"), match.group("value")
                        if name:
                            index = self.INT_ARGS_NAMES.index(name)
                        arg_values[index] = value

                    num_digits, minumum, maximum = arg_values
                    schema = {
                        "type": "integer",
                        "format": f"int{num_digits}" if num_digits else "int32",
                    }
                    if minumum:
                        schema["minimum"] = minumum
                    if maximum:
                        schema["maximum"] = maximum
                elif converter == "uuid":
                    schema = {"type": "string", "format": "uuid"}
                elif converter == "dt":
                    schema = {
                        "type": "string",
                        "format": "date-time",
                    }
                else:
                    # no converter specified or customized converters
                    schema = {"type": "string"}

                parameters.append(
                    {
                        "name": variable,
                        "in": "path",
                        "required": True,
                        "schema": schema,
                    }
                )

        return f'/{"/".join(subs)}', parameters

    def request_validation(self, req, query, json, headers, cookies):
        if query:
            req.context.query = query.parse_obj(req.params)
        if headers:
            req.context.headers = headers.parse_obj(req.headers)
        if cookies:
            req.context.cookies = cookies.parse_obj(req.cookies)
        try:
            media = req.media
        except self.UnsupportedMediaType:
            media = None
        if json:
            req.context.json = json.parse_obj(media)

    def validate(
        self, func, query, json, headers, cookies, resp, before, after, *args, **kwargs
    ):
        # falcon endpoint method arguments: (self, req, resp)
        _self, _req, _resp = args[:3]
        req_validation_error, resp_validation_error = None, None
        try:
            self.request_validation(_req, query, json, headers, cookies)
            if self.config.ANNOTATIONS:
                for name in ("query", "json", "headers", "cookies"):
                    if func.__annotations__.get(name):
                        kwargs[name] = getattr(_req.context, name)

        except ValidationError as err:
            req_validation_error = err
            _resp.status = "422 Unprocessable Entity"
            _resp.media = err.errors()

        before(_req, _resp, req_validation_error, _self)
        if req_validation_error:
            return

        func(*args, **kwargs)
        if resp and resp.has_model():
            model = resp.find_model(_resp.status[:3])
            if model:
                try:
                    model.parse_obj(_resp.media)
                except ValidationError as err:
                    resp_validation_error = err
                    _resp.status = "500 Internal Service Response Validation Error"
                    _resp.media = err.errors()

        after(_req, _resp, resp_validation_error, _self)

    def bypass(self, func, method):
        if not isinstance(func, partial):
            return False
        if inspect.ismethod(func.func):
            return False
        # others are <cyfunction>
        return True
