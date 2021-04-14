# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/20
from yqn_project_cli.utils.core.as_flask import JSONResponse
from config import ProjectConfig


def heartbeats(*args, **kwargs):
    return JSONResponse(
        data={'app_id': ProjectConfig.id, 'app_status': "OK", 'engine_version': ProjectConfig.version_int}
    )
