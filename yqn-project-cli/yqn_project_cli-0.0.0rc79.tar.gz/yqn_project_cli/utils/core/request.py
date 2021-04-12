# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/13
from flask_restx import SchemaModel


class RequestSchemaBase(SchemaModel):
    def __init__(self, name, schema=None):
        self.name = name
        request_params = self.get_request_params_schema() or schema or {}
        super(RequestSchemaBase, self).__init__(self.name, request_params)

    def get_request_params_schema(self):
        header = {'type': 'object', 'properties': {}}
        header['properties']['accessToken'] = {
            'type': 'string',
            'description': "accessToken"
        }
        header['properties']['viewAll'] = {
            'type': 'boolean',
            'default': True,
            'description': "是否展示所有"
        }
        header['properties']['xAppId'] = {
            'type': 'string',
            'description': "调用方app id"
        }
        header['properties']['xBPId'] = {
            'type': 'string',
            'description': "xBPId"
        }
        header['properties']['xCallerId'] = {
            'type': 'string',
            'description': "调用方请求ID"
        }
        header['properties']['xClientIp'] = {
            'type': 'string',
            'description': "客户端IP"
        }
        header['properties']['xDeviceId'] = {
            'type': 'string',
            'description': "设备ID"
        }
        header['properties']['xIsTest'] = {
            'type': 'boolean',
            'description': "xIsTest",
            'default': False,
        }
        header['properties']['xJsFinger'] = {
            'type': 'string',
            'description': "Js指纹"
        }
        header['properties']['xLangCode'] = {
            'type': 'string',
            'description': "语言"
        }
        header['properties']['xOpenId'] = {
            'type': 'string',
            'description': "开放ID"
        }
        header['properties']['xOpenPlatform'] = {
            'type': 'integer',
            'default': 0,
            'description': "开放平台"
        }
        header['properties']['xPushToken'] = {
            'type': 'string',
            'description': "app推送token"
        }
        header['properties']['xSession'] = {
            'type': 'string',
            'description': "登录的Session"
        }
        header['properties']['xSourceAppId'] = {
            'type': 'string',
            'description': "初始来源调用方app id"
        }
        header['properties']['xSystemLangCode'] = {
            'type': 'string',
            'description': "系统环境语言"
        }
        header['properties']['xTestFlag'] = {
            'type': 'string',
            'description': "xTestFlag"
        }
        header['properties']['xToken'] = {
            'type': 'string',
            'description': "xToken"
        }
        header['properties']['xTraceId'] = {
            'type': 'string',
            'description': "调用链"
        }
        header['properties']['xUserId'] = {
            'type': 'integer',
            'default': 0,
            'description': "用户ID"
        }
        header['properties']['xUserName'] = {
            'type': 'string',
            'description': "用户名"
        }
        request_params = {
            "type": "object",
            "properties": {
                'header': header,
                "model": self.get_model_schema()
            }
        }
        return request_params

    def get_model_schema(self):
        pass

