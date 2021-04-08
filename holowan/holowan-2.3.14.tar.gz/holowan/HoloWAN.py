import requests
from utils import XmlUtil as xt
from utils import MyUtil as mt
import os
import json
from functools import wraps
import inspect

# 检测参数类型的类装饰器
class checkParameter(object):
    def __call__(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            newArgs = list()
            newKwargs = dict()
            sig = inspect.signature(function)  # 提取函数签名
            params = sig.parameters
            va = list(params.values())
            for arg, param in zip(args, va):
                if type(arg) == int and param.annotation ==float:
                    arg = float(arg)
                if param.annotation != inspect._empty and not isinstance(arg, param.annotation):
                    raise TypeError("{} parameter type error".format(param.name))
                if param.name == "holowan_ip":
                    if mt.isIP(arg) is False:
                        return '{"errCode":"-500","errMsg":"Parameter ERROR","errReason":"Error IP address"}'
                if param.name == "holowan_port":
                    if mt.isPort(arg) is False:
                        return '{"errCode":"-500","errMsg":"Parameter ERROR","errReason":"Error Port"}'
                newArgs.append(arg)
            for k, v in kwargs.items():
                if isinstance(v, int) and params[k].annotation == float:
                    v = float(v)
                if params[k].annotation != inspect._empty and not isinstance(v, params[k].annotation):
                    raise TypeError("{} parameter type error".format(params[k].name))
                if k == "holowan_ip":
                    if mt.isIP(v) is False:
                        return '{"errCode":"-500","errMsg":"Parameter ERROR","errReason":"Error IP address"}'
                if k == "holowan_port":
                    if mt.isPort(v) is False:
                        return '{"errCode":"-500","errMsg":"Parameter ERROR","errReason":"Error Port"}'
                newKwargs[k] = v
            # return function(*args, **kwargs)
            return function(*tuple(newArgs), **dict(newKwargs))
        return wrapper

# Modify参数检测的类装饰器
class checkModify(object):
    project_path = os.path.abspath(os.path.dirname(__file__))
    ini = mt.open_ini(project_path + r"/resources/HoloWAN.ini")
    matchTypeList = ini.get("modify", "matchType").split(", ")
    modifyTypeList = ini.get("modify", "modifyType").split(", ")

    def __call__(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(function)  # 提取函数签名
            params = sig.parameters
            va = list(params.values())
            for arg, param in zip(args, va):
                if param.name == "matchType":
                    if str(arg) not in self.matchTypeList:
                        return '{"errCode":"-43","errMsg":"ERROR","errReason":"Error parameter values ' + param.name + '"}'
                if param.name == "modifyType":
                    if str(arg) not in self.modifyTypeList:
                        return '{"errCode":"-51","errMsg":"ERROR","errReason":"Error parameter values ' + param.name + '"}'
                if param.name == "matchValue":
                    if mt.isDoubleHexadecimal(arg) is False:
                        return '{"errCode":"-49","errMsg":"ERROR","errReason":"Error parameter values ' + param.name + '"}'
                if param.name == "modifyValue":
                    if mt.isDoubleHexadecimal(arg) is False:
                        return '{"errCode":"-57","errMsg":"ERROR","errReason":"Error parameter values ' + param.name + '"}'
            for k, v in kwargs.items():
                if k == "matchType":
                    if str(v) not in self.matchTypeList:
                        return '{"errCode":"-43","errMsg":"ERROR","errReason":"Error parameter values ' + k + '"}'
                if k == "modifyType":
                    if str(v) not in self.modifyTypeList:
                        return '{"errCode":"-51","errMsg":"ERROR","errReason":"Error parameter values ' + k + '"}'
                if k == "matchValue":
                    if mt.isDoubleHexadecimal(v) is False:
                        return '{"errCode":"-49","errMsg":"ERROR","errReason":"Error parameter values ' + k + '"}'
                if k == "modifyValue":
                    if mt.isDoubleHexadecimal(v) is False:
                        return '{"errCode":"-57","errMsg":"ERROR","errReason":"Error parameter values ' + k + '"}'
            return function(*args, **kwargs)
        return wrapper

class HoloWAN:

    def __init__(self):
        self.project_path = os.path.abspath(os.path.dirname(__file__))
        self.path_crud_fileName = r"{}/resources/path_crud.xml".format(self.project_path)
        self.path_config_fileName = r"{}/resources/path_config.xml".format(self.project_path)
        self.get_HoloWAN_information_api = "statistics_information"
        self.emulator_config_api = "emulator_config"
        self.history_data_count = "history_data_count"

        # 初始化配置信息
        self.ini = mt.open_ini(self.project_path + r"/resources/HoloWAN.ini")
        self.matchTypeList = self.ini.get("modify", "matchType").split(", ")
        self.modifyTypeList = self.ini.get("modify", "modifyType").split(", ")

        self.modifyRandomRateDecimal = self.ini.get("modify", "modifyRandomRateDecimal")
        self.constantDelayDecimal = self.ini.get("delay", "constantDelayDecimal")
        self.uniformMinimumDecimal = self.ini.get("delay", "uniformMinimumDecimal")
        self.uniformMaximumDecimal = self.ini.get("delay", "uniformMaximumDecimal")
        self.normalMinDecimal = self.ini.get("delay", "normalMinDecimal")
        self.normalMeanDecimal = self.ini.get("delay", "normalMeanDecimal")
        self.normalStdDeviationDecimal = self.ini.get("delay", "normalStdDeviationDecimal")
        self.normalAdvancedPeriodDecimal = self.ini.get("delay", "normalAdvancedPeriodDecimal")
        self.normalAdvancedDurationDecimal = self.ini.get("delay", "normalAdvancedDurationDecimal")
        self.normalAdvancedMinDecimal = self.ini.get("delay", "normalAdvancedMinDecimal")
        self.normalAdvancedMaxDecimal = self.ini.get("delay", "normalAdvancedMaxDecimal")
        self.customMeanDelayDecimal = self.ini.get("delay", "customMeanDelayDecimal")
        self.customMinDelayDecimal = self.ini.get("delay", "customMinDelayDecimal")
        self.customMaxDelayDecimal = self.ini.get("delay", "customMaxDelayDecimal")
        self.customPositiveDeltaDecimal = self.ini.get("delay", "customPositiveDeltaDecimal")
        self.customNegativeDeltaDecimal = self.ini.get("delay", "customNegativeDeltaDecimal")
        self.customSpreadDeltaDecimal = self.ini.get("delay", "customSpreadDeltaDecimal")
        self.randomRateDecimal = self.ini.get("loss", "randomRateDecimal")
        self.burstProbabilityDecimal = self.ini.get("loss", "burstProbabilityDecimal")
        self.dualGoodStateLossDecimal = self.ini.get("loss", "dualGoodStateLossDecimal")
        self.dualGoodToBadProbabilityDecimal = self.ini.get("loss", "dualGoodToBadProbabilityDecimal")
        self.dualBadStateLossDecimal = self.ini.get("loss", "dualBadStateLossDecimal")
        self.dualBadToGoodProbabilityDecimal = self.ini.get("loss", "dualBadToGoodProbabilityDecimal")
        self.normalProbabilityDecimal = self.ini.get("reordering", "normalProbabilityDecimal")
        self.normalDelayMinDecimal = self.ini.get("reordering", "normalDelayMinDecimal")
        self.normalDelayMaxDecimal = self.ini.get("reordering", "normalDelayMaxDecimal")
        self.duplicationNormalProbabilityDecimal = self.ini.get("duplication", "duplicationNormalProbabilityDecimal")
        self.etherType =self.ini.get("mac", "etherType")

        self.IPV4 = 0
        self.IPV6 = 1
        self.MAC = 2
        self.TCP = 3
        self.UDP = 4
        self.IPV4ANDTCP = 5
        self.IPV4ANDUDP = 6
        self.ADD = 0
        self.REMOVE = 1
        self.REMOVEALL = 2

        self.REMOVEPATH = 1
        self.OPENORCLOSEPATH = 3
        self.CLOSEPATH = 1
        self.OPENPATH = 2

        # 错误码[链路增删配置]
        self.ini2 = mt.open_ini2(self.project_path + r"/resources/HoloWAN.ini", "PathOperateErrorCode")
        self.POengineIDError = self.ini2.getOption("engineIDError")
        self.POpathIDError = self.ini2.getOption("pathIDError")
        self.POpathNameError = self.ini2.getOption("pathIDError")
        self.POremovePathNotFound = self.ini2.getOption("removePathNotFound")
        self.POpathExist = self.ini2.getOption("pathExist")
        self.POopenPathNotFound = self.ini2.getOption("openPathNotFound")
        self.POclosePathNotFound = self.ini2.getOption("closePathNotFound")
        self.POpathIsOpening = self.ini2.getOption("pathIsOpening")
        
        # 错误码[链路损伤配置]
        self.ini2.setSection("PathConfigErrorCode")
        self.PCengineIDError = self.ini2.getOption("engineIDError")
        self.PCpathIDError = self.ini2.getOption("pathIDError")
        self.PCpathNotFound = self.ini2.getOption("pathNotFound")
        self.PCpathNameTooLong = self.ini2.getOption("pathNameTooLong")
        self.PCpathDirectionError = self.ini2.getOption("pathDirectionError")

    ''' =============================================身份验证相关接口================================================='''
    # 引擎锁
    @checkParameter()
    def hold_engine(self, holowan_ip: str, holowan_port: str, engineID: int, password: int, new_password: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param password: 原密码
        :param new_password: 新密码
        :return: 功能：1.检测锁状态 输入[password=0, new_password=0] return [0:无锁, -4:锁]
                      2.开     锁 输入[password=0或xxxx, new_password=xxxx] return [0:成功, -4:password错误]
                      3.设置新密码 输入[password=0或xxxx, new_password=xxxx] return [0:成功, -4:password错误]
                      4.清除 密码  输入[password=4123456789, new_password=4123456789] return [0:成功, -4:password错误]

        '''
        try:
            isCheck = (password == 0 and new_password == 0)
            isOpen = (mt.isFourInteger(password) and new_password == 0)
            isSet = (mt.isFourInteger(password) or password == 0) and mt.isFourInteger(new_password)
            isClean = (password == 4123456789 and new_password == 4123456789)
            if (isCheck or isOpen or isSet or isClean) is False:
                raise RuntimeError(r'{"errCode":"-4","errMsg":"error","errReason":"password error"}')
            requestURL = "http://{0}:{1}//hold_engine?engine={2}&passwd={3}&new_passwd={4}".format(holowan_ip, holowan_port, engineID, password, new_password)
            return requests.get(requestURL).text
        except requests.exceptions.ConnectionError:
            return r'{"errCode":"-200","errMsg":"ConnectionError","errReason":"Failed to establish a new connection"}'
        except RuntimeError as r:
            return r

    ''' ===============================================损伤参数相关接口===================================================='''
    # 获取当前HoloWAN设备xml信息
    @checkParameter()
    def get_HoloWAN_information(self, holowan_ip: str, holowan_port: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :return: 当前HoloWAN设备xml信息，详见附录一（1.1设备概述信息XML格式）
        '''
        requestURL = "http://{0}:{1}/{2}".format(holowan_ip, holowan_port, self.get_HoloWAN_information_api)
        return requests.get(requestURL).text

    # 新增虚拟链路path
    @checkParameter()
    def add_path(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathName: str = "PATH"):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathName: 链路名
        :return: json 正确：errCode 等于 0，错误：errCode小于0（详见附录二（1.1修改虚拟链路配置错误编号））
        '''
        if pathName == "PATH":
            pathName = pathName+" "+str(pathID)
        children_node_Map = {"modify_switch": "2", "engine_id": engineID, "path_id": pathID,
                             "path_name": pathName, "if_enable": "1"}
        node = xt.get_node(xt.xmlFile_to_Object(self.path_crud_fileName), ".")
        xt.remove_children(node)
        xt.add_children(node, children_node_Map)
        XMLStr = xt.xmlObject_to_string(node)
        add_path_return = mt.post_original_api("http://{0}:{1}/{2}".format(holowan_ip, holowan_port, self.emulator_config_api), XMLStr)
        if json.loads(add_path_return)["errCode"] == "0":
            return self.init_path(holowan_ip, holowan_port, engineID, pathID, pathName)
        else:
            return add_path_return

    # 初始化的链路
    @checkParameter()
    def init_path(self, holowan_ip:str, holowan_port: str, engineID: int, pathID: int, pathName: str):
        root = xt.get_node(xt.xmlFile_to_Object(self.path_config_fileName), ".")
        xt.set_node_text(xt.get_node(root, "./eid"), engineID)
        xt.set_node_text(xt.get_node(root, "./pid"), pathID)
        xt.set_node_text(xt.get_node(root, "./pn"), pathName)
        pathXMLStr = xt.xmlObject_to_string(root)
        requestURL = "http://{0}:{1}/emulator_config.xml".format(holowan_ip, holowan_port)
        return mt.post_original_api(requestURL, pathXMLStr)

    # 删除虚拟链路path
    @checkParameter()
    def remove_path(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathName: str,
                    force: bool = False):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathName: 链路名
        :param force: 是否强制删除
        :return: json 正确：errCode 等于 0，错误：errCode小于0（详见附录二（1.1修改虚拟链路配置错误编号））
        '''
        children_node_Map = {"modify_switch": "1", "engine_id": engineID, "path_id": pathID, "path_name": pathName,
                             "if_enable": "1"}
        if self.has_engine(holowan_ip, holowan_port, engineID) is False:
            return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"ENGINE is not found"}}'.format(self.POengineIDError)
        elif self.has_path(holowan_ip, holowan_port, engineID, pathID) is False:
            if pathID > 15 or pathID <= 0:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH Error"}}'.format(self.POpathIDError)
            else:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH is not found"}}'.format(self.POremovePathNotFound)
        if force is False:
            if self.path_is_open(holowan_ip, holowan_port, engineID, pathID):
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH is enabled, can not be deleted"}}'.format(self.POpathIsOpening)
        return self.remove_or_open_or_close_path(holowan_ip, holowan_port, engineID, pathID, pathName,
                                                 children_node_Map)

    # 开启虚拟链路path
    @checkParameter()
    def open_path(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathName: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathName: 链路名
        :return: json 正确：errCode 等于 0，错误：errCode小于0（详见附录二（1.1修改虚拟链路配置错误编号））
        '''
        if self.has_engine(holowan_ip, holowan_port, engineID) is False:
            return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"ENGINE is not found"}}'.format(self.POengineIDError)
        elif self.has_path(holowan_ip, holowan_port, engineID, pathID) is False:
            if pathID > 15 or pathID <= 0:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH Error"}}'.format(self.POpathIDError)
            else:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH is not found"}}'.format(self.POopenPathNotFound)
        if pathName == "PATH" or pathName == None:
            pathName = self.get_path_Name(holowan_ip, holowan_port, engineID, pathID)
        children_node_Map = {"modify_switch": "3", "engine_id": engineID, "path_id": pathID, "path_name": pathName,
                             "if_enable": "2"}
        return self.remove_or_open_or_close_path(holowan_ip, holowan_port, engineID, pathID, pathName,
                                                 children_node_Map)

    # 关闭虚拟链路path
    @checkParameter()
    def close_path(self, holowan_ip:str, holowan_port:str, engineID:int, pathID:int, pathName: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathName: 链路名
        :return: json 正确：errCode 等于 0，错误：errCode小于0（详见附录二（1.1修改虚拟链路配置错误编号））
        '''
        if self.has_engine(holowan_ip, holowan_port, engineID) is False:
            return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"ENGINE is not found"}}'.format(self.POengineIDError)
        elif self.has_path(holowan_ip, holowan_port, engineID, pathID) is False:
            if pathID > 15 or pathID <= 0:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH Error"}}'.format(self.POpathIDError)
            else:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH is not found"}}'.format(self.POclosePathNotFound)
        if pathName == "PATH" or pathName == None:
            pathName = self.get_path_Name(holowan_ip, holowan_port, engineID, pathID)
        children_node_Map = {"modify_switch": "3", "engine_id": engineID, "path_id": pathID, "path_name": pathName,
                             "if_enable": "1"}
        return self.remove_or_open_or_close_path(holowan_ip, holowan_port, engineID, pathID, pathName,
                                                 children_node_Map)

    # 删除/开启/关闭虚拟链路path共同代码
    def remove_or_open_or_close_path(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathName, children_node_Map):
        root = xt.xmlFile_to_Object(self.path_crud_fileName)
        node = xt.get_node(root, ".")
        xt.remove_children(node)
        xt.add_children(node, children_node_Map)
        XMLStr = xt.xmlObject_to_string(node)
        return mt.post_original_api("http://{0}:{1}/{2}".format(holowan_ip, holowan_port, self.emulator_config_api), XMLStr)

    # 设置虚拟链路（PATH）上下行方向
    @checkParameter()
    def set_path_direction(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1. 仅损伤下行，2. 仅损伤上行，3. 损伤上下行]
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        tagPath = "pd"
        tagText = pathDirection
        return self.set_one_tag_text(holowan_ip, holowan_port, engineID, pathID, tagPath, tagText)

    # 设置path带宽，Fixed正常模式
    @checkParameter()
    def set_path_Bandwidth_Fixed(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int,
                                 pathDirection: int, rateValue: int, rateUnit: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1. 仅损伤下行，2. 仅损伤上行]
        :param rateValue: 带宽限制值
        :param rateUnit: 带宽单位  [1.bps, 2.Kbps, 3.Mbps]
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        parent_node_ID = "bd"
        children_node_Map = {"s": 1, "r": rateValue, "t": rateUnit}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 关闭背景流量 [s=1: 关闭]
    @checkParameter()
    def close_Background_Utilization(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int,
                                     pathDirection: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        try:
            return self.close_damage_config(holowan_ip, holowan_port, engineID, pathID, pathDirection, "/bg/s")
        except RuntimeError as e:
            return e

    # 设置背景流量
    @checkParameter()
    def set_Background_Utilization(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int,
                                   pathDirection: int, rate: int, burst: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param rate: 背景流量带宽占比例
        :param burst: 背景流量报文大小
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        parent_node_ID = "bg"
        children_node_Map = {"s": 2, "lu": rate, "bs": burst}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置队列深度
    @checkParameter()
    def set_Queue_Limit_Drop_Tail(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int,
                                  pathDirection: int, queueDepthValue: int,
                                  queueDepthType: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向  [1.仅损伤下行，2.仅损伤上行]
        :param queueDepthValue: 队列深度值大小
        :param queueDepthType: 队列深度值类型  [1.报文格式， 2.内存大小， 3.时间ms]
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        parent_node_ID = "ql"
        children_node_Map = {"qd": queueDepthValue, "qdt": queueDepthType}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 关闭报文配置
    @checkParameter()
    def close_message_Modify(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        try:
            return self.close_damage_config(holowan_ip, holowan_port, engineID, pathID, pathDirection, "/md/cs")
        except RuntimeError as e:
            return e



    # 设置报文配置 Normal模式
    @checkParameter()
    @checkModify()
    def set_message_Modify_Normal(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int,
                                  pathDirection: int, matchType: int,
                                  matchOffset: int, matchSize: int, matchValue: str,
                                  modifyType: int, modifyOffset: int, modifySize: int, modifyValue: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param matchType: 修改报文二次匹配起始位置类型,[1.Ether, 4.Valn, 5.Vlan Stack, 6.Mpls, 7.PPPoE, 8.IPv4, 12.IPv6, 15.TCP, 17.UDP]
        :param matchOffset: 修改报文二次匹配距离起始位置偏移量
        :param matchSize: 修改报文二次匹配值大小,[1,2,4,6,8],单位Byte
        :param(str) mathValue: 修改报文二次匹配值
        :param modifyType: 修改报文修改起始位置类型,??????????????????????????????????????????????????????
        :param modifyOffset: 修改报文修改位置距离起始位置的偏移量
        :param modifySize: 修改报文新的值大小,[1,2,4,6,8],单位Byte
        :param(str) modifyValue:修改报文新的值
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        parent_node_ID = "md"
        children_node_Map = {"cs": "1", "pt": matchType, "po": matchOffset, "ps": matchSize,
                             "pv": "0x" + matchValue,
                             "mt": modifyType, "mo": modifyOffset, "ms": modifySize, "mv": "0x" + modifyValue}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置报文配置 Cycle模式
    @checkParameter()
    @checkModify()
    def set_message_Modify_Cycle(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int,
                                 pathDirection: int, matchType: int, matchOffset: int, matchSize: int,
                                 matchValue: str, modifyType: int, modifyOffset: int, modifySize: int,
                                 modifyValue: str, modifyCyclePeriod: int, modifyCycleBurst: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param matchType: 修改报文二次匹配起始位置类型,[1.Ether, 4.Valn, 5.Vlan Stack, 6.Mpls, 7.PPPoE, 8.IPv4, 12.IPv6, 15.TCP, 17.UDP]
        :param matchOffset:修改报文二次匹配距离起始位置偏移量
        :param matchSize: 修改报文二次匹配值大小,[1,2,4,6,8],单位Byte
        :param(str) mathValue: 修改报文二次匹配值
        :param modifyType: 修改报文修改起始位置类型,??????????????????????????????????????????????????????
        :param modifyOffset: 修改报文修改位置距离起始位置的偏移量
        :param modifySize: 修改报文新的值大小,[1,2,4,6,8],单位Byte
        :param(str) modifyValue: 修改报文新的值
        :param modifyCyclePeriod: ??????????????????????????????????????????????????????
        :param modifyCycleBurst: ??????????????????????????????????????????????????????
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''

        parent_node_ID = "md"
        children_node_Map = {"cs": "2", "pt": matchType, "po": matchOffset, "ps": matchSize,
                             "pv": "0x" + matchValue,
                             "mt": modifyType,
                             "mo": modifyOffset, "ms": modifySize, "mv": "0x" + modifyValue,
                             "mcp": modifyCyclePeriod,
                             "mcb": modifyCycleBurst}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置报文配置 Random模式
    @checkParameter()
    @checkModify()
    def set_message_Modify_Random(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int,
                                 pathDirection: int, matchType: int, matchOffset: int, matchSize: int,
                                 matchValue: str, modifyType: int, modifyOffset: int, modifySize: int,
                                 modifyValue: str, modifyRandomRate: float):
        '''

        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param matchType: 修改报文二次匹配起始位置类型,[1.Ether, 4.Valn, 5.Vlan Stack, 6.Mpls, 7.PPPoE, 8.IPv4, 12.IPv6, 15.TCP, 17.UDP]
        :param matchOffset:修改报文二次匹配距离起始位置偏移量
        :param matchSize: 修改报文二次匹配值大小,[1,2,4,6,8],单位Byte
        :param(str) mathValue: 修改报文二次匹配值
        :param modifyType: 修改报文修改起始位置类型,??????????????????????????????????????????????????????
        :param modifyOffset: 修改报文修改位置距离起始位置的偏移量
        :param modifySize: 修改报文新的值大小,[1,2,4,6,8],单位Byte
        :param(str) modifyValue: 修改报文新的值
        :param modifyRandomRate: ??????????????????????????????????????????????????????
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        if len(str(modifyRandomRate).split('.')[1]) > int(self.modifyRandomRateDecimal):
            return r'{"errCode":"-64","errMsg":"ERROR","errReason":"Error parameter values modifyRandomRate"}'

        parent_node_ID = "md"
        children_node_Map = {"cs": "3", "pt": matchType, "po": matchOffset, "ps": matchSize,
                             "pv": "0x" + matchValue,
                             "mt": modifyType,
                             "mo": modifyOffset, "ms": modifySize, "mv": "0x" + modifyValue,
                             "mrr": modifyRandomRate}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 关闭MTU限制配置
    @checkParameter()
    def close_MTU_Limit(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int):
        '''

        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        try:
            return self.close_damage_config(holowan_ip, holowan_port, engineID, pathID, pathDirection, "/m/s")
        except RuntimeError as e:
            return e

    # 设置MTU限制配置
    @checkParameter()
    def set_MTU_Limit(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                      limitValue: int):
        '''

        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param limitValue:
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        parent_node_ID = "m"
        children_node_Map = {"s": "2", "n": limitValue}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置以太网间隙占用配置
    @checkParameter()
    def set_Frame_Overhead(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                           type: int, rate: int):
        '''

        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param type: 帧间隙占用类型,[1.默认以太网24, 2.最小4, 3.自定义值]
        :param rate: 帧间隙大小值
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        parent_node_ID = "fo"
        if type == 1:
            children_node_Map = {"t": 1, "r": 24}
        elif type == 2:
            children_node_Map = {"t": 2, "r": 4}
        elif type == 3:
            children_node_Map = {"t": 3, "r": rate}
            if rate <= 0 or rate > 64:
                return r'{"errCode":"-500","errMsg":"ERROR","errReason":"rate ranges from 1 to 64"}'
        else:
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(type)"}'
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置时延配置  常量时延(Constant)
    @checkParameter()
    def set_Delay_Constant(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                           delay: float):
        '''

        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param(float) delay: 时延值 [>0.1] 单位ms
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        if len(str(delay).split(".")[1]) > int(self.constantDelayDecimal) or delay < 0.1:
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(delay)"}'

        parent_node_ID = "d"
        children_node_Map = {"s": "1", "co": {"de": delay}}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置时延配置  平均分布时延(Uniform)  无高级设置
    @checkParameter()
    def set_Delay_Uniform(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                          minimum: float, maximum: float,
                          enableReordering: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param(float) minimum: 平均分布最小值
        :param(float) maximum: 平均分布最大值
        :param enableReordering: 是否允许时延乱序 [0.关闭, 1.开启]
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''

        if len(str(minimum).split(".")[1]) > int(self.uniformMinimumDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(minimum)"}'

        if len(str(maximum).split(".")[1]) > int(self.uniformMaximumDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(maximum)"}'

        if enableReordering not in [0, 1]:
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(enableReordering)"}'



        parent_node_ID = "d"
        children_node_Map = {"s": "2", "un": {"dmi": minimum, "dma": maximum, "reo": enableReordering, "shake": ""}}
        properties_Map = {"un/shake": {"type_id": "0"}}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置时延配置  正太分布时延(Uniform)  无高级设置
    @checkParameter()
    def set_Delay_Normal(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                         min: float, mean: float, stdDeviation: float, enableReordering: int):
        '''

        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param(float) min: 最小截断值
        :param(float) mean: 期望值
        :param stdDeviation: 标准差
        :param enableReordering: 是否允许时延乱序 [0.关闭, 1.开启]
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''

        if (len(str(min).split(".")[1])) > int(self.normalMinDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(min)"}'

        if (len(str(mean).split(".")[1])) > int(self.normalMeanDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(mean)"}'

        if (len(str(stdDeviation).split(".")[1])) > int(self.normalStdDeviationDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(stdDeviation)"}'

        if enableReordering not in [0, 1]:
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(enableReordering)"}'

        parent_node_ID = "d"
        children_node_Map = {"s": "3",
                             "no": {"de": min, "me": mean, "sd": stdDeviation, "reo": enableReordering, "b": ""}}
        properties_Map = {"./no/b": {"e": "0"}}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置时延配置  正太分布时延(Uniform)  高级设置
    @checkParameter()
    def set_Delay_Normal_AdvancedSetup(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                         min: float, mean: float, stdDeviation: float, enableReordering: int, advancedPeriod: float,
                                       advancedDuration: float, advancedMin: float, advancedMax: float):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param(float) min: 最小截断值
        :param(float) mean: 期望值
        :param stdDeviation: 标准差
        :param enableReordering: 是否允许时延乱序 [0.关闭, 1.开启]
        :param advancedPeriod: ???????????????????????????????????????????????
        :param adcancedDuration: ???????????????????????????????????????????????
        :param advancedMin: ???????????????????????????????????????????????
        :param advancedMax: ???????????????????????????????????????????????
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''

        if (len(str(min).split(".")[1])) > int(self.normalMinDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(min)"}'

        if (len(str(mean).split(".")[1])) > int(self.normalMeanDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(mean)"}'

        if (len(str(stdDeviation).split(".")[1])) > int(self.normalStdDeviationDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(stdDeviation)"}'

        if enableReordering not in [0, 1]:
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(enableReordering)"}'

        if (len(str(advancedPeriod).split(".")[1])) > int(self.normalAdvancedPeriodDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(advancedPeriod)"}'

        if (len(str(advancedDuration).split(".")[1])) > int(self.normalAdvancedDurationDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(adcancedDuration)"}'

        if (len(str(advancedMax).split(".")[1])) > int(self.normalAdvancedMaxDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(advancedMax)"}'

        if (len(str(advancedMin).split(".")[1])) > int(self.normalAdvancedMinDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(advancedMin)"}'

        parent_node_ID = "d"
        children_node_Map = {"s": "3", "no": {"de": min, "me": mean, "sd": stdDeviation, "reo": enableReordering,
                                              "b": {"p": advancedPeriod, "d": advancedDuration, "mi": advancedMin,
                                                    "ma": advancedMax}}}
        properties_Map = {"./no/b": {"e": "1"}}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置时延配置  可自定义的正太分布时延(Custom)
    @checkParameter()
    def set_Delay_Custom(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                         meanDelay: float, minDelay: float, maxDelay: float, positiveDelta: float,
                         negativeDelta: float, spread: float, enableReordering: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param meanDelay: 平均时延
        :param minDelay: 最小时延
        :param maxDelay: 最大时延
        :param positiveDelta: 最大正向变化值
        :param negativeDelta: 最大负向变化值
        :param spread: Spread值
        :param enableReordering: 是否允许时延乱序 [0.关闭, 1.开启]
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''

        if (len(str(meanDelay).split(".")[1])) > int(self.customMeanDelayDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(meanDelay)"}'
        if (len(str(minDelay).split(".")[1])) > int(self.customMinDelayDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(minDelay)"}'
        if (len(str(maxDelay).split(".")[1])) > int(self.customMaxDelayDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(maxDelay)"}'
        if (len(str(positiveDelta).split(".")[1])) > int(self.customPositiveDeltaDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(positiveDelta)"}'
        if (len(str(negativeDelta).split(".")[1])) > int(self.customNegativeDeltaDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(negativeDelta)"}'
        if (len(str(spread).split(".")[1])) > int(self.customSpreadDeltaDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(spread)"}'
        if meanDelay >= maxDelay:
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"meanDelay must be less than maxDelay"}'

        if enableReordering not in [0, 1]:
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(enableReordering)"}'

        parent_node_ID = "d"
        children_node_Map = {"s": "4", "cu": {"made": maxDelay, "mede": meanDelay, "mide": minDelay, "pd": positiveDelta,
                                              "nd": negativeDelta, "spd": spread, "reo": enableReordering}}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                     parent_node_ID,
                                     children_node_Map, properties_Map)

    # 设置丢包配置  Random普通概率模式
    @checkParameter()
    def set_Loss_Random(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int, rate: float):
        '''

        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param rate: 普通概率丢包概率值
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        if (len(str(rate).split(".")[1])) > int(self.randomRateDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(rate)"}'

        parent_node_ID = "l"
        children_node_Map = {"s": "1", "ra": {"r": rate}}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置丢包配置  Cycle周期丢包模式
    @checkParameter()
    def set_Loss_Cycle(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                       period: int, burst: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param period: 周期丢包周期值，单位为报文个数
        :param burst: 周期丢包数量，单位为报文个数
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        parent_node_ID = "l"
        children_node_Map = {"s": "2", "cy": {"a": period, "l": burst}}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置丢包配置  Burst突发丢包模式
    @checkParameter()
    def set_Loss_Burst(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                       probability: float, minimum: int, maximum: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param probability: 突发丢包概率值
        :param minimum: 突发丢包最小丢包数量
        :param maximum: 突发丢包最大丢包数量
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''

        if (len(str(probability).split(".")[1])) > int(self.burstProbabilityDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(probability)"}'

        parent_node_ID = "l"
        children_node_Map = {"s": "3", "bu": {"l": probability, "mi": minimum, "ma": maximum}}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置丢包配置  Dual双通道丢包模式
    @checkParameter()
    def set_Loss_Dual(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                      goodStateLoss: float, goodToBadProbability: float, badStateLoss: float,
                      badToGoodProbability: float):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param goodStateLoss: 好通道丢包概率
        :param goodToBadProbability: 好通道转换到坏通道的转换概率
        :param badStateLoss: 坏通道丢包概率
        :param badToGoodProbability: 坏通道转换到好通道的转换概率
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        if (len(str(goodStateLoss).split(".")[1])) > int(self.dualGoodStateLossDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(goodStateLoss)"}'
        if (len(str(goodToBadProbability).split(".")[1])) > int(self.dualGoodToBadProbabilityDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(goodToBadProbability)"}'
        if (len(str(badStateLoss).split(".")[1])) > int(self.dualBadStateLossDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(badStateLoss)"}'
        if (len(str(badToGoodProbability).split(".")[1])) > int(self.dualBadToGoodProbabilityDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(badToGoodProbability)"}'

        parent_node_ID = "l"
        children_node_Map = {"s": "4", "du": {"g": goodStateLoss, "b": badStateLoss, "gtb": goodToBadProbability,
                                              "btg": badToGoodProbability}}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置BER配置
    @checkParameter()
    def set_BER(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                bitErrorValue: int, bitErrorIndex: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param bitErrorValue: BER值
        :param bitErrorIndex: BER指数值
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        if bitErrorIndex >= 0:
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(bitErrorIndex)"}'
        bitErrorIndex = abs(bitErrorIndex)
        parent_node_ID = "cor"
        children_node_Map = {"ber": bitErrorValue, "beri": bitErrorIndex}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置报文乱序配置  默认类型
    @checkParameter()
    def set_Reordering_Normal(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                              probability: float, delayMin: float, delayMax: float):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param probability: 报文乱序概率
        :param delayMin: 报文乱序延时最小值
        :param delayMax: 报文乱序延时最大值
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        if (len(str(probability).split(".")[1])) > int(self.normalProbabilityDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(probability)"}'
        if (len(str(delayMin).split(".")[1])) > int(self.normalDelayMinDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(delayMin)"}'
        if (len(str(delayMax).split(".")[1])) > int(self.normalDelayMaxDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(delayMax)"}'

        parent_node_ID = "reo"
        children_node_Map = {"s": "1", "p": probability, "dmi": delayMin, "dma": delayMax}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 设置重复报文配置  默认类型
    @checkParameter()
    def set_Duplication_Normal(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int,
                               probability: float):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1.仅损伤下行，2.仅损伤上行]
        :param probability: 重复报文概率
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        if (len(str(probability).split(".")[1])) > int(self.duplicationNormalProbabilityDecimal):
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(probability)"}'
        parent_node_ID = "du"
        children_node_Map = {"s": "1", "p": probability}
        properties_Map = {}
        return self.set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                  parent_node_ID,
                                                  children_node_Map, properties_Map)

    # 获取path链路xml信息
    @checkParameter()
    def get_path_config_information(self, holowan_ip:str, holowan_port:str, engineID:int, pathID: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :return: 修改虚拟链路损伤参数XML
        '''
        try:
            requestURL = "http://{0}:{1}/path_config_info_{2}_{3}.xml".format(holowan_ip, holowan_port, engineID, pathID)
            return requests.get(requestURL).text
        except Exception as e:
            if self.has_engine(holowan_ip, holowan_port, engineID) is False:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"ENGINE has no found"}}'.format(self.PCengineIDError)
            if self.right_path(holowan_ip, holowan_port, engineID, pathID) is False:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH has no found"}}'.format(self.PCpathIDError)
            if self.has_path(holowan_ip, holowan_port, engineID, pathID) is False:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH has no found"}}'.format(self.PCpathNotFound)

    # 关闭相关损伤配置
    def close_damage_config(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection: int, tapPath: str):
        try:
            tapPath_list = []
            if pathDirection == 1:
                tapPath_list.append("pltr" + tapPath)
            elif pathDirection == 2:
                tapPath_list.append("prtl" + tapPath)
            elif pathDirection == 3:
                tapPath_list.append("pltr" + tapPath)
                tapPath_list.append("prtl" + tapPath)
            else:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"Error pathDirection"}}'.format(self.PCpathDirectionError)
            tagText = 1
            response = None
            for tagPath in tapPath_list:
                response = self.set_one_tag_text(holowan_ip, holowan_port, engineID, pathID, tagPath, tagText)
                if response is RuntimeError:
                    break
                elif json.loads(response)['errCode'] != "0":
                    break
            return response
        except RuntimeError as e:
            return e


    ''' ===============================================Classifier===================================================='''
    # 添加IPV4分类器  无隧道
    @checkParameter()
    def add_IPV4_to_Classifier(self, holowan_ip:str, holowan_port:str, engineID:int, portID: int, sourceIP: str,
                               sourceMask: int, destinationIP: str, destinationMask: int, TOS: str, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourceIP": sourceIP, "sourceMask": sourceMask, "destinationIP": destinationIP,
                      "destinationMask": destinationMask, "TOS": TOS, "action": action}
        return self.classifier(self.IPV4, self.ADD, parameters)

    # 删除IPV4分类器  无隧道
    @checkParameter()
    def remove_IPV4_from_Classifier(self, holowan_ip: str, holowan_port: str, engineID:int, portID: int, sourceIP: str,
                               sourceMask: int, destinationIP: str, destinationMask: int, TOS: str, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourceIP": sourceIP, "sourceMask": sourceMask, "destinationIP": destinationIP,
                      "destinationMask": destinationMask, "TOS": TOS, "action": action}
        return self.classifier(self.IPV4, self.REMOVE, parameters)

    # 删除所有的IPV4分类器
    @checkParameter()
    def remove_all_IPV4_from_Classifier(self, holowan_ip:str, holowan_port:str, engineID:int, portID: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID}
        return self.classifier(self.IPV4, self.REMOVEALL, parameters)

    # 创建IPV4节点
    def create_IPV4(self, holowan_ip: str, holowan_port: str, engineID:int, sourceIP: str, sourceMask: int,
                    destinationIP: str, destinationMask: int, TOS: str, action: int):
        ipv4_node = xt.create_node("ipv4", {}, {})
        children_node_Map = {"src": "", "smask": sourceMask, "dst": "", "dmask": destinationMask, "tos": "",
                             "path_id": action}
        properties = {}
        # ===============src================== #
        if sourceIP == "any":
            properties["src"] = {"any": 1}
        elif mt.isIP(sourceIP):
            children_node_Map["src"] = sourceIP
        else:
            return RuntimeError(r'{"errCode":"-9","errMsg":"ERROR","errReason":"sourceIP必须输入any或ipv4地址"}')
        # ===============src mask================== #
        if sourceMask not in [32, 24, 16, 8]:
            return RuntimeError(r'{"errCode":"-9","errMsg":"ERROR","errReason":"sourceIP掩码必须为32、24、16、8中的一个"}')
        # ===============dst================== #
        if destinationIP == "any":
            properties["dst"] = {"any": 1}
        elif mt.isIP(destinationIP):
            children_node_Map["dst"] = destinationIP
        else:
            return RuntimeError(r'{"errCode":"-9","errMsg":"ERROR","errReason":"destinationIP必须输入any或ipv4地址"}')
        # ===============dst mask================== #
        if destinationMask not in [32, 24, 16, 8]:
            return RuntimeError(r'{"errCode":"-9","errMsg":"ERROR","errReason":"destinationIP掩码必须为32、24、16、8中的一个"}')
        # ===============tos================== #
        if TOS == "any":
            properties["tos"] = {"any": 1}
        elif mt.isDoubleHexadecimal(TOS):
            children_node_Map["tos"] = TOS
        else:
            return RuntimeError(r'{"errCode":"-9","errMsg":"ERROR","errReason":"TOS必须输入any或2位十六进制"}')
        # ===============action================== #
        paths_dic = self.get_pathDict_from_engine(holowan_ip, holowan_port, engineID)
        if action not in [-1, -2] and action not in paths_dic.keys():
            return RuntimeError(r'{"errCode":"-9","errMsg":"ERROR","errReason":"action值输入错误"}')
        xt.add_children(ipv4_node, children_node_Map)
        xt.add_properties(ipv4_node, properties)
        return ipv4_node

    # 添加IPV6分类器  无隧道
    @checkParameter()
    def add_IPV6_to_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int,
                               sourceIP: str, destinationIP: str, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourceIP": sourceIP, "destinationIP": destinationIP, "action": action}
        return self.classifier(self.IPV6, self.ADD, parameters)

    # 删除IPV6分类器  无隧道
    @checkParameter()
    def remove_IPV6_from_Classifier(self, holowan_ip:str, holowan_port:str, engineID:int, portID: int,
                               sourceIP: str, destinationIP: str, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourceIP": sourceIP, "destinationIP": destinationIP, "action": action}
        return self.classifier(self.IPV6, self.REMOVE, parameters)

    # 删除所有的IPV6分类器
    @checkParameter()
    def remove_all_IPV6_from_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID}
        return self.classifier(self.IPV6, self.REMOVEALL, parameters)

    # 创建IPV6节点
    def create_IPV6(self, holowan_ip:str, holowan_port:str, engineID:int, sourceIP: str, destinationIP: str, action: int):
        ipv6_node = xt.create_node("ipv6", {}, {})
        children_node_Map = {"src": "", "dst": "", "path_id": action}
        properties = {}
        # ===============src================== #
        if sourceIP == "any":
            properties["src"] = {"any": 1}
        elif mt.isIPV6(sourceIP):
            children_node_Map["src"] = sourceIP
        else:
            return RuntimeError(r'{"errCode":"-10","errMsg":"ERROR","errReason":"sourceIP必须输入any或ipv6地址"}')
        # ===============dst================== #
        if destinationIP == "any":
            properties["dst"] = {"any": 1}
        elif mt.isIPV6(sourceIP):
            children_node_Map["dst"] = sourceIP
        else:
            return RuntimeError(r'{"errCode":"-10","errMsg":"ERROR","errReason":"destinationIP必须输入any或ipv6地址"}')
        # ===============Action================== #
        paths_dic = self.get_pathDict_from_engine(holowan_ip, holowan_port, engineID)
        if action not in [-1, -2] and action not in paths_dic.keys():
            return RuntimeError(r'{"errCode":"-10","errMsg":"ERROR","errReason":"action值输入错误"}')
        xt.add_children(ipv6_node, children_node_Map)
        xt.add_properties(ipv6_node, properties)
        return ipv6_node

    # 添加MAC分类器  无隧道
    @checkParameter()
    def add_MAC_to_Classifier(self, holowan_ip:str, holowan_port:str, engineID:int, portID: int, sourceMAC: str,
                              destinationMAC: str, EtherType: str, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourceMAC": sourceMAC, "destinationMAC": destinationMAC, "EtherType": EtherType, "action": action}
        return self.classifier(self.MAC, self.ADD, parameters)

    # 删除MAC分类器  无隧道
    @checkParameter()
    def remove_MAC_from_Classifier(self, holowan_ip:str, holowan_port:str, engineID:int, portID: int, sourceMAC: str,
                              destinationMAC: str, EtherType: str, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourceMAC": sourceMAC, "destinationMAC": destinationMAC, "EtherType": EtherType, "action": action}
        return self.classifier(self.MAC, self.REMOVE, parameters)

    # 删除所有的MAC分类器
    @checkParameter()
    def remove_all_MAC_from_Classifier(self, holowan_ip:str, holowan_port:str, engineID:int, portID: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID}
        return self.classifier(self.MAC, self.REMOVEALL, parameters)

    # 创建MAC节点
    def create_MAC(self, holowan_ip:str, holowan_port:str, engineID:int, sourceMAC: str, destinationMAC: str, EtherType: str, action: int):
        MAC_node = xt.create_node("mac", {}, {})
        children_node_Map = {"src": "", "dst": "", "type": "", "path_id": action}
        properties = {}
        # ===============src================== #
        if sourceMAC == "any":
            properties["src"] = {"any": 1}
        elif mt.isMac(sourceMAC):
            children_node_Map["src"] = sourceMAC
        else:
            return RuntimeError(r'{"errCode":"-6","errMsg":"ERROR","errReason":"sourceIP必须输入any或MAC地址"}')
        # ===============dst================== #
        if destinationMAC == "any":
            properties["dst"] = {"any": 1}
        elif mt.isMac(destinationMAC):
            children_node_Map["dst"] = destinationMAC
        else:
            return RuntimeError(r'{"errCode":"-6","errMsg":"ERROR","errReason":"destinationIP必须输入any或MAC地址"}')
        # ===============EtherType================== #
        if EtherType == "any":
            properties["type"] = {"any": 1}
        elif EtherType in self.etherType.split(", "):
            children_node_Map["type"] = EtherType
        else:
            return RuntimeError(r'{"errCode":"-6","errMsg":"ERROR","errReason":"MAC的EtherType输入值不正确"}')
        # ===============Action================== #
        paths_dic = self.get_pathDict_from_engine(holowan_ip, holowan_port, engineID)
        if action not in [-1, -2] and action not in paths_dic.keys():
            return RuntimeError(r'{"errCode":"-6","errMsg":"ERROR","errReason":"action值输入错误"}')
        xt.add_children(MAC_node, children_node_Map)
        xt.add_properties(MAC_node, properties)
        return MAC_node

    # 添加TCP分类器
    @checkParameter()
    def add_TCP_to_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int, sourcePort: str, destPort: str,
                              checkVersion: int, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourcePort": sourcePort, "destPort": destPort, "checkVersion": checkVersion, "action": action}
        return self.classifier(self.TCP, self.ADD, parameters)

    # 删除TCP分类器
    @checkParameter()
    def remove_TCP_from_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int, sourcePort: str, destPort: str,
                              checkVersion: int, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourcePort": sourcePort, "destPort": destPort, "checkVersion": checkVersion, "action": action}
        return self.classifier(self.TCP, self.REMOVE, parameters)

    # 删除所有TCP分类器
    @checkParameter()
    def remove_all_TCP_from_Classifier(self, holowan_ip:str, holowan_port:str, engineID:int, portID: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID}
        return self.classifier(self.TCP, self.REMOVEALL, parameters)

    # 添加UDP分类器 无隧道
    @checkParameter()
    def add_UDP_to_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int, sourcePort: str, destPort: str,
                              checkVersion: int, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourcePort": sourcePort, "destPort": destPort, "checkVersion": checkVersion, "action": action}
        return self.classifier(self.UDP, self.ADD, parameters)

    # 删除UDP分类器 无隧道
    @checkParameter()
    def remove_UDP_from_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int,
                                   sourcePort: str, destPort: str,
                                   checkVersion: int, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourcePort": sourcePort, "destPort": destPort, "checkVersion": checkVersion, "action": action}
        return self.classifier(self.UDP, self.REMOVE, parameters)

    # 删除所有UDP分类器
    @checkParameter()
    def remove_all_UDP_from_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID}
        return self.classifier(self.UDP, self.REMOVEALL, parameters)


    # 创建TCP/UDP节点
    def create_TCP_or_UDP(self, holowan_ip: str, holowan_port: str, engineID: int, TCPUDP: int, sourcePort: str, destPort: str, checkVersion: int, action: int):
        '''
        :param TCPUDP: 1：TCP，2：UDP
        :param sourcePort: 源端口号
        :param destPort: 目标端口号
        :param checkVersion:
        :param action:
        :return:
        '''
        tcpudp_node = xt.create_node("tcp_udp", {}, {})
        children_node_map = {"type": TCPUDP, "src": "", "dst": "", "check": checkVersion, "path_id": action}
        properties = {}
        # ===============src================== #
        if sourcePort == "any":
            properties["src"] = {"any": 1}
        elif mt.isPort(sourcePort):
            children_node_map["src"] = sourcePort
        else:
            return RuntimeError(r'{"errCode":"-11","errMsg":"ERROR","errReason":"sourcePort必须为1-65535之间"}')
        # ===============dst================== #
        if destPort == "any":
            properties["dst"] = {"any": 1}
        elif mt.isPort(destPort):
            children_node_map["dst"] = destPort
        else:
            return RuntimeError(r'{"errCode":"-11","errMsg":"ERROR","errReason":"dstPort必须为1-65535之间"}')
        # ===============checkVersion================== #
        if checkVersion not in [0, 4, 6]:
            return RuntimeError(r'{"errCode":"-11","errMsg":"ERROR","errReason":"checkVersion必须为0、4、6中的一个"}')
        # ===============Action================== #
        paths_dic = self.get_pathDict_from_engine(holowan_ip, holowan_port, engineID)
        if action not in [-1, -2] and action not in paths_dic.keys():
            return RuntimeError(r'{"errCode":"-11","errMsg":"ERROR","errReason":"action值输入错误"}')
        xt.add_children(tcpudp_node, children_node_map)
        xt.add_properties(tcpudp_node, properties)
        return tcpudp_node

    # 添加Combination(IPV4 and TCP)过滤器
    @checkParameter()
    def add_IPV4_TCP_to_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int, sourceIP: str,
                               sourceMask: int, destinationIP: str, destinationMask: int, TOS: str, sourcePort: str, destPort: str,
                              checkVersion: int, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourceIP": sourceIP, "sourceMask": sourceMask, "destinationIP": destinationIP,
                      "destinationMask": destinationMask, "TOS": TOS, "sourcePort": sourcePort,
                      "destPort": destPort, "checkVersion": checkVersion, "action": action}
        return self.classifier(self.IPV4ANDTCP, self.ADD, parameters)

    # 删除Combination(IPV4 and TCP)过滤器
    @checkParameter()
    def remove_IPV4_TCP_from_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int, sourceIP: str,
                               sourceMask: int, destinationIP: str, destinationMask: int, TOS: str, sourcePort: str, destPort: str,
                              checkVersion: int, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourceIP": sourceIP, "sourceMask": sourceMask, "destinationIP": destinationIP,
                      "destinationMask": destinationMask, "TOS": TOS, "sourcePort": sourcePort,
                      "destPort": destPort, "checkVersion": checkVersion, "action": action}
        return self.classifier(self.IPV4ANDTCP, self.REMOVE, parameters)

    # 删除所有Combination(IPV4 and TCP)过滤器
    @checkParameter()
    def remove_all_IPV4_TCP_from_Classifier(self, holowan_ip:str, holowan_port:str, engineID:int, portID: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID}
        return self.classifier(self.IPV4ANDTCP, self.REMOVEALL, parameters)

    # 添加Combination(IPV4 and UDP)过滤器
    @checkParameter()
    def add_IPV4_UDP_to_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int, sourceIP: str,
                               sourceMask: int, destinationIP: str, destinationMask: int, TOS: str, sourcePort: str, destPort: str,
                              checkVersion: int, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourceIP": sourceIP, "sourceMask": sourceMask, "destinationIP": destinationIP,
                      "destinationMask": destinationMask, "TOS": TOS, "sourcePort": sourcePort,
                      "destPort": destPort, "checkVersion": checkVersion, "action": action}
        return self.classifier(self.IPV4ANDUDP, self.ADD, parameters)

    # 删除Combination(IPV4 and UDP)过滤器
    @checkParameter()
    def remove_IPV4_UDP_from_Classifier(self, holowan_ip: str, holowan_port: str, engineID: int, portID: int, sourceIP: str,
                               sourceMask: int, destinationIP: str, destinationMask: int, TOS: str, sourcePort: str, destPort: str,
                              checkVersion: int, action: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID,
                      "sourceIP": sourceIP, "sourceMask": sourceMask, "destinationIP": destinationIP,
                      "destinationMask": destinationMask, "TOS": TOS, "sourcePort": sourcePort,
                      "destPort": destPort, "checkVersion": checkVersion, "action": action}
        return self.classifier(self.IPV4ANDUDP, self.REMOVE, parameters)


    # 删除所有Combination(IPV4 and UDP)过滤器
    @checkParameter()
    def remove_all_IPV4_UDP_from_Classifier(self, holowan_ip:str, holowan_port:str, engineID:int, portID: int):
        parameters = {"holowan_ip": holowan_ip, "holowan_port": holowan_port, "engineID": engineID, "portID": portID}
        return self.classifier(self.IPV4ANDUDP, self.REMOVEALL, parameters)


    # 创建Combination(IPV4 and TCP/UDP)节点
    def create_IPV4_and_TCP_or_UDP(self, holowan_ip: str, holowan_port: str, engineID: int, TCPUDP:int, sourceIP: str,
                                   sourceMask: int, destinationIP: str, destinationMask: int, TOS: str,
                                   sourcePort: str, destPort: str, checkVersion: int, action: int):
        # 创建ipv4节点
        ipv4_node = self.create_IPV4(holowan_ip, holowan_port, engineID, sourceIP, sourceMask, destinationIP, destinationMask, TOS, action)
        if type(ipv4_node) == RuntimeError:
            return ipv4_node
        ipv4_node.remove(xt.get_node(ipv4_node, "./path_id"))
        # 创建TCP节点
        tcp_or_udp_node = self.create_TCP_or_UDP(holowan_ip, holowan_port, engineID, TCPUDP, sourcePort, destPort, checkVersion, action)
        if type(tcp_or_udp_node) == RuntimeError:
            return tcp_or_udp_node
        tcp_or_udp_node.remove(xt.get_node(tcp_or_udp_node, "./path_id"))
        # 创建comb混合节点
        comb_node = xt.create_node("comb", {}, {})
        children_node_map = {"path_id": action}
        xt.add_children(comb_node, children_node_map)
        comb_node.append(ipv4_node)
        comb_node.append(tcp_or_udp_node)
        return comb_node


    # 获取报文分类器（Packet Classifier）最后一次配置参数
    @checkParameter()
    def get_Packet_Classifier_config_information(self, holowan_ip: str, holowan_port: str, engineID: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :return: 修改报文分类器参数XML
        '''
        try:
            requestURL = "http://{0}:{1}/classifier_config_info_{2}.xml".format(holowan_ip, holowan_port, engineID)
            return requests.get(requestURL).text
        except Exception:
            return RuntimeError(r'{"errCode":"-3","errMsg":"ERROR","errReason":"ENGINE has no found"}')

    # 添加/删除/删除所有过滤器
    # classifierType（IPV4: 0, IPV6: 1, MAC: 2, TCP: 3, UDP: 4, IPV4&TCP: 5, IPV4&UDP: 6）
    # operation（0: 添加一个, 1: 删除一个, 2: 删除所有）
    @checkParameter()
    def classifier(self, classifierType: int, operation: int, parameters: dict):
        holowan_ip = parameters.get("holowan_ip")
        holowan_port = parameters.get("holowan_port")
        engineID = parameters.get("engineID")
        portID = parameters.get("portID")
        classifierNode = None
        classifierNodeName = ""
        try:
            parent_node_path = "./port"
            classifierXMLStr = self.get_Packet_Classifier_config_information(holowan_ip, holowan_port, engineID)
            if type(classifierXMLStr) is RuntimeError:
                return str(classifierXMLStr)
        except Exception:
            return r'{{"errCode":"-3","errMsg":"ERROR","errReason":"ENGINE has no found"}}'
        root = xt.xmlString_to_Object(classifierXMLStr)
        nodes = xt.get_nodes(root, parent_node_path)
        port_node = None
        for node in nodes:
            if xt.get_node(node, "./port_id").text == str(portID):
                port_node = node
        if port_node is None:
            return r'{{"errCode":"-16",' \
                   r'"errMsg":"ConnectionError",' \
                   r'"errReason":"Engine{0} has no port{1}"}}'.format(engineID, portID)
        if operation == self.ADD or operation == self.REMOVE:
            # 创建classifier节点
            if classifierType == self.IPV4:
                sourceIP = parameters.get("sourceIP")
                sourceMask = parameters.get("sourceMask")
                destinationIP = parameters.get("destinationIP")
                destinationMask = parameters.get("destinationMask")
                TOS = parameters.get("TOS")
                action = parameters.get("action")
                classifierNodeName = "ipv4"
                # 创建ipv4节点
                classifierNode = self.create_IPV4(holowan_ip, holowan_port, engineID, sourceIP, sourceMask, destinationIP, destinationMask, TOS, action)
            elif classifierType == self.IPV6:
                sourceIP = parameters.get("sourceIP")
                destinationIP = parameters.get("destinationIP")
                action = parameters.get("action")
                classifierNodeName = "ipv6"
                # 创建ipv6节点
                classifierNode = self.create_IPV6(holowan_ip, holowan_port, engineID, sourceIP, destinationIP, action)
            elif classifierType == self.MAC:
                sourceMAC = parameters.get("sourceMAC")
                destinationMAC = parameters.get("destinationMAC")
                EtherType = parameters.get("EtherType")
                action = parameters.get("action")
                classifierNodeName = "mac"
                # 创建MAC节点
                classifierNode = self.create_MAC(holowan_ip, holowan_port, engineID, sourceMAC, destinationMAC, EtherType, action)
            elif classifierType == self.TCP:
                sourcePort = parameters.get("sourcePort")
                destPort = parameters.get("destPort")
                checkVersion = parameters.get("checkVersion")
                action = parameters.get("action")
                classifierNodeName = "tcp_udp"
                # 创建tcp节点
                classifierNode = self.create_TCP_or_UDP(holowan_ip, holowan_port, engineID, 1, sourcePort, destPort, checkVersion, action)
            elif classifierType == self.UDP:
                sourcePort = parameters.get("sourcePort")
                destPort = parameters.get("destPort")
                checkVersion = parameters.get("checkVersion")
                action = parameters.get("action")
                classifierNodeName = "tcp_udp"
                # 创建udp节点
                classifierNode = self.create_TCP_or_UDP(holowan_ip, holowan_port, engineID, 2, sourcePort, destPort, checkVersion, action)
            elif classifierType == self.IPV4ANDTCP:
                sourceIP = parameters.get("sourceIP")
                sourceMask = parameters.get("sourceMask")
                destinationIP = parameters.get("destinationIP")
                destinationMask = parameters.get("destinationMask")
                TOS = parameters.get("TOS")
                sourcePort = parameters.get("sourcePort")
                destPort = parameters.get("destPort")
                checkVersion = parameters.get("checkVersion")
                action = parameters.get("action")
                classifierNodeName = "comb"
                # 创建IPV4&TCP混合节点
                classifierNode = self.create_IPV4_and_TCP_or_UDP(holowan_ip, holowan_port, engineID, 1, sourceIP, sourceMask,
                                                            destinationIP, destinationMask, TOS, sourcePort,
                                                            destPort, checkVersion, action)
            elif classifierType == self.IPV4ANDUDP:
                sourceIP = parameters.get("sourceIP")
                sourceMask = parameters.get("sourceMask")
                destinationIP = parameters.get("destinationIP")
                destinationMask = parameters.get("destinationMask")
                TOS = parameters.get("TOS")
                sourcePort = parameters.get("sourcePort")
                destPort = parameters.get("destPort")
                checkVersion = parameters.get("checkVersion")
                action = parameters.get("action")
                classifierNodeName = "comb"
                # 创建IPV4&UDP混合节点
                classifierNode = self.create_IPV4_and_TCP_or_UDP(holowan_ip, holowan_port, engineID, 2, sourceIP, sourceMask,
                                                            destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                            checkVersion, action)
            # 若创建节点错误，则返回错误
            if type(classifierNode) == RuntimeError:
                return str(classifierNode)
            if operation == self.ADD:
                if classifierNode is not None:  # 把classifier节点添加到父节点中
                    port_node.append(classifierNode)
            elif operation == self.REMOVE:
                remove_flags = False
                classifierNodes = xt.get_nodes(port_node, classifierNodeName)
                for node in classifierNodes:
                    if xt.classifier_equal(classifierNode, node):
                        port_node.remove(node)
                        remove_flags = True
                        break
                if remove_flags is False:
                    return r'{{"errCode":"-15",' \
                           r'"errMsg":"ConnectionError",' \
                           r'"errReason":"Engine{0} port{1} has not such {2}"}}'.\
                        format(engineID, portID, classifierNodeName)
        elif operation == self.REMOVEALL:
            # 遍历所有对应的classifier节点
            if classifierType == self.IPV4:
                for node in xt.get_nodes(port_node, "./ipv4"):
                    port_node.remove(node)
            elif classifierType == self.IPV6:
                for node in xt.get_nodes(port_node, "./ipv6"):
                    port_node.remove(node)
            elif classifierType == self.MAC:
                for node in xt.get_nodes(port_node, "./mac"):
                    port_node.remove(node)
            elif classifierType == self.TCP:
                for node in xt.get_nodes(port_node, "./tcp_udp"):
                    if xt.get_node(node, "./type").text == "1":
                        port_node.remove(node)
            elif classifierType == self.UDP:
                for node in xt.get_nodes(port_node, "./tcp_udp"):
                    if xt.get_node(node, "./type").text == "2":
                        port_node.remove(node)
            elif classifierType == self.IPV4ANDTCP:
                for node in xt.get_nodes(port_node, "./comb"):
                    if xt.get_node(node, "./tcp_udp/type").text == "1":
                        port_node.remove(node)
            elif classifierType == self.IPV4ANDUDP:
                for node in xt.get_nodes(port_node, "./comb"):
                    if xt.get_node(node, "./tcp_udp/type").text == "2":
                        port_node.remove(node)
        pathXMLStr = xt.xmlObject_to_string(root)
        return mt.post_original_api(
            "http://{0}:{1}/{2}".format(holowan_ip, holowan_port, self.emulator_config_api), pathXMLStr)

    '''============================================================================================================='''
    # 开启指定引擎
    @checkParameter()
    def start_engine(self, holowan_ip: str, holowan_port: str, engineID: int):
        requestURL = "http://{0}:{1}/start_running?engine={2}".format(holowan_ip, holowan_port, engineID)
        print(requestURL)
        return requests.get(requestURL).text

    # 关闭指定引擎
    @checkParameter()
    def stop_engine(self, holowan_ip: str, holowan_port: str, engineID: int):
        requestURL = "http://{0}:{1}/stop_running?engine={2}".format(holowan_ip, holowan_port, engineID)
        return requests.get(requestURL).text

    # 保存当前HoloWAN设备xml信息，用于开机后自动运行保存配置
    @checkParameter()
    def save_HoloWAN_information(self, holowan_ip: str, holowan_port: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :return: json 正确：errCode 等于 0，错误：errCode小于0（详见附录二（1.3修改虚拟链路配置错误编号））
        '''
        requestURL = "http://{0}:{1}/{2}".format(holowan_ip, holowan_port, self.emulator_config_api)
        HoloWAN_information_xml = self.get_HoloWAN_information(holowan_ip, holowan_port)
        return mt.post_original_api(requestURL, HoloWAN_information_xml)

    # 判断链路是否存在
    def exist_path(self, holowan_ip:str, holowan_port:str, engineID:int, pathID:int, pathName):
        HoloWAN_information_str = self.get_HoloWAN_information(holowan_ip, holowan_port)
        HoloWAN_information_tree = xt.xmlString_to_Object(HoloWAN_information_str)
        engine_nodes = xt.get_nodes(HoloWAN_information_tree, "./e")
        for engine_node in engine_nodes:
            if str(engineID) == xt.get_node(engine_node, "./ei").text:
                path_nodes = xt.get_nodes(engine_node, "./ep/p")
                for path in path_nodes:
                    if str(pathID) == xt.get_node(path, "./pi").text:
                        return True
        return False

    # 设置path：仅修改一个tag的text值
    def set_one_tag_text(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, tagPath: str, tagText):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param tagPath: 标签tag的路径
        :param tagText: 标签tag内容改为tagtext值
        :return: Json [正确：erroCode等于0， 错误：erroCode小于0（详见附录二（1.2修改虚拟链路损伤错误编号））]
        '''
        try:
            pathXMLStr = self.get_path_config_information(holowan_ip, holowan_port, engineID, pathID)
            if pathXMLStr == r'{{"errCode":"{}","errMsg":"ERROR","errReason":"ENGINE has no found"}}'.format(self.PCengineIDError) or \
                    pathXMLStr == r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH has no found"}}'.format(self.PCpathIDError) or \
                    pathXMLStr == r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH has no found"}}'.format(self.PCpathNotFound):
                return pathXMLStr
            root = xt.xmlString_to_Object(pathXMLStr)
            node = xt.get_node(root, tagPath)
            xt.set_node_text(node, tagText)
            pathXMLStr = xt.xmlObject_to_string(root)
            return mt.post_original_api("http://{0}:{1}/{2}".format(holowan_ip, holowan_port, self.emulator_config_api), pathXMLStr)
        except RuntimeError:
            return RuntimeError

    # 设置path：修改父节点下所有的子节点
    def set_tag_children(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection,
                         parent_node_ID,
                         children_node_Map, properties_map):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param pathDirection: 链路损伤方向 [1. 仅损伤下行，2. 仅损伤上行]
        :param parent_node_ID: 父节点tag
        :param children_node_Map: 子节点map
        :param properties_map: 子节点属性map
        :return:
        '''
        try:
            parent_node_path_list = []
            if pathDirection == 1:
                # parent_node_path = "pltr/" + parent_node_ID
                parent_node_path_list.append("pltr/" + parent_node_ID)
            elif pathDirection == 2:
                # parent_node_path = "prtl/" + parent_node_ID
                parent_node_path_list.append("prtl/" + parent_node_ID)
            elif pathDirection == 3:
                parent_node_path_list.append("pltr/" + parent_node_ID)
                parent_node_path_list.append("prtl/" + parent_node_ID)

            else:
                return r'{{"errCode":"{}","errMsg":"ERROR","errReason":"Error pathDirection"}}'.format(self.PCpathDirectionError)
            pathXMLStr = self.get_path_config_information(holowan_ip, holowan_port, engineID, pathID)
            if pathXMLStr == r'{{"errCode":"{}","errMsg":"ERROR","errReason":"ENGINE has no found"}}'.format(self.PCengineIDError) or \
                    pathXMLStr == r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH has no found"}}'.format(self.PCpathIDError) or \
                    pathXMLStr == r'{{"errCode":"{}","errMsg":"ERROR","errReason":"PATH has no found"}}'.format(self.PCpathNotFound):
                return pathXMLStr
            root = xt.xmlString_to_Object(pathXMLStr)
            for parent_node_path in parent_node_path_list:
                node = xt.get_node(root, parent_node_path)
                xt.remove_children(node)
                xt.add_children(node, children_node_Map)
                if len(properties_map) != 0:  # 添加properties属性
                    xt.add_properties(node, properties_map)
            pathXMLStr = xt.xmlObject_to_string(root)
            return mt.post_original_api(
                "http://{0}:{1}/{2}".format(holowan_ip, holowan_port, self.emulator_config_api),
                pathXMLStr)
        except RuntimeError:
            return RuntimeError

    ''' ===============================================统计数据接口===================================================='''
    # 获取虚拟链路path每秒完成统计数据
    @checkParameter()
    def get_path_current_data(self, holowan_ip:str, holowan_port:str, engineID:int, pathID: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :return: xml 详见附录一（1.5 PATH每秒统计数据 XML格式）
        '''
        requestURL = "http://{0}:{1}/current_resault_data?engine={2}&path={3}".format(holowan_ip, holowan_port,
                                                                                      engineID, pathID)
        return requests.get(requestURL).text

    # 获取指定引擎的虚拟链路每秒指定类型的统计数据
    @checkParameter()
    def get_path_graph_current(self, holowan_ip:str, holowan_port:str, engineID:int, pathID:int, id: int, type: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param id: 指定请求起始位置的ID编号，第一次该值设定为0
        :param type: String 详见附录三（1.1 返回数据类型列举）
        :return: xml 详见附录一（1.5 PATH每秒统计数据 XML格式）
        '''
        requestURL = "http://{0}:{1}/graph_current?engine={2}&path={3}&id={4}&type={5}".format(holowan_ip, holowan_port,
                                                                                      engineID, pathID, id, type)
        return requests.get(requestURL).text

    # # 获取所有引擎目前所有的历史数据点数量
    # def get_HoloWAN_history_data_count(self, holowan_ip, holowan_port):
    #     '''
    #     :param holowan_ip: holowan IP地址
    #     :param holowan_port: holowan 端口号
    #     :return: xml 详见附录一（1.7设备当前历史数据存在点XML格式）
    #     '''
    #     requestURL = "http://{0}:{1}/{2}".format(holowan_ip, holowan_port, self.history_data_count)
    #     print(requestURL)
    #     return requests.get(requestURL).text

    # 获取指定引擎的虚拟链路历史完全统计数据点组
    @checkParameter()
    def get_HoloWAN_history_entire_data(self, holowan_ip:str, holowan_port:str, engineID:int, pathID:int, last: int, count: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param last: 指定请求的起始位置，第一次默认从0开始
        :param count: 每次获取的数量，最多支持每次获取30个数据点
        :return:
        '''
        requestURL = "http://{0}:{1}/entire_resault_data?engine={2}&path={3}&last={4}&count={5}".format(holowan_ip, holowan_port, engineID, pathID, last, count)
        return requests.get(requestURL).text

    # 获取指定引擎的虚拟链路指定类型的历史统计数据点组
    @checkParameter()
    def get_path_graph_current_dataGroup(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, type: str, offset: int, count: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :param pathID: 链路ID
        :param type: String 详见附录三（1.1 返回数据类型列举）
        :param offsest: 指定请求的起始位置，第一次默认从0开始
        :param count: 每次获取的数量，最多支持每次获取30个数据点
        :return:
        '''
        requestURL = "http://{0}:{1}//graph_current?engine={2}&path={3}&type={4}&offset={5}&count={6}".format(holowan_ip, holowan_port, engineID, pathID, type, offset, count)
        return requests.get(requestURL).text

    # 清空指定引擎统计数据
    @checkParameter()
    def clean_engine_statistic_data(self, holowan_ip:str, holowan_port:str, engineID: int):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param engineID: 引擎ID
        :return: json  正确：errCode等于0， 错误：errCode小于0（详见附录二（1.5引擎数据清空错误编号））
        '''
        requestURL = "http://{0}:{1}/clean_engine_resault_data?engine={2}".format(holowan_ip, holowan_port, engineID)
        return requests.get(requestURL).text

    # 将指定引擎（Engine）虚拟链路（PATH）存在的统计数据导出为CSV文件
    @checkParameter()
    def create_csv(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, filePath: str):
        # 必须先关闭引擎，才能下载
        self.stop_engine(holowan_ip, holowan_port, engineID)
        requestURL1 = "http://{0}:{1}/csv_data?type=1&engine={2}&path={3}".format(holowan_ip, holowan_port, engineID, pathID)
        response = requests.get(requestURL1)
        if eval(response.text)["errCode"] == "0":
            requestURL2 = "http://{0}:{1}/csv_data?type=2&engine={2}&path={3}".format(holowan_ip, holowan_port, engineID, pathID)
            response2 = requests.get(requestURL2)
            with open(filePath, "w") as f:
                f.write(response2.text)
        return response.text

    # ===============================================设备控制口相关接口====================================================#
    # 获取设备控制口（Control Prot）网络状态
    @checkParameter()
    def get_network_information(self, holowan_ip: str, holowan_port: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :return: xml 详见附录一（1.8设备控制口状态XML格式）
        '''
        requestURL = "http://{0}:{1}/network_info".format(holowan_ip, holowan_port)
        return requests.get(requestURL).text

    # 设置设备控制口（Control Prot）网络状态
    @checkParameter()
    def set_network(self, holowan_ip: str, holowan_port: str, hostName: str, ipAddress: str,
                    ipNetmask: str, gateway: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param hostName: Hostname名称
        :param ipAddress: ip地址
        :param ipNetmask: ip地址掩码
        :param gateway: 网关
        :return: json 正确：errCode等于0， 错误：errCode小于0（详见附录二（1.7配置控制口错误编号））
        '''
        network_xmlStr = self.get_network_information(holowan_ip, holowan_port)
        tree = xt.xmlString_to_Object(network_xmlStr)
        node = xt.get_node(tree, "./network_settings")
        xt.get_node(node, "./hostname").text = hostName
        if mt.isIP(ipAddress): xt.get_node(node, "./ipaddr").text = ipAddress
        if mt.isIP(ipNetmask): xt.get_node(node, "./netmask").text = ipNetmask
        if mt.isIP(gateway): xt.get_node(node, "./gateway").text = gateway
        nodes = xt.get_nodes(tree, "./network_settings/")
        network_node = xt.create_node("holowan_admin_network_config_info", {}, "")
        for node in nodes:
            network_node.append(node)
        xt.get_node(network_node, "./dhcp_switch").text = "1"       # dhcp_switch必须设置为1才能发送，若为off则报错
        xmlStr = xt.xmlObject_to_string(network_node)
        url = "http://{0}:{1}/setting_network".format(holowan_ip, holowan_port)
        return mt.post_original_api(url, xmlStr)

    ''' ===============================================设备业务口相关接口===================================================='''
    @checkParameter()
    def get_worker_port_information(self, holowan_ip: str, holowan_port: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :return: xml 详见附录一（1.9设备业务口状态XML格式）
        '''
        requestURL = "http://{0}:{1}/worker_port_info".format(holowan_ip, holowan_port)
        return requests.get(requestURL).text

    # ===============================================设备日志相关接口====================================================#
    # 获取当前设备本次开机以来运行日志信息
    @checkParameter()
    def get_log(self, holowan_ip: str, holowan_port: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :return: 设备状态描述文本
        '''
        requestURL = "http://{0}:{1}/log".format(holowan_ip, holowan_port)
        return requests.get(requestURL).text


    # ===============================================Recorder相关接口====================================================#
    # 上传HoloWAN Recorder 录制文件或Apposite Recorder APP 录制文件
    # def upload_recorder(self, holowan_ip:str, holowan_port:str, filePath):
    #     pass


    # 获取上传Recorder文件信息
    # def get_upload_recorder_information(self, holowan_ip, holowan_port):
    #     '''
    #     :param holowan_ip: holowan IP地址
    #     :param holowan_port: holowan 端口号
    #     :return: xml 详见附录一（1.10Recorder文件概述XML格式）
    #     '''
    #     requestURL = "http://{0}:{1}/recorder_info".format(holowan_ip, holowan_port)
    #     return requests.get(requestURL).text


    # 获取最有一次Recorder配置参数
    # def get_recorder_config_information(cself, holowan_ip, holowan_port):
    #     '''
    #     :param holowan_ip: holowan IP地址
    #     :param holowan_port: holowan 端口号
    #     :return: xml 详见附录一（1.11Recorder文件概述XML格式）
    #     '''
    #     requestURL = "http://{0}:{1}/recorder.xml".format(holowan_ip, holowan_port)
    #     return requests.get(requestURL).text

    # ===============================================设备管理相关接口====================================================#
    # 重启设备接口
    @checkParameter()
    def reboot(self, holowan_ip: str, holowan_port: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        '''
        requestURL = "http://{0}:{1}/reboot".format(holowan_ip, holowan_port)
        requests.get(requestURL)

    # ===============================================偏好设置相关接口====================================================#
    # 获取偏好设置
    @checkParameter()
    def get_preferences(self, holowan_ip: str, holowan_port: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :return: xml 详见附录一（1.10偏好设置XML格式）
        '''
        requestURL = "http://{0}:{1}/get_preferences".format(holowan_ip, holowan_port)
        return requests.get(requestURL).text


    # 设置偏好
    @checkParameter()
    def set_preferences(self, holowan_ip:str, holowan_port:str, clean_buffer: str, zero_line: str):
        '''
        :param holowan_ip: holowan IP地址
        :param holowan_port: holowan 端口号
        :param clean_buffer: 下发Path配置时，是否清空buffer，True：是；False：否
        :param zero_line: 报文时延起点，取值：receive_time或bandwitdh_time
        :return: xml 详见附录二（1.8下发偏好设置错误编号）
        '''

        if clean_buffer not in ["true", "false"]:
            return r'{"errCode":"-500","errMsg":"ERROR","errReason":"Error parameter values(clean_buffer)"}'

        parent_node = xt.create_node("holowan_admin_preferences", {}, "")
        parent_node.append(xt.create_node("clean_buffer", {}, clean_buffer))
        parent_node.append(xt.create_node("zero_line", {}, zero_line))
        xmlStr = xt.xmlObject_to_string(parent_node)
        url = "http://{0}:{1}/set_preferences".format(holowan_ip, holowan_port)
        return mt.post_original_api(url, xmlStr)

    '''===============================================新增功能===================================================='''
    # 获取PATH链路Name
    @checkParameter()
    def get_path_Name(self, holowan_ip:str, holowan_port:str, engineID:int, pathID: int) -> str:
        xmlData = self.get_path_config_information(holowan_ip, holowan_port, engineID, pathID)
        return xt.get_node(xt.xmlString_to_Object(xmlData), "./pn").text

    # 获取当前设备支持的引擎数
    def get_engine_count(self, holowan_ip: str, holowan_port: str) -> int:
        response = self.get_HoloWAN_information(holowan_ip=holowan_ip, holowan_port=holowan_port)
        return int(xt.get_node(xt.xmlString_to_Object(response), "./eeq").text)

    # 判断引擎是否存在
    def has_engine(self, holowan_ip: str, holowan_port: str, engineID: int):
        if engineID > 0 and engineID <= self.get_engine_count(holowan_ip, holowan_port):
            return True
        else:
            return False

    # 判断链路ID是否正确
    def right_path(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int):
        if pathID > 0 and pathID <= 15:
            return True
        return False

    # 判断链路是否存在
    def has_path(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int):
        if pathID not in self.get_pathDict_from_engine(holowan_ip, holowan_port, engineID).keys():
            return False
        return True

    # 判断链路开启状态
    def path_is_open(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int):
        responseInString = self.get_HoloWAN_information(holowan_ip, holowan_port)
        responseInXml = xt.xmlString_to_Object(responseInString)
        for engineNode in xt.get_nodes(responseInXml, "./e"):
            if xt.get_node(engineNode, "./ei").text == str(engineID):
                for pathNode in xt.get_nodes(engineNode, "./ep/p"):
                    if xt.get_node(pathNode, "./pi").text == str(pathID):
                        isOpen = xt.get_node(pathNode, "./ie").text
                        if isOpen == "1":
                            return False
                        elif isOpen == "2":
                            return True
        return False

        # print(xt.xmlObject_to_string(a))
        # b = xt.get_nodes(a, "./ep/p")
        # print(b)

        # for engineNode in xt.get_nodes(responseInXml, "./e"):
        #     if xt.get_node(engineNode, "./ei").text == str(engineID):
        #         for pathNode in xt.get_nodes(engineNode, "./ep/p"):
        #             if xt.get_node(pathNode, "./pi").text == pathID:
        #                 isOpen = xt.get_node(pathNode, "./ie").text
        #                 if isOpen == 1:
        #                     return False
        #                 elif isOpen == 2:
        #                     return True
        # return False

    # 获取指定引擎Engine上所有的链路ID和Name，返回字典{pathID: pathName}
    @checkParameter()
    def get_pathDict_from_engine(self, holowan_ip: str, holowan_port: str, engineID: int) -> dict:
        path_dic = {}
        holowanInformationXmlStr = self.get_HoloWAN_information(holowan_ip, holowan_port)
        engineNodes = xt.get_nodes(xt.xmlString_to_Object(holowanInformationXmlStr), "./e")
        for engineNode in engineNodes:
            each_engineID = xt.get_node(engineNode, "./ei").text
            if int(each_engineID) == engineID:
                pathNodes = xt.get_nodes(engineNode, "./ep/p")
                for pathNode in pathNodes:
                    pathID = int(xt.get_node(pathNode, "./pi").text)
                    pathName = xt.get_node(pathNode, "./pn").text
                    path_dic[pathID] = pathName
        return path_dic

    # 获取指定引擎Engine上所有的链路ID，返回列表list
    def get_pathIDList_from_engine(self, holowan_ip: str, holowan_port: str, engineID: int) -> list:
        pathDict = self.get_pathDict_from_engine(holowan_ip, holowan_port, engineID)
        return list(pathDict.keys())

    # 重置链路PATH
    @checkParameter()
    def resetPath(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int):
        pathName = self.get_path_Name(holowan_ip, holowan_port, engineID, pathID)
        return self.init_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    # 重置过滤器
    @checkParameter()
    def resetClassifier(self, holowan_ip:str, holowan_port:str, engineID:int, portID: int):
        remove_all_IPV4_from_Classifier_return = self.remove_all_IPV4_from_Classifier(holowan_ip, holowan_port, engineID, portID)
        if json.loads(remove_all_IPV4_from_Classifier_return)["errCode"] != "0":
            return remove_all_IPV4_from_Classifier_return
        remove_all_IPV6_from_Classifier_return = self.remove_all_IPV6_from_Classifier(holowan_ip, holowan_port, engineID, portID)
        if json.loads(remove_all_IPV6_from_Classifier_return)["errCode"] != "0":
            return remove_all_IPV6_from_Classifier_return
        remove_all_MAC_from_Classifier_return = self.remove_all_MAC_from_Classifier(holowan_ip, holowan_port, engineID, portID)
        if json.loads(remove_all_MAC_from_Classifier_return)["errCode"] != "0":
            return remove_all_MAC_from_Classifier_return
        add_MAC_to_Classifier_return = self.add_MAC_to_Classifier(holowan_ip, holowan_port, engineID, portID, "any", "any", "any", 1)
        if json.loads(add_MAC_to_Classifier_return)["errCode"] != "0":
            return add_MAC_to_Classifier_return
        return r'{"errCode":"0","errMsg":"OK","errReason":"API Successful implementation"}'

    # 重置引擎 (port1、port2各自仅剩一个MAC Classifier，链路仅剩PATH 1，ID=1，开启状态)
    @checkParameter()
    def resetEngine(self, holowan_ip: str, holowan_port: str, engineID: int):
        paths_dic = self.get_pathDict_from_engine(holowan_ip, holowan_port, engineID)
        # 重置链路ATH
        for pathId in paths_dic.keys():
            pathName = paths_dic[pathId]
            remove_path_return = self.remove_path(holowan_ip, holowan_port, engineID, pathId, pathName, True)
            if json.loads(remove_path_return)["errCode"] != "0":
                return remove_path_return
        add_path_return = self.add_path(holowan_ip, holowan_port, engineID, 1)
        if json.loads(add_path_return)["errCode"] != "0":
            return add_path_return
        open_path_return = self.open_path(holowan_ip, holowan_port, engineID, 1, "PATH 1")
        if json.loads(add_path_return)["errCode"] != "0":
            return open_path_return
        # 重置过滤器
        resetClassifier_return1 = self.resetClassifier(holowan_ip=holowan_ip, holowan_port=holowan_port, engineID=engineID, portID=2*(engineID-1)+1)
        if json.loads(resetClassifier_return1)["errCode"] != "0":
            return resetClassifier_return1
        resetClassifier_return2 = self.resetClassifier(holowan_ip=holowan_ip, holowan_port=holowan_port, engineID=engineID, portID=2*(engineID-1)+2)
        if json.loads(resetClassifier_return1)["errCode"] != "0":
            return resetClassifier_return2
        return r'{"errCode":"0","errMsg":"OK","errReason":"API Successful implementation"}'

class SubHoloWAN(HoloWAN):

    def __init__(self, holowan_ip, holowan_port):
        super().__init__()
        self.holowan_ip = holowan_ip
        self.holowan_port = holowan_port

    # 设置默认值
    def setDefaultParameter(self, holowan_ip: str, holowan_port: str):
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

    def hold_engine(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                    password: int = 1234, new_password: int = 1234):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().hold_engine(holowan_ip, holowan_port, engineID, password, new_password)

    def get_HoloWAN_information(self, holowan_ip: str = "default", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_HoloWAN_information(holowan_ip, holowan_port)

    def add_path(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                 pathID: int = 1,
                 pathName: str = "PATH"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    def init_path(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                  pathID: int = 1, pathName: str = "PATH"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().init_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    def remove_path(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                    pathID: int = 1, pathName: str = "PATH", force: bool = False):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_path(holowan_ip, holowan_port, engineID, pathID, pathName, force)

    def open_path(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                  pathID: int = 1, pathName: str = "PATH"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().open_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    def close_path(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                   pathID: int = 1, pathName: str = "PATH"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().close_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    def set_path_direction(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                           pathID: int = 1, pathDirection: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_path_direction(holowan_ip, holowan_port, engineID, pathID, pathDirection)

    def set_path_Bandwidth_Fixed(self, holowan_ip: str = "default", holowan_port: str = "default",
                                 engineID: int = 1, pathID: int = 1,
                                 pathDirection: int = 1, rateValue: int = 1000, rateUnit: int = 2):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_path_Bandwidth_Fixed(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                rateValue,
                                                rateUnit)

    def close_Background_Utilization(self, holowan_ip: str = "default", holowan_port: str = "default",
                                     engineID: int = 1, pathID: int = 1,
                                     pathDirection: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().close_Background_Utilization(holowan_ip, holowan_port, engineID, pathID, pathDirection)

    def set_Background_Utilization(self, holowan_ip: str = "default", holowan_port: str = "default",
                                   engineID: int = 1, pathID: int = 1,
                                   pathDirection: int = 1, rate: int = 50, burst: int = 64):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Background_Utilization(holowan_ip, holowan_port, engineID, pathID, pathDirection, rate,
                                                  burst)

    def set_Queue_Limit_Drop_Tail(self, holowan_ip: str = "default", holowan_port: str = "default",
                                  engineID: int = 1, pathID: int = 1,
                                  pathDirection: int = 1, queueDepthValue: int = 50, queueDepthType: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Queue_Limit_Drop_Tail(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                 queueDepthValue, queueDepthType)

    def close_message_Modify(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                             pathID: int = 1, pathDirection: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().close_message_Modify(holowan_ip, holowan_port, engineID, pathID, pathDirection)

    def set_message_Modify_Normal(self, holowan_ip: str = "default", holowan_port: str = "default",
                                  engineID: int = 1, pathID: int = 1,
                                  pathDirection: int = 1, matchType: int = 1, matchOffset: int = 0,
                                  matchSize: int = 1, matchValue: str = "FF",
                                  modifyType: int = 1, modifyOffset: int = 0, modifySize: int = 1,
                                  modifyValue: str = "FF"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_message_Modify_Normal(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                 matchType,
                                                 matchOffset, matchSize, matchValue, modifyType, modifyOffset,
                                                 modifySize, modifyValue)

    def set_message_Modify_Cycle(self, holowan_ip: str = "default", holowan_port: str = "default",
                                 engineID: int = 1, pathID: int = 1,
                                 pathDirection: int = 1, matchType: int = 1, matchOffset: int = 0,
                                 matchSize: int = 1, matchValue: str = "FF",
                                 modifyType: int = 1, modifyOffset: int = 0, modifySize: int = 1,
                                 modifyValue: str = "FF",
                                 modifyCyclePeriod: int = 1000, modifyCycleBurst: int = 10):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_message_Modify_Cycle(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                matchType,
                                                matchOffset, matchSize, matchValue, modifyType, modifyOffset,
                                                modifySize, modifyValue, modifyCyclePeriod, modifyCycleBurst)

    def set_message_Modify_Random(self, holowan_ip: str = "default", holowan_port: str = "default",
                                  engineID: int = 1, pathID: int = 1,
                                  pathDirection: int = 1, matchType: int = 1, matchOffset: int = 0,
                                  matchSize: int = 1, matchValue: str = "FF",
                                  modifyType: int = 1, modifyOffset: int = 0, modifySize: int = 1,
                                  modifyValue: str = "FF",
                                  modifyRandomRate: float = 1.1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_message_Modify_Random(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                 matchType,
                                                 matchOffset, matchSize, matchValue, modifyType, modifyOffset,
                                                 modifySize, modifyValue, modifyRandomRate)

    def close_MTU_Limit(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                        pathID: int = 1, pathDirection: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().close_MTU_Limit(holowan_ip, holowan_port, engineID, pathID, pathDirection)

    def set_MTU_Limit(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                      pathID: int = 1, pathDirection: int = 1,
                      limitValue: int = 1500):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_MTU_Limit(holowan_ip, holowan_port, engineID, pathID, pathDirection, limitValue)

    def set_Frame_Overhead(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                           pathID: int = 1, pathDirection: int = 1,
                           type: int = 3, rate: int = 24):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Frame_Overhead(holowan_ip, holowan_port, engineID, pathID, pathDirection, type, rate)

    def set_Delay_Constant(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                           pathID: int = 1, pathDirection: int = 1,
                           delay: float = 2):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Delay_Constant(holowan_ip, holowan_port, engineID, pathID, pathDirection, delay)

    def set_Delay_Uniform(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                          pathID: int = 1, pathDirection: int = 1,
                          minimum: float = 0.0, maximum: float = 50.0, enableReordering: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Delay_Uniform(holowan_ip, holowan_port, engineID, pathID, pathDirection, minimum,
                                         maximum,
                                         enableReordering)

    def set_Delay_Normal(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                         pathID: int = 1, pathDirection: int = 1,
                         min: float = 1.0, mean: float = 50.0, stdDeviation: float = 10.0,
                         enableReordering: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Delay_Normal(holowan_ip, holowan_port, engineID, pathID, pathDirection, min, mean,
                                        stdDeviation, enableReordering)

    def set_Delay_Normal_AdvancedSetup(self, holowan_ip: str = "default", holowan_port: str = "default",
                                       engineID: int = 1, pathID: int = 1,
                                       pathDirection: int = 1, min: float = 1.0, mean: float = 50.0,
                                       stdDeviation: float = 10.0,
                                       enableReordering: int = 1, advancedPeriod: float = 60000,
                                       advancedDuration: float = 1000,
                                       advancedMin: float = 900, advancedMax: float = 1000):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Delay_Normal_AdvancedSetup(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                                      min,
                                                      mean, stdDeviation, enableReordering, advancedPeriod,
                                                      advancedDuration, advancedMin, advancedMax)

    def set_Delay_Custom(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                         pathID: int = 1, pathDirection: int = 1,
                         meanDelay: float = 200.0, minDelay: float = 1.0, maxDelay: float = 1000.0,
                         positiveDelta: float = 99.9, negativeDelta: float = 99.9,
                         spread: float = 1.58, enableReordering: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Delay_Custom(holowan_ip, holowan_port, engineID, pathID, pathDirection, meanDelay,
                                        minDelay,
                                        maxDelay, positiveDelta, negativeDelta, spread, enableReordering)

    def set_Loss_Random(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                        pathID: int = 1, pathDirection: int = 1,
                        rate: float = 5.000):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Loss_Random(holowan_ip, holowan_port, engineID, pathID, pathDirection, rate)

    def set_Loss_Cycle(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                       pathID: int = 1, pathDirection: int = 1,
                       period: int = 1000, burst: int = 10):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Loss_Cycle(holowan_ip, holowan_port, engineID, pathID, pathDirection, period, burst)

    def set_Loss_Burst(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                       pathID: int = 1, pathDirection: int = 1,
                       probability: float = 50.00, minimum: int = 0, maximum: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Loss_Burst(holowan_ip, holowan_port, engineID, pathID, pathDirection, probability,
                                      minimum,
                                      maximum)

    def set_Loss_Dual(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                      pathID: int = 1, pathDirection: int = 1,
                      goodStateLoss: float = 1.0, goodToBadProbability: float = 50.0, badStateLoss: float = 1.0,
                      badToGoodProbability: float = 50.0):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Loss_Dual(holowan_ip, holowan_port, engineID, pathID, pathDirection, goodStateLoss,
                                     goodToBadProbability, badStateLoss, badToGoodProbability)

    def set_BER(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                pathID: int = 1, pathDirection: int = 1,
                bitErrorValue: int = 1, bitErrorIndex: int = -14):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_BER(holowan_ip, holowan_port, engineID, pathID, pathDirection, bitErrorValue,
                               bitErrorIndex)

    def set_Reordering_Normal(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                              pathID: int = 1, pathDirection: int = 1,
                              probability: float = 0.0, delayMin: float = 0.1, delayMax: float = 0.5):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Reordering_Normal(holowan_ip, holowan_port, engineID, pathID, pathDirection, probability,
                                             delayMin, delayMax)

    def set_Duplication_Normal(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                               pathID: int = 1, pathDirection: int = 1,
                               probability: float = 20.0):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_Duplication_Normal(holowan_ip, holowan_port, engineID, pathID, pathDirection,
                                              probability)

    def get_path_config_information(self, holowan_ip: str = "default", holowan_port: str = "default",
                                    engineID: int = 1, pathID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_path_config_information(holowan_ip, holowan_port, engineID, pathID)

    def add_IPV4_to_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                               portID: int = 1, sourceIP: str = "any",
                               sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32,
                               TOS: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_IPV4_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, sourceMask,
                                              destinationIP, destinationMask, TOS, action)

    def remove_IPV4_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                    engineID: int = 1, portID: int = 1, sourceIP: str = "any",
                                    sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32,
                                    TOS: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_IPV4_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, sourceMask,
                                                   destinationIP, destinationMask, TOS, action)

    def remove_all_IPV4_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                        engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_IPV4_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def add_IPV6_to_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                               portID: int = 1, sourceIP: str = "any",
                               destinationIP: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_IPV6_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, destinationIP,
                                              action)

    def remove_IPV6_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                    engineID: int = 1, portID: int = 1, sourceIP: str = "any",
                                    destinationIP: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_IPV6_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP,
                                                   destinationIP,
                                                   action)

    def remove_all_IPV6_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                        engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_IPV6_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def add_MAC_to_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                              portID: int = 1, sourceMAC: str = "any",
                              destinationMAC: str = "any", EtherType: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_MAC_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourceMAC, destinationMAC,
                                             EtherType, action)

    def remove_MAC_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                   engineID: int = 1, portID: int = 1, sourceMAC: str = "any",
                                   destinationMAC: str = "any", EtherType: str = "any", action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_MAC_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourceMAC,
                                                  destinationMAC,
                                                  EtherType, action)

    def remove_all_MAC_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                       engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_MAC_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def add_TCP_to_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                              portID: int = 1, sourcePort: str = "any",
                              destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_TCP_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourcePort, destPort,
                                             checkVersion, action)

    def remove_TCP_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                   engineID: int = 1, portID: int = 1,
                                   sourcePort: str = "any", destPort: str = "any", checkVersion: int = 0,
                                   action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_TCP_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourcePort, destPort,
                                                  checkVersion, action)

    def remove_all_TCP_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                       engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_TCP_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def add_UDP_to_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                              portID: int = 1, sourcePort: str = "any",
                              destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_UDP_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourcePort, destPort,
                                             checkVersion, action)

    def remove_UDP_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                   engineID: int = 1, portID: int = 1,
                                   sourcePort: str = "any", destPort: str = "any", checkVersion: int = 0,
                                   action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_UDP_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourcePort, destPort,
                                                  checkVersion, action)

    def remove_all_UDP_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                       engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_UDP_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def create_TCP_or_UDP(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                          TCPUDP: int = 1, sourcePort: str = "any",
                          destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().create_TCP_or_UDP(holowan_ip, holowan_port, engineID, TCPUDP, sourcePort, destPort,
                                         checkVersion,
                                         action)

    def add_IPV4_TCP_to_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                   engineID: int = 1, portID: int = 1, sourceIP: str = "any",
                                   sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32,
                                   TOS: str = "any", sourcePort: str = "any",
                                   destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_IPV4_TCP_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, sourceMask,
                                                  destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                  checkVersion, action)

    def remove_IPV4_TCP_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                        engineID: int = 1, portID: int = 1,
                                        sourceIP: str = "any", sourceMask: int = 32, destinationIP: str = "any",
                                        destinationMask: int = 32,
                                        TOS: str = "any", sourcePort: str = "any", destPort: str = "any",
                                        checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_IPV4_TCP_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP,
                                                       sourceMask,
                                                       destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                       checkVersion, action)

    def remove_all_IPV4_TCP_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                            engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_IPV4_TCP_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def add_IPV4_UDP_to_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                   engineID: int = 1, portID: int = 1, sourceIP: str = "any",
                                   sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32,
                                   TOS: str = "any", sourcePort: str = "any",
                                   destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().add_IPV4_UDP_to_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP, sourceMask,
                                                  destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                  checkVersion, action)

    def remove_IPV4_UDP_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                        engineID: int = 1, portID: int = 1,
                                        sourceIP: str = "any", sourceMask: int = 32, destinationIP: str = "any",
                                        destinationMask: int = 32,
                                        TOS: str = "any", sourcePort: str = "any", destPort: str = "any",
                                        checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_IPV4_UDP_from_Classifier(holowan_ip, holowan_port, engineID, portID, sourceIP,
                                                       sourceMask,
                                                       destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                       checkVersion, action)

    def remove_all_IPV4_UDP_from_Classifier(self, holowan_ip: str = "default", holowan_port: str = "default",
                                            engineID: int = 1, portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_all_IPV4_UDP_from_Classifier(holowan_ip, holowan_port, engineID, portID)

    def create_IPV4_and_TCP_or_UDP(self, holowan_ip: str = "default", holowan_port: str = "default",
                                   engineID: int = 1, TCPUDP: int = 1, sourceIP: str = "any",
                                   sourceMask: int = 32, destinationIP: str = "any", destinationMask: int = 32,
                                   TOS: str = "any", sourcePort: str = "any",
                                   destPort: str = "any", checkVersion: int = 0, action: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().create_IPV4_and_TCP_or_UDP(holowan_ip, holowan_port, engineID, TCPUDP, sourceIP, sourceMask,
                                                  destinationIP, destinationMask, TOS, sourcePort, destPort,
                                                  checkVersion, action)

    def get_Packet_Classifier_config_information(self, holowan_ip: str = "default", holowan_port: str = "default",
                                                 engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_Packet_Classifier_config_information(holowan_ip, holowan_port, engineID)

    def start_engine(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().start_engine(holowan_ip, holowan_port, engineID)

    def stop_engine(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().stop_engine(holowan_ip, holowan_port, engineID)

    def save_HoloWAN_information(self, holowan_ip: str = "default", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().save_HoloWAN_information(holowan_ip, holowan_port)

    def remove_or_open_or_close_path(self, holowan_ip: str = "default", holowan_port: str = "default",
                                     engineID: int = 1, pathID: int = 1, pathName: str = "PATH",
                                     children_node_Map=None):
        if children_node_Map is None:
            children_node_Map = {}
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().remove_or_open_or_close_path(holowan_ip, holowan_port, engineID, pathID, pathName,
                                                    children_node_Map)

    def get_path_current_data(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                              pathID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_path_current_data(holowan_ip, holowan_port, engineID, pathID)

    def get_path_graph_current(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                               pathID: int = 1, id: int = "rx_bytes",
                               type: str = "rx_bytes"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_path_graph_current(holowan_ip, holowan_port, engineID, pathID, id, type)

    def get_HoloWAN_history_entire_data(self, holowan_ip: str = "default", holowan_port: str = "default",
                                        engineID: int = 1, pathID: int = 1, last: int = 0,
                                        count: int = 30):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_HoloWAN_history_entire_data(holowan_ip, holowan_port, engineID, pathID, last, count)

    def get_path_graph_current_dataGroup(self, holowan_ip: str = "default", holowan_port: str = "default",
                                         engineID: int = 1, pathID: int = 1,
                                         type: str = "rx_bytes", offset: int = 10, count: int = 30):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_path_graph_current_dataGroup(holowan_ip, holowan_port, engineID, pathID, type, offset,
                                                        count)

    def clean_engine_statistic_data(self, holowan_ip: str = "default", holowan_port: str = "default",
                                    engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().clean_engine_statistic_data(holowan_ip, holowan_port, engineID)

    def create_csv(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                   pathID: int = 1, filePath: str = ""):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().create_csv(holowan_ip, holowan_port, engineID, pathID, filePath)

    def get_network_information(self, holowan_ip: str = "default", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_network_information(holowan_ip, holowan_port)

    def set_network(self, holowan_ip: str = "default", holowan_port: str = "default", hostName: str = "MyHoloWAN",
                    ipAddress: str = "192.168.1.199", ipNetmask: str = "255.255.255.255",
                    gateway: str = "192.168.1.1"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_network(holowan_ip, holowan_port, hostName, ipAddress, ipNetmask, gateway)

    def get_worker_port_information(self, holowan_ip: str = "default", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_worker_port_information(holowan_ip, holowan_port)

    def get_log(self, holowan_ip: str = "default", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_log(holowan_ip, holowan_port)

    def reboot(self, holowan_ip: str = "default", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().reboot(holowan_ip, holowan_port)

    def get_preferences(self, holowan_ip: str = "default", holowan_port: str = "default"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_preferences(holowan_ip, holowan_port)

    def set_preferences(self, holowan_ip: str = "default", holowan_port: str = "default",
                        clean_buffer: str = "true", zero_line: str = "receive_time"):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().set_preferences(holowan_ip, holowan_port, clean_buffer, zero_line)

    def get_path_Name(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                      pathID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_path_Name(holowan_ip, holowan_port, engineID, pathID)

    def get_pathDict_from_engine(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().get_pathDict_from_engine(holowan_ip, holowan_port, engineID)

    def resetPath(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                  pathID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().resetPath(holowan_ip, holowan_port, engineID, pathID)

    def resetClassifier(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1,
                        portID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().resetClassifier(holowan_ip, holowan_port, engineID, portID)

    def resetEngine(self, holowan_ip: str = "default", holowan_port: str = "default", engineID: int = 1):
        holowan_ip, holowan_port = self.setDefaultParameter(holowan_ip, holowan_port)
        return super().resetEngine(holowan_ip, holowan_port, engineID)

    def create_IPV4(self, holowan_ip: str, holowan_port: str, engineID: int, sourceIP: str, sourceMask: int,
                    destinationIP: str, destinationMask: int, TOS: str, action: int):
        return super().create_IPV4(holowan_ip, holowan_port, engineID, sourceIP, sourceMask, destinationIP,
                                   destinationMask, TOS, action)

    def create_IPV6(self, holowan_ip: str, holowan_port: str, engineID: int, sourceIP: str, destinationIP: str,
                    action: int):
        return super().create_IPV6(holowan_ip, holowan_port, engineID, sourceIP, destinationIP, action)

    def create_MAC(self, holowan_ip: str, holowan_port: str, engineID: int, sourceMAC: str, destinationMAC: str,
                   EtherType: str, action: int):
        return super().create_MAC(holowan_ip, holowan_port, engineID, sourceMAC, destinationMAC, EtherType, action)

    def classifier(self, classifierType: int, operation: int, parameters: dict):
        return super().classifier(classifierType, operation, parameters)

    def exist_path(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathName):
        return super().exist_path(holowan_ip, holowan_port, engineID, pathID, pathName)

    def set_one_tag_text(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, tagPath, tagText):
        return super().set_one_tag_text(holowan_ip, holowan_port, engineID, pathID, tagPath, tagText)

    def set_tag_children(self, holowan_ip: str, holowan_port: str, engineID: int, pathID: int, pathDirection,
                         parent_node_ID, children_node_Map, properties_map):
        return super().set_tag_children(holowan_ip, holowan_port, engineID, pathID, pathDirection, parent_node_ID,
                                        children_node_Map, properties_map)

if __name__ == '__main__':
    holowan_ip = "192.168.1.198"
    holowan_port = "8080"
    engineID = 1
    pathID = 1
    pathDirection = 1
    min = 1.0
    mean = 50.0
    stdDeviation = 10.0
    enableReordering = 1
    subholowan = SubHoloWAN(holowan_ip, holowan_port)
    subResponse = subholowan.set_Delay_Normal()
    print(subResponse)
