import pytest
from holowan.HoloWAN import SubHoloWAN
# from holowan.HoloWAN import HoloWAN
import json
import os
from utils import MyUtil as mt

HoloWANIP = "192.168.1.198"
HoloWANPort = "8080"
engineID = 1
project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
POErrCode = mt.open_ini2("./resources/Holowan.ini", "PathOperateErrorCode")
PCErrCode = mt.open_ini2("./resources/Holowan.ini", "PathConfigErrorCode")
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
    (1, 1, 1, 4, 24, "-500"),  # 这个没有对应的错误码
    (1, 1, 1, 3, 65, "-500"),  # 最大值不受限, 在type为3时, rate的最大值应为64
    (1, 1, 1, 2, 64, ok),  # 在type不为3的时候, rate设置无效, 不用修改
]
set_delay_constant_data = [
    (1, 1, 1, 10000.0, ok),  # 还是没有将float自动转换成int, 火大
    (1, 1, 1, 65536.0, PCErrCode.getOption("constantDelayValueError")),  # 前端限制为10000.0, 后端限制为65536.0
    (1, 1, 1, 1500.12, PCErrCode.getOption("constantDelayValueError")),  # 两位小数返回-500, 用-68会比较好
    (4, 1, 1, 10000.0, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 10000.0, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 10000.0, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 10000.0, PCErrCode.getOption("pathDirectionError")),
    # (1, 1, 1, 10000, ok),  # 自动类型转换
]
set_delay_uniform_data = [
    (1, 1, 1, 1.0, 50.0, 1, ok),
    (1, 1, 1, 1.0, 50.0, 0, ok),
    (1, 1, 1, 1.0, 50.0, 2, "-500"),  # 这个又是-500, 好像也没有相应的错误码, 用bool值会比较好吧
    (4, 1, 1, 1.0, 50.0, 1, PCErrCode.getOption("engineIDError")),
    (1, 4, 1, 10.0, 50.0, 1, PCErrCode.getOption("pathNotFound")),
    (1, 16, 1, 10.0, 50.0, 1, PCErrCode.getOption("pathIDError")),
    (1, 1, 3, 10.0, 50.0, 1, PCErrCode.getOption("pathDirectionError")),
    # ↓ 前后端范围不一致, 前端为10000, 后端范围为65535, 返回值为-71(为空), 应为-72(值错误)
    (1, 1, 1, 0.1, 65535.1, 1, PCErrCode.getOption("uniformDelayValueError")),
    (1, 1, 1, 50.0, 1.0, 1, PCErrCode.getOption("uniformDelayValueError")),  # 大小顺序反了才是-72?
    # (1, 1, 1, 1, 50, 1, ok),  # 自动类型转换
]
set_delay_normal_data = [
    (1, 1, 1, 1.0, 50.0, 10.0, 1, ok),
    # (4, 1, 1, 1.0, 50.0, 10.0, 1, PCErrCode.getOption("engineIDError")),
    # (1, 4, 1, 1.0, 50.0, 10.0, 1, PCErrCode.getOption("pathNotFound")),
    # (1, 16, 1, 1.0, 50.0, 10.0, 1, PCErrCode.getOption("pathIDError")),
    # (1, 1, 3, 1.0, 50.0, 10.0, 1, PCErrCode.getOption("pathDirectionError")),
    # (1, 1, 1, 50.0, 1.0, 10.0, 1, ok),  # min不能比mean大, 后端没有限制
    # (1, 1, 1, 1.0, 50.0, 9951.0, 1, ok),  # 设置了但是没有用
    # (1, 1, 1, 1.0, 51.0, 20.0, 1, ok)
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


# 测试链路的增删、启动关闭
class TestPath:
    hw = SubHoloWAN(HoloWANIP, HoloWANPort)

    def setup_class(self):
        print("setup run!!!!!")
        assert int(json.loads(self.hw.resetEngine())['errCode']) == 0

    # @pytest.mark.run(order=1)
    @pytest.mark.parametrize('engine_id, path_id, path_name, expect', add_path)
    def test_add_path(self, engine_id, path_id, path_name, expect):
        ret = self.hw.add_path(engineID=engine_id, pathID=path_id, pathName=path_name)
        assert json.loads(ret)['errCode'] == expect

    # @pytest.mark.run(order=2)
    @pytest.mark.parametrize('engine_id, path_id, expect', open_path)
    def test_open_path(self, engine_id, path_id, expect):
        ret = self.hw.open_path(engineID=engine_id, pathID=path_id)
        assert json.loads(ret)['errCode'] == expect

    # @pytest.mark.run(order=3)
    @pytest.mark.parametrize('engine_id, path_id, expect', remove_path)
    def test_remove_path(self, engine_id, path_id, expect):
        ret = self.hw.remove_path(engineID=engine_id, pathID=path_id)
        assert json.loads(ret)['errCode'] == expect

    # @pytest.mark.run(order=4)
    @pytest.mark.parametrize('engine_id, path_id, expect', close_path)
    def test_close_path(self, engine_id, path_id, expect):
        ret = self.hw.close_path(engineID=engine_id, pathID=path_id)
        assert json.loads(ret)['errCode'] == expect

    # @pytest.mark.run(order=5)
    @pytest.mark.parametrize('engine_id, path_id, path_direction, expect', path_direction_data)
    def test_set_path_direction(self, engine_id, path_id, path_direction, expect):
        ret = self.hw.set_path_direction(engineID=engine_id, pathID=path_id, pathDirection=path_direction)
        assert json.loads(ret)['errCode'] == expect

    # @pytest.mark.run(order=6)
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

    @pytest.mark.parametrize('engine_id, path_id, path_direction, minimum, maximum, enable_reordering, expect',
                             set_delay_uniform_data)
    def test_set_delay_uniform(self, engine_id, path_id, path_direction, minimum, maximum, enable_reordering, expect):
        ret = self.hw.set_Delay_Uniform(engineID=engine_id, pathID=path_id,
                                        pathDirection=path_direction,
                                        minimum=minimum, maximum=maximum,
                                        enableReordering=enable_reordering)
        assert json.loads(ret)['errCode'] == expect

    @pytest.mark.parametrize('engine_id, path_id, path_direction, min, mean, std_deviation, enable_reordering, expect',
                             set_delay_normal_data)
    def test_set_delay_normal(self, engine_id, path_id, path_direction,
                              min, mean, std_deviation, enable_reordering, expect):
        ret = self.hw.set_Delay_Normal(engineID=engine_id, pathID=path_id, pathDirection=path_direction,
                                       min=min, mean=mean, enableReordering=enable_reordering)
        assert json.loads(ret)['errCode'] == expect


if __name__ == '__main__':
    pytest.main(['-sv'])
