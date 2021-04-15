# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-01-07 10:30:16
:LastEditTime: 2021-04-13 16:32:04
:LastEditors: HuangJingCan
@Description: 
"""
from seven_wxapp.handlers.base.client_base import *

from seven_wxapp_zxchj.models.db_models.act.act_info_model import *


class IndexHandler(BaseHandler):
    """
    :description: 默认页
    """
    def get_async(self):
        """
        :description: 默认页
        :param 
        :return 字符串
        :last_editors: HuangJingCan
        """
        self.write(config.get_value("run_port") + "_api")

    def head_async(self):
        """
        docstring: 默认页
        """
        self.write(config.get_value("run_port") + "_api")


class CoreBaseHandler(ClientBaseHandler):
    """
    :description: 业务基类
    """
    @client_filter_check_head()
    def get_async(self):
        """
        :param act_id：活动id
        :return: dict
        :last_editors: WangQiang
        """
        #活动信息
        act_info_model = ActInfoModel(context=self)
        act_dict = act_info_model.get_dict()
        base_info = {}
        base_info["is_open"] = 1
        base_info["close_word"] = "对不起，小程序已关闭"
        base_info["coin_name"] = config.get_value("coin_name")
        if act_dict:
            base_info["act_id"] = act_dict['id']
            base_info["is_open"] = act_dict['is_open']  #小程序是否开启
            base_info["close_word"] = act_dict['close_word']  #小程序关闭文案
            base_info["share_desc"] = act_dict['share_desc']  #分享内容
            base_info["back_pic"] = ""  #首页背景图
            if act_dict['skin_desc']:
                skin_desc = [j for j in self.json_loads(act_dict['skin_desc']) if j["is_select"] == 1]
                base_info["back_pic"] = skin_desc[0]["image"] if len(skin_desc) > 0 else ""
            base_info["menu_desc"] = act_dict['menu_desc']  #底部导航菜单
            base_info["freight_price"] = act_dict['freight_price']  #运费价格
            base_info["deliver_explain"] = act_dict['deliver_explain']  #发货说明
            base_info["is_num_free_shipping"] = act_dict['is_num_free_shipping']  #是否开启满件包邮
            base_info["free_shipping_count"] = act_dict['free_shipping_count']  #包邮件数
            base_info["is_amount_free_shipping"] = act_dict['is_amount_free_shipping']  #是否开启满金额包邮
            base_info["free_shipping_amount"] = act_dict['free_shipping_amount']  #包邮金额
            base_info["is_home_page_notice"] = act_dict['is_home_page_notice']  #是否开启首页中奖公告（0否1是）

        return self.client_reponse_json_success(base_info)


def client_filter_check_act_open():
    """
    :description: 小程序活动是否开启校验 仅限handler使用,
    :param must_params: 必须传递的参数集合
    :last_editors: WangQiang
    """
    def check_params(handler):
        def wrapper(self, **args):
            act_id = int(self.get_param("act_id", 0))
            if act_id == 0:
                return self.client_reponse_json_error("ParamError", "参数错误,缺少活动id参数")
            act_info_model = ActInfoModel(context=self)
            act_dict = act_info_model.get_dict_by_id(act_id)
            if not act_dict:
                return self.client_reponse_json_error("ParamError", "未找到活动信息")
            if not act_dict['is_open']:
                return self.client_reponse_json_error("ParamError", act_dict['close_word'] if act_dict['close_word'] else "对不起，小程序未开启")
            return handler(self, **args)

        return wrapper

    return check_params
