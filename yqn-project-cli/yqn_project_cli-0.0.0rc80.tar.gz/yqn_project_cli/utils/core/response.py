# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/13
from flask_restx import SchemaModel


class ResponseSchemaBase(SchemaModel):
    def __init__(self, name, schema=None):
        self.name = name
        response_params = self.get_response_params_schema() or schema or {}
        super(ResponseSchemaBase, self).__init__(self.name, response_params)

    def get_response_params_schema(self):
        header = {'type': 'object', 'properties': {}}
        header['properties']['xTraceId'] = {
            'type': 'string',
            'description': "调用链"
        }
        header['properties']['xAppId'] = {
            'type': 'string',
            'description': "调用方app id"
        }
        response_params = {
            "type": "object",
            "properties": {
                'success': {
                    'type': 'boolean',
                    'default': True
                },
                'header': header,
                "data": self.get_model_schema(),
                'msgCode': {
                    'type': 'string',
                },
                'code': {
                    'type': 'integer',
                },
                'msg': {
                    'type': 'string',
                },
                'msgDetail': {
                    'type': 'string',
                },
                'headers': {
                    'type': 'object',
                },
                'bizExtMap': {
                    'type': 'string',
                },
            }
        }
        return response_params

    def get_model_schema(self: dict):
        pass

