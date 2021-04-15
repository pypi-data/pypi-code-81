#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : cm_delte
# @Time         : 2021/4/6 5:54 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
from meutils.date_utils import date_difference

s = os.popen('cloudml jobs_v2 list | grep failed | grep yuanjie').read()
df = pd.DataFrame(s.split() | xgroup(5))
df = df[df[3].str[:10] <= date_difference(fmt='%Y-%m-%d', days=1)]

for job in df[1]:
    os.system(f'cloudml jobs_v2 delete {job}')
