#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : ann_v1
# @Time         : 2021/4/17 12:22 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
import copy
from meutils.pipe import *
from milvus import Milvus, DataType


class ANN(object):

    def __init__(self, host='10.46.242.23', port='19530', pool="SingletonThread", show_info=False):
        self.host = host
        self.client = Milvus(host, port, pool=pool)  # 线程池

        if show_info:
            logger.info(
                {
                    "ClientVersion": self.client.client_version(),
                    "ServerVersion": self.client.server_version()
                }
            )

    def __getattr__(self, collection_name) -> Collection:
        return Collection(collection_name, self.client)

    def create_collection(self, collection_name, fields, auto_id=True, segment_row_limit=4096, overwrite=True):
        """

        :param collection_name:
        :param fields: # type: BOOL INT32 INT64 FLOAT BINARY_VECTOR FLOAT_VECTOR
            fields = [
                {
                    "name": "scalar",
                    "type": 'INT32',
                    "params": {},
                    "indexes": [{}]
                },
                {
                    "name": "vector",
                    "type": 'FLOAT_VECTOR',
                    "params": {"dim": 768},
                    "indexes": [{"index_type": 'IVF_FLAT', 'metric_type': 'IP', 'params': {'nlist': 1024}, 'index_file_size': 1024}]
                }
            ]
        # index_file_size不确定放在哪生效
        :param auto_id:
        :param segment_row_limit: range 4096 ~ 4194304
        :return:
        """
        fields = copy.deepcopy(fields)  # fields[:]

        if self.client.has_collection(collection_name):
            if overwrite:
                logger.warning(f"{collection_name} already exists! to drop.")
                self.client.drop_collection(collection_name, timeout=300)
            else:
                return f"{collection_name} already exists!"

        vec_field = [_ for _ in fields if _.get('type', '').__contains__('VECTOR')][0]
        # assert len(vec_fields) > 0, "至少有一个矢量"

        for _ in fields:
            if 'type' in _:
                _['type'] = DataType.__getattr__(_['type'])

        collection_param = {
            "fields": fields,
            "auto_id": auto_id,
            "segment_row_limit": segment_row_limit,
        }

        # collection vector index
        self.client.create_collection(collection_name, fields=collection_param)

        self.client.create_index(collection_name, vec_field['name'], vec_field['indexes'][0])

        logger.info(f"{self.client.get_collection_info(collection_name)}")

    @property
    def collection_names(self):
        return self.client.list_collections()

    def __create_index(self, collection_name, field_name, index_type='IVF_FLAT', metric_type='IP', index_params=None):

        if index_params is None:
            index_params = {'nlist': 1024}

        params = {
            'index_type': index_type,
            # 'index_file_size': 1024, # TODO: 不确定放在哪生效
            'params': index_params,

            'metric_type': metric_type,
        }
        self.client.create_index(collection_name, field_name, params)  # field_name='embedding'
