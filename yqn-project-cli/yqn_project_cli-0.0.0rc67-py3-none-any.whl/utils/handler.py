# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/24
import os
import sys
import json
import os.path as op
import datetime
import inspect
import platform
import importlib

methods = ('get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace')

view_cls_template = '''

class {view_cls}:
    """{view_cls}'s doc"""
'''

view_mth_template = '''
    def {view_mth}(self, *args, **kwargs):
        """{doc}"""
        return JSONResponse()
'''

empty_init = """
# -*- coding: utf-8 -*-
# Author: {author}
# Date：{_date}
""".format(author=(platform.node() or 'SOMEBODY').upper(), _date=datetime.date.today().strftime('%Y/%m/%d')).lstrip()

empty_handler = empty_init

empty_model = empty_init.rstrip() + """
from yqn_project_cli.utils.core.request import RequestSchemaBase
from yqn_project_cli.utils.core.response import ResponseSchemaBase
"""
empty_parser = empty_init.rstrip() + """
from yqn_project_cli.utils.core.parser import (
    DAArgument,
    DARequestParser
)
'''

class DemoParser(DARequestParser):
    arg1 = DAArgument('arg1', required=True, type=int, location='args')
    arg2 = DAArgument('arg2', required=True, type=str, location='args')
'''

"""
empty_views = empty_init.rstrip() + """
from yqn_project_cli.utils.core.as_flask import JSONResponse
from yqn_project_cli.utils.restx import DANamespace

# one module, one namespace, more will be ignored
ns = DANamespace('{module}', description='', path='/')
"""

empties = {
    '__init__.py': empty_init,
    'handler.py': empty_handler,
    'model.py': empty_model,
    'parser.py': empty_parser,
    'views.py': empty_views,
}


def create_module(path, module_name):
    os.makedirs(op.join(path, module_name), exist_ok=False)

    for file, content in empties.items():
        if file == 'views.py':
            content = content.format(module=module_name)

        with open(op.join(path, module_name, file), 'w') as writer:
            writer.write(content)


def add_2_file(file_path, route):
    dst = view_cls_template.format(view_cls=route['view_cls'])

    if route.get('view_mth', False):
        dst += view_mth_template.format(view_mth=route['view_mth'], doc=route['doc'])

    else:
        raise ValueError('%s.%s must defined' % (route['view_cls'], route['view_mth']))

    with open(file_path, 'a') as writer:
        writer.write(dst)


def update_2_file(file_path, views, route):
    src = dst = inspect.getsource(getattr(views, route['view_cls']))

    if route.get('view_mth', False):
        if not getattr(getattr(views, route['view_cls']), route['view_mth'], False):
            dst += view_mth_template.format(view_mth=route['view_mth'], doc=route['doc'])
    else:
        raise ValueError('%s.%s must defined' % (route['view_cls'], route['view_mth']))

    if dst != src:
        with open(file_path, 'r') as reader:
            read_str = reader.read()

        read_str = read_str.replace(src, dst)

        with open(file_path, 'w') as writer:
            writer.write(read_str)


def auto_view(config, init=False):
    if op.join(config['app_path'], config['app_name']) not in sys.path:
        sys.path.append(op.join(config['app_path'], config['app_name']))

    routes = json.load(open(op.join(config['app_path'], config['app_name'],
                                    'config/{}.json'.format(config['app_name'])), 'rb'))

    for route in routes['path_list']:
        # not existed view_cls
        assert isinstance(route, dict), "path_list中的值需为对象"
        assert all([route["module"], route["view_cls"], route["http_methods"]]), \
            "module、view_cls、http_methods需为bool转换后为真数据"

        # create new module
        if not op.exists(op.join(config['app_path'], config['app_name'], 'api', route['module'])):
            create_module(op.join(config['app_path'], config['app_name'], 'api'), route['module'])

        file_path = op.join(config['app_path'], config['app_name'], 'api', route['module'], 'views.py')

        # init project by filling in views.py based on json-config
        if init:
            add_2_file(file_path, route)

        else:

            api_module = importlib.import_module('api')
            importlib.reload(api_module)

            views = importlib.import_module('api.{}.views'.format(route['module']))
            importlib.reload(views)

            if not getattr(views, route['view_cls'], False):
                add_2_file(file_path, route)

            else:
                update_2_file(file_path, views, route)

    if op.join(config['app_path'], config['app_name']) in sys.path:
        sys.path.pop(sys.path.index(op.join(config['app_path'], config['app_name'])))
