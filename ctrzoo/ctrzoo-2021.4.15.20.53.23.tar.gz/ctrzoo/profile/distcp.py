#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : copy_groups
# @Time         : 2021/3/1 8:05 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
"""
1. 垂类包监控
2. 垂类包同步

"""
from meutils.pipe import *
from meutils.aizoo import tf_io
from meutils.pd_utils import df_split
from meutils.date_utils import date_difference
from meutils.log_utils import logger4feishu
from meutils.zk_utils import get_zk_config
from meutils.decorators.feishu import feishu_catch, feishu_hook
from meutils.hash_utils import murmurhash

magic_cmd("kinit -k -t ./data/s_feeds.keytab s_feeds@XIAOMI.HADOOP")

# 获取垂类包
# profile2path = request('http://10.162.76.32:10101/recommend/push/getProfileConf?app=mitv')
# profile2path = {k: v for k, v in profile2path.items() if v.endswith('date=')}
r = get_zk_config(
    '/data/services/recommend/engine/mitvpushmaster/conf/files/mitv_profile.conf',
    'tjwqstaging.zk.hadoop.srv:2181',
    mode=''
)
profile2path = {
    x[0]: x[2].replace('"', '') for x in (r.strip().split()[6:-2] | xgroup)
    if x[2].startswith('"/user/h_miui_ad/dmp') or x[2].endswith('date="')
}
logger.debug(profile2path)


@feishu_catch()
def distcp(args, date):
    profile, path = args
    if not path.startswith('/user/h_miui_ad/dmp'):
        path = f"{path}{date}"
    output = f"/user/h_data_platform/platform/feeds/mitv_profile_push/date={date}/{profile}"

    if tf_io.check_path(f"{output}/_SUCCESS"): return  # 同步完的不再同步

    df = tf_io.read_hdfs(path, reader=lambda f: pd.read_csv(f, names=['userid']), cache_dir=profile)
    n = len(df)

    # 弃用
    dfs = df_split(df, batch_size=100000)
    for i, df in enumerate(dfs):
        tf_io.to_hdfs(df, f'{output}/part-{i}.tsv', with_success=False, cache_dir=f"{profile}_")
    tf_io.process_success(output)

    logger4feishu(profile, f"垂类包【{profile}】同步完成: {n / 10000:.2f} w \n{path}\n{output}", "小米视频垂类包建设")


if __name__ == '__main__':
    class Copy(Main):

        @args
        def main(self, **kwargs):
            # logger4feishu("垂类包同步作业", "START", "小米视频垂类包建设")

            part = kwargs.get('part', 0)
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            func = functools.partial(distcp, date=date)

            # list(profile2path.items())[-6:] | xThreadPoolExecutor(func, 4)

            for kv in profile2path.items():
                if murmurhash(kv[0], bins=3) == part:
                    func(kv)


    Copy.cli()
