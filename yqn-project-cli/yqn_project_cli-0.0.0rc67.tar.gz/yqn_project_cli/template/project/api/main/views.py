# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/8
from yqn_project_cli.utils.restx import DANamespace
from yqn_project_cli.utils.core.as_flask import JSONResponse

# one module, one namespace, more will be ignored
ns = DANamespace('main', description='', path='/')


"""
import datetime
from yqn_project_cli.utils.core.as_flask import JSONResponse
from yqn_project_cli.utils.decorators import parse_request_with
from api.main.parser import MainIndexParser
from api.main.model import (
    RequestSchema,
    ResponseSchema
)

req = RequestSchema("Request")
res = ResponseSchema("Response")
ns.add_model('Request', req)
ns.add_model('Response', res)


class Swagger:

    @ns.doc(expect=[req])
    @ns.doc(responses={200: ("description", res)})
    @parse_request_with(MainIndexParser())
    def new_add(self, *args, **kwargs):
        return JSONResponse({'now': datetime.datetime.now()})
"""
