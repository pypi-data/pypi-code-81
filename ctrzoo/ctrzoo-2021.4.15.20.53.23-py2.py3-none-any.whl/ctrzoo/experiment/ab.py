#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : ab
# @Time         : 2021/3/16 10:30 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
from meutils.aizoo import tf_io
from meutils.date_utils import date_difference
from meutils.hash_utils import murmurhash
from meutils.pd_utils import df_split
from pypinyin import lazy_pinyin

magic_cmd("kinit -k -t ./data/s_feeds.keytab s_feeds@XIAOMI.HADOOP")

# 历史垂类包偶数用户+新垂类包奇数用户
# 覆盖历史包


if __name__ == '__main__':

    """资讯包下发时间0316 20:00"""
    # 划分实验的垂类包
    user_category = []
    # user_category = ['军事', '财经', '猎奇']
    # 拷贝新垂类包至木变路径
    # copy_new_user_category = ['小品', '少儿', '搞笑', '电影', '电视剧', '科技', '综艺', '游戏', '情感', '美女', '民生', '美食']
    # 做垂类向量vec实验的
    copy_new_user_category = ['小品', '少儿', '搞笑',
                              '影视', '动漫', '电视剧',
                              '科技', '游戏', '美女', '美食']
    # 不做实验的
    direct_copy_new_user_category = ['电影', '电视剧', '综艺', '情感', '美女', '民生', '美食', '情感', '民生']

    class AB(Main):

        @args
        def main(self, **kwargs):
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            input1 = kwargs.get(
                'input1',
                f'/user/h_data_platform/platform/feeds/mitv_profile_push/date={date}',
            )
            input2 = kwargs.get(
                'input2',
                '/user/h_data_platform/platform/feeds/biz/biz=profile_',
            )
            # "/user/h_data_platform/platform/feeds/biz/o2o_top_dura_32_item_strategy/profile2vec/biz=profile_  少儿/date=20210411"
            profile2vec_res = kwargs.get(
                'profile2vec_res',
                '/user/h_data_platform/platform/feeds/biz/o2o_top_dura_32_item_strategy/profile2vec/biz=profile_',
            )
            profile2vec_operator_res = kwargs.get(
                'profile2vec_res',
                '/user/h_data_platform/platform/feeds/biz/o2o_top_dura_32_item_strategy/profile2vec_operator/biz=profile_',
            )

            # user_category = ['资讯', '娱乐', '健康', '军事', '财经', '猎奇', '生活']  # 可从zk读取
            for user_cat in user_category:
                old_path = f"{input1}/{user_cat}"
                new_path = f"{input2}{user_cat}/date={date}"
                output = old_path

                # 跑数也是按hash取id分别join
                df1 = (
                    tf_io.read_hdfs(old_path, reader=lambda p: pd.read_csv(p, names=['userid']))
                        .drop_duplicates()[lambda df: df['userid'].map(lambda x: murmurhash(x, bins=2) == 0)]
                        .assign(hash_index=0)
                )
                df2 = (
                    tf_io.read_hdfs(new_path, reader=lambda p: pd.read_csv(p, names=['userid']))
                        .drop_duplicates()[lambda df: df['userid'].map(lambda x: murmurhash(x, bins=2) == 1)]
                        .assign(hash_index=1)
                )

                tf_io.cp(old_path, f"{old_path}.bak")  # 复制历史垂类包备份.bak
                tf_io.rm(old_path)  # 删除旧包

                df = pd.concat([df1, df2], ignore_index=True)

                # 存一份带hash索引的数据，便于统计实验效果
                tf_io.to_hdfs(
                    df,
                    f"/user/h_data_platform/platform/feeds/biz_date/biz=profile_{''.join(lazy_pinyin(user_cat))}/date={date}/DATA"
                )

                dfs = df_split(df[['userid']], batch_size=100000)
                for i, df in tqdm(enumerate(dfs)):
                    tf_io.df2write(df, f"{output}/part-{i}-merge")  # 数据必须以part-为前缀
                    time.sleep(3)

                tf_io.process_success(output)


            # ------------------- experiment1 : 垂类向量Gen策略实验 ------------------------

            for cp_user_cat in copy_new_user_category:
                in_path_1 = f"{profile2vec_res}{cp_user_cat}/date={date}"
                in_path_2 = f"{profile2vec_operator_res}{cp_user_cat}/date={date}"
                out_path = f"{input1}/{cp_user_cat}"
                df1 = pd.DataFrame(columns=['userid'])
                try:
                    df1 = (
                        tf_io.read_hdfs(in_path_1, reader=lambda p: pd.read_csv(p, names=['userid']))
                            .drop_duplicates()[lambda df: df['userid'].map(lambda x: murmurhash(x, bins=2) == 0)]
                            .assign(hash_index=0)
                    )
                except Exception:
                    pass

                df2 = pd.DataFrame(columns=['userid'])
                try:
                    df2 = (
                        tf_io.read_hdfs(in_path_2, reader=lambda p: pd.read_csv(p, names=['userid']))
                            .drop_duplicates()[lambda df: df['userid'].map(lambda x: murmurhash(x, bins=2) == 1)]
                            .assign(hash_index=1)
                    )
                except Exception:
                    pass

                if len(df1.index) == 0:
                    # 影视(无此分类)
                    df = df2
                elif len(df2.index) == 0:
                    df = df1
                else:
                    df = pd.concat([df1, df2], ignore_index=True)


                tf_io.to_hdfs(
                    df,
                    f"/user/h_data_platform/platform/feeds/biz_date/biz=profile_{''.join(lazy_pinyin(cp_user_cat))}/date={date}/DATA"
                )
                dfs = df_split(df[['userid']], batch_size=100000)
                for i, df in tqdm(enumerate(dfs)):
                    tf_io.df2write(df, f"{out_path}/part-{i}-merge")  # 数据必须以part-为前缀
                    time.sleep(3)
                tf_io.process_success(out_path)


            # ------------------- normal : 直接拷贝, copy 新垂类包 ------------------------

            for cp_user_cat in direct_copy_new_user_category:
                tf_io.cp(f"{input2}{cp_user_cat}/date={date}",
                         f"{input1}/{cp_user_cat}")

    AB().cli()
