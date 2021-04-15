#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : ann_profile
# @Time         : 2021/4/14 5:50 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

"""
1. ANN召回 1w 用户，需要 5s
2. IdMapping 需要 1s

召回1000w用户预计需要 20 m, todo: 开启多进程多线程加速
"""

from meutils.decorators.feishu import *
from meutils.date_utils import date_difference
from meutils.pd_utils import df_split
from meutils.aizoo import tf_io

from meutils.http_utils.results import get_simbert_vectors
from meutils.db.mongo import Mongo

# project
from ctrzoo.ann.ann_create import anns

mongo = Mongo(url=None)
browser_push_user_ann = mongo.db.browser_push_user_ann


def recall_user(ann_part, ann, push_vec, topk=10000, nprobe=32, threshold=None):  # todo: 多条查询
    entities = ann.user_ann.search(
        push_vec, topk,
        nprobe=nprobe,
        scalar_list=[{'term': {'ann_part': [ann_part]}}]
    )
    if threshold is None:
        ids = entities.ids
    else:
        ids = np.array(entities.ids)[np.where(np.array(entities.distances) > threshold)[0]].tolist()
    r = browser_push_user_ann.find({"id": {'$in': ids}}, {'userId': 1, '_id': 0})  # 只返回 userId
    return pd.DataFrame(r)  # ['userId'].tolist()


if __name__ == '__main__':
    # TODO: 监控PUSH文案执行多次

    class AnnProfile(Main):

        @feishu_hook('ANN: AB-包已生成', hook_url='垂类')
        @feishu_catch('垂类')
        @args
        def main(self, **kwargs):
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            ann_path = kwargs.get(
                'out_path',
                f'/user/h_data_platform/platform/feeds/biz/biz=ann_profile/date={date}'  # todo: 垂类目录
            )
            zixun = kwargs.get(
                'args',
                f'/user/h_data_platform/platform/feeds/mitv_profile_push/date={date}/资讯'
            )
            # TODO: 获取审核之后的标题 or docid 【运营标题或者原始标题】
            itemid = 'TEST'
            push_vec = get_simbert_vectors('广东一主任医师在医院内坠楼身亡')

            # 召回 1000w，并采样一半的人
            args_list = enumerate(sum(([ann] * 100 for ann in anns), []))  # i, ann

            def func(args):
                return recall_user(*args, push_vec) # 下次定义函数

            df = (
                pd.concat(args_list | xThreadPoolExecutor(func, 32))
                [lambda df: df['userId'].map(lambda x: murmurhash(x, bins=2) == 1)]
            )
            logger.info(f"######{df.shape}")



            # 存一份带itemid索引的数据，便于统计实验效果: 这一半是动态的 公平？
            tf_io.to_hdfs(df.assign(itemid=itemid), f"{ann_path}/{itemid}")
            tf_io.to_hdfs(df, zixun, batch_size=100000)

            return self.__class__.__name__


    AnnProfile.cli()
