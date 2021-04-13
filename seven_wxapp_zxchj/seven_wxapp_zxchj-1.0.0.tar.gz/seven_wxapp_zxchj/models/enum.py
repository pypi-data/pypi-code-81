# -*- coding: utf-8 -*-
"""
@Author: WangQiang
@Date: 2021-01-11 12:00:36
:LastEditTime: 2021-04-12 10:57:16
:LastEditors: HuangJingCan
@Description: 
"""
from enum import Enum, unique


class TaskType(Enum):
    """
    docstring：任务类型
    """
    # [{"reward_value":0}]
    每日签到 = 1
    # {"satisfy_count":0,"reward_value":0}
    每日参与1次抽盒 = 2
    # {"satisfy_count":0,"reward_value":0}
    每日参与抽盒N次 = 3
    # {"satisfy_count":0,"reward_value":0}
    每日使用1张透视卡 = 4
    # {"satisfy_count":0,"reward_value":0}
    每日使用1张重抽卡 = 5
    # {"satisfy_count":0,"reward_value":0}
    每日使用1张提示卡 = 6
    # {"reward_value":0,"user_num":0,"day_limit_count":0}
    邀请 = 7
    # [{"satisfy_count":0,"reward_value":0}]
    每周参与抽盒N次 = 8
    # [{"satisfy_count":0,"reward_value":0}]
    每周使用N张提示卡 = 9
    # [{"satisfy_count":0,"reward_value":0}]
    每周使用N张透视卡 = 10
    # [{"satisfy_count":0,"reward_value":0}]
    每周使用N张重抽卡 = 11


class PropsCardType(Enum):
    """
    docstring：道具卡类型
    """
    透视卡 = 2
    提示卡 = 3
    重抽卡 = 4


class LogisticsType(Enum):
    """
    docstring:物流类型
    """
    yuantong = "圆通速递"
    yunda = "韵达快递"
    zhongtong = "中通快递"
    youzhengguonei = "邮政快递包裹"
    shunfeng = "顺丰速运"
    huitongkuaidi = "百世快递"
    shentong = "申通快递"
    jd = "京东物流"
    ems = "EMS"
    tiantian = "天天快递"
    youzhengbk = "邮政标准快递"
    debangwuliu = "德邦"
    debangkuaidi = "德邦快递"
    zhaijisong = "宅急送"
    zhongyouex = "众邮快递"
    youshuwuliu = "优速快递"
    baishiwuliu = "百世快运"
    yuantongkuaiyun = "圆通快运"
    yundakuaiyun = "韵达快运"
    annengwuliu = "安能快运"
    zhongtongkuaiyun = "中通快运"