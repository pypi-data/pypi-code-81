#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MICTRZOO.
# @File         : experiment_expired
# @Time         : 2021/3/22 3:11 下午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.zk_utils import get_zk_config
from meutils.log_utils import logger4feishu

cfg = get_zk_config('/mipush/experiment')

days = 7
if 'days' in cfg:
    days = cfg.pop('days')

today = datetime.datetime.today()
for exp_layer in cfg:
    logger.info(f"exp_layer: {exp_layer}")
    for expid2endtime in cfg[exp_layer]:
        for expid, endtime in expid2endtime.items():
            delta = (endtime - today).days
            if delta <= days:
                logger4feishu(
                    f"{exp_layer}",
                    f"实验**{expid}**还剩**{delta}**天过期, 如需充值请进 https://abtest.pt.xiaomi.com/#/dashboard",
                    '小米视频和多看push小分队',
                )

if __name__ == '__main__':
    """一大堆业务逻辑"""


    class TEST(Main):
        @args
        def main(self, **kwargs):
            pass


    TEST.cli()
