# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/2/25
import os
import abc
import copy
import inspect
import datetime
from flask import (
    Flask,
    Blueprint,
    request,
    views,
    jsonify,
)
from flask.json import JSONEncoder
from yqn_project_cli.utils import (
    merge_iterable_objs,
    load_module_from_pyfile,
)
from yqn_project_cli.utils.core.exceptions import APIException
from yqn_project_cli.utils.core.parser import DAJsonBase
from yqn_project_cli.utils.core.logger import Logger
from yqn_project_cli.rpc import RPCConfigBase


class UrlBase:
    def __init__(self, rule, view_func, title, endpoint, **options):
        """
        :param rule:
        :param view_func:
        :param title: url desc
        :param options:
        """
        self.rule = rule
        self.title = title
        self.params = dict(
            view_func=view_func,
            endpoint=endpoint,
            **options
        )

    def __str__(self):
        return str(self.title) + ": " + str(self.rule)


class BlueprintBase(Blueprint):
    def __init__(self, name, import_name, urls, title, **options):
        """
        :param name:
        :param import_name:
        :param urls: list-typed
        :param title: blueprint desc
        :param options:
        """
        super().__init__(name, import_name, **options)
        self.params = dict(
            name=name,
            import_name=import_name,
            **options
        )
        self.title = title
        self.urls = urls
        self.add_url_rules(urls)

    def add_url_rules(self, urls):
        for url in urls:
            self.add_url_rule(url.rule, **url.params)

    def __str__(self):
        return str(self.title) + ": " + str(self.urls)


class DAJson(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')

        elif isinstance(obj, bytes):
            return obj.decode("utf-8")

        elif isinstance(obj, DAJsonBase):
            return obj.to_json()

        else:
            return str(obj)

        # else:
        #     return super(DAJson, self).default(o)


class DAFlask(Flask):
    json_encoder = DAJson

    def __init__(self, import_name, project_config, config_object,
                 logger_config=None,
                 **options):

        super(DAFlask, self).__init__(import_name, **options)

        self.project_config = project_config

        self.config.from_object(config_object)

        self.loggers = Logger(logger_config)

        self.plugins = {}

        self.services = {}

        self.server_manager = None  # (server_name, server_connector)

    def add_url_rules(self, rules, endpoint=None, view_func=None, provide_automatic_options=None, **options):
        assert isinstance(rules, (str, list, tuple)), '%s rules allow single str rule or rules list-typed' % rules
        if isinstance(rules, str):
            self.add_url_rule(rules, endpoint=endpoint, view_func=view_func,
                              provide_automatic_options=provide_automatic_options, **options)

        elif isinstance(rules, (list, tuple)):
            for rule in rules:
                self.add_url_rule(rule, endpoint=endpoint, view_func=view_func,
                                  provide_automatic_options=provide_automatic_options, **options)

    def register_urls(self, *urls):
        for url in merge_iterable_objs(urls):
            assert isinstance(url, UrlBase), '%s is not subclass of UrlBase' % type(url)
            self.add_url_rule(url.rule, **url.params)

    def register_blueprints(self, *bps):
        for bp in merge_iterable_objs(bps):
            assert isinstance(bp, BlueprintBase), '%s is not subclass of BlueprintBase' % type(bp)
            self.register_blueprint(bp, **bp.params)

    def register_before_first_requests(self, *fs):
        for f in fs:
            self.before_first_request(f)

    def register_before_requests(self, *fs):
        for f in fs:
            self.before_request(f)

    def register_after_requests(self, *fs):
        for f in fs:
            self.after_request(f)

    def register_teardown_requests(self, *fs):
        for f in fs:
            self.teardown_request(f)

    def register_request_hooks(self, *request_hooks):
        for hook, f in request_hooks:
            if hook == 'before_first_request':
                self.before_first_request(f)

            elif hook == 'before_request':
                self.before_request(f)

            elif hook == 'after_request':
                self.after_request(f)

            elif hook == 'teardown_request':
                self.teardown_request(f)

    def register_error_handlers(self, *error_handlers):
        for code_or_exception, f in error_handlers:
            self.register_error_handler(code_or_exception, f)

    def register_plugins(self, *plugins):
        for _ in plugins:
            assert isinstance(_, Plugin), '%s is not subclass of Plugin' % type(_)
            self.plugins[_.name] = _.plugin(self, *_.args, **_.kwargs)

    def register_plugin_tails(self, *plugin_tails):
        for _ in plugin_tails:
            assert isinstance(_, PluginTail), '%s is not subclass of PluginTail' % type(_)
            _.caller(self.plugins[_.plugin_name], *_.args, **_.kwargs)

    def register_services(self, *servers):
        for _ in servers:
            assert isinstance(_, Server), '%s is not subclass of Server' % type(_)

            assert not (self.server_manager is None and _.use_conf_management), \
                "server_manager isn't inited yet, keep it foremost and init it"

            if self.server_manager is None and _.as_server_manager:
                server = _.server_cls(client_config=_.client_config,
                                      project_config=copy.deepcopy(self.project_config), **_.kwargs)

                print(server.connect())
                self.server_manager = (_.name, server.connector)

            else:
                server = _.server_cls(client_config=_.client_config,
                                      use_conf_management=_.use_conf_management,
                                      server_manager=self.server_manager[1] if self.server_manager else None,
                                      **_.kwargs)
                server.connect()

            self.services[_.name] = server

        else:
            if self.server_manager is not None:
                setattr(self.services[self.server_manager[0]], 'services', self.services)


class View(views.MethodView):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self, *args, **kwargs):
        self.args = args
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def as_view(cls, *args, **kwargs):

        for key in kwargs:
            if str(key).lower() in cls.http_method_names:
                raise TypeError("Forbidden http verbs keyword %s to method %s()" % (key, cls.__name__))

            if not hasattr(cls, key):
                raise TypeError("%s() refuse keyword %s which not in attrs-classed" % (cls.__name__, key))

        name = str(args and args[0] or cls.__name__)
        args = args and args[1:]

        return super(View, cls).as_view(name, *args, **kwargs)

    def dispatch_request(self, *args, **kwargs):
        method = request.method.lower() if request.method != "HEAD" else 'get'

        handler = getattr(self, method, self._not_allowed_method)

        return handler(*args, **kwargs)

    def _not_allowed_method(self, *args, **kwargs):
        raise APIException(errmsg='%s is not allowed' % request.method, errcode="-1",
                           data={'methods': [m.upper() for m in self.http_method_names if hasattr(self, m)]})


class RoutePluginBase(metaclass=abc.ABCMeta):
    def __init__(self, app, **kwargs):
        self.app = app
        self.path = os.path.dirname(inspect.getabsfile(self.__class__))
        self.routes = []

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.plugin_app()

    @abc.abstractmethod
    def plugin_app(self):
        raise NotImplementedError

    def auto_register_blueprints(self):
        for pkg in os.listdir(self.path):
            if pkg.startswith(('_', '.')) \
                    or not os.path.isdir(os.path.join(self.path, pkg)) \
                    or not os.path.exists(os.path.join(self.path, pkg, 'route.py')):
                continue

            route = load_module_from_pyfile(os.path.join(self.path, pkg, 'route.py'))

            self.app.register_blueprints(getattr(route, 'blueprints', []))

            self.routes.append(route)


class _JSONResponse:
    def __call__(self, data=None, errmsg='success', errcode='0'):
        return jsonify({'errmsg': errmsg,
                        'errcode': errcode,
                        'data': data})


JSONResponse = _JSONResponse()


class Plugin:
    def __init__(self, name, plugin, *args, **kwargs):
        self.name = name
        self.plugin = plugin
        self.args = args
        self.kwargs = kwargs


class PluginTail:
    def __init__(self, plugin_name, caller, *args, **kwargs):
        """
        caller(plugin, *args, **kwargs)
        """
        self.plugin_name = plugin_name
        self.caller = caller
        self.args = args
        self.kwargs = kwargs


class Server:
    def __init__(self, name, server_cls,
                 client_config=None, use_conf_management=False, as_server_manager=False, **kwargs):
        assert issubclass(server_cls, RPCConfigBase), '%s is not subclass of RPCConfigBase' % type(server_cls)

        self.name = name
        self.server_cls = server_cls
        self.client_config = client_config
        self.use_conf_management = use_conf_management
        self.as_server_manager = as_server_manager
        self.kwargs = kwargs


if __name__ == '__main__':
    print('in as_flask')
