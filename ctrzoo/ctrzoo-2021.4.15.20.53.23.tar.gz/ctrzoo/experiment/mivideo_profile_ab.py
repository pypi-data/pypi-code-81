#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : ab
# @Time         : 2021/3/16 10:30 上午
# @Author       : jiangbowen
# @Software     : PyCharm
# @Description  :
from meutils.pipe import *
from meutils.aizoo import tf_io
from meutils.date_utils import date_difference
from meutils.hash_utils import murmurhash
from meutils.pd_utils import df_split
from pypinyin import lazy_pinyin

magic_cmd("kinit -k -t ./data/s_feeds.keytab s_feeds@XIAOMI.HADOOP")

if __name__ == '__main__':

    exp_config_map = {
        "o2o_latest_32_item_strategy" : "3",
        # "push_latest_32_item_strategy" : "3"
    }

    # 划分实验的垂类包
    # user_category = ['军事', '财经', '猎奇']
    # 拷贝新垂类包至木变路径
    copy_new_user_category = ['情感', '美女', '民生', '美食']

    class AB(Main):

        @args
        def main(self, **kwargs):
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            current_profile_path_prefix = kwargs.get(
                'input1',
                f'/user/h_data_platform/platform/feeds/mitv_profile_push/date={date}',
            )
            o2o_strategy_profile_exp_path_prefix = kwargs.get(
                'input2',
                f'/user/h_data_platform/platform/feeds/biz/o2o_latest_32_item_strategy/biz=profile_',
            )

            # user_category = ['资讯', '娱乐', '健康', '军事', '财经', '猎奇', '生活']  # 可从zk读取
            # 资讯人群不够1000万, 不同量级垂类包采样做实验不置信，故故暂时先验证其他垂类包

            # 融合垂类包测试
            for user_cat in user_category:

                old_path = f"{current_profile_path_prefix}/{user_cat}"
                new_path = f"{o2o_strategy_profile_exp_path_prefix}{user_cat}/date={date}"
                output = old_path

                o2o_compare_df = (
                    tf_io.read_hdfs(old_path, reader=lambda p: pd.read_csv(p, names=['userid']))
                        .drop_duplicates()[lambda df: df['userid'].map(lambda x: murmurhash(x, bins=2) == 0)]
                        .assign(hash_index=0)
                )

                o2o_exp_df = (
                    tf_io.read_hdfs(new_path, reader=lambda p: pd.read_csv(p, names=['userid']))
                        .drop_duplicates()[lambda df: df['userid'].map(lambda x: murmurhash(x, bins=2) == 1)]
                        .assign(hash_index=1)
                )

                # 跑数也是按hash取id分别join

                tf_io.cp(old_path, f"{old_path}.bak")  # 复制历史垂类包备份.bak
                tf_io.rm(old_path)  # 删除旧包

                df = pd.concat([o2o_compare_df, o2o_exp_df], ignore_index=True)

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

            # copy 新垂类包
            for cp_user_cat in copy_new_user_category:
                tf_io.cp(f"{o2o_strategy_profile_exp_path_prefix}{cp_user_cat}/date={date}", f"{current_profile_path_prefix}/{cp_user_cat}")


    AB().cli()
