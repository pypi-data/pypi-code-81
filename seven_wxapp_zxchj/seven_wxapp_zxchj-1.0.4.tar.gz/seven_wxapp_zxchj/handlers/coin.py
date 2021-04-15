# -*- coding: utf-8 -*-
"""
@Author: WangQiang
@Date: 2021-01-15 18:12:24
:LastEditTime: 2021-04-14 09:33:57
:LastEditors: HuangJingCan
@Description: 
"""
from seven_wxapp.handlers.base.client_base import *

from seven_wxapp_zxchj.models.ex_model import *
from seven_wxapp_zxchj.models.seven_model import PageInfo
from seven_wxapp_zxchj.models.db_models.coin.coin_record_model import *
from seven_wxapp_zxchj.models.db_models.user.user_info_model import *
from seven_wxapp_zxchj.models.db_models.user.user_coupon_model import *
from seven_wxapp_zxchj.models.db_models.user.user_prop_model import *
from seven_wxapp_zxchj.models.db_models.coin.coin_exchange_model import *
from seven_wxapp_zxchj.models.db_models.exchange.exchange_record_model import *
from seven_wxapp_zxchj.models.db_models.exchange.exchange_order_model import *
from seven_wxapp_zxchj.models.db_models.coupon.coupon_info_model import *


class NewCoinExchangeListHandler(ClientBaseHandler):
    """
    :description: 1.3版本 T币兑换列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :return: dict
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_request_param("act_id", 0))

        coin_exchange_model = CoinExchangeModel(context=self)
        coupon_info_model = CouponInfoModel(context=self)

        condition = "act_id=%s and is_release=1"
        result = {}
        result["coin_list"] = []
        result["coupon_list"] = []
        result["tool_list"] = []
        coin_exchange_list = coin_exchange_model.get_dict_list(condition, order_by="sort_index desc", params=[act_id])
        if len(coin_exchange_list) > 0:
            coupon_id_list = [int(i["coupon_id"]) for i in coin_exchange_list]
            coupon_info_list = []
            if len(coupon_id_list) > 0:
                coupon_info_list = coupon_info_model.get_dict_list(SevenHelper.get_condition_by_int_list("id", coupon_id_list))
            for item in coin_exchange_list:
                if int(item["goods_type"]) == 1:
                    result["coin_list"].append(item)
                elif int(item["goods_type"]) in [2, 3, 4]:
                    result["tool_list"].append(item)
                else:
                    coupon_info = [i for i in coupon_info_list if i["id"] == item["coupon_id"]]
                    if len(coupon_info) <= 0:
                        continue
                    if self.get_now_datetime() > str(coupon_info[0]["effective_end_date"]):
                        continue
                    item["stock_num"] = int(coupon_info[0]["total_num"]) - int(coupon_info[0]["draw_num"])
                    item["coupon_name"] = str(coupon_info[0]["coupon_name"])
                    item["effective_start_date"] = str(coupon_info[0]["effective_start_date"])
                    item["effective_end_date"] = str(coupon_info[0]["effective_end_date"])
                    item["rule_desc"] = str(coupon_info[0]["rule_desc"])
                    item["coupon_type"] = int(coupon_info[0]["coupon_type"])
                    item["discount_amount"] = int(coupon_info[0]["discount_amount"])
                    item["use_amount"] = int(coupon_info[0]["use_amount"])
                    item["discount_value"] = str(coupon_info[0]["discount_value"])
                    result["coupon_list"].append(item)

        return self.client_reponse_json_success(result)


class NewCoinExchangeHandler(ClientBaseHandler):
    """
    :description: 1.3版本 T币兑换
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,coin_exchange_id,login_token")
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :param coin_exchange_id：T币兑换id
        :param login_token:用户访问令牌
        :param real_name:收货人
        :param telephone:手机号
        :param province:省
        :param city:市
        :param county:区
        :param street:街道
        :param adress:详细地址
        :return: dict
        :last_editors: HuangJianYi
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        coin_exchange_id = int(self.get_request_param("coin_exchange_id", 0))
        login_token = self.get_request_param("login_token")
        real_name = self.get_request_param("real_name")
        telephone = self.get_request_param("telephone")
        province = self.get_request_param("province")
        city = self.get_request_param("city")
        county = self.get_request_param("county")
        street = self.get_request_param("street")
        adress = self.get_request_param("adress")

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        user_info_model = UserInfoModel(db_transaction=db_transaction, context=self)
        coin_exchange_model = CoinExchangeModel(db_transaction=db_transaction, context=self)
        user_prop_model = UserPropModel(db_transaction=db_transaction, context=self)
        exchange_order_model = ExchangeOrderModel(db_transaction=db_transaction, context=self)
        user_coupon_model = UserCouponModel(db_transaction=db_transaction, context=self)
        coupon_info_model = CouponInfoModel(context=self)

        #T币名称
        coinName = config.get_value("coinName")
        now_day = SevenHelper.get_now_day_int()
        #请求太频繁限制
        if self.check_post(f"CoinExchangeHandler_Get_{str(user_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")

        coin_exchange = coin_exchange_model.get_entity_by_id(coin_exchange_id)
        if not coin_exchange or coin_exchange.is_release == False:
            return self.client_reponse_json_error("Error", "对不起，当前兑换不存在")
        #获取当前用户
        user_info = user_info_model.get_entity_by_id(user_id)
        if not user_info:
            return self.client_reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if user_info.login_token != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录")
        if user_info.surplus_coin < coin_exchange.need_coin_count:
            return self.client_reponse_json_error("Error", f"对不起，{coinName}不足")
        if coin_exchange.goods_type == 5:
            coupon_info = coupon_info_model.get_entity_by_id(coin_exchange.coupon_id)
            if not coupon_info or coupon_info.is_del == 1 or coupon_info.is_release == 0:
                return self.client_reponse_json_error("Error", "对不起，优惠券不存在或已下架")
            if coupon_info.total_num - coupon_info.draw_num <= 0:
                return self.client_reponse_json_error("Error", "该优惠券库存不足")
        else:
            if coin_exchange.stock_num <= 0:
                if coin_exchange.goods_type == 1:
                    return self.client_reponse_json_error("Error", "该奖品库存不足")
                return self.client_reponse_json_error("Error", "该道具卡库存不足")

        #获取当日兑换该商品数量
        if coin_exchange.goods_type == 1:
            condition = "act_id=%s and user_id=%s and exchange_id=%s and create_date_int=%s"
            exchange_order_count = exchange_order_model.get_total(condition, params=[act_id, user_id, coin_exchange_id, now_day])
            if exchange_order_count >= coin_exchange.day_limit:
                return self.client_reponse_json_error("Error", "对不起，每日兑换已达上限")
        elif coin_exchange.goods_type == 5:
            condition = "act_id=%s and user_id=%s and exchange_id=%s and create_date_int=%s"
            user_coupon_count = user_coupon_model.get_total(condition, params=[act_id, user_id, coin_exchange_id, now_day])
            if user_coupon_count >= coin_exchange.day_limit:
                return self.client_reponse_json_error("Error", "对不起，每日兑换已达上限")
        else:
            condition = "act_id=%s and user_id=%s and prop_type=%s and create_date_int=%s"
            days_user_prop_count = user_prop_model.get_total(condition, params=[act_id, user_id, coin_exchange.goods_type, now_day])
            if days_user_prop_count >= coin_exchange.day_limit:
                return self.client_reponse_json_error("Error", "对不起，每日兑换已达上限")

        now_datetime = self.get_now_datetime()
        update_result = None
        if coin_exchange.goods_type == 5:
            update_result = coupon_info_model.update_table("draw_num=draw_num+1", "id=%s and draw_num=%s", params=[coupon_info.id, coupon_info.draw_num])
        else:
            update_result = coin_exchange_model.update_table("stock_num=stock_num-1,draw_num=draw_num+1", "id=%s and stock_num=%s", params=[coin_exchange.id, coin_exchange.stock_num])
        if update_result:
            try:
                db_transaction.begin_transaction()
                if coin_exchange.goods_type == 1:
                    #创建兑换订单
                    exchange_order = ExchangeOrder()
                    exchange_order.order_no = SevenHelper.create_order_id()
                    exchange_order.act_id = act_id
                    exchange_order.user_id = user_id
                    exchange_order.exchange_id = coin_exchange_id
                    exchange_order.real_name = real_name
                    exchange_order.telephone = telephone
                    exchange_order.province = province
                    exchange_order.city = city
                    exchange_order.county = county
                    exchange_order.street = street
                    exchange_order.adress = adress
                    exchange_order.goods_img = coin_exchange.goods_img
                    exchange_order.goods_num = 1
                    exchange_order.goods_name = coin_exchange.goods_name
                    exchange_order.goods_code = coin_exchange.goods_code
                    exchange_order.order_status = 0
                    exchange_order.create_date = now_datetime
                    exchange_order.create_date_int = SevenHelper.get_now_day_int()
                    exchange_order_model.add_entity(exchange_order)
                elif coin_exchange.goods_type == 5:
                    #创建优惠券
                    user_coupon = UserCoupon()
                    user_coupon.act_id = act_id
                    user_coupon.user_id = user_id
                    user_coupon.exchange_id = coin_exchange_id
                    user_coupon.coupon_id = coin_exchange.coupon_id
                    user_coupon.access_type = 2
                    user_coupon.coupon_status = 0
                    user_coupon.create_date = now_datetime
                    user_coupon.create_date_int = SevenHelper.get_now_day_int()
                    user_coupon_model.add_entity(user_coupon)
                else:
                    #创建道具记录
                    user_prop = UserProp()
                    user_prop.act_id = act_id
                    user_prop.user_id = user_id
                    user_prop.is_use = 0
                    user_prop.prop_type = coin_exchange.goods_type
                    user_prop.create_date_int = SevenHelper.get_now_day_int()
                    user_prop.create_date = now_datetime
                    user_prop_model.add_entity(user_prop)
                #添加T币记录
                CoinRecordModelEx(context=self).add_coin_record(act_id, user_info, "兑换：" + coin_exchange.goods_name, 4, 2, coin_exchange.need_coin_count, db_transaction)
                #添加兑换记录
                ExchangeRecordModelEx(context=self).add_exchange_record(act_id, user_info, "兑换：" + coin_exchange.goods_name, coin_exchange.goods_type, coin_exchange.need_coin_count, db_transaction)
                #更新用户
                update = "surplus_coin=surplus_coin-%s,modify_date=%s"
                params = [coin_exchange.need_coin_count, now_datetime]
                if coin_exchange.goods_type == 2:
                    update += ",perspective_card_count=perspective_card_count+1"
                    user_info.perspective_card_count += 1
                elif coin_exchange.goods_type == 3:
                    update += ",tips_card_count=tips_card_count+1"
                    user_info.tips_card_count += 1
                elif coin_exchange.goods_type == 4:
                    update += ",redraw_card_count=redraw_card_count+1"
                    user_info.redraw_card_count += 1
                user_info_model.update_table(update, f"id={user_id} and surplus_coin={user_info.surplus_coin}", params=params)

                user_info.surplus_coin -= coin_exchange.need_coin_count
                user_info.modify_date = now_datetime
                db_transaction.commit_transaction()
            except Exception as ex:
                db_transaction.rollback_transaction()
                if coin_exchange.goods_type == 5:
                    coupon_info_model.update_table("draw_num=draw_num-1", "id=%s", params=[coupon_info.id])
                else:
                    coin_exchange_model.update_table("stock_num=stock_num+1,draw_num=draw_num-1", "id=%s", params=[coin_exchange.id])
                self.logger_info.info("CoinExchangeHandler:" + str(ex))
        else:
            return self.client_reponse_json_error("Error", "当前人数过多,请稍后再试")

        return self.client_reponse_json_success(user_info)


class CoinRecordListHandler(ClientBaseHandler):
    """
    :description: T币交易记录
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :param page_size:页大小
        :param user_id：用户id
        :param transaction_type：交易类型:1增加2减少
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        page_index = int(self.get_request_param("page_index", 0))
        page_size = int(self.get_request_param("page_size", 20))
        transaction_type = int(self.get_request_param("transaction_type", 0))

        conidtion = "act_id=%s AND user_id=%s"
        params = [act_id, user_id]
        if transaction_type > 0:
            params.append(transaction_type)
            conidtion += " AND transaction_type=%s"

        coin_record_model = CoinRecordModel(context=self)
        field = "user_id,title,change_type,transaction_type,coin_count"
        coin_record_list_dict, total = coin_record_model.get_dict_page_list("*", page_index, page_size, conidtion, "", "create_date desc", params)
        page_info = PageInfo(page_index, page_size, total, coin_record_list_dict)

        return self.client_reponse_json_success(page_info)