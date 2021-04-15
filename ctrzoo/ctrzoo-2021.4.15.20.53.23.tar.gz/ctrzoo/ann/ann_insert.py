#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : insert
# @Time         : 2021/4/13 8:51 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


from meutils.decorators.feishu import *
from meutils.aizoo import tf_io
from meutils.np_utils import normalize
from meutils.date_utils import date_difference
from meutils.db.mongo import Mongo

# project
from ctrzoo.ann.ann_create import anns, collection_name

mongo = Mongo(url=None)
browser_push_user_ann = mongo.db.browser_push_user_ann


@feishu_catch()
def ann_insert_fn(ann, p, ann_part):
    df = (
        pd.read_parquet(p)[['userId', 'vector']]
            .assign(ann_part=ann_part)
            .assign(vector=lambda df: normalize(np.row_stack(df['vector'])).tolist())  # 归一化
    )

    df['id'] = ann.__getattr__(collection_name).batch_insert(df)
    df['date'] = datetime.datetime.utcnow()

    # id mapping
    browser_push_user_ann.insert_many(
        df[['id', 'userId', 'ann_part', 'date']].to_dict('r'),
        False
    )


if __name__ == '__main__':

    class AnnInsert(Main):

        # @feishu_hook('更新ANN服务', hook_url='垂类')
        @feishu_catch('垂类')
        @args
        def main(self, **kwargs):
            part = kwargs.get('part', 0)  # 机器索引
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            user_vec_path = kwargs.get(
                'user_vec_path',
                f'/user/h_data_platform/platform/feeds/biz/biz=mitv_user_embedding/date={date}'
            )

            ann = anns[part]  # 分配ann服务

            def filter_fn(p, bins=100):  # 1000个文件，10台机器插入10个ANN服务，每个ANN服务100个分区
                index = int(Path(p).name[5:10])
                return index in range(part * bins, (part + 1) * bins)

            for file in tqdm(tf_io.cp(user_vec_path, filter_fn=filter_fn)):
                # 前100个文件都插入到第一台机器
                ann_insert_fn(ann, file, ann_part=int(Path(file).name[5:10]))

            return self.__class__.__name__


    AnnInsert.cli()
