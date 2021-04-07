# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/1
from flask import current_app
from yqn_project_cli.utils import error_mark
from yqn_project_cli.utils.restx import add_view_mth_resource
from yqn_project_cli.utils.core.as_flask import RoutePluginBase
from yqn_project_cli.utils.core.exceptions import (
    APIException,
    PortalException,
    HTTPException
)
from yqn_project_cli.rpc import RPCConfigBase


def general_error_handler(e):
    if isinstance(e, (APIException, PortalException)) or current_app.config['DEBUG']:
        return e

    elif isinstance(e, HTTPException):
        return APIException(errmsg=e.description, code=e.code)

    else:
        error_mark(e)  # log it
        return PortalException()


# add resource type
def flask_restx_tail(plugin):
    import os
    import json
    import importlib
    from flask_restx import Namespace
    from yqn_project_cli.utils import load_module_from_pyfile
    from yqn_project_cli.utils.restx import DANamespace

    routes = json.load(
        open(os.path.join(plugin.app.project_config.project_base_dir,
                          'config/{}.json'.format(plugin.app.project_config.name)), 'r'))

    for route in routes['path_list']:
        # views = load_module_from_pyfile(os.path.join(api_path, module, 'views.py'))
        views = importlib.import_module('api.{}.views'.format(route['module']))
        # importlib.reload(views)

        for k, v in views.__dict__.items():
            if isinstance(v, DANamespace):

                add_view_mth_resource(v, getattr(getattr(views, route['view_cls']), route['view_mth']), route)

                plugin.add_namespace(v)

                break  # only allow one namespace

            elif isinstance(v, Namespace):
                raise ValueError('%s need inheriting from %s, rather than %s ' % (v, DANamespace, Namespace))


# decorator type
def flask_restx_tail_old(plugin):
    import os
    import importlib
    from flask_restx import Namespace
    from yqn_project_cli.utils import load_module_from_pyfile
    from yqn_project_cli.utils.restx import DANamespace

    api_path = os.path.join(plugin.app.project_config.project_base_dir, 'api')
    for module in os.listdir(api_path):
        if module.startswith(('_', '.')) \
                or not os.path.isdir(os.path.join(api_path, module)) \
                or not os.path.exists(os.path.join(api_path, module, 'views.py')):
            continue

        # views = load_module_from_pyfile(os.path.join(api_path, module, 'views.py'))
        views = importlib.import_module('api.{}.views'.format(module))
        # importlib.reload(views)

        for k, v in views.__dict__.items():
            if isinstance(v, DANamespace):
                plugin.add_namespace(v)

            elif isinstance(v, Namespace):
                raise ValueError('%s need inheriting from %s, rather than %s ' % (v, DANamespace, Namespace))


def close_rpc_services(e):
    for name, server in current_app.services.items():
        if name != (current_app.server_manager and current_app.server_manager[0]) and isinstance(server, RPCConfigBase):
            server.close()
