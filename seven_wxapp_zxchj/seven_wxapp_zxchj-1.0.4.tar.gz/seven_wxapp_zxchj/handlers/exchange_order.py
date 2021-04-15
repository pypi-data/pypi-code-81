# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2021-02-04 11:29:04
:LastEditTime: 2021-04-12 17:33:13
:LastEditors: HuangJingCan
:Description: 
"""
from seven_wxapp.handlers.base.client_base import *

from seven_wxapp_zxchj.models.enum import *
from seven_wxapp_zxchj.models.seven_model import PageInfo
from seven_wxapp_zxchj.models.db_models.exchange.exchange_order_model import *


class ExchangeOrderListHandler(ClientBaseHandler):
    """
    :description: 用户兑换实物订单列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param page_index:页索引
        :param page_size:页大小
        :param user_id：用户id
        :param order_status:订单状态（0待发货1已发货）
        :return list
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        page_index = int(self.get_request_param("page_index", 0))
        page_size = int(self.get_request_param("page_size", 20))
        user_id = int(self.get_request_param("user_id", 0))
        order_status = int(self.get_request_param("order_status", 0))

        exchange_order_model = ExchangeOrderModel(context=self)

        params = [act_id, user_id]
        conidtion = "act_id=%s and user_id=%s"
        if order_status == 0:
            conidtion += " and order_status in(0,2)"
        else:
            conidtion += " and order_status=1"

        #奖品订单显示字段
        exchange_order_list_dict, total = exchange_order_model.get_dict_page_list("*", page_index, page_size, conidtion, "", "create_date desc", params)
        if exchange_order_list_dict:
            for i in range(len(exchange_order_list_dict)):
                #物流公司名称转换
                exchange_order_list_dict[i]["express_company"] = self.get_express_company(exchange_order_list_dict[i]["express_company"])

        page_info = PageInfo(page_index, page_size, total, exchange_order_list_dict)

        return self.client_reponse_json_success(page_info)

    def get_express_company(self, express_company):
        """
        :param express_company：物流公司（拼音）
        :return list
        :last_editors: WangQiang
        """
        express_company_name = "未知"
        if express_company:
            for enum in LogisticsType:
                if enum.name == express_company:
                    express_company_name = enum.value
                    break
        return express_company_name