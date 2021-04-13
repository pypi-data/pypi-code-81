#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-02 17:38
    @Author : Yin Jian
    @Version：V 0.1
    @File : fingraph_data.py
    @desc :
"""
import datetime
import hashlib
import json
import random
import time
import typing
import pandas as pd
from typing import List

from datavita.core.auth import Auth
from datavita.core.common import contants
from datavita.core.transport.comrequests import CommonRequests
from datavita.core.transport.http import Request
from datavita.core.utils import log
from datavita.core.utils.middleware import Middleware
from datavita.fingraph.fingraph_apis import fingraph_apis_dict


def tid_mak():
    uuid_str = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
        [str(random.randint(1, 10)) for i in range(5)])
    return uuid_str


def _drop_prop(properties: dict, field: list):
    for f in field:
        del properties[f]
    return properties


def _convert_node(node_dict: dict):
    n = {}
    p = node_dict['properties']
    n['node_id'] = p['node_id']
    n['node_name'] = p['node_name']
    n['label'] = node_dict['label']
    del p['node_id']
    del p['node_name']
    n['properties'] = p
    return n


def _default_prop(prop: List[str], default_prop: List[str] = None, node=True):
    if prop is None:
        prop = []
    if default_prop is not None:
        prop.extend(default_prop)
    if node:
        prop.extend(['node_id', 'node_name'])
    else:
        prop.append('relationship_id')
    prop = list(set(prop))
    return prop


def _convert_relation(relation_dict: dict):
    n = {}
    p = relation_dict['properties']
    n['relationship_id'] = p['relationship_id']
    n['label'] = relation_dict['label']
    del p['relationship_id']
    n['properties'] = p
    return n


def _convert_path(path):
    p = []
    for i in range(len(path)):
        if i % 2 == 1:
            p.append(_convert_relation(path[i]))
        else:
            p.append(_convert_node(path[i]))
    return p


class FingraphData(object):
    """
        中台数据
        初始化固定参数 auth 超时 最大重试次数
    """

    def __init__(
            self,
            auth: typing.Optional[Auth] = None,
            base_url: str = contants.BASE_URL,
            timeout: int = contants.SESSION_PERIOD_TIMEOUT,
            max_retries: int = contants.MAX_RETRIES,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.auth = auth
        middleware = Middleware()
        self._middleware = middleware
        self.logger = log.default_logger

    def _send(self, api_name, action, api, params, max_retries, timeout):
        try:
            req = self._build_http_request(api_name, action, api, params=params)
            resp = CommonRequests(auth=self.auth, max_retries=max_retries, timeout=timeout).send(req=req)
        except Exception as e:
            return pd.DataFrame()
            raise e
        return self._middleware.logged_response_df_handler(self.auth, resp, resp.request.request_name)

    def _build_http_request(self, api_name, action, api, params) -> Request:
        nonce = tid_mak()
        timestamp = int(time.time())
        date_str = datetime.datetime.now()
        path_parm = api.replace(contants.BASE_URL, '')
        parm_md5 = hashlib.md5(str(json.dumps(params, ensure_ascii=False)).encode(encoding='UTF-8')).hexdigest()
        if action.upper() == 'GET':
            sign_str = f"""{action.upper()}\n*/*\n\n\n{date_str}\nx-datavita-nonce:{nonce}\nx-datavita-signature-method:HmacSHA1\n{path_parm}"""
        else:
            sign_str = f"""{action.upper()}\n*/*\n{parm_md5}\napplication/json\n{date_str}\nx-datavita-nonce:{nonce}\nx-datavita-signature-method:HmacSHA1\n{path_parm}"""
        signature = self.auth.make_authorization(sign_str)
        if action.upper() == 'GET':
            headers = {
                'Accept': '*/*',
                'x-datavita-key': '{}'.format(self.auth.access_id),
                'x-datavita-nonce': '{}'.format(nonce),
                'x-datavita-timestamp': '{}'.format(timestamp),
                'x-datavita-signature-method': 'HmacSHA1',
                'date': '{}'.format(date_str),
                'x-datavita-signature-headers': 'x-datavita-signature-method,x-datavita-nonce',
                'x-datavita-signature': '{}'.format(signature)
            }
        else:
            headers = {
                'Accept': '*/*',
                'Content-Type': 'application/json',
                'x-datavita-key': '{}'.format(self.auth.access_id),
                'x-datavita-nonce': '{}'.format(nonce),
                'x-datavita-timestamp': '{}'.format(timestamp),
                'x-datavita-signature-method': 'HmacSHA1',
                'date': '{}'.format(date_str),
                'x-datavita-signature-headers': 'x-datavita-signature-method,x-datavita-nonce',
                'x-datavita-signature': '{}'.format(signature)
            }
        return Request(
            request_name=api_name,
            url=api,
            method=action.upper(),
            data=params,
            headers=headers
        )

    def get_fingraph_data_by_group_id(self, group_id: str) -> pd.DataFrame:
        """
            根据图谱组获取datacode数据 get_fingraph_data_by_group_id()
        :param group_id: 图谱组代码
        :return:
        """
        url = fingraph_apis_dict.get('get_fingraph_data_by_group_id').format(base_url=self.base_url,
                                                                             group_id=str(group_id))
        return self._send(api_name="根据图谱组获取数据", action='get', api=url, params=None, max_retries=self.max_retries,
                          timeout=self.timeout)

    def _query_node(self, key: List[str], property: List[str], by_id=True):
        """
          根据节点名称查询节点详细信息
        :param key: 节点名称(或者节点id)的列表
        :param property:返回的属性列表
        :return:
        """
        property = _default_prop(property)
        if by_id:
            url = fingraph_apis_dict.get('query_node').format(base_url=self.base_url)
            p = {'nodeId': key,
                 'nodeProperty': property}
            df = self._send(api_name="根据节点id查询节点详细信息", action='post', api=url, params=p, max_retries=self.max_retries,
                            timeout=self.timeout)
        else:
            url = fingraph_apis_dict.get('query_node_detail').format(base_url=self.base_url)
            p = {'nodeName': key,
                 'nodeProperty': property}
            df = self._send(api_name="根据节点名称查询节点详细信息", action='post', api=url, params=p, max_retries=self.max_retries,
                            timeout=self.timeout)
        if df.shape[0] == 0:
            return pd.DataFrame(columns=['node_id', 'node_name', 'label', 'properties'])
        df['node_id'] = df['properties'].apply(lambda x: x['node_id'])
        df['node_name'] = df['properties'].apply(lambda x: x['node_name'])
        del df['id']
        df['properties'] = df['properties'].apply(lambda x: _drop_prop(x, ['node_id', 'node_name']))
        return df

    def query_node_detail(self, node_name: List[str], property=None):
        """
            根据节点名称查询节点详细信息
        :param node_name: 节点名称
        :param property:返回的属性列表
        :return:
        """
        return self._query_node(node_name, property, by_id=False)

    def query_node(self, node_id: List[str], property=None):
        """
            根据节点id查询节点详细信息
        :param node_id: 节点id
        :param property:返回的属性列表
        :return:
        """
        return self._query_node(node_id, property, by_id=True)

    def query_node_data_bind_info(self, node_id: List[str], data_node_property: List[str] = None,
                                  relationship_property: List[str] = None):
        """
            根据节点ID查询节点绑定的数据列表
        :param node_id: 节点id
        :param data_node_property:返回的数据节点属性
        :param relationship_property:返回的关系属性
        :return:
        """
        if data_node_property is None:
            data_node_property = ['node_id', 'node_name']
        data_node_property.append('node_id')
        data_node_property.append('node_name')
        data_node_property = list(set(data_node_property))
        if relationship_property is None:
            relationship_property = ['relationship_id', 'relationship_weight']
        relationship_property.append('relationship_id')
        relationship_property = list(set(relationship_property))
        p = {
            'nodeId': node_id,
            'nodeProperty': data_node_property,
            'relationProperty': relationship_property
        }
        url = fingraph_apis_dict.get('query_node_data_bind_info').format(base_url=self.base_url)
        df = self._send(api_name="根据节点ID查询节点绑定的数据列表", action='post', api=url, params=p, max_retries=self.max_retries,
                        timeout=self.timeout)
        if df.shape[0] == 0:
            return pd.DataFrame(columns=['node_id', 'data_node', 'relationship'])
        df['node_id'] = df['inNode'].apply(lambda x: x['properties']['node_id'])
        df['data_node'] = df['outNode'].apply(lambda x: _convert_node(x))
        df['relationship'] = df['relationship'].apply(lambda x: _convert_relation(x))
        del df['inNode']
        del df['outNode']
        return df

    def traversal_group_node(self, group_node_id: str, property: List[str] = None, include_children=False):
        """
            根据组节点ID遍历组内所有非数据节点
        :param group_node_id: 组节点id
        :param property:返回的节点属性
        :param include_children:是否包含字组（暂不支持）
        :return:
        """
        property = _default_prop(property)
        p = {
            'nodeId': group_node_id,
            'nodeProperty': property
        }
        url = fingraph_apis_dict.get('traversal_group_node').format(base_url=self.base_url)
        df = self._send(api_name="根据组节点ID遍历组内所有非数据节点", action='post', api=url, params=p, max_retries=self.max_retries,
                        timeout=self.timeout)
        if df.empty:
            return pd.DataFrame(columns=['node_id', 'node_name', 'label', 'properties'])
        df['node_name'] = df['properties'].apply(lambda x: x['node_name'])
        df['node_id'] = df['properties'].apply(lambda x: x['node_id'])
        df['properties'] = df['properties'].apply(lambda x: _drop_prop(x, ['node_id', 'node_name']))
        del df['id']
        return df

    def traversal_group_relationship(self, group_node_id: str,
                                     start_node_property=None,
                                     relationship_property=None,
                                     end_node_property=None,
                                     include_children=False):
        """
            根据组节点ID遍历组内所有非数据节点
        :param group_node_id: 组节点id
        :param start_node_property:返回的起点属性
        :param relationship_property:返回的关系属性
        :param end_node_property:返回的终点属性
        :param include_children:是否包含字组（暂不支持）
        :return:
        """
        relationship_property = _default_prop(relationship_property, ['direction_toggle'], node=False)
        end_node_property = _default_prop(end_node_property)
        start_node_property = _default_prop(start_node_property)
        p = {
            'nodeId': group_node_id,
            'relationProperty': relationship_property,
            'inNodeProperty': end_node_property,
            'outNodeProperty': start_node_property
        }
        url = fingraph_apis_dict.get('traversal_group_relationship').format(base_url=self.base_url)
        df = self._send(api_name="根据组节点ID遍历组内所有非数据节点", action='post', api=url, params=p, max_retries=self.max_retries,
                        timeout=self.timeout)
        if df.empty:
            return pd.DataFrame(columns=['factor', 'relationship', 'data_node'])
        df['factor'] = df['outNode'].apply(lambda x: _convert_node(x))
        df['data_node'] = df['inNode'].apply(lambda x: _convert_node(x))
        df['relationship'] = df['relationship'].apply(lambda x: _convert_relation(x))
        del df['outNode']
        del df['inNode']
        return df

    def traversal_group_data_relationship(self, group_node_id: str,
                                          factor_property=None,
                                          relationship_property=None,
                                          data_property=None,
                                          include_children=False):
        """
            根据组节点ID组内数据绑定关系信息
        :param group_node_id: 组节点id
        :param factor_property: 返回的factor点属性
        :param relationship_property:返回的关系属性
        :param data_property:返回数据点属性
        :param include_children:是否包含字组（暂不支持）
        :return:
        """
        relationship_property = _default_prop(relationship_property, ['relationship_weight'], node=False)
        data_property = _default_prop(data_property)
        factor_property = _default_prop(factor_property)
        p = {
            'nodeId': group_node_id,
            'nodeProperty': data_property,
            'factorProperty': factor_property,
            'relationProperty': relationship_property
        }
        url = fingraph_apis_dict.get('traversal_group_data_relationship').format(base_url=self.base_url)
        df = self._send(api_name="根据组节点ID组内数据绑定关系信息", action='post', api=url, params=p, max_retries=self.max_retries,
                        timeout=self.timeout)
        if df.empty:
            return pd.DataFrame(columns=['factor', 'relationship', 'data_node'])
        df['data_name'] = df['outNode'].apply(lambda x: _convert_node(x))
        df['factor'] = df['inNode'].apply(lambda x: _convert_node(x))
        df['relationship'] = df['relationship'].apply(lambda x: _convert_relation(x))
        del df['outNode']
        del df['inNode']
        return df

    def path_traversal(self, start_node_id: str, end_node_id: str, node_property: List[str] = None,
                       relation_property: [str] = None):
        """
             遍历起始节点和终止节点的路径
        :param start_node_id: 起始点id
        :param end_node_id: 结束点id
        :param node_property:返回点的属性
        :param relation_property:返回关系的属性
        :return:
        """
        node_property = _default_prop(node_property, node=True)
        relation_property = _default_prop(relation_property, ['relationship_weight', 'direction_toggle', 'direction'],
                                          node=False)
        p = {
            'startNodeId': start_node_id,
            'endNodeId': end_node_id,
            'nodeProperty': node_property,
            'relationProperty': relation_property
        }
        url = fingraph_apis_dict.get('path_traversal').format(base_url=self.base_url)
        df = self._send(api_name="遍历起始节点和终止节点的路径", action='post', api=url, params=p, max_retries=self.max_retries,
                        timeout=self.timeout)
        if df.empty:
            return pd.DataFrame(columns=['path', 'step'])
        df['step'] = df['length']
        del df['length']
        del df['weightMult']
        df['path'] = df['path'].apply(lambda x: _convert_path(x))
        return df

    def path_search(self, node_id: str,
                    node_property: List[str] = None,
                    relation_property: List[str] = None,
                    label: List[str] = None,
                    type: int = 1, step: int = 6):
        """
            根据节点id和步长 获取相关节点信息
       :param node_id: 起始点id(或结束点id)
       :param node_property: 返回点的属性
       :param relation_property:返回边的属性
       :param label:label为节点标签，如果用户设置了，那么只返回该类型的节点；否则返回全部类型的节点
       :param type:1为只返回以该节点向外发射的路径节点；-1为只返回射向该节点的路径节点；
       :param step:当type参数为空时，step最大为6；当type参数给定时，step最大为10
       :return:
       """
        relation_property = _default_prop(relation_property, node=False)
        node_property = _default_prop(node_property)
        if label is None:
            label = []
        p = {
            'nodeId': node_id,
            'step': step,
            'type': type,
            'label': label,
            'nodeProperty': node_property,
            'relationProperty': relation_property
        }
        url = fingraph_apis_dict.get('path_search').format(base_url=self.base_url)
        df = self._send(api_name="根据节点id和步长 获取相关节点信息", action='post', api=url, params=p, max_retries=self.max_retries,
                        timeout=self.timeout)
        if df.empty:
            return pd.DataFrame(columns=['path', 'step', 'weight'])
        df.rename(columns={'length': 'step', 'weightMult': 'weight'}, inplace=True)
        df['path'] = df['path'].apply(lambda x: _convert_path(x))
        return df

    def get_label_property(self, label: List[str]):
        """
            根据节点LABEL获取白名单属性列表
        :param label: 节点label列表
        :return:
        """
        p = {
            'label': label,
            'type': 1
        }
        url = fingraph_apis_dict.get('get_label_property').format(base_url=self.base_url)
        df = self._send(api_name="根据节点LABEL获取白名单属性列表", action='post', api=url, params=p, max_retries=self.max_retries,
                        timeout=self.timeout)
        if df.empty:
            return pd.DataFrame(columns=['label', 'name', 'cn_name'])
        df.rename(columns={'cnName': 'cn_name'}, inplace=True)
        return df
