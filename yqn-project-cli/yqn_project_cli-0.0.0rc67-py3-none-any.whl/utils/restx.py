# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/15
import re
import inspect
from flask_restx import (
    Resource,
    Namespace
)
from yqn_project_cli.utils import merge_iterable_objs


class DANamespace(Namespace):
    def __init__(self, name, description=None, path=None, decorators=None,
                 validate=None, authorizations=None, ordered=False, **kwargs):
        super(DANamespace, self).__init__(name, description=description, path=path, decorators=decorators,
                                          validate=validate, authorizations=authorizations, ordered=ordered, **kwargs)

        self.error_handlers[BaseException] = self.default_error_deposit

    @staticmethod
    def default_error_deposit(error):
        raise error

    def route(self, *urls, **kwargs):
        def wrapper(cls):
            if inspect.isfunction(cls):
                name = ''.join(map(lambda _str: _str.capitalize(), re.split(r'\.|_', cls.__qualname__)))
                attrs = {cls.__name__: cls}
                for method in kwargs.get('methods', []):
                    attrs[str(method).lower()] = cls
                cls = type(name, (Resource,), attrs)

            doc = kwargs.pop("doc", None)
            if doc is not None:
                kwargs["route_doc"] = self._build_doc(cls, doc)
            self.add_resource(cls, *urls, **kwargs)
            return cls

        return wrapper


def add_view_mth_resource(ns, view_mth, route):
    if inspect.isfunction(view_mth):
        name = ''.join(map(lambda _str: _str.capitalize(), re.split(r'\.|_', view_mth.__qualname__)))
        attrs = {view_mth.__name__: view_mth}
        for method in route.get('http_methods', []):
            attrs[str(method).lower()] = view_mth
        cls = type(name, (Resource,), attrs)

    else:
        raise TypeError('%s must a function' % view_mth)

    doc = route.pop("doc", None)
    if doc is not None:
        route["route_doc"] = ns._build_doc(cls, doc)

    ns.add_resource(cls, *merge_iterable_objs(route['path']), methods=route.pop('http_methods'),
                    **route.pop('path_kwargs', {}))

    return cls
