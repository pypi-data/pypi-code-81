import pytest
from holowan.HoloWAN import SubHoloWAN
# from holowan.HoloWAN import HoloWAN
import json
import os
from holowan.myUtils import MyUtil as mt

HoloWANIP = "192.168.1.223"
HoloWANPort = "8080"
engineID = 1
project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
POErrCode = mt.open_ini2("../holowan/resources/Holowan.ini", "PathOperateErrorCode")
PCErrCode = mt.open_ini2("../holowan/resources/Holowan.ini", "PathConfigErrorCode")
ok = "0"

add_path = [
    (-1, 2, "path2", POErrCode.getOption("engineIDError")),
    (4, 2, "path2", POErrCode.getOption("engineIDError")),
    (1, -1, "path16", POErrCode.getOption("pathIDError")),
    (1, 16, "path16", POErrCode.getOption("pathIDError")),
    (1, 2, "a"*200, POErrCode.getOption("pathNameError")),
    (1, 1, "path1", POErrCode.getOption("pathExist")),
    (1, 2, "PATH", ok),
    (1, 3, "PATH", ok),
    (1, 4, "PATH", ok),
    (1, 5, "PATH", ok),
    (1, 6, "PATH", ok),
    (1, 7, "PATH", ok),
    (1, 9, "PATH", ok),
    (1, 10, "PATH", ok),
    (1, 11, "PATH", ok),
    (1, 12, "PATH", ok),
    (1, 13, "PATH", ok),
    (1, 14, "PATH", ok),
    (1, 15, "PATH", ok)
    # (1, 2, None, -8)  #会直接报错，应该不会出现控制的情况
    # -14最多只能添加15条PATH 应该跟 -7有点相似，只要path_id是15以上的就会报-7，不知道怎么弄出-14来
]
open_path = [
    (-1, 2, POErrCode.getOption("engineIDError")),
    (4, 2, POErrCode.getOption("engineIDError")),
    (1, -1, POErrCode.getOption("pathIDError")),
    (1, 16, POErrCode.getOption("pathIDError")),
    (1, 1, ok),
    (1, 2, ok),
    (1, 8, POErrCode.getOption("openPathNotFound"))
]
remove_path = [
    (-1, 2, POErrCode.getOption("engineIDError")),
    (4, 2, POErrCode.getOption("engineIDError")),
    (1, -1, POErrCode.getOption("pathIDError")),
    (1, 16, POErrCode.getOption("pathIDError")),
    (1, 1, POErrCode.getOption("pathIsOpening")),
    (1, 2, POErrCode.getOption("pathIsOpening")),
    (1, 3, ok),
    (1, 4, ok),
    (1, 5, ok),
    (1, 6, ok),
    (1, 7, ok),
    (1, 8, POErrCode.getOption("removePathNotFound")),
    (1, 9, ok),
    (1, 10, ok),
    (1, 11, ok),
    (1, 12, ok),
    (1, 13, ok),
    (1, 14, ok),
    (1, 15, ok),
]
close_path = [
    (-1, 2, POErrCode.getOption("engineIDError")),
    (4, 2, POErrCode.getOption("engineIDError")),
    (1, -1, POErrCode.getOption("pathIDError")),
    (1, 16, POErrCode.getOption("pathIDError")),
    (1, 2, ok),
    (1, 3, POErrCode.getOption("closePathNotFound")),
]
path_direction_data = [
    (-1, 2, 1, PCErrCode.getOption("engineIDError")),
    (4, 2, 1, PCErrCode.getOption("engineIDError")),
    (1, -1, 1, PCErrCode.getOption("pathIDError")),
    (1, 16, 1, PCErrCode.getOption("pathIDError")),
    (1, 1, 1, ok),
    (1, 1, 2, ok),
    (1, 1, 3, ok),
    (1, 1, 4, PCErrCode.getOption("pathDirectionError")),
    (1, 15, 1, PCErrCode.getOption("pathNotFound"))
]
path_bandwidth_fixed_data = [
    (-1, 1, 1, 1000, 3, PCErrCode.getOption("engineIDError")),
    (4, 1, 1, 1000, 3, PCErrCode.getOption("engineIDError")),
    (1, -1, 1, 1000, 3, PCErrCode.getOption("pathIDError")),
    (1, 16, 1, 1000, 3, PCErrCode.getOption("pathIDError")),
    (1, 1, 1, 1000, 3, ok),
    (1, 1, 1, 1000, 3, ok),
    (1, 1, 3, 1000, 3, PCErrCode.getOption("pathDirectionError")),
    (1, 1, 4, 1000, 3, PCErrCode.getOption("pathDirectionError")),
    (1, 1, 1, 1000, 1, ok),
    (1, 1, 1, 1000, 2, ok),
    (1, 1, 1, 1000, 3, ok),
    (1, 1, 1, 1000, 4, PCErrCode.getOption("pathBandwidthRateUnitError"))
]
close_background_utilization_data = [
    (1, 1, 1, ok),
    (1, 1, 2, ok),
    (1, 2, 1, ok),
    (1, 1, 3, PCErrCode.getOption("pathDirectionError")),  # 等改好了再把注释去掉
    (4, 1, 1, PCErrCode.getOption("engineIDError")),
    (1, 8, 1, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, PCErrCode.getOption("pathIDError"))
]
set_background_utilization_data = [
    (1, 1, 1, 20, 64, ok),
    (1, 1, 2, 25, 32, ok),
    (1, 1, 2, 25, 128, ok),
    (1, 1, 2, 25, 9100, ok),  # 最大应该是9100，但是这里没有限制
    (1, 2, 1, 20, 64, ok),
    (1, 1, 1, 110, 64, PCErrCode.getOption("backgroundUtilizationRateError")),
    (1, 1, 1, -20, 64, PCErrCode.getOption("backgroundUtilizationRateError")),
    (1, 1, 3, 20, 64, PCErrCode.getOption("pathDirectionError")),
    (4, 1, 1, 20, 64, PCErrCode.getOption("engineIDError")),
    (1, 8, 1, 20, 64, PCErrCode.getOption("pathNotFound")),
    (1, 20, 1, 20, 64, PCErrCode.getOption("pathIDError"))
]
queue_limit_data = [
    # MS最大值为1000  KB最大值为10000 packets最大值为10000
    (1, 1, 1, 24, 2, ok),
    (1, 1, 1, 36, 1, ok),
    (1, 1, 1, 48, 3, ok),
    (1, 2, 1, 23, 3, ok),  # 这个有点问题，不能复现
    (1, 1, 1, 10001, 1, PCErrCode.getOption("queueDepthValueError")),
    (1, 1, 1, 10001, 2, PCErrCode.getOption("queueDepthValueError")),
    (1, 1, 1, 1001, 3, PCErrCode.getOption("queueDepthValueError")),  # 这个要等后端改好再测
    (4, 1, 1, 24, 2, PCErrCode.getOption("engineIDError")),
    (1, 8, 1, 24, 2, PCErrCode.getOption("pathNotFound")),
    (1, 1, 3, 24, 2, PCErrCode.getOption("pathDirectionError")),
    (1, 16, 1, 24, 1, PCErrCode.getOption("pathIDError")),
    (1, 1, 1, 64, 4, PCErrCode.getOption("queueDepthTypeError"))

]
close_message_modify_data = [
    (1, 1, 1, ok),
    (1, 1, 2, ok),
    (1, 2, 3, PCErrCode.getOption("pathDirectionError")),
    (1, 16, 1, PCErrCode.getOption("pathIDError")),
    (1, 8, 1, PCErrCode.getOption("pathNotFound")),
    (1, 2, 1, ok),
    (4, 1, 1, PCErrCode.getOption("engineIDError"))
]
set_message_modify_normal_data = [
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", ok),
    (4, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", PCErrCode.getOption("engineIDError")),
    (1, 8, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 1, 0, 1, "FF", 1, 0, 1, "AA", PCErrCode.getOption("pathDirectionError")),
    (1, 1, 1, 3, 0, 1, "FF", 1, 0, 1, "AA", PCErrCode.getOption("messageModifyMatchTypeError")),  # 这个有问题，该报错不报错
    (1, 1, 1, 7, 0, 1, "FF", 1, 0, 10, "AA", PCErrCode.getOption("messageModifySizeError")),
    (1, 1, 1, 1, 0, 1, "FF", 8, 0, 1, "AA", ok),
    (1, 1, 1, 1, 0, 1, "FF", 3, 0, 1, "AA", "-500"),  # 这个没有错误码，只有一个-500
    # (1, 1, 1, 1, 9100, 1, "FF", 1, 0, 1, "AA", ok),  # 如果后端改好了，这个不会报错
    (1, 1, 1, 1, 9101, 1, "FF", 1, 0, 1, "AA", PCErrCode.getOption("messageModifyMatchOffsetError")),
    # (1, 1, 1, 1, 0, 1, "FF", 1, 9100, 1, "AA", ok),  # 如果后端改好了，这个不会报错
    (1, 1, 1, 1, 0, 1, "FF", 1, 9101, 1, "AA", PCErrCode.getOption("messageModifyOffsetError")),
    (1, 1, 1, 1, 0, 3, "FF", 1, 0, 1, "AA", PCErrCode.getOption("messageModifyMatchSizeError")),
    (1, 1, 1, 1, 0, 1, "GG", 1, 0, 1, "FF", PCErrCode.getOption("messageModifyMatchValueError")),
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "GG", PCErrCode.getOption("messageModifyValueError")),
]
set_message_modify_cycle_data = [
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", 1000, 10, ok),
    (4, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", 1000, 10, PCErrCode.getOption("engineIDError")),
    (1, 8, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", 1000, 10, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", 1000, 10, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 1, 0, 1, "FF", 1, 0, 1, "AA", 1000, 10, PCErrCode.getOption("pathDirectionError")),
    (1, 1, 1, 3, 0, 1, "FF", 1, 0, 1, "AA", 1000, 10, PCErrCode.getOption("messageModifyMatchTypeError")),  # 这个有问题，该报错不报错
    (1, 1, 1, 7, 0, 1, "FF", 1, 0, 10, "AA", 1000, 10, PCErrCode.getOption("messageModifySizeError")),
    (1, 1, 1, 1, 0, 1, "FF", 8, 0, 1, "AA", 1000, 10, ok),
    (1, 1, 1, 1, 0, 1, "FF", 3, 0, 1, "AA", 1000, 10, "-500"),  # 这个没有错误码，只有一个-500
    # (1, 1, 1, 1, 9100, 1, "FF", 1, 0, 1, 1000, 10, "AA", ok),  # 如果后端改好了，这个不会报错
    (1, 1, 1, 1, 9101, 1, "FF", 1, 0, 1, "AA", 1000, 10, PCErrCode.getOption("messageModifyMatchOffsetError")),
    # (1, 1, 1, 1, 0, 1, "FF", 1, 9100, 1, "AA", 1000, 10, ok),  # 如果后端改好了，这个不会报错
    (1, 1, 1, 1, 0, 1, "FF", 1, 9101, 1, "AA", 1000, 10, PCErrCode.getOption("messageModifyOffsetError")),
    (1, 1, 1, 1, 0, 3, "FF", 1, 0, 1, "AA", 1000, 10, PCErrCode.getOption("messageModifyMatchSizeError")),
    (1, 1, 1, 1, 0, 1, "GG", 1, 0, 1, "FF", 1000, 10, PCErrCode.getOption("messageModifyMatchValueError")),
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "GG", 1000, 10, PCErrCode.getOption("messageModifyValueError")),
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", 20, 21, PCErrCode.getOption("cycleBurstMoreThanCyclePeriod")),
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", -100, 10, PCErrCode.getOption("messageModifyCyclePeriodError")),  # 找不到正整数可以得出这个错误码
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", 1000, -1, PCErrCode.getOption("messageModifyCycleBurst")),  # 同理。。
]
set_message_modify_random_data = [
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", 20.0, ok),
    (4, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", 20.0, PCErrCode.getOption("engineIDError")),
    (1, 8, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", 20.0, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 1, 0, 1, "FF", 1, 0, 1, "AA", 20.0, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 1, 0, 1, "FF", 1, 0, 1, "AA", 20.0, PCErrCode.getOption("pathDirectionError")),
    (1, 1, 1, 3, 0, 1, "FF", 1, 0, 1, "AA", 20.0, PCErrCode.getOption("messageModifyMatchTypeError")),  # 这个有问题，该报错不报错
    (1, 1, 1, 7, 0, 1, "FF", 1, 0, 10, "AA", 20.0, PCErrCode.getOption("messageModifySizeError")),
    (1, 1, 1, 1, 0, 1, "FF", 8, 0, 1, "AA", 20.0, ok),
    (1, 1, 1, 1, 0, 1, "FF", 3, 0, 1, "AA", 20.0, "-500"),  # 这个没有错误码，只有一个-500
    # (1, 1, 1, 1, 9100, 1, "FF", 1, 0, 1, "AA", 20.0, ok),  # 如果后端改好了，这个不会报错
    (1, 1, 1, 1, 9101, 1, "FF", 1, 0, 1, "AA", 20.0, PCErrCode.getOption("messageModifyMatchOffsetError")),
    # (1, 1, 1, 1, 0, 1, "FF", 1, 9100, 1, "AA", 20.0, ok),  # 如果后端改好了，这个不会报错
    (1, 1, 1, 1, 0, 1, "FF", 1, 9101, 1, "AA", 20.0, PCErrCode.getOption("messageModifyOffsetError")),
    (1, 1, 1, 1, 0, 3, "FF", 1, 0, 1, "AA", 20.0, PCErrCode.getOption("messageModifyMatchSizeError")),
    (1, 1, 1, 1, 0, 1, "GG", 1, 0, 1, "FF", 20.0, PCErrCode.getOption("messageModifyMatchValueError")),
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "FF", 20.0, PCErrCode.getOption("messageModifyValueError")),
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "FF", 110.0, PCErrCode.getOption("modifyRandomRateError")),
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "FF", -20.0, PCErrCode.getOption("modifyRandomRateError")),
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "FF", 1.123, ok),
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "FF", 1.10, ok),
    (1, 1, 1, 1, 0, 1, "FF", 1, 0, 1, "FF", 1.2345, PCErrCode.getOption("modifyRandomRateError")),
]
# 2020/10/27
close_mtu_limit_data = [
    (1, 1, 1, ok),
    (4, 1, 1, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, PCErrCode.getOption("pathDirectionError"))  # 这个错了，等一下要写在看板上 输出-500, 应为-10
]
set_mtu_limit_data = [
    (1, 1, 1, 9000, ok),  # 有问题, 最大值web前端为9216, web后端为9000
    (1, 1, 1, 9217, PCErrCode.getOption("mtuLimitValueError")),  # 超出之后api返回值也有问题, 返回-38, 应为 -36
    (4, 1, 1, 1500, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 1500, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 1500, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 1500, PCErrCode.getOption("pathDirectionError"))
]
set_frame_overhead_data = [
    (1, 1, 1, 1, 24, ok),
    (4, 1, 1, 1, 24, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 1, 24, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 1, 24, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 1, 24, PCErrCode.getOption("pathDirectionError")),
    (1, 1, 1, 4, 24, "-500"),  # 这个没有对应的错误码, 貌似可以不管了
    (1, 1, 1, 3, 65, "-500"),  # 最大值不受限, 在type为3时, rate的最大值应为64
    (1, 1, 1, 2, 64, ok),  # 在type不为3的时候, rate设置无效, 不用修改
]
set_delay_constant_data = [
    (1, 1, 1, 10000.0, ok),  # 还是没有将float自动转换成int, 火大
    (1, 1, 1, 60001.0, PCErrCode.getOption("constantDelayValueError")),  # 前端限制为10000.0, 后端限制为65536.0
    (1, 1, 1, 1500.12, "-500"),  # 两位小数返回-500, 用-68会比较好
    (4, 1, 1, 10000.0, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 10000.0, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 10000.0, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 10000.0, PCErrCode.getOption("pathDirectionError")),
    (1, 1, 1, 10000, ok),  # 自动类型转换
]
set_delay_uniform_data = [
    (1, 1, 1, 1.0, 50.0, 1, ok),
    (1, 1, 1, 1.0, 50.0, 0, ok),
    (1, 1, 1, 1.0, 50.0, 2, "-500"),  # -500可以看后面的详细描述
    (4, 1, 1, 1.0, 50.0, 1, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 10.0, 50.0, 1, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 10.0, 50.0, 1, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 10.0, 50.0, 1, PCErrCode.getOption("pathDirectionError")),
    # ↓ 前后端范围不一致, 前端为10000, 后端范围为65535, 返回值为-71(为空), 应为-72(值错误)
    (1, 1, 1, 0.1, 60000.1, 1, PCErrCode.getOption("uniformDelayValueError")),
    (1, 1, 1, 50.0, 1.0, 1, PCErrCode.getOption("uniformDelayValueError")),  # 大小顺序反了才是-72?
    (1, 1, 1, 1, 50, 1, ok),  # 自动类型转换
]
set_delay_normal_data = [
    (1, 1, 1, 1.0, 50.0, 10.0, 1, ok),
    (4, 1, 1, 1.0, 50.0, 10.0, 1, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 1.0, 50.0, 10.0, 1, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 1.0, 50.0, 10.0, 1, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 1.0, 50.0, 10.0, 1, PCErrCode.getOption("pathDirectionError")),
    # 下面的均没有报错
    (1, 1, 1, 50.0, 1.0, 10.0, 1, "-500"),  # min不能比mean大, 后端没有限制
    (1, 1, 1, 1.0, 52.0, 9951.0, 1, "-500"),  # 标准差不受限制, 前端限制为mean+std<=10000
    (1, 1, 1, 50.0, 50.0, 10.0, 1, "-500"),  # 最小值与期望不能相同, 后端没有限制
]
set_delay_normal_advanced_data = [
    (1, 1, 1, 1.0, 50.0, 10.0, 1, 6000.1, 4000.1, 900.0, 1000.0, ok),  # 前端的单位为s, 后端的单位为ms
    (4, 1, 1, 1.0, 50.0, 10.0, 1, 6000.1, 1000.1, 900.0, 1000.0, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 1.0, 50.0, 10.0, 1, 6000.1, 1000.1, 900.0, 1000.0, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 1.0, 50.0, 10.0, 1, 6000.1, 1000.1, 900.0, 1000.0, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 1.0, 50.0, 10.0, 1, 6000.1, 1000.1, 900.0, 1000.0, PCErrCode.getOption("pathDirectionError")),
    # 危险行为
    (1, 1, 1, 1.0, 50.0, 10.0, 1, 6000.1, 4000.1, 10000.0, 10000.0, "-500"),  # 没报错
    (1, 1, 1, 1.0, 50.0, 10.0, 1, 6000.1, 4000.1, 10001.0, 10000.0,
     PCErrCode.getOption("delayNormalAdvancedMinMoreThanMax")),  # 最小值比最大值大，返回-164
    (1, 1, 1, 1.0, 50.0, 10.0, 1, 3600001.0, 3600000.0, 9999.0, 10000.0,
     PCErrCode.getOption("delayNormalAdvancedPeriodError")),  # Period最大值为3600s, 即1小时
    (1, 1, 1, 1.0, 50.0, 10.0, 1, 3600000.0, 3600001.0, 9999.0, 10000.0,
     PCErrCode.getOption("delayNormalAdvancedDurationError")),
    (1, 1, 1, 1.0, 9900.1, 10.0, 1, 6000.1, 4000.1, 10000.0, 10000.0, "-500"),  # mean+std应小于10000
    (1, 1, 1, 1.0, 9900.0, 10.1, 1, 6000.1, 4000.1, 10000.0, 10000.0, "-500"),  # mean+std应小于10000
    (1, 1, 1, 9900.0, 9900.0, 10.0, 1, 6000.1, 4000.1, 10000.0, 10000.0, "-500"),  # 最小值等于期望
    (1, 1, 1, 9901.0, 9900.0, 10.0, 1, 6000.1, 4000.1, 10000.0, 10000.0, "-500"),  # 最小值大于期望
    # 暂时写这么多先
]
# engine_id, path_id, path_direction, mean_delay, min_delay, max_delay, positive_delta, negative_delta, spread,
# enable_reordering, expect
set_delay_custom_data = [
    (1, 1, 1, 200.0, 1.0, 1000.0, 99.9, 99.9, 1.58, 1, ok),
    (4, 1, 1, 200.0, 1.0, 1000.0, 99.9, 99.9, 1.58, 1, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 200.0, 1.0, 1000.0, 99.9, 99.9, 1.58, 1, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 200.0, 1.0, 1000.0, 99.9, 99.9, 1.58, 1, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 200.0, 1.0, 1000.0, 99.9, 99.9, 1.58, 1, PCErrCode.getOption("pathDirectionError")),
    # (1, 1, 1, 60001.0, 1.0, 1000.0, 99.9, 99.9, 1.58, 1, ok),  # 不要运行这个用例，会导致死机
]
# 10/28
loss_random_data = [
    # 正常参数，应该要全部返回ok
    (1, 1, 1, 1, ok),  # rate为整数
    (1, 1, 1, 1.123, ok),  # rate取3位小数
    (1, 1, 1, 100.0, ok),  # rate取最大值
    (1, 1, 1, 0.001, ok),  # rate最小值
    (1, 1, 1, 0, ok),  # 设置为0
    # 错误参数， 应返回错误码
    (4, 1, 1, 1, PCErrCode.getOption("engineIDError")),  # 引擎错误
    (1, 4, 1, 1, PCErrCode.getOption("pathNotFound")),  # path没创建
    (1, 16, 1, 1, PCErrCode.getOption("pathIDError")),  # path号码太大
    (1, 1, 3, 1, PCErrCode.getOption("pathDirectionError")),  # 链路方向错误
    (1, 1, 1, -1, PCErrCode.getOption("lossRandomRateError")),  # 下越界
    (1, 1, 1, 100.001, PCErrCode.getOption("lossRandomRateError")),  # 上越界
]
loss_cycle_data = [
    # 正常情况, 主要是period跟burst两个参数, 0<burst<period<9999999
    (1, 1, 1, 1000, 10, ok),
    (1, 1, 1, 9999999, 1, ok),
    (1, 1, 1, 9999999, 9999998, ok),
    (1, 1, 1, 2, 1, ok),
    # 错误情况
    (4, 1, 1, 1000, 10, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 1000, 10, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 1000, 10, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 1000, 10, PCErrCode.getOption("pathDirectionError")),
    (1, 1, 1, 10000000, 9999999, "-500"),  # 上越界, 暂时不知道给什么错误码
    (1, 1, 1, 1000, 0, PCErrCode.getOption("lossCyclePeriodError")),  # 下越界
    # (1, 1, 1, 1000, -1, ok),  # 下越界, -1转成了unsigned int型, 变得很大
    (1, 1, 1, 1000, 1001, PCErrCode.getOption("lossCycleBurstMoreThanPeriod")),  # burst比period大, 危险
]
loss_burst_data = [
    # 正常情况
    (1, 1, 1, 10.0, 1000, 2000, ok),
    (1, 1, 1, 10.0, 9999998, 9999999, ok),  # 最大值为9999999
    (1, 1, 1, 10, 0, 1, ok),  # probability为整数的情况
    (1, 1, 1, 10.0, 0, 0, ok),  # 两个都是0也可以
    (1, 1, 1, 1.123, 1000, 2000, ok),  # 支持小数点后三位
    (1, 1, 1, 100.0, 1000, 2000, ok),  # 概率为最大值的情况
    (1, 1, 1, 0.0, 1000, 2000, ok),  # 概率为最小值的情况
    # engine path direction 错误
    (4, 1, 1, 10.0, 1000, 2000, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 10.0, 1000, 2000, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 10.0, 1000, 2000, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 10.0, 1000, 2000, PCErrCode.getOption("pathDirectionError")),
    # 参数越界
    (1, 1, 1, 100.1, 1000, 2000, PCErrCode.getOption("lossBurstProbabilityError")),  # 概率上越界
    (1, 1, 1, -1.0, 1000, 2000, PCErrCode.getOption("lossBurstProbabilityError")),  # 概率下越界
    (1, 1, 1, 10.0, 9999999, 10000000, "-500"),  # max值上越界
    (1, 1, 1, 10.0, -1, 2000, PCErrCode.getOption("lossBurstMinMoreThanMax")),  # min值下越界
    (1, 1, 1, 10.0, 2000, 1000, PCErrCode.getOption("lossBurstMinMoreThanMax")),  # min值比max值大, 可能导致死机!!

]
loss_dual_data = [
    # 正常的情况
    (1, 1, 1, 10.0, 10.0, 10.0, 10.0, ok),
    (1, 1, 1, 10, 10, 10, 10, ok),  # 整数的情况
    (1, 1, 1, 10.123, 10.123, 10.123, 10.123, ok),  # 支持三位小数
    (1, 1, 1, 0, 0, 0, 0, ok),  # 全部取最小值
    (1, 1, 1, 100, 100, 100, 100, ok),  # 全部取最大值
    # engine path 等错误
    (4, 1, 1, 10, 10, 10, 10, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 10, 10, 10, 10, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 10, 10, 10, 10, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 10, 10, 10, 10, PCErrCode.getOption("pathDirectionError")),
    # 概率超出上限, 每个位置超出都会报不同的错误
    (1, 1, 1, 100.1, 10, 10, 10, PCErrCode.getOption("lossDualGoodLossError")),
    (1, 1, 1, 10, 100.1, 10, 10, PCErrCode.getOption("lossDualGoodChangeError")),
    (1, 1, 1, 10, 10, 100.1, 10, PCErrCode.getOption("lossDualBadLossError")),
    (1, 1, 1, 10, 10, 10, 100.1, PCErrCode.getOption("lossDualBadChangeError")),
    # 概率低于下限, 每个位置超出都会报不同的错误
    (1, 1, 1, -1.1, 10, 10, 10, PCErrCode.getOption("lossDualGoodLossError")),
    (1, 1, 1, 10, -1.1, 10, 10, PCErrCode.getOption("lossDualGoodChangeError")),
    (1, 1, 1, 10, 10, -1.1, 10, PCErrCode.getOption("lossDualBadLossError")),
    (1, 1, 1, 10, 10, 10, -1.1, PCErrCode.getOption("lossDualBadChangeError")),

    (1, 1, 1, 10.1234, 10.1234, 10.1234, 10.1234, "-500"),  # 要报错才对, 但是没有相应错误码
]
ber_data = [
    (1, 1, 1, 1, -14, ok),  # 正常情况
    (1, 1, 1, 0, -14, ok),  # value取最小值
    (1, 1, 1, 10, -14, ok),  # value取最大值
    (1, 1, 1, 1, -18, ok),  # index取最大值
    (1, 1, 1, 1, -1, ok),  # index取最小值
    # engine path 等错误
    (4, 1, 1, 1, -14, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 1, -14, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 1, -14, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 1, -14, PCErrCode.getOption("pathDirectionError")),
    # 越界的情况, 下面都没有限制, 改正后应填入相应的错误码
    (1, 1, 1, -1, -14, "-500"),  # value下越界
    (1, 1, 1, 11, -14, "-500"),  # value上越界
    (1, 1, 1, 1, 0, "-500"),  # index上越界
    (1, 1, 1, 1, -19, "-500"),  # index 下越界
]
reordering_normal_data = [
    # 正常情况
    (1, 1, 1, 5.0, 10.0, 20.0, ok),
    (1, 1, 1, 5, 10, 20, ok),  # 整数
    (1, 1, 1, 20.0, 10.0, 20.0, ok),  # Probability取最大值
    (1, 1, 1, 5.0, 0, 10000, ok),  # max取最大值, min取最小值
    (1, 1, 1, 0, 0, 0, ok),  # 全部取0(最小值)
    (1, 1, 1, 1.123, 10.1, 20.1, ok),  # Probability取三位小数
    # engine path 等错误
    (4, 1, 1, 5.0, 10.0, 20.0, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 5.0, 10.0, 20.0, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 5.0, 10.0, 20.0, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 5.0, 10.0, 20.0, PCErrCode.getOption("pathDirectionError")),
    # 越界的情况
    (1, 1, 1, 21.0, 10.0, 20.0, "-500"),  # Probability上越界
    (1, 1, 1, -1.0, 10.0, 20.0, PCErrCode.getOption("reorderingProbabilityError")),  # Probability下越界
    (1, 1, 1, 5, -1, 20, PCErrCode.getOption("reorderingMinError")),  # min下越界
    (1, 1, 1, 5, 10, 10001, "-500"),  # max上越界
    (1, 1, 1, 5, 20, 10, "-500"),  # min大于max
    # 小数精度问题, pythonAPI已经做了限制
    (1, 1, 1, 1.1234, 10.0, 20.0, "-500"),  # Probability取四位小数
    (1, 1, 1, 1.123, 10.12, 20.0, "-500"),  # min取2位小数
    (1, 1, 1, 1.123, 10.0, 20.12, "-500"),  # max取2位小数
]
duplication_data = [
    # 正常情况
    (1, 1, 1, 20.000, ok),
    (1, 1, 1, 20, ok),  # 整数
    (1, 1, 1, 100, ok),  # 最大值
    (1, 1, 1, 0, ok),  # 最小值
    (1, 1, 1, 20.123, ok),  # 三位小数
    # engine path 等错误
    (4, 1, 1, 20, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 20, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 20, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 20, PCErrCode.getOption("pathDirectionError")),
    # 越界的情况
    (1, 1, 1, -1, PCErrCode.getOption("duplicationProbabilityError")),
    (1, 1, 1, 100.1, PCErrCode.getOption("duplicationProbabilityError")),
    # 精度问题 python Api已经解决
    (1, 1, 1, 10.1234, "-500"),

]


@pytest.fixture()
def resetEngine():
    hw = SubHoloWAN(HoloWANIP, HoloWANPort)
    ret = hw.resetEngine()
    assert json.loads(ret)['errCode'] == ok


class TestHold:
    hw = SubHoloWAN(HoloWANIP, HoloWANPort)

    def test_hold_engine(self):
        self.hold_engine(4123456789, 4123456789, 0)
        self.hold_engine(0, 2345, 0)
        self.hold_engine(4321, 4321, -4)
        ret = json.loads(str(self.hw.hold_engine()))
        assert int(ret['errCode']) == -4
        self.hold_engine(4123456789, 4123456789, 0)

    def hold_engine(self, password, new_password, errcode):
        s = self.hw.hold_engine(password=int(password), new_password=int(new_password))
        ret = json.loads(str(s))
        assert int(ret['errCode']) == errcode

    def test_get_holowan_info(self):
        ret = self.hw.get_HoloWAN_information()
        assert isinstance(ret, str)


# 测试链路的增删、启动关闭、损伤参数等等
class TestPath:
    hw = SubHoloWAN(HoloWANIP, HoloWANPort)

    def setup_class(self):
        print("setup run!!!!!")
        assert int(json.loads(self.hw.resetEngine())['errCode']) == 0

    @pytest.mark.parametrize('engine_id, path_id, path_name, expect', add_path)
    def test_add_path(self, engine_id, path_id, path_name, expect):
        ret = self.hw.add_path(engineID=engine_id, pathID=path_id, pathName=path_name)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, expect', open_path)
    def test_open_path(self, engine_id, path_id, expect):
        ret = self.hw.open_path(engineID=engine_id, pathID=path_id)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, expect', remove_path)
    def test_remove_path(self, engine_id, path_id, expect):
        ret = self.hw.remove_path(engineID=engine_id, pathID=path_id)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, expect', close_path)
    def test_close_path(self, engine_id, path_id, expect):
        ret = self.hw.close_path(engineID=engine_id, pathID=path_id)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, expect', path_direction_data)
    def test_set_path_direction(self, engine_id, path_id, path_direction, expect):
        ret = self.hw.set_path_direction(engineID=engine_id, pathID=path_id, pathDirection=path_direction)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, rate_value, rate_unit, expect',
                             path_bandwidth_fixed_data)
    def test_set_path_bandwidth_fixed(self, engine_id, path_id, path_direction, rate_value, rate_unit, expect):
        ret = self.hw.set_path_Bandwidth_Fixed(engineID=engine_id,
                                               pathID=path_id,
                                               pathDirection=path_direction,
                                               rateValue=rate_value,
                                               rateUnit=rate_unit)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, rate, burst, expect',
                             set_background_utilization_data)
    def test_set_background_utilization(self, engine_id, path_id, path_direction, rate, burst, expect):
        ret = self.hw.set_Background_Utilization(engineID=engine_id,
                                                 pathID=path_id,
                                                 pathDirection=path_direction,
                                                 rate=rate,
                                                 burst=burst)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, expect', close_background_utilization_data)
    def test_close_background_utilization(self, engine_id, path_id, path_direction, expect):
        ret = self.hw.close_Background_Utilization(engineID=engine_id, pathID=path_id, pathDirection=path_direction)
        assert json.loads(str(ret))['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, depth_value, depth_type, expect', queue_limit_data)
    def test_set_queue_limit_drop_tail(self, engine_id, path_id, path_direction, depth_value, depth_type, expect):
        ret = self.hw.set_Queue_Limit_Drop_Tail(engineID=engine_id,
                                                pathID=path_id,
                                                pathDirection=path_direction,
                                                queueDepthValue=depth_value,
                                                queueDepthType=depth_type)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, expect', close_message_modify_data)
    def test_close_message_modify(self, engine_id, path_id, path_direction, expect):
        ret = self.hw.close_message_Modify(engineID=engine_id,
                                           pathID=path_id,
                                           pathDirection=path_direction)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, match_type, '
                             'match_offset, match_size, match_value, modify_type, '
                             'modify_offset, modify_size, modify_value, expect', set_message_modify_normal_data)
    def test_set_message_modify_normal(self, engine_id, path_id,
                                       path_direction, match_type,
                                       match_offset, match_size,
                                       match_value, modify_type,
                                       modify_offset, modify_size,
                                       modify_value, expect):
        ret = self.hw.set_message_Modify_Normal(engineID=engine_id,
                                                pathID=path_id,
                                                pathDirection=path_direction,
                                                matchType=match_type,
                                                matchOffset=match_offset,
                                                matchSize=match_size,
                                                matchValue=match_value,
                                                modifyType=modify_type,
                                                modifyOffset=modify_offset,
                                                modifySize=modify_size,
                                                modifyValue=modify_value)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, match_type, '
                             'match_offset, match_size, match_value, modify_type, '
                             'modify_offset, modify_size, modify_value, '
                             'modify_cycle_period, modify_cycle_burst, expect', set_message_modify_cycle_data)
    def test_set_message_modify_cycle(self,
                                      engine_id, path_id,
                                      path_direction, match_type,
                                      match_offset, match_size, match_value,
                                      modify_type, modify_offset, modify_size,
                                      modify_value, modify_cycle_period, modify_cycle_burst, expect):
        ret = self.hw.set_message_Modify_Cycle(engineID=engine_id,
                                               pathID=path_id, pathDirection=path_direction,
                                               matchType=match_type,
                                               matchOffset=match_offset,
                                               matchSize=match_size,
                                               matchValue=match_value,
                                               modifyType=modify_type,
                                               modifyOffset=modify_offset,
                                               modifySize=modify_size,
                                               modifyValue=modify_value,
                                               modifyCyclePeriod=modify_cycle_period,
                                               modifyCycleBurst=modify_cycle_burst)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, match_type, '
                             'match_offset, match_size, match_value, modify_type, '
                             'modify_offset, modify_size, modify_value, modify_random_rate, expect',
                             set_message_modify_random_data)
    def test_set_message_modify_random(self, engine_id, path_id,
                                       path_direction, match_type,
                                       match_offset, match_size,
                                       match_value, modify_type,
                                       modify_offset, modify_size,
                                       modify_value,
                                       modify_random_rate, expect):
        ret = self.hw.set_message_Modify_Random(engineID=engine_id,
                                                pathID=path_id,
                                                pathDirection=path_direction,
                                                matchType=match_type,
                                                matchOffset=match_offset,
                                                matchSize=match_size,
                                                matchValue=match_value,
                                                modifyType=modify_type,
                                                modifyOffset=modify_offset,
                                                modifySize=modify_size,
                                                modifyValue=modify_value,
                                                modifyRandomRate=modify_random_rate)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, expect', close_mtu_limit_data)
    def test_close_mtu_limit(self, engine_id, path_id, path_direction, expect):
        ret = self.hw.close_MTU_Limit(engineID=engine_id, pathID=path_id, pathDirection=path_direction)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, limit_value, expect', set_mtu_limit_data)
    def test_set_mtu_limit(self, engine_id, path_id, path_direction, limit_value, expect):
        ret = self.hw.set_MTU_Limit(engineID=engine_id, pathID=path_id,
                                    pathDirection=path_direction, limitValue=limit_value)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, type, rate, expect', set_frame_overhead_data)
    def test_set_frame_overhead(self, engine_id, path_id, path_direction, type, rate, expect):
        ret = self.hw.set_Frame_Overhead(engineID=engine_id, pathID=path_id, pathDirection=path_direction,
                                         type=type, rate=rate)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, delay, expect', set_delay_constant_data)
    def test_set_delay_constant(self, engine_id, path_id, path_direction, delay, expect):
        ret = self.hw.set_Delay_Constant(engineID=engine_id, pathID=path_id,
                                         pathDirection=path_direction, delay=delay)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, '
                             'minimum, maximum, enable_reordering, expect',
                             set_delay_uniform_data)
    def test_set_delay_uniform(self, engine_id, path_id, path_direction, minimum, maximum, enable_reordering, expect):
        ret = self.hw.set_Delay_Uniform(engineID=engine_id, pathID=path_id,
                                        pathDirection=path_direction,
                                        minimum=minimum, maximum=maximum,
                                        enableReordering=enable_reordering)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, '
                             'min, mean, std_deviation, enable_reordering, expect',
                             set_delay_normal_data)
    def test_set_delay_normal(self, engine_id, path_id, path_direction,
                              min, mean, std_deviation, enable_reordering, expect):
        ret = self.hw.set_Delay_Normal(engineID=engine_id, pathID=path_id, pathDirection=path_direction,
                                       min=min, mean=mean, stdDeviation=std_deviation,
                                       enableReordering=enable_reordering)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, '
                             'min, mean, std_deviation, enable_reordering,'
                             'advanced_period, advanced_duration,advanced_min, '
                             'advanced_max, expect', set_delay_normal_advanced_data)
    def test_set_delay_normal_advanced(self, engine_id, path_id, path_direction,
                                       min, mean, std_deviation, enable_reordering,
                                       advanced_period, advanced_duration,
                                       advanced_min, advanced_max, expect):
        ret = self.hw.set_Delay_Normal_AdvancedSetup(engineID=engine_id, pathID=path_id, min=min, mean=mean,
                                                     pathDirection=path_direction,
                                                     stdDeviation=std_deviation, enableReordering=enable_reordering,
                                                     advancedPeriod=advanced_period, advancedDuration=advanced_duration,
                                                     advancedMin=advanced_min, advancedMax=advanced_max)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.skip("会导致死机，先跳过这个")
    @pytest.mark.parametrize('engine_id, path_id, path_direction,'
                             'mean_delay, min_delay, max_delay,'
                             'positive_delta, negative_delta,spread,'
                             'enable_reordering, expect', set_delay_custom_data)
    def test_set_delay_custom(self, engine_id, path_id, path_direction,
                              mean_delay, min_delay, max_delay,
                              positive_delta, negative_delta,
                              spread, enable_reordering, expect):
        ret = self.hw.set_Delay_Custom(engineID=engine_id, pathID=path_id,
                                       pathDirection=path_direction,
                                       meanDelay=mean_delay, minDelay=min_delay, maxDelay=max_delay,
                                       positiveDelta=positive_delta, negativeDelta=negative_delta,
                                       spread=spread, enableReordering=enable_reordering)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, rate, expect', loss_random_data)
    def test_set_loss_random(self, engine_id, path_id, path_direction, rate, expect):
        ret = self.hw.set_Loss_Random(engineID=engine_id, pathID=path_id, pathDirection=path_direction, rate=rate)
        print(json.loads(ret)['errReason'])
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, period, burst, expect', loss_cycle_data)
    def test_set_loss_cycle(self, engine_id, path_id, path_direction, period, burst, expect):
        ret = self.hw.set_Loss_Cycle(engineID=engine_id, pathID=path_id, pathDirection=path_direction,
                                     period=period, burst=burst)
        print(json.loads(ret)['errReason'])
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize("engine_id, path_id, path_direction, probability, minimum, maximum, expect",
                             loss_burst_data)
    def test_set_loss_burst(self, engine_id, path_id, path_direction, probability, minimum, maximum, expect):
        ret = self.hw.set_Loss_Burst(engineID=engine_id, pathID=path_id, pathDirection=path_direction,
                                     probability=probability, minimum=minimum, maximum=maximum)
        print(json.loads(ret)['errReason'])
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, good_state_loss, good_to_bad_probability,'
                             'bad_state_loss, bad_to_good_probability, expect', loss_dual_data)
    def test_set_loss_dual(self, engine_id, path_id, path_direction, good_state_loss, good_to_bad_probability,
                           bad_state_loss, bad_to_good_probability, expect):
        ret = self.hw.set_Loss_Dual(engineID=engine_id, pathID=path_id, pathDirection=path_direction,
                                    goodStateLoss=good_state_loss, goodToBadProbability=good_to_bad_probability,
                                    badStateLoss=bad_state_loss, badToGoodProbability=bad_to_good_probability)
        print(json.loads(ret)['errReason'])
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, bit_error_value, bit_error_index, expect', ber_data)
    def test_set_ber(self, engine_id, path_id, path_direction, bit_error_value, bit_error_index, expect):
        ret = self.hw.set_BER(engineID=engine_id, pathID=path_id, pathDirection=path_direction,
                              bitErrorValue=bit_error_value, bitErrorIndex=bit_error_index)
        print(json.loads(ret)['errReason'])
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, probability, delay_min, delay_max, expect',
                             reordering_normal_data)
    def test_set_reordering_normal(self, engine_id, path_id, path_direction, probability, delay_min, delay_max, expect):
        ret = self.hw.set_Reordering_Normal(engineID=engine_id, pathID=path_id, pathDirection=path_direction,
                                            probability=probability, delayMin=delay_min, delayMax=delay_max)
        print(json.loads(ret)['errReason'])
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, probability, expect', duplication_data)
    def test_set_duplication_normal(self, engine_id, path_id, path_direction, probability, expect):
        ret = self.hw.set_Duplication_Normal(engineID=engine_id, pathID=path_id, pathDirection=path_direction,
                                             probability=probability)
        print(json.loads(ret)['errReason'])
        assert json.loads(ret)['errCode'] == expect





