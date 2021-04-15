#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : update_ann
# @Time         : 2021/4/13 10:25 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : https://www.milvus.io/cn/blogs/2020-2-16-api-setting.md/


from meutils.decorators.feishu import *
from meutils.annzoo.ann import ANN
from meutils.zk_utils import zk

ips = zk.get_children('/mipush/ann/ips')
anns = list(map(ANN, ips))

# Create collection
collection_name = 'user_ann'
# [ann.user_ann.count for ann in anns]

# 参数
# nlist = 4 * sqrt(n)
fields = [
    {
        "name": "ann_part",
        "type": 'INT32',
        "params": {},
        "indexes": [{}]
    },
    {
        "name": "vector",
        "type": 'FLOAT_VECTOR',
        "params": {"dim": 768},
        "indexes": [
            {"index_type": 'IVF_FLAT', 'metric_type': 'IP', 'params': {'nlist': 2 ** 14}, 'index_file_size': 2 ** 12}
        ]
    }
]

if __name__ == '__main__':
    """一大堆业务逻辑"""


    class TEST(Main):
        @args
        def main(self, **kwargs):
            for ann in anns:
                ann.create_collection(collection_name, fields, overwrite=True)  # 每日重建ANN表


    TEST.cli()
