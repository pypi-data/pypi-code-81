import pytest
from holowan.HoloWAN import SubHoloWAN
import json

add_data = [
    (1, 1, "path1", -15),
    (2, 2, "path2", -5),
    (1, 17, "path17", -7),
    # (1, 2, None, -8)  #会直接报错，应该不会出现控制的情况
    (1, 2, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", -9)
    # -14最多只能添加15条PATH 应该跟 -7有点相似，只要path_id是15以上的就会报-7，不知道怎么弄出-14来
]

init_data = [
    (1, 1, 0),
    (1, 12, -6),
    (2, 1, -3),
    (1, 17, -5)
]

remove_data = [
    (1, 88, -7),
    (1, -12, -7),
    (-1, 1, -5),
    (2, -1, -5),
    (1, 12, -12)
]

open_path_data = [
    (1, 2, 0)

]

close_path_data = [
    (1, 1, 0)
]


class TestHold:
    hw = SubHoloWAN("192.168.1.222", "8080")

    def test_hold_engine(self):
        self.hold_engine(4123456789, 4123456789, 0)
        self.hold_engine(0, 1234, 0)
        self.hold_engine(4321, 4321, -4)
        ret = json.loads(str(self.hw.hold_engine()))
        assert int(ret['errCode']) == -1
        self.hold_engine(4123456789, 4123456789, 0)

    def hold_engine(self, password, new_password, errcode):
        s = self.hw.hold_engine(password=int(password), new_password=int(new_password))
        ret = json.loads(str(s))
        assert int(ret['errCode']) == errcode

    def test_get_holowan_info(self):
        ret = self.hw.get_HoloWAN_information()
        assert isinstance(ret, str)


# 链路的添加删除修改
class TestPath:
    hw = SubHoloWAN("192.168.1.222", "8080")

    @pytest.mark.parametrize('engine_id, path_id, path_name, expect', add_data)
    def test_add_path(self, engine_id, path_id, path_name, expect):
        ret = self.hw.add_path(engineID=engine_id, pathID=path_id, pathName=path_name)
        assert int(json.loads(ret)['errCode']) == expect

    @pytest.mark.parametrize('engine_id, path_id, expect', init_data)
    def test_init_path(self, engine_id, path_id, expect):
        ret = self.hw.init_path(engineID=engine_id, pathID=path_id)
        assert int(json.loads(ret)['errCode']) == expect

    @pytest.mark.parametrize('engine_id, path_id, expect', remove_data)
    def test_remove_path(self,engine_id, path_id, expect):
        ret = self.hw.remove_path(engineID=engine_id, pathID=path_id)
        assert int(json.loads(ret)['errCode']) == expect

    def test_add_paths(self):
        for i in range(2, 16):
            ret = self.hw.add_path(engineID=1, pathID=i)
            assert int(json.loads(ret)['errCode']) == 0

    def test_remove_paths(self):
        for i in range(4, 16):
            ret = self.hw.remove_path(engineID=1, pathID=i)
            assert int(json.loads(ret)['errCode']) == 0

    @pytest.mark.parametrize('engine_id, path_id, expect', open_path_data)
    def test_open_path(self, engine_id, path_id, expect):
        ret = self.hw.open_path(engineID=engine_id, pathID=path_id)
        assert int(json.loads(ret)['errCode']) == expect

    @pytest.mark.parametrize('engine_id, path_id, expect', close_path_data)
    def test_close_path(self, engine_id, path_id, expect):
        ret = self.hw.close_path(engineID=engine_id, pathID=path_id)
        assert int(json.loads(ret)['errCode']) == expect


if __name__ == '__main__':
    # -v 可以输出用例更加详细的执行信息，比如用例所在的文件及用例名称等
    # -s 显示print的内容
    pytest.main(['-sv'])
    # hw = SubHoloWAN("192.168.1.222", "8080")
    # ret = hw.hold_engine(password=4123456789, new_password=4123456789)
    # print(ret)

