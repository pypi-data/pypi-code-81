# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/13
from yqn_project_cli.utils.core.request import RequestSchemaBase
from yqn_project_cli.utils.core.response import ResponseSchemaBase


class RequestSchema(RequestSchemaBase):

    def get_model_schema(self):
        model = {'type': 'object', 'properties': {}}
        model['properties']['carrier_id'] = {
            'type': 'integer',
            'description': "carrier_id"
        }

        return model


class ResponseSchema(ResponseSchemaBase):

    def get_model_schema(self):
        model = {'type': 'object', 'properties': {}}
        model['properties']['version'] = {
            'type': 'string',
            'description': "version"
        }

        return model
