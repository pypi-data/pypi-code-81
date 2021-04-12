#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AppZoo.
# @File         : mongo_item
# @Time         : 2021/4/12 7:17 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.db.mongo import Mongo

m = Mongo(url=None)
collection_name = 'item'
c = m.db[collection_name]


# df['date'] = datetime.datetime.utcnow()

@lru_cache()
def insert(**kwargs):
    # docid = kwargs.get('data', 'id')
    kwargs.pop('_id', None)

    c.insert(kwargs)
    return 'ok'


@lru_cache()
def query(**kwargs):
    key = kwargs.get('key', {})
    return c.find_one(key)


if __name__ == '__main__':
    from appzoo import App

    app = App()
    app.add_route('/mongocache/item/insert', insert, method="POST")
    app.add_route('/mongocache/item/query', query, method="GET")

    app.run(port=8000, access_log=False)
