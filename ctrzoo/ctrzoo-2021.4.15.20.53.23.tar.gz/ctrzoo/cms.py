#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : cms
# @Time         : 2021/4/13 5:34 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.db.mongo import Mongo
from meutils.date_utils import date_difference


m = Mongo(url=None)
collection_name = 'item'
c = m.db[collection_name]
_ = c.find_one({"push_item_meta1.start_time": date_difference('%Y-%m-%d 22:00:00')})
print(_)
