# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2021-02-03 16:52:59
:LastEditTime: 2021-04-12 17:26:22
:LastEditors: HuangJingCan
:Description: 优惠券相关接口
"""
from seven_wxapp.handlers.base.client_base import *

from seven_wxapp_zxchj.models.seven_model import PageInfo
from seven_wxapp_zxchj.models.db_models.coupon.coupon_info_model import *
from seven_wxapp_zxchj.models.db_models.user.user_coupon_model import *
from seven_wxapp_zxchj.models.db_models.machine.machine_info_model import *
from seven_wxapp_zxchj.models.db_models.coupon.coupon_machine_model import *


class GetEnableCouponListHandler(ClientBaseHandler):
    """
    :description: 下单前可以选择优惠券列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,machine_id")
    def get_async(self):
        """
        :description: 下单前可以选择优惠券列表
        :param act_id:活动id
        :param user_id:用户id
        :return: 
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_request_param("act_id", 1))
        user_id = int(self.get_request_param("user_id", 0))
        machine_id = int(self.get_request_param("machine_id", 0))

        user_coupon_model = UserCouponModel(context=self)
        coupon_info_model = CouponInfoModel(context=self)
        machine_info_model = MachineInfoModel(context=self)
        coupon_machine_model = CouponMachineModel(context=self)

        new_dict_list = []
        if machine_id <= 0:
            return self.client_reponse_json_success(new_dict_list)
        machine_info = machine_info_model.get_entity_by_id(machine_id)
        if machine_info.is_release == 0 or machine_info.is_del == 1:
            return self.client_reponse_json_success(new_dict_list)

        now_date = self.get_now_datetime()
        user_coupon_dict_list = user_coupon_model.get_dict_list("act_id=%s and user_id=%s and coupon_status=0 and is_del=0", field="id,coupon_id", params=[act_id, user_id])
        if len(user_coupon_dict_list) > 0:
            coupon_id_list = [int(i["coupon_id"]) for i in user_coupon_dict_list]
            coupon_info_dict_list = coupon_info_model.get_dict_list(SevenHelper.get_condition_by_int_list("id", coupon_id_list))
            if len(coupon_info_dict_list) > 0:
                coupon_machine_dict_list = coupon_machine_model.get_dict_list("act_id=%s and machine_id=%s and " + SevenHelper.get_condition_by_int_list("coupon_id", coupon_id_list), params=[act_id, machine_id])
                user_coupon_dict_list = SevenHelper.merge_dict_list(user_coupon_dict_list, "coupon_id", coupon_info_dict_list, "id", "coupon_type,coupon_name,is_appoint_machine,discount_amount,use_amount,discount_value,effective_start_date,effective_end_date,rule_desc")
                if len(user_coupon_dict_list) > 0:
                    for user_coupon in user_coupon_dict_list:
                        if int(user_coupon["is_appoint_machine"]) == 1:
                            if len(coupon_machine_dict_list) > 0:
                                coupon_machine_dict = [i for i in coupon_machine_dict_list if i["coupon_id"] == user_coupon["coupon_id"]]
                                if len(coupon_machine_dict) <= 0:
                                    continue
                            else:
                                continue
                        if int(user_coupon["coupon_type"]) == 1:
                            if decimal.Decimal(machine_info.machine_price) <= decimal.Decimal(user_coupon["discount_amount"]):
                                continue
                        elif int(user_coupon["coupon_type"]) == 2:
                            if decimal.Decimal(machine_info.machine_price) < decimal.Decimal(user_coupon["use_amount"]):
                                continue
                            if decimal.Decimal(machine_info.machine_price) <= decimal.Decimal(user_coupon["discount_amount"]):
                                continue
                        if now_date < str(user_coupon["effective_start_date"]):
                            continue
                        if now_date > str(user_coupon["effective_end_date"]):
                            continue
                        user_coupon["discount_amount"] = int(user_coupon["discount_amount"])
                        user_coupon["use_amount"] = int(user_coupon["use_amount"])
                        user_coupon["discount_value"] = "%.1f" % user_coupon["discount_value"]
                        new_dict_list.append(user_coupon)

        return self.client_reponse_json_success(new_dict_list)


class GetUserCouponListHandler(ClientBaseHandler):
    """
    :description: 用户优惠券列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :description: 用户优惠券列表
        :param act_id:活动id
        :param user_id:用户id
        :param coupon_status:优惠劵状态（0未使用1已使用2已失效）
        :return: 
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_request_param("act_id", 1))
        user_id = int(self.get_request_param("user_id", 0))
        coupon_status = int(self.get_request_param("coupon_status", 0))
        page_size = int(self.get_request_param("page_size", 20))
        page_index = int(self.get_request_param("page_index", 0))

        user_coupon_model = UserCouponModel(context=self)
        coupon_info_model = CouponInfoModel(context=self)

        where = "a.act_id=%s and a.user_id=%s and a.coupon_id=b.id and b.is_del=0"
        order_by = "a.id desc"
        params = [act_id, user_id]
        limit = f"{str(int(page_index) * int(page_size))}, {str(page_size)}"
        now = self.get_now_datetime()
        if coupon_status == 0:
            where += f" and a.coupon_status=0 and '{now}'<b.effective_end_date"
        elif coupon_status == 2:
            where += f" and ((a.coupon_status=0 and '{now}'>b.effective_end_date) or a.coupon_status=2)"
        else:
            where += f" and a.coupon_status=1"

        db = MySQLHelper(config.get_value("db_wxapp"))
        sql = f"SELECT b.id,b.coupon_type,b.coupon_name,b.discount_amount,b.use_amount,b.discount_value,b.effective_start_date,b.effective_end_date,b.rule_desc FROM user_coupon_tb as a,coupon_info_tb as b where {where} order by {order_by} limit {limit};"
        user_coupon_dict_list = db.fetch_all_rows(sql, params)
        sql = f"SELECT COUNT(a.id) AS count FROM user_coupon_tb as a,coupon_info_tb as b where {where};"
        row = db.fetch_one_row(sql, params)
        row_count = 0
        if row and 'count' in row and int(row['count']) > 0:
            row_count = int(row["count"])
        if len(user_coupon_dict_list) > 0:
            for item in user_coupon_dict_list:
                item["discount_amount"] = int(item["discount_amount"])
                item["use_amount"] = int(item["use_amount"])
                item["discount_value"] = "%.1f" % item["discount_value"]

        page_info = PageInfo(page_index, page_size, row_count, user_coupon_dict_list)

        return self.client_reponse_json_success(page_info)


class GetCouponList(ClientBaseHandler):
    """
    :description: 获取优惠券列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :description: 获取优惠券列表
        :param act_id：活动id
        :param user_id：用户id
        :param page_size:页大小
        :param user_id：用户id
        :return: 返回字段coupon_status 0 去领取1已领取
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        page_index = int(self.get_request_param("page_index", 0))
        page_size = int(self.get_request_param("page_size", 20))

        coupon_info_model = CouponInfoModel(context=self)
        user_coupon_model = UserCouponModel(context=self)

        coupon_info_list_dict, total = coupon_info_model.get_dict_page_list("*", page_index, page_size, "act_id=%s and scene_type=1 and is_release=1 and is_del=0 and %s<=effective_end_date", order_by="id desc", params=[act_id, self.get_now_datetime()])
        if len(coupon_info_list_dict) > 0:
            coupon_id_list = [int(i["id"]) for i in coupon_info_list_dict]
            user_coupon_num_group = user_coupon_model.get_dict_list("user_id=%s and " + SevenHelper.get_condition_by_int_list("coupon_id", coupon_id_list), "user_id,coupon_id", field="COUNT(0) AS total,coupon_id", params=[user_id])
            for i in range(len(coupon_info_list_dict)):
                coupon_info_list_dict[i]["coupon_status"] = 0
                user_coupon_num = [int(user_coupon_num["total"]) for user_coupon_num in user_coupon_num_group if int(user_coupon_num["coupon_id"]) == int(coupon_info_list_dict[i]["id"])]
                if len(user_coupon_num) > 0:
                    if user_coupon_num[0] >= int(coupon_info_list_dict[i]["get_limit"]):
                        coupon_info_list_dict[i]["coupon_status"] = 1
                coupon_info_list_dict[i]["discount_amount"] = int(coupon_info_list_dict[i]["discount_amount"])
                coupon_info_list_dict[i]["use_amount"] = int(coupon_info_list_dict[i]["use_amount"])
                coupon_info_list_dict[i]["discount_value"] = "%.1f" % coupon_info_list_dict[i]["discount_value"]

        page_info = PageInfo(page_index, page_size, total, coupon_info_list_dict)

        return self.client_reponse_json_success(page_info)


class GetCouponInfo(ClientBaseHandler):
    """
    :description: 获取指定优惠券信息
    """
    @client_filter_check_head()
    @client_filter_check_params("coupon_id")
    def get_async(self):
        """
        :description: 获取指定优惠券信息
        :param coupon_id:优惠劵id
        :return: 
        :last_editors: HuangJianYi
        """
        coupon_id = int(self.get_request_param("coupon_id", 0))

        coupon_info_model = CouponInfoModel(context=self)

        coupon_info = coupon_info_model.get_dict_by_id(coupon_id)
        if not coupon_info or coupon_info["is_del"] == 1 or coupon_info["is_release"] == 0:
            return self.client_reponse_json_success({})

        coupon_info["discount_amount"] = int(coupon_info["discount_amount"])
        coupon_info["use_amount"] = int(coupon_info["use_amount"])
        coupon_info["discount_value"] = "%.1f" % coupon_info["discount_value"]

        return self.client_reponse_json_success(coupon_info)


class DrawCouponHandler(ClientBaseHandler):
    """
    :description: 领取优惠券
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,coupon_id")
    def get_async(self):
        """
        :description: 领取优惠券
        :param act_id:活动id
        :param user_id:用户id
        :param coupon_id:优惠劵id
        :return: 
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_request_param("act_id", 1))
        user_id = int(self.get_request_param("user_id", 0))
        coupon_id = int(self.get_request_param("coupon_id", 0))

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        coupon_info_model = CouponInfoModel(db_transaction=db_transaction, context=self)
        user_coupon_model = UserCouponModel(db_transaction=db_transaction, context=self)

        coupon_info = coupon_info_model.get_entity_by_id(coupon_id)
        if not coupon_info or coupon_info.is_del == 1:
            return self.client_reponse_json_error("HintMessage", "对不起，优惠券不存在")
        if coupon_info.is_release == 0:
            return self.client_reponse_json_error("HintMessage", "对不起，优惠券已下架")
        if self.get_now_datetime() > coupon_info.effective_end_date:
            return self.client_reponse_json_error("HintMessage", "对不起，优惠券不可领取，已失效")
        if coupon_info.scene_type == 2:
            return self.client_reponse_json_error("HintMessage", "对不起，优惠券不可领取，只能兑换")
        if coupon_info.total_num - coupon_info.draw_num <= 0:
            return self.client_reponse_json_error("HintMessage", "对不起，优惠券已领完")
        user_coupon_count = user_coupon_model.get_total("act_id=%s and user_id=%s and coupon_id=%s and exchange_id=0", params=[act_id, user_id, coupon_id])
        if user_coupon_count >= coupon_info.get_limit:
            return self.client_reponse_json_error("Error", "对不起，已达领取上限")

        #创建优惠券
        user_coupon = UserCoupon()
        user_coupon.act_id = act_id
        user_coupon.user_id = user_id
        user_coupon.exchange_id = 0
        user_coupon.coupon_id = coupon_id
        user_coupon.access_type = 1
        user_coupon.coupon_status = 0
        user_coupon.create_date = self.get_now_datetime()
        user_coupon.create_date_int = SevenHelper.get_now_day_int()

        result = coupon_info_model.update_table("draw_num=draw_num+1", "id=%s and draw_num=%s", params=[coupon_id, coupon_info.draw_num])
        if not result:
            return self.client_reponse_json_error("Error", "当前领取人数过多,请稍后再试")

        user_coupon_model.add_entity(user_coupon)

        return self.client_reponse_json_success(user_coupon)