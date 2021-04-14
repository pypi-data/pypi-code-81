# -*- coding: utf-8 -*-
"""
@Author: WangQiang
@Date: 2021-01-06 10:35:09
:LastEditTime: 2021-04-12 17:44:41
:LastEditors: HuangJingCan
@Description: 
"""
from seven_wxapp.handlers.base.client_base import *

from seven_wxapp_zxchj.models.seven_model import PageInfo
from seven_wxapp_zxchj.models.db_models.ip.ip_series_model import *
from seven_wxapp_zxchj.models.db_models.carousel.carousel_map_model import *
from seven_wxapp_zxchj.models.db_models.home.home_page_config_model import *
from seven_wxapp_zxchj.models.db_models.machine.machine_info_model import *
from seven_wxapp_zxchj.models.db_models.copywriting.copywriting_config_model import *


class HomePageHandler(ClientBaseHandler):
    """
    :description: 首页处理
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id")
    def get_async(self):
        """
        :description: 首页处理
        :param act_id: 活动id
        :return dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        #轮播图列表
        carousel_map_list = CarouselMapListHandler.get_list(act_id)
        #table列表
        tab_list = HomePageConfigListHandler.get_list(act_id, 1)
        #推荐列表
        recommend_list = HomePageConfigListHandler.get_list(act_id, 2)
        #ip列表
        ip_series_list = IpSeriesListHandler.get_list(act_id, 0, 5)
        obj_data = {}
        obj_data["carousel_map_list"] = carousel_map_list
        obj_data["tab_list"] = tab_list
        obj_data["recommend_list"] = recommend_list
        obj_data["ip_series_list"] = ip_series_list.__dict__

        return self.client_reponse_json_success(obj_data)


class CarouselMapListHandler(ClientBaseHandler):
    """
    :description: 轮播图列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id")
    def get_async(self):
        """
        :description: 轮播图列表
        :param act_id: 活动id
        :return list
        :last_editors: HuangJingCan
        """
        act_id = int(self.get_request_param("act_id", 0))

        data_list = self.get_list(act_id)

        return self.client_reponse_json_success(data_list)

    @classmethod
    def get_list(self, act_id):
        """
        :param act_id: 活动id
        :return: dict
        :last_editors: WangQiang
        """
        carousel_map_model = CarouselMapModel(context=self)
        machine_info_model = MachineInfoModel(context=self)
        ip_series_model = IpSeriesModel(context=self)

        field = "title,ImgIcon,jump_type,app_id,jump_url,series_id,machine_id"
        carousel_map_dict_list = carousel_map_model.get_dict_list("act_id=%s and is_release=%s", order_by="sort_index", field=field, params=[act_id, 1])
        if len(carousel_map_dict_list) > 0:
            #机台列表
            machine_id_list = [str(carousel_map_dict["machine_id"]) for carousel_map_dict in carousel_map_dict_list]
            machine_ids = ",".join(machine_id_list)
            machine_info_dict_list = machine_info_model.get_dict_list(f"id in ({machine_ids})")
            if len(machine_info_dict_list) > 0:
                #系列id列表
                series_id_list = [str(machine_info_dict["series_id"]) for machine_info_dict in machine_info_dict_list]
                series_ids = ",".join(series_id_list)
                ip_series_dict_list = ip_series_model.get_dict_list(f"id in ({series_ids})")
                for carousel_map_dict in carousel_map_dict_list:
                    machine_info_dict = [machine_info_dict for machine_info_dict in machine_info_dict_list if machine_info_dict["id"] == carousel_map_dict["machine_id"]]
                    if len(machine_info_dict) > 0:
                        machine_info_dict = machine_info_dict[0]
                        carousel_map_dict["machine_info"] = machine_info_dict
                        #匹配系列信息
                        ip_series_dict = [ip_series_dict for ip_series_dict in ip_series_dict_list if ip_series_dict["id"] == machine_info_dict["series_id"]]
                        if len(ip_series_dict) > 0:
                            carousel_map_dict["series_name"] = ip_series_dict[0]["series_name"]
        return carousel_map_dict_list


class HomePageConfigListHandler(ClientBaseHandler):
    """
    :description: 首页配置
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,config_type")
    def get_async(self):
        """
        :description: 首页配置
        :param act_id: 活动id
        :param config_type: config_type
        :return list
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        config_type = int(self.get_request_param("config_type", 1))

        data_list = self.get_list(act_id, config_type)

        return self.client_reponse_json_success(data_list)

    @classmethod
    def get_list(self, act_id, config_type):
        """
        :description: 首页配置列表
        :param act_id：活动id
        :param config_type:配置类型:1页签2推荐
        :return: dict
        :last_editors: WangQiang
        """
        home_page_config_model = HomePageConfigModel(context=self)
        machine_info_model = MachineInfoModel(context=self)

        condition = "act_id=%s and is_release=%s and config_type=%s"
        params = [act_id, 1, config_type]
        machine_field = "id,machine_name,machine_long_name,skin_id,machine_price,series_id,specs_type,index_pic,goods_detail,carousel_map_img,box_style_detail"
        home_page_config_dict_list = home_page_config_model.get_dict_list(condition, order_by="sort_index", field="id,title,config_type,img,content", params=params)
        is_need_machine = True
        if config_type == 1:
            is_need_machine = False
        if is_need_machine == True and len(home_page_config_dict_list) > 0:
            for home_page_config in home_page_config_dict_list:
                home_page_config["machine_list"] = []
                if home_page_config["content"]:
                    content_list = ast.literal_eval(home_page_config["content"])
                    if len(content_list) > 0:
                        content_list = sorted(content_list, key=lambda x: x["sort_index"])
                        machine_info_id_list = [str(content_info["machine_id"]) for content_info in content_list]
                        if len(machine_info_id_list) > 0:
                            machine_info_ids = ",".join(machine_info_id_list)
                            machine_info_dict_list = machine_info_model.get_dict_list(f"id in ({machine_info_ids}) and is_release=1 and is_del=0", field=machine_field)
                            if len(machine_info_dict_list) > 0:
                                #机台排序
                                machine_sort_list = []
                                for machine_id in machine_info_id_list:
                                    current_machine_dict = [machine_info_dict for machine_info_dict in machine_info_dict_list if int(machine_info_dict["id"]) == int(machine_id)]
                                    if len(current_machine_dict) > 0:
                                        machine_sort_list.append(current_machine_dict[0])

                                home_page_config["machine_list"] = machine_sort_list
                                home_page_config["content"] = content_list

        return home_page_config_dict_list


class HomePageConfigDetailsHandler(ClientBaseHandler):
    """
    :description: 首页配置详情
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,home_page_config_id")
    def get_async(self):
        """
        :description: 首页配置详情
        :param act_id: 活动id
        :return {*}
        :last_editors: HuangJingCan
        """
        act_id = int(self.get_request_param("act_id", 0))
        home_page_config_id = int(self.get_request_param("home_page_config_id", 0))

        data_list = self.get_details(act_id, home_page_config_id)

        return self.client_reponse_json_success(data_list)

    @classmethod
    def get_details(self, act_id, home_page_config_id):
        """
        :description: 首页配置详情
        :param act_id：活动id
        :param home_page_config_id:首页配置id
        :return: dict
        :last_editors: WangQiang
        """
        home_page_config_model = HomePageConfigModel(context=self)
        machine_info_model = MachineInfoModel(context=self)

        machine_field = "id,machine_name,machine_long_name,skin_id,machine_price,series_id,specs_type,index_pic,goods_detail,carousel_map_img,box_style_detail"
        home_page_config_dict = home_page_config_model.get_dict_by_id(home_page_config_id, "id,title,config_type,img,content")
        if home_page_config_dict:
            home_page_config_dict["machine_list"] = []
            if home_page_config_dict["content"]:
                content_list = ast.literal_eval(home_page_config_dict["content"])
                if len(content_list) > 0:
                    content_list = sorted(content_list, key=lambda x: x["sort_index"])
                    machine_info_id_list = [str(content_info["machine_id"]) for content_info in content_list]
                    if len(machine_info_id_list) > 0:
                        machine_info_ids = ",".join(machine_info_id_list)
                        machine_info_dict_list = machine_info_model.get_dict_list(f"id in ({machine_info_ids}) and is_release=1 and is_del=0", field=machine_field)
                        if len(machine_info_dict_list) > 0:
                            #机台排序
                            machine_sort_list = []
                            for machine_id in machine_info_id_list:
                                current_machine_dict = [machine_info_dict for machine_info_dict in machine_info_dict_list if int(machine_info_dict["id"]) == int(machine_id)]
                                if len(current_machine_dict) > 0:
                                    machine_sort_list.append(current_machine_dict[0])

                            home_page_config_dict["machine_list"] = machine_sort_list
                            home_page_config_dict["content"] = content_list

        return home_page_config_dict


class IpSeriesListHandler(ClientBaseHandler):
    """
    :description: ip系列
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id")
    def get_async(self):
        """
        :description: ip系列
        :param act_id: 活动id
        :param page_index: page_index
        :param page_size: page_size
        :return list
        :last_editors: HuangJingCan
        """
        act_id = int(self.get_request_param("act_id", 0))
        page_index = int(self.get_request_param("page_index", 0))
        page_size = int(self.get_request_param("page_size", 20))

        data_list = self.get_list(act_id, page_index, page_size)

        return self.client_reponse_json_success(data_list)

    @classmethod
    def get_list(self, act_id, page_index, page_size):
        """
        :description: ip系列表
        :param act_id：活动id
        :param page_index:页索引
        :param page_size:页大小
        :return: dict
        :last_editors: WangQiang
        """
        ip_series_model = IpSeriesModel(context=self)

        ip_series_page_list, total = ip_series_model.get_dict_page_list("*", page_index, page_size, "act_id=%s and is_release=1 and is_del=0", order_by="sort_index", params=[act_id])
        page_info = PageInfo(page_index, page_size, total, ip_series_page_list)

        return page_info


class CopywritingConfigListHandler(ClientBaseHandler):
    """
    :description: 文案配置列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param copywriting_type：文案配置id
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        copywriting_type = int(self.get_request_param("copywriting_type", 0))

        condition = "act_id=%s"
        params = [act_id]
        if copywriting_type > 0:
            condition += " AND copywriting_type=%s"
            params.append(copywriting_type)

        copywriting_config_model = CopywritingConfigModel(context=self)
        copywriting_config_dict_list = copywriting_config_model.get_dict_list(condition, field="title,content,copywriting_type", params=params)

        return self.client_reponse_json_success(copywriting_config_dict_list)