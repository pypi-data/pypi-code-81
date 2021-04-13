'''
Description: tykit(TianYu Kit)
version:
Author: TianyuYuan
Date: 2021-04-02 15:40:39
LastEditors: TianyuYuan
LastEditTime: 2021-04-06 22:40:48
'''
name = "tykit"
from .pb_api import pb_range, pb_iter, pb_multi_thread, pb_multi_thread_partial
from .progressbar import ProgressBar
from .rlog import RLog

rlog = RLog()

# only for aibees
from .facex_client import FacexClient
from .parse_np import ParseNP

pnp = ParseNP()

if __name__ == "__main__":
    rlog.start('hello world')
