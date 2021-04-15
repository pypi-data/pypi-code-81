'''
Description: tykit(TianYu Kit)
version:
Author: TianyuYuan
Date: 2021-04-02 15:40:39
LastEditors: TianyuYuan
LastEditTime: 2021-04-14 23:48:49
'''
name = "tykit"
from .pb_api import pb_range, pb_iter, pb_multi_thread, pb_multi_thread_partial
from .progressbar import ProgressBar
from .rlog import RLog


# * * * * * * * * * * * * * * * * * * * * * * * #
# * * * * * * Exclusive for AIBEE * * * * * * * #
# * * * * * * * * * * * * * * * * * * * * * * * #

from .facex_client import FacexClient   # 方便使用face-x服务
from .parse_np import ParseNP           # 解析np_samples.json的方法库
from .npsamples import NPsamples        # 对标注结果np_samples的进一步抽象，以samples.json作为对象，集成删除，显示信息等方法


if __name__ == "__main__":
    rlog.start('hello world')
