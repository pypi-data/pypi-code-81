# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/26
from flask_restx import Resource
from yqn_project_cli.utils.restx import DANamespace
from yqn_project_cli.utils.core.as_flask import (
    UrlBase,
    BlueprintBase,
    View,
)


class ApiUrl(UrlBase):
    pass


class ApiBlueprint(BlueprintBase):
    pass


class ApiResource:
    def __init__(self, url, resource, title, **kwargs):
        assert isinstance(resource, (Resource, View)) \
               or issubclass(getattr(resource, 'view_class', None), (Resource, View)), \
            '%s is not subclass or instance of Resource or View' % type(resource)

        self.url = url
        self.resource = resource
        self.title = title
        self.kwargs = kwargs


class ApiNamespace:
    def __init__(self, namespace, resources, title, **kwargs):
        assert isinstance(namespace, DANamespace), '%s is not instance of DANamespace' % type(namespace)
        self.namespace = namespace
        self.resources = resources
        self.title = title
        self.kwargs = kwargs
        self.add_resources(resources)

    def add_resources(self, resources):
        for res in resources:
            assert isinstance(res, ApiResource), '%s is not instance of ApiResource' % type(res)
            view_class = getattr(res.resource, 'view_class', None)
            if view_class is not None and issubclass(view_class, (Resource, View)):
                res.resource = view_class

            self.namespace.add_resource(res.resource, res.url, **res.kwargs)
