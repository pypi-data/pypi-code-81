#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : auto_title
# @Time         : 2021/4/2 4:57 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
from meutils.date_utils import date_difference
from ctrzoo.utils.db import mysql_browser_conn as conn

date = date_difference("%Y%m%d", days=1)
sql = f"""
select distinct json_extract(task_data,'$.pushItemModels') as pushItemModels
from push_task_data
where app_id='browser'
and create_time >= unix_timestamp({date})
""".strip()

df = (
    pd.read_sql(sql, conn)
        .assign(pushItemModels=lambda df: df['pushItemModels'].map(json.loads))
        .explode('pushItemModels')
)
df['itemId'] = df['pushItemModels'].str['itemId']
df['title'] = df['pushItemModels'].str['title']
df['subTitle'] = df['pushItemModels'].str['subTitle']
df.pop('pushItemModels')

df.drop_duplicates(inplace=True)
