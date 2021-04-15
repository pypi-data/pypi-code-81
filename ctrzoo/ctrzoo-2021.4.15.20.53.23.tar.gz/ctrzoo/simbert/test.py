#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : test
# @Time         : 2021/3/10 12:18 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
from ctrzoo.utils import kinit
from ctrzoo.utils.db import Hive

kinit()

sql = """
select reachItems[0] from feeds.o2o_mivideo_push_log_info
where date >= 20210315
and reachItems[0].stockid in ('howtojp_Xw57wKRm45z7', 'fengxing_152323437', 'fengxing_152254771', 'fengxing_152311033')
limit 5
"""

df = Hive.query(sql)

print(df)

if __name__ == '__main__':
    """一大堆业务逻辑"""


    class TEST(Main):
        print("######")

        @args
        def main(self, **kwargs):
            pass


    TEST.cli()
