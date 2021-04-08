import pytest
from holowan.HoloWAN import SubHoloWAN
import json
import os
from utils import MyUtil as mt

HoloWANIP = "192.168.1.224"
HoloWANPort = "8080"
engineID = 1
project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ini = mt.open_ini(project_path + r"/holowan/resources/Holowan.ini")



add_path = [
    (-1, 2, "path2", ini.get("PathOperateErrorCode", "engineIDError")),
    (4, 2, "path2", ini.get("PathOperateErrorCode", "engineIDError")),
    (1, -1, "path16", ini.get("PathOperateErrorCode", "pathIDError")),
    (1, 16, "path16", ini.get("PathOperateErrorCode", "pathIDError")),
    (1, 2, "a"*200, ini.get("PathOperateErrorCode", "pathNameError")),
    (1, 1, "path1", ini.get("PathOperateErrorCode", "pathExist")),
    (1, 2, "PATH", "0"),
    (1, 3, "PATH", "0"),
    (1, 4, "PATH", "0"),
    (1, 5, "PATH", "0"),
    (1, 6, "PATH", "0"),
    (1, 7, "PATH", "0"),
    (1, 9, "PATH", "0"),
    (1, 10, "PATH", "0"),
    (1, 11, "PATH", "0"),
    (1, 12, "PATH", "0"),
    (1, 13, "PATH", "0"),
    (1, 14, "PATH", "0"),
    (1, 15, "PATH", "0")
    # (1, 2, None, -8)  #会直接报错，应该不会出现控制的情况
    # -14最多只能添加15条PATH 应该跟 -7有点相似，只要path_id是15以上的就会报-7，不知道怎么弄出-14来
]

open_path = [
    (-1, 2, ini.get("PathOperateErrorCode", "engineIDError")),
    (4, 2, ini.get("PathOperateErrorCode", "engineIDError")),
    (1, -1, ini.get("PathOperateErrorCode", "pathIDError")),
    (1, 16, ini.get("PathOperateErrorCode", "pathIDError")),
    (1, 1, "0"),
    (1, 2, "0"),
    (1, 8, ini.get("PathOperateErrorCode", "openPathNotFound"))
]
remove_path = [
    (-1, 2, ini.get("PathOperateErrorCode", "engineIDError")),
    (4, 2, ini.get("PathOperateErrorCode", "engineIDError")),
    (1, -1, ini.get("PathOperateErrorCode", "pathIDError")),
    (1, 16, ini.get("PathOperateErrorCode", "pathIDError")),
    (1, 1, ini.get("PathOperateErrorCode", "pathIsOpening")),
    (1, 2, ini.get("PathOperateErrorCode", "pathIsOpening")),
    (1, 3, "0"),
    (1, 4, "0"),
    (1, 5, "0"),
    (1, 6, "0"),
    (1, 7, "0"),
    (1, 8, ini.get("PathOperateErrorCode", "removePathNotFound")),
    (1, 9, "0"),
    (1, 10, "0"),
    (1, 11, "0"),
    (1, 12, "0"),
    (1, 13, "0"),
    (1, 14, "0"),
    (1, 15, "0"),
]


close_path = [
    (-1, 2, ini.get("PathOperateErrorCode", "engineIDError")),
    (4, 2, ini.get("PathOperateErrorCode", "engineIDError")),
    (1, -1, ini.get("PathOperateErrorCode", "pathIDError")),
    (1, 16, ini.get("PathOperateErrorCode", "pathIDError")),
    (1, 2, "0"),
    (1, 3, ini.get("PathOperateErrorCode", "closePathNotFound")),
]


path_direction_data = [
    (-1, 2, 1, ini.get("PathConfigErrorCode", "engineIDError")),
    (4, 2, 1, ini.get("PathConfigErrorCode", "engineIDError")),
    (1, -1, 1, ini.get("PathConfigErrorCode", "pathIDError")),
    (1, 16, 1, ini.get("PathConfigErrorCode", "pathIDError")),
    (1, 1, 1, "0"),
    (1, 1, 2, "0"),
    (1, 1, 3, "0"),
    (1, 1, 4, ini.get("PathConfigErrorCode", "pathDirectionError")),
    (1, 15, 1, ini.get("PathConfigErrorCode", "pathNotFound"))
]
path_bandwidth_fixed_data = [
    (-1, 1, 1, 1000, 3, ini.get("PathConfigErrorCode", "engineIDError")),
    (4, 1, 1, 1000, 3, ini.get("PathConfigErrorCode", "engineIDError")),
    (1, -1, 1, 1000, 3, ini.get("PathConfigErrorCode", "pathIDError")),
    (1, 16, 1, 1000, 3, ini.get("PathConfigErrorCode", "pathIDError")),
    (1, 1, 1, 1000, 3, "0"),
    (1, 1, 1, 1000, 3, "0"),
    (1, 1, 3, 1000, 3, ini.get("PathConfigErrorCode", "pathDirectionError")),
    (1, 1, 4, 1000, 3, ini.get("PathConfigErrorCode", "pathDirectionError")),
    (1, 1, 1, 1000, 1, "0"),
    (1, 1, 1, 1000, 2, "0"),
    (1, 1, 1, 1000, 3, "0"),
    (1, 1, 1, 1000, 4, ini.get("PathConfigErrorCode", "pathBandwidthRateUnitError"))
]



close_background_utilization_data = [
    (1, 1, 1, 0),
    (1, 1, 2, 0),
    (1, 2, 1, 0),
    (1, 1, 3, -10),  # 等改好了再把注释去掉
    (8, 1, 1, -501),
    (1, 4, 1, -502),
    (1, 20, 1, -502)
]
set_background_utilization_data = [
    (1, 1, 1, 20, 64, 0),
    (1, 1, 2, 25, 32, 0),
    (1, 1, 2, 25, 128, 0),
    # (1, 1, 2, 25, 9100, 0),  # 最大应该是9100，但是这里没有限制
    (1, 2, 1, 20, 64, 0),
    (1, 1, 1, 110, 64, -29),
    (1, 1, 1, -20, 64, -29),
    (1, 1, 3, 20, 64, -10),
    (8, 1, 1, 20, 64, -501),
    (1, 4, 1, 20, 64, -502),
    (1, 20, 1, 20, 64, -502)
]
queue_limit_data = [
    # MS最大值为1000  KB最大值为10000 packets最大值为10000
    (1, 1, 1, 24, 2, 0),
    (1, 1, 1, 36, 1, 0),
    (1, 1, 1, 48, 3, 0),
    (1, 2, 1, 23, 3, 0),  # 这个有点问题，不能复现
    (1, 1, 1, 10001, 1, -32),
    (1, 1, 1, 10001, 2, -32),
    (1, 1, 1, 1001, 3, -32),  # 这个要等后端改好再测
    (8, 1, 1, 24, 2, -501),
    (1, 4, 1, 24, 2, -502),
    (1, 1, 3, 24, 2, -10),
    (1, 20, 1, 24, 1, -502),

]
close_message_modify_data = [
    (1, 1, 1, 0),
    (1, 1, 2, 0),
    (1, 2, 3, -10),  # 这个怎么变成 -500 ？？
    (1, 20, 1, -502),
    (1, 4, 1, -502),
    (1, 2, 1, 0),
]

@pytest.fixture()
def resetEngine():
    hw = SubHoloWAN(HoloWANIP, HoloWANPort)
    ret = hw.resetEngine()
    assert json.loads(ret)['errCode'] == "0"


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
    @pytest.mark.parametrize('engine_id, path_id, path_direction, rate_value, rate_unit, expect', path_bandwidth_fixed_data)
    def test_set_path_bandwidth_fixed(self, engine_id, path_id, path_direction, rate_value, rate_unit, expect):
        ret = self.hw.set_path_Bandwidth_Fixed(engineID=engine_id,
                                               pathID=path_id,
                                               pathDirection=path_direction,
                                               rateValue=rate_value,
                                               rateUnit=rate_unit)
        assert json.loads(ret)['errCode'] == expect
    #
    # @pytest.mark.parametrize('engine_id, path_id, path_direction, rate, burst, expect', set_background_utilization_data)
    # # @pytest.mark.skip()
    # def test_set_background_utilization(self, engine_id, path_id, path_direction, rate, burst, expect):
    #     ret = self.hw.set_Background_Utilization(engineID=engine_id,
    #                                              pathID=path_id,
    #                                              pathDirection=path_direction,
    #                                              rate=rate,
    #                                              burst=burst)
    #     assert int(json.loads(ret)['errCode']) == expect
    #
    # @pytest.mark.parametrize('engine_id, path_id, path_direction, expect', close_background_utilization_data)
    # # @pytest.mark.skip()
    # def test_close_background_utilization(self, engine_id, path_id, path_direction, expect):
    #     ret = self.hw.close_Background_Utilization(engineID=engine_id, pathID=path_id, pathDirection=path_direction)
    #     assert int(json.loads(str(ret))['errCode']) == expect
    #
    # @pytest.mark.parametrize('engine_id, path_id, path_direction, depth_value, depth_type, expect', queue_limit_data)
    # def test_set_queue_limit_drop_tail(self, engine_id, path_id, path_direction, depth_value, depth_type, expect):
    #     ret = self.hw.set_Queue_Limit_Drop_Tail(engineID=engine_id,
    #                                             pathID=path_id,
    #                                             pathDirection=path_direction,
    #                                             queueDepthValue=depth_value,
    #                                             queueDepthType=depth_type)
    #     assert int(json.loads(ret)['errCode']) == expect
    #
    # @pytest.mark.parametrize('engine_id, path_id, path_direction, expect', close_message_modify_data)
    # def test_close_message_modify(self, engine_id, path_id, path_direction, expect):
    #     ret = self.hw.close_message_Modify(engineID=engine_id,
    #                                        pathID=path_id,
    #                                        pathDirection=path_direction)
    #     assert int(json.loads(str(ret))['errCode']) == expect


if __name__ == '__main__':
    pytest.main(['-sv'])
