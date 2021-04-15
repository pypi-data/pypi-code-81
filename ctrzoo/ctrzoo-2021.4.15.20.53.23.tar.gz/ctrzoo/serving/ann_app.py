#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : ann_app
# @Time         : 2021/4/13 7:12 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


from ctrzoo.ann.recall_user import *
from appzoo import App

app = App()

if __name__ == '__main__':
    class ANN(Main):

        @feishu_hook('个性化垂类包', hook_url=get_zk_config('/mipush/bot')['垂类'])
        @feishu_catch()
        @args
        def main(self, **kwargs):
            date = kwargs.get('date', date_difference('%Y%m%d', days=1))
            part = kwargs.get('part', 0)

            user_vec_path = kwargs.get(
                'user_vec_path',
                f'/user/h_data_platform/platform/feeds/biz/biz=mitv_user_embedding/date={date}'
            )
            output = f"/user/h_data_platform/platform/feeds/mitv_profile_push/date={date}/ann"

            anns = []
            for file in tf_io.cp(user_vec_path, filter_fn=lambda p: int(Path(p).name[5:10]) % 10 == part):  # 1000份
                df = pd.read_parquet(file)
                ann = gensim.models.KeyedVectors(768)
                ann.add(df['userId'], np.row_stack(df['vector']), True)
                ann.init_sims(replace=True)
                anns.append(ann)


            def predict(**kwargs):
                docid = kwargs.get('docid')
                topk = int(kwargs.get('topk', 10))

                rs = []
                for ann in anns:
                    r = ann.wv.similar_by_vector(get_vec(docid), topk)
                    rs.append(r)
                return rs

            logger4feishu(LOCAL_HOST)

            app.add_route('/', predict, method="POST")
            app.run(port=8000)

            return self.__class__.__name__


    ANN.cli()
