# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2021-02-02 18:08:00
:LastEditTime: 2021-04-12 17:24:57
:LastEditors: HuangJingCan
:Description: 
"""
from seven_wxapp.handlers.base.client_base import *
from seven_wxapp.handlers.base.wechatpay_base import *

from seven_wxapp_zxchj.models.db_models.user.user_info_model import *
from seven_wxapp_zxchj.models.db_models.prize.prize_roster_model import *
from seven_wxapp_zxchj.models.db_models.pay.pay_order_model import *
from seven_wxapp_zxchj.models.db_models.buy.buy_order_model import *
from seven_wxapp_zxchj.models.db_models.coupon.coupon_info_model import *
from seven_wxapp_zxchj.models.db_models.user.user_prop_model import *
from seven_wxapp_zxchj.models.db_models.user.user_coupon_model import *
from seven_wxapp_zxchj.models.db_models.machine.machine_info_model import *


class GetWaitPayOrderHandler(ClientBaseHandler):
    """
    :description: 最近一条等待支付的购买订单,在进入每个中盒的时候调用
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :description: 最近一条等待支付的购买订单
        :param act_id: 活动id
        :param user_id: 用户id
        :return: dict
        :last_editors: HuangJianYi
        """
        user_id = int(self.get_request_param("user_id", 0))
        act_id = int(self.get_request_param("act_id", 1))

        buy_order_model = BuyOrderModel(context=self)
        machine_info_model = MachineInfoModel(context=self)

        buy_order = buy_order_model.get_dict("act_id=%s and user_id=%s and order_status=0", order_by="create_date desc", field="id,pay_order_no,machine_id,machine_name,buy_amount,pay_amount,discount_amount,order_status", params=[act_id, user_id])
        if buy_order:
            machine_info = machine_info_model.get_dict_by_id(buy_order["machine_id"])
            if machine_info and machine_info["is_release"] == 1 and machine_info["is_del"] == 0:
                buy_order["machine_bg_pic"] = machine_info["machine_bg_pic"]
                buy_order["box_style_detail"] = machine_info["box_style_detail"]
            else:
                return self.client_reponse_json_success({})
            for key in buy_order:
                if key in ["buy_amount", "pay_amount", "discount_amount"]:
                    buy_order[key] = int(buy_order[key])
            return self.client_reponse_json_success(buy_order)

        return self.client_reponse_json_success({})


class CancelBuyOrderHandler(ClientBaseHandler):
    """
    :description: 取消购买订单
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,buy_order_id,login_token")
    def get_async(self):
        """
        :description: 取消购买订单
        :param act_id:活动id
        :param user_id:用户id
        :param pay_order_no:支付订单号
        :return: dict
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_request_param("act_id", 1))
        user_id = int(self.get_request_param("user_id", 0))
        login_token = self.get_request_param("login_token")
        buy_order_id = int(self.get_request_param("buy_order_id", 0))

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        pay_order_model = PayOrderModel(db_transaction=db_transaction, context=self)
        buy_order_model = BuyOrderModel(db_transaction=db_transaction, context=self)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction, context=self)
        user_coupon_model = UserCouponModel(db_transaction=db_transaction, context=self)
        user_info_model = UserInfoModel(context=self)

        #请求太频繁限制
        if self.check_post(f"CancelBuyOrderHandler:{str(user_id)}_{str(buy_order_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")
        #奖品订单信息
        buy_order = buy_order_model.get_entity_by_id(buy_order_id)
        #获取用户信息
        user_info = user_info_model.get_dict_by_id(user_id)
        if not user_info:
            return self.client_reponse_json_error("Error", "对不起，用户不存在")
        if user_info["login_token"] != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录")
        if int(user_info["user_state"]) == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if not buy_order:
            return self.client_reponse_json_error("Error", "对不起，订单不存在")
        if buy_order.user_id != user_id:
            return self.client_reponse_json_error("Error", "对不起，非法操作")
        if buy_order.order_status != 0:
            return self.client_reponse_json_error("Error", "对不起，当前不可取消订单")
        if not buy_order.pay_order_no:
            return self.client_reponse_json_error("Error", "对不起，订单异常，请联系客服")

        #是否已支付订单
        pay_status = WeiXinPayRequest().get_pay_status(buy_order.pay_order_no)
        if pay_status == "":
            return self.client_reponse_json_error("Error", "对不起，取消订单失败")
        is_paid_order = True if pay_status == "SUCCESS" else False
        if is_paid_order:
            return self.client_reponse_json_error("Error", "订单已支付,无法取消")
        try:
            db_transaction.begin_transaction()
            pay_order_model.del_entity("pay_order_no=%s", params=[buy_order.pay_order_no])
            buy_order_model.del_entity("pay_order_no=%s", params=[buy_order.pay_order_no])
            prize_roster_model.del_entity("pay_order_no=%s", params=[buy_order.pay_order_no])
            user_coupon_model.update_table("pay_order_no='',coupon_status=0,use_date='1900-01-01 00:00:00'", "pay_order_no=%s and coupon_status=1", params=[buy_order.pay_order_no])
            db_transaction.commit_transaction()

        except Exception as ex:
            db_transaction.rollback_transaction()
            self.logger_error.error(f"取消购买订单异常:" + str(ex))
            return self.client_reponse_json_error("Error", "对不起，取消订单失败")

        return self.client_reponse_json_success({})