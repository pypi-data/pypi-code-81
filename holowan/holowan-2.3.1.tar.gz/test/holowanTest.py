import unittest
from holowan.HoloWAN import HoloWAN
import re

class HoloWANTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        super().setUp()
        holowan_ip = "192.168.1.99"
        holowan_port = "8080"
        self.holowan = SubHoloWAN(holowan_ip=holowan_ip, holowan_port=holowan_port)
        self.excluedMethods = ["setDefaultParameter", "create_IPV4", "create_IPV4_and_TCP_or_UDP", "create_IPV6",
                          "create_MAC", "create_TCP_or_UDP", "exist_path", "remove_or_open_or_close_path",
                          "set_holowan_ip", "set_holowan_port", "set_one_tag_text", "set_tag_children"]
        self.subHoloWANDir = dir(SubHoloWAN)


    def tearDown(self) -> None:
        super().tearDown()

    # 测试ip格式
    def test_ip(self):
        ipTestExpectResult = '{"errCode":"-500","errMsg":"Parameter ERROR","errReason":"Error IP address"}'
        self.ipTest("", ipTestExpectResult)
        self.ipTest("192.168.1.1.1", ipTestExpectResult)
        self.ipTest("192.168.1.256", ipTestExpectResult)
        self.ipTest("123", ipTestExpectResult)
        self.ipTest("asd", ipTestExpectResult)

    # 测试port端口格式
    def test_port(self):
        portTestExpectResult = '{"errCode":"-500","errMsg":"Parameter ERROR","errReason":"Error IP address"}'
        self.portTest("", portTestExpectResult)
        self.portTest("192.168.1.1.1", portTestExpectResult)
        self.portTest("192.168.1.256", portTestExpectResult)
        self.portTest("123", portTestExpectResult)
        self.portTest("asd", portTestExpectResult)
        self.portTest("65536", portTestExpectResult)


    def ipTest(self, ip, expectResult):
        self.holowan.set_holowan_ip(ip)
        for methodName in self.subHoloWANDir:
            if re.match("^__.*", methodName) == None and methodName not in self.excluedMethods:
                if hasattr(self.holowan, methodName):
                    response = getattr(self.holowan, methodName)()
                    self.assertEqual(response, expectResult)

    def portTest(self, port, expectResult):
        self.holowan.set_holowan_ip(port)
        for methodName in self.subHoloWANDir:
            if re.match("^__.*", methodName) == None and methodName not in self.excluedMethods:
                if hasattr(self.holowan, methodName):
                    response = getattr(self.holowan, methodName)()
                    self.assertEqual(response, expectResult)


class SubHoloWAN(HoloWAN):

    def __init__(self, holowan_ip, holowan_port):
        super().__init__()
        self.holowan_ip = holowan_ip
        self.holowan_port = holowan_port

    # 设置默认值
    def setDefaultParameter(self, holowan_ip: str = "defaule", holowan_port: str = "default"):
        if holowan_ip == "default":
            holowan_ip = self.holowan_ip
        if holowan_port == "default":
            holowan_port = self.holowan_port
        return holowan_ip, holowan_port

    # 设置IP地址
    def set_holowan_ip(self, holowan_ip):
        self.holowan_ip = holowan_ip

    # 设置port端口号
    def set_holowan_port(self, holowan_port):
        self.holowan_port = holowan_port

    def hold_engine(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1 , password: int = 123456, new_password: int = 123456):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().hold_engine(holowan_ip, holowan_port, engineID, password, new_password)

    def get_HoloWAN_information(self, holowan_ip: str = "default", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_HoloWAN_information(holowan_ip, holowan_port)

    def add_path(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, 
                 pathName: str = "PATH"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    def init_path(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathName: str = "PATH"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().init_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    def remove_path(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathName: str = "PATH"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    def open_path(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathName: str = "PATH"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().open_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    def close_path(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathName: str = "PATH"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().close_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    def set_path_direction(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_path_direction(holowan_ip, holowan_port, engineID, pathID, pathDirection)

    def set_path_Bandwidth_Fixed(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1,
                                 pathDirection: int = 3, rateValue: int = 1000, rateUnit: int = 2):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_path_Bandwidth_Fixed(holowan_ip, holowan_port, engineID, pathID, pathDirection, rateValue,
                                                rateUnit)

    def close_Background_Utilization(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1,
                                     pathDirection: int = 3):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().close_Background_Utilization(holowan_ip, holowan_port, engineID, pathID, pathDirection)

    def set_Background_Utilization(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1,
                                   pathDirection: int = 3, rate: int = 50, burst: int = 64):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Background_Utilization(holowan_ip, holowan_port, engineID, pathID, pathDirection, rate,
                                                  burst)

    def set_Queue_Limit_Drop_Tail(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1,
                                  pathDirection: int = 3, queueDepthValue: int = 50, queueDepthType: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Queue_Limit_Drop_Tail(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                 queueDepthValue, queueDepthType)

    def close_message_Modify(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().close_message_Modify(holowan_ip, holowan_port, engineID, pathID, pathDirection)

    def set_message_Modify_Normal(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1,
                                  pathDirection: int = 3, matchType: int = 1, matchOffset: int = 0, matchSize: int = 1, matchValue: str = "FF",
                                  modifyType: int = 1, modifyOffset: int = 0, modifySize: int = 1, modifyValue: str = "FF"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_message_Modify_Normal(holowan_ip, holowan_port, engineID, pathID, pathDirection, matchType,
                                                 matchOffset, matchSize, matchValue, modifyType, modifyOffset,
                                                 modifySize, modifyValue)

    def set_message_Modify_Cycle(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1,
                                 pathDirection: int = 3, matchType: int = 1, matchOffset: int = 0, matchSize: int = 1, matchValue: str = "FF",
                                  modifyType: int = 1, modifyOffset: int = 0, modifySize: int = 1, modifyValue: str = "FF",
                                 modifyCyclePeriod: int = 1000, modifyCycleBurst: int = 10):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_message_Modify_Cycle(holowan_ip, holowan_port, engineID, pathID, pathDirection, matchType,
                                                matchOffset, matchSize, matchValue, modifyType, modifyOffset,
                                                modifySize, modifyValue, modifyCyclePeriod, modifyCycleBurst)

    def set_message_Modify_Random(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1,
                                  pathDirection: int = 3, matchType: int = 1, matchOffset: int = 0, matchSize: int = 1, matchValue: str = "FF",
                                  modifyType: int = 1, modifyOffset: int = 0, modifySize: int = 1, modifyValue: str = "FF",
                                  modifyRandomRate: float = 1.1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_message_Modify_Random(holowan_ip, holowan_port, engineID, pathID, pathDirection, matchType,
                                                 matchOffset, matchSize, matchValue, modifyType, modifyOffset,
                                                 modifySize, modifyValue, modifyRandomRate)

    def close_MTU_Limit(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().close_MTU_Limit(holowan_ip, holowan_port, engineID, pathID, pathDirection)

    def set_MTU_Limit(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                      limitValue: int = 1500):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_MTU_Limit(holowan_ip, holowan_port, engineID, pathID, pathDirection, limitValue)

    def set_Frame_Overhead(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                           type: int = 3, rate: int = 24):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Frame_Overhead(holowan_ip, holowan_port, engineID, pathID, pathDirection, type, rate)

    def set_Delay_Constant(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                           delay: float = 2):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Delay_Constant(holowan_ip, holowan_port, engineID, pathID, pathDirection, delay)

    def set_Delay_Uniform(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                          minimum: float = 0.0, maximum: float = 50.0, enableReordering: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Delay_Uniform(holowan_ip, holowan_port, engineID, pathID, pathDirection, minimum, maximum,
                                         enableReordering)

    def set_Delay_Normal(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                         min: float = 1.0, mean: float = 50.0, stdDeviation: float = 10.0, enableReordering: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Delay_Normal(holowan_ip, holowan_port, engineID, pathID, pathDirection, min, mean,
                                        stdDeviation, enableReordering)

    def set_Delay_Normal_AdvancedSetup(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1,
                                       pathDirection: int = 3, min: float = 1.0, mean: float = 50.0, stdDeviation: float = 10.0,
                                       enableReordering: int = 1, advancedPeriod: float = 60000, advancedDuration: float = 1000,
                                       advancedMin: float = 900, advancedMax: float = 1000):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Delay_Normal_AdvancedSetup(holowan_ip, holowan_port, engineID, pathID, pathDirection, min,
                                                      mean, stdDeviation, enableReordering, advancedPeriod,
                                                      advancedDuration, advancedMin, advancedMax)

    def set_Delay_Custom(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                         meanDelay: float = 200.0, minDelay: float = 1.0, maxDelay: float = 1000.0, positiveDelta: float = 99.9, negativeDelta: float = 99.9,
                         spread: float = 1.58, enableReordering: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Delay_Custom(holowan_ip, holowan_port, engineID, pathID, pathDirection, meanDelay, minDelay,
                                        maxDelay, positiveDelta, negativeDelta, spread, enableReordering)

    def set_Loss_Random(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                        rate: float = 5.000):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Loss_Random(holowan_ip, holowan_port, engineID, pathID, pathDirection, rate)

    def set_Loss_Cycle(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                       period: int = 1000, burst: int = 10):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Loss_Cycle(holowan_ip, holowan_port, engineID, pathID, pathDirection, period, burst)

    def set_Loss_Burst(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                       probability: float = 50.00, minimum: int = 0, maximum: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Loss_Burst(holowan_ip, holowan_port, engineID, pathID, pathDirection, probability, minimum,
                                      maximum)

    def set_Loss_Dual(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                      goodStateLoss: float = 1.0, goodToBadProbability: float = 50.0, badStateLoss: float = 1.0,
                      badToGoodProbability: float = 50.0):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Loss_Dual(holowan_ip, holowan_port, engineID, pathID, pathDirection, goodStateLoss,
                                     goodToBadProbability, badStateLoss, badToGoodProbability)

    def set_BER(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                bitErrorValue: int = 1, bitErrorIndex: int = -14):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_BER(holowan_ip, holowan_port, engineID, pathID, pathDirection, bitErrorValue, bitErrorIndex)

    def set_Reordering_Normal(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                              probability: float = 0.0, delayMin: float = 0.1, delayMax: float = 0.5):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Reordering_Normal(holowan_ip, holowan_port, engineID, pathID, pathDirection, probability,
                                             delayMin, delayMax)

    def set_Duplication_Normal(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathDirection: int = 3,
                               probability: float = 20.0):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Duplication_Normal(holowan_ip, holowan_port, engineID, pathID, pathDirection, probability)

    def get_path_config_information(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_path_config_information(holowan_ip, holowan_port, engineID, pathID)

    def add_IPV4_to_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1, sourceIP: str = "any",
                               sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32, TOS: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_IPV4_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, sourceMask,
                                              destinationIP, destinationMask, TOS, action)

    def remove_IPV4_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1, sourceIP: str = "any",
                                    sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32, TOS: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_IPV4_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, sourceMask,
                                                   destinationIP, destinationMask, TOS, action)

    def remove_all_IPV4_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_IPV4_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def add_IPV6_to_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1, sourceIP: str = "any",
                               destinationIP: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_IPV6_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, destinationIP,
                                              action)

    def remove_IPV6_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1, sourceIP: str = "any",
                                    destinationIP: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_IPV6_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, destinationIP,
                                                   action)

    def remove_all_IPV6_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_IPV6_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def add_MAC_to_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1, sourceMAC: str = "any",
                              destinationMAC: str = "any", EtherType: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_MAC_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourceMAC, destinationMAC,
                                             EtherType, action)

    def remove_MAC_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1, sourceMAC: str = "any",
                                   destinationMAC: str = "any", EtherType: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_MAC_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourceMAC, destinationMAC,
                                                  EtherType, action)

    def remove_all_MAC_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_MAC_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def add_TCP_to_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1, sourcePort: str = "any",
                              destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_TCP_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourcePort, destPort,
                                             checkVersion, action)

    def remove_TCP_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1,
                                   sourcePort: str = "any", destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_TCP_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourcePort, destPort,
                                                  checkVersion, action)

    def remove_all_TCP_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_TCP_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def add_UDP_to_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1, sourcePort: str = "any",
                              destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_UDP_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourcePort, destPort,
                                             checkVersion, action)

    def remove_UDP_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1,
                                   sourcePort: str = "any", destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_UDP_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourcePort, destPort,
                                                  checkVersion, action)

    def remove_all_UDP_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_UDP_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def create_TCP_or_UDP(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, TCPUDP: int = 1, sourcePort: str = "any",
                          destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().create_TCP_or_UDP(holowan_ip, holowan_port, engineID, TCPUDP, sourcePort, destPort, checkVersion,
                                         action)

    def add_IPV4_TCP_to_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1, sourceIP: str = "any",
                                   sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32, TOS: str = "any", sourcePort: str = "any",
                                   destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_IPV4_TCP_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, sourceMask,
                                                  destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                  checkVersion, action)

    def remove_IPV4_TCP_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1,
                                        sourceIP: str = "any", sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32,
                                        TOS: str = "any", sourcePort: str = "any", destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_IPV4_TCP_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, sourceMask,
                                                       destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                       checkVersion, action)

    def remove_all_IPV4_TCP_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_IPV4_TCP_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def add_IPV4_UDP_to_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1, sourceIP: str = "any",
                                   sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32, TOS: str = "any", sourcePort: str = "any",
                                   destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_IPV4_UDP_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, sourceMask,
                                                  destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                  checkVersion, action)

    def remove_IPV4_UDP_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1,
                                        sourceIP: str = "any", sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32,
                                        TOS: str = "any", sourcePort: str = "any", destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_IPV4_UDP_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, sourceMask,
                                                       destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                       checkVersion, action)

    def remove_all_IPV4_UDP_from_Classifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_IPV4_UDP_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def create_IPV4_and_TCP_or_UDP(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, TCPUDP: int = 1, sourceIP: str = "any",
                                   sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32, TOS: str = "any", sourcePort: str = "any",
                                   destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().create_IPV4_and_TCP_or_UDP(holowan_ip, holowan_port, engineID, TCPUDP, sourceIP, sourceMask,
                                                  destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                  checkVersion, action)

    def get_Packet_Classifier_config_information(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_Packet_Classifier_config_information(holowan_ip, holowan_port, engineID)

    def start_engine(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().start_engine(holowan_ip, holowan_port, engineID)

    def stop_engine(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().stop_engine(holowan_ip, holowan_port, engineID)

    def save_HoloWAN_information(self, holowan_ip: str = "defaule", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().save_HoloWAN_information(holowan_ip, holowan_port)

    def remove_or_open_or_close_path(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, pathName: str = "PATH",
                                     children_node_Map = {}):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_or_open_or_close_path(holowan_ip, holowan_port, engineID, pathID, pathName,
                                                    children_node_Map)

    def get_path_current_data(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_path_current_data(holowan_ip, holowan_port, engineID, pathID)

    def get_path_graph_current(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, id: int = "rx_bytes",
                               type: str = "rx_bytes"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_path_graph_current(holowan_ip, holowan_port, engineID, pathID, id, type)

    def get_HoloWAN_history_entire_data(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, last: int = 0,
                                        count: int = 30):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_HoloWAN_history_entire_data(holowan_ip, holowan_port, engineID, pathID, last, count)

    def get_path_graph_current_dataGroup(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1,
                                         type: str = "rx_bytes", offset: int = 10, count: int = 30):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_path_graph_current_dataGroup(holowan_ip, holowan_port, engineID, pathID, type, offset, count)

    def clean_engine_statistic_data(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().clean_engine_statistic_data(holowan_ip, holowan_port, engineID)

    def create_csv(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1, filePath: str = ""):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().create_csv(holowan_ip, holowan_port, engineID, pathID, filePath)

    def get_network_information(self, holowan_ip: str = "defaule", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_network_information(holowan_ip, holowan_port)

    def set_network(self, holowan_ip: str = "defaule", holowan_port: str = "default", hostName: str = "MyHoloWAN", ipAddress: str = "192.168.1.199", ipNetmask: str = "255.255.255.255",
                    gateway: str = "192.168.1.1"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_network(holowan_ip, holowan_port, hostName, ipAddress, ipNetmask, gateway)

    def get_worker_port_information(self, holowan_ip: str = "defaule", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_worker_port_information(holowan_ip, holowan_port)

    def get_log(self, holowan_ip: str = "defaule", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_log(holowan_ip, holowan_port)

    def reboot(self, holowan_ip: str = "defaule", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().reboot(holowan_ip, holowan_port)

    def get_preferences(self, holowan_ip: str = "defaule", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_preferences(holowan_ip, holowan_port)

    def set_preferences(self, holowan_ip: str = "defaule", holowan_port: str = "default", clean_buffer: str = "true", zero_line: str = "receive_time"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_preferences(holowan_ip, holowan_port, clean_buffer, zero_line)

    def get_path_Name(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_path_Name(holowan_ip, holowan_port, engineID, pathID)

    def get_paths_from_engine(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_paths_from_engine(holowan_ip, holowan_port, engineID)

    def resetPath(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, pathID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().resetPath(holowan_ip, holowan_port, engineID, pathID)

    def resetClassifier(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().resetClassifier(holowan_ip, holowan_port, engineID, portID)

    def resetEngine(self, holowan_ip: str = "defaule", holowan_port: str = "default", engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().resetEngine(holowan_ip, holowan_port, engineID)



if __name__ == '__main__':
    unittest.main()
    # # print(SubHoloWAN.__dict__.values())
    # # print(type(SubHoloWAN.__dict__))
    # # print(dir(SubHoloWAN))
    # holowan = SubHoloWAN("192.168.1.199", "8080")
    # for callable in SubHoloWAN.__dict__.values():
    #     if type(callable) is str:
    #         continue
    #     if callable.__name__ == "__init__":
    #         continue
    #     print(type(callable))
    #     print(callable)
    #     callable(holowan)
    # ip = "192.168.1.1.1"
    # port = "8080"
    # holowan = SubHoloWAN(ip, port)
    # response = holowan.get_HoloWAN_information()
    # print(response)

