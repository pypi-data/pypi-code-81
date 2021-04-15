# -*- coding: utf-8 -*-
"""
@Author: WangQiang
@Date: 2021-01-06 18:17:35
:LastEditTime: 2021-04-12 17:58:03
:LastEditors: HuangJingCan
@Description: 
"""
from seven_wxapp.handlers.base.client_base import *

from seven_wxapp_zxchj.models.seven_model import PageInfo
from seven_wxapp_zxchj.models.db_models.machine.machine_info_model import *
from seven_wxapp_zxchj.models.db_models.machine.machine_prize_model import *


class MachineInfoListHandler(ClientBaseHandler):
    """
    :description: 机台列表
    """
    @client_filter_check_params()
    @client_filter_check_params("act_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param series_id：系列id
        :param page_index:页索引
        :param page_size:页大小
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        series_id = int(self.get_request_param("series_id", 0))
        page_index = int(self.get_request_param("page_index", 0))
        page_size = int(self.get_request_param("page_size", 20))

        machine_info_model = MachineInfoModel(context=self)

        conidtion = "act_id=%s and is_release=%s and is_del=0"
        params = [act_id, 1]
        if series_id > 0:
            conidtion += " AND series_id=%s"
            params.append(series_id)
        field = "id,machine_name,machine_long_name,skin_id,machine_price,series_id,specs_type,index_pic,machine_bg_pic,goods_detail,carousel_map_img,box_style_detail"

        machine_info_page_list, total = machine_info_model.get_dict_page_list(field, page_index, page_size, conidtion, order_by="sort_index desc", params=params)

        page_info = PageInfo(page_index, page_size, total, machine_info_page_list)

        return self.client_reponse_json_success(page_info)


class MachinePrizeListHandler(ClientBaseHandler):
    """
    :description: 机台奖品列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param series_id：系列id
        :param page_index:页索引
        :param page_size:页大小
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        machine_id = int(self.get_request_param("machine_id", 0))
        page_index = int(self.get_request_param("page_index", 0))
        page_size = int(self.get_request_param("page_size", 20))

        machine_prize_model = MachinePrizeModel(context=self)

        conidtion = "act_id=%s and is_release=%s and is_del=0"
        params = [act_id, 1]
        if machine_id > 0:
            conidtion += " AND machine_id=%s"
            params.append(machine_id)
        field = "id,machine_id,prize_name,prize_title,prize_pic,toy_cabinet_pic,goods_code,prize_type,prize_price,surplus,prize_tag"

        machine_prize_page_list, total = machine_prize_model.get_dict_page_list(field, page_index, page_size, conidtion, order_by="sort_index desc", params=params)

        page_info = PageInfo(page_index, page_size, total, machine_prize_page_list)

        return self.client_reponse_json_success(page_info)
