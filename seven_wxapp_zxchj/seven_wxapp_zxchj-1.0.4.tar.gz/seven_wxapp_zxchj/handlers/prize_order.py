# -*- coding: utf-8 -*-
"""
@Author: WangQiang
@Date: 2021-01-21 14:57:37
:LastEditTime: 2021-04-15 11:25:28
:LastEditors: HuangJingCan
@Description: 
"""
from seven_wxapp.handlers.base.client_base import *
from seven_wxapp.handlers.base.wechatpay_base import *

from seven_wxapp_zxchj.models.enum import *
from seven_wxapp_zxchj.models.seven_model import PageInfo
from seven_wxapp_zxchj.models.db_models.prize.prize_roster_model import *
from seven_wxapp_zxchj.models.db_models.prize.prize_order_model import *
from seven_wxapp_zxchj.models.db_models.exchange.exchange_order_model import *
from seven_wxapp_zxchj.models.db_models.ip.ip_series_model import *
from seven_wxapp_zxchj.models.db_models.act.act_info_model import *
from seven_wxapp_zxchj.models.db_models.user.user_info_model import *
from seven_wxapp_zxchj.models.db_models.pay.pay_order_model import *


class PrizeRosterListHandler(ClientBaseHandler):
    """
    :description: 用户奖品列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param page_index:页索引
        :param page_size:页大小
        :param user_id：用户id
        :param prize_status:奖品状态（0未下单1已下单10处理中）
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        page_index = int(self.get_request_param("page_index", 0))
        page_size = int(self.get_request_param("page_size", 20))
        user_id = int(self.get_request_param("user_id", 0))
        prize_status = int(self.get_request_param("prize_status", -1))

        conidtion = "act_id=%s and pay_status=%s and user_id=%s"
        params = [act_id, 1, user_id]
        if prize_status >= 0:
            if prize_status == 0:
                conidtion += " AND (prize_status=%s or prize_status=%s)"
            params.append(prize_status)
            params.append(10)
        field = "id,user_id,machine_id,machine_name,machine_price,prize_id,prize_name,prize_price,prize_pic,toy_cabinet_pic,prize_detail,prize_tag,series_id,prize_status,create_date"

        prize_roster_model = PrizeRosterModel(context=self)
        ip_series_model = IpSeriesModel(context=self)

        prize_roster_list_dict, total = prize_roster_model.get_dict_page_list(field, page_index, page_size, conidtion, order_by="prize_status,create_date desc", params=params)
        if len(prize_roster_list_dict) > 0:
            ip_series_list_dict = []
            ip_series_id_list = [str(i["series_id"]) for i in prize_roster_list_dict]
            if len(ip_series_id_list) > 0:
                ip_series_id_ids = ",".join(ip_series_id_list)
                ip_series_list_dict = ip_series_model.get_dict_list("id in (" + ip_series_id_ids + ")")
            for i in range(len(prize_roster_list_dict)):
                current_ip_series = [ip_series for ip_series in ip_series_list_dict if prize_roster_list_dict[i]["series_id"] == ip_series["id"]]
                if len(current_ip_series) > 0:
                    prize_roster_list_dict[i]["series_name"] = current_ip_series[0]["series_name"]

        page_info = PageInfo(page_index, page_size, total, prize_roster_list_dict)

        return self.client_reponse_json_success(page_info)


class PrizeOrderListHandler(ClientBaseHandler):
    """
    :description: 用户奖品订单列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param page_index:页索引
        :param page_size:页大小
        :param user_id：用户id
        :param order_status:订单状态（0未付款1未发货2已发货3不予发货4已退款5已完成）
        :return list
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        page_index = int(self.get_request_param("page_index", 0))
        page_size = int(self.get_request_param("page_size", 20))
        user_id = int(self.get_request_param("user_id", 0))
        order_status = int(self.get_request_param("order_status", 0))

        conidtion = "act_id=%s AND user_id=%s"
        params = [act_id, user_id]
        if order_status >= 0:
            if order_status == 5:
                conidtion += " AND (order_status=%s or order_status=3)"
            else:
                conidtion += " AND order_status=%s"
            params.append(order_status)
        field = "id,order_no,user_id,real_name,telephone,province,city,county,street,adress,deliver_date,express_no,express_company,order_status,freight_price,is_free_shipping,remarks,create_date,freight_pay_order_no"

        prize_order_model = PrizeOrderModel(context=self)
        prize_roster_model = PrizeRosterModel(context=self)
        ip_series_model = IpSeriesModel(context=self)

        #奖品订单显示字段
        prize_order_list_dict, total = prize_order_model.get_dict_page_list(field, page_index, page_size, conidtion, "", "create_date desc", params)
        if prize_order_list_dict:
            prize_order_no_list = [str(i["order_no"]) for i in prize_order_list_dict]
            condition = SevenHelper.get_condition_by_str_list("prize_order_no", prize_order_no_list)
            #奖品显示字段
            prize_field = "id,user_id,machine_id,machine_name,machine_price,prize_id,prize_name,prize_price,prize_pic,toy_cabinet_pic,prize_detail,prize_tag,series_id,prize_status,prize_order_no,create_date"

            prize_roster_list_dict = prize_roster_model.get_dict_list(condition, field=prize_field)

            ip_series_list_dict = []
            ip_series_id_list = [str(i["series_id"]) for i in prize_roster_list_dict]
            if len(ip_series_id_list) > 0:
                ip_series_id_ids = ",".join(ip_series_id_list)
                ip_series_list_dict = ip_series_model.get_dict_list("id in (" + ip_series_id_ids + ")")

            for i in range(len(prize_order_list_dict)):
                prize_list = [prize_roster for prize_roster in prize_roster_list_dict if prize_order_list_dict[i]["order_no"] == prize_roster["prize_order_no"]]
                cur_prize = prize_list[0] if len(prize_list) > 0 else None
                cur_series_id = cur_prize["series_id"] if cur_prize != None else 0
                series_name_list = [ip_series["series_name"] for ip_series in ip_series_list_dict if cur_series_id == ip_series["id"]]
                prize_order_list_dict[i]["series_name"] = series_name_list[0] if len(series_name_list) > 0 else ""
                prize_order_list_dict[i]["prize_list"] = prize_list
                #物流公司名称转换
                prize_order_list_dict[i]["express_company"] = self.get_express_company(prize_order_list_dict[i]["express_company"])

        page_info = PageInfo(page_index, page_size, total, prize_order_list_dict)

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


class CreatePrizeOrderHandler(ClientBaseHandler):
    """
    :description: 创建奖品订单
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,prize_ids,login_token,real_name,telephone")
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :param login_token:用户访问令牌
        :param prize_ids:用户奖品id串，逗号分隔
        :param real_name:用户名
        :param telephone:电话
        :param province:省
        :param city:市
        :param county:区县
        :param street:街道
        :param address:地址
        :return list
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        login_token = self.get_request_param("login_token")
        prize_ids = self.get_request_param("prize_ids")
        real_name = self.get_request_param("real_name")
        telephone = self.get_request_param("telephone")
        province = self.get_request_param("province")
        city = self.get_request_param("city")
        county = self.get_request_param("county")
        street = self.get_request_param("street")
        address = self.get_request_param("address")

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        user_info_model = UserInfoModel(db_transaction=db_transaction, context=self)
        act_info_model = ActInfoModel(db_transaction=db_transaction, context=self)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction, context=self)
        pay_order_model = PayOrderModel(db_transaction=db_transaction, context=self)

        #请求太频繁限制
        if self.check_post(f"CreatePrizeOrder_Post_{str(user_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")

        #获取用户信息
        user_info = user_info_model.get_dict_by_id(user_id)
        if not user_info:
            return self.client_reponse_json_error("Error", "对不起，用户不存在")
        if user_info["login_token"] != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录,当前无法下单")
        if int(user_info["user_state"]) == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        #活动信息
        act_info = act_info_model.get_entity(f"id={act_id}")
        #用户奖品列表

        prize_roster_list = prize_roster_model.get_list("id in (" + prize_ids + ")")
        if len(prize_roster_list) == 0:
            return self.client_reponse_json_error("Error", "对不起，所选下单奖品不存在")
        order_placed_prize = [prize_roster for prize_roster in prize_roster_list if prize_roster.prize_status != 0]
        if len(order_placed_prize) > 0:
            return self.client_reponse_json_error("Refresh", "对不起，部分奖品已下单，请刷新页面")
        now_date = self.get_now_datetime()
        prize_order_id = 0
        prize_order = PrizeOrder()
        prize_roster_dict_list = []
        #支付订单
        pay_order_no = ""
        try:
            #创建订单
            prize_order_model = PrizeOrderModel(context=self)
            prize_order.user_id = user_id
            prize_order.act_id = act_id
            prize_order.real_name = real_name
            prize_order.telephone = telephone
            prize_order.province = province
            prize_order.city = city
            prize_order.county = county
            prize_order.street = street
            prize_order.adress = address
            prize_order.order_status = 0  #订单状态（0未付款1未发货2已发货3不予发货4已退款5已完成10处理中）
            prize_order.is_free_shipping = 0
            prize_order.is_auto_deliver = 0
            prize_order.create_date = now_date
            prize_order.modify_date = now_date
            prize_order.order_no = SevenHelper.create_order_id()
            #是否包邮
            is_free_shipping = False
            #满足包邮件数
            if act_info.is_num_free_shipping and act_info.free_shipping_count <= len(prize_roster_list):
                is_free_shipping = True
                prize_order.is_free_shipping = 1
                prize_order.order_status = 1
            elif act_info.is_amount_free_shipping:
                #满足包邮金额
                prize_amount = 0
                for prize_roster in prize_roster_list:
                    prize_amount += decimal.Decimal(prize_roster.prize_price)
                if prize_amount >= decimal.Decimal(act_info.free_shipping_amount):
                    #包邮
                    is_free_shipping = True
                    prize_order.is_free_shipping = 1
                    prize_order.order_status = 1
            if is_free_shipping == False:
                prize_order.freight_price = act_info.freight_price
                pay_order_no = SevenHelper.create_order_id()
                prize_order.freight_pay_order_no = pay_order_no
            #保存奖品订单
            prize_order_id = prize_order_model.add_entity(prize_order)
            #开始事务
            db_transaction.begin_transaction()
            if prize_order_id <= 0:
                return self.client_reponse_json_error("Error", "对不起，请重新选择")
            #更新用户奖品列表
            for prize_roster in prize_roster_list:
                prize_roster.prize_order_no = prize_order.order_no
                #更新奖品状态为处理中
                prize_roster.prize_status = 10
                if is_free_shipping == True:
                    prize_roster.prize_status = 1
                prize_roster_dict_list.append(prize_roster.__dict__)
            if is_free_shipping == False:
                #创建支付订单
                pay_order = PayOrder()
                pay_order.open_id = user_info["open_id"]
                pay_order.pay_order_no = pay_order_no
                pay_order.order_name = "运费付款"
                pay_order.order_desc = ""
                pay_order.order_status = 0
                pay_order.pay_amount = act_info.freight_price
                pay_order.create_date = now_date
                pay_order.scene = 2
                pay_order_model.add_entity(pay_order)
                update_result = prize_roster_model.update_list(prize_roster_list, "prize_status,prize_order_no")
            #更新奖品信息
            update_result = prize_roster_model.update_list(prize_roster_list, "prize_status,prize_order_no")
            #结束事务
            db_transaction.commit_transaction()
            if update_result == False and prize_order_id > 0:
                prize_order_model.del_entity("id=%s", params=prize_order_id)
                return self.client_reponse_json_error("Error", "对不起，请重新选择")
        except Exception as ex:
            db_transaction.rollback_transaction()
            self.logger_info.info("CreatePrizeOrderHandler:" + str(ex))
            if prize_order_id > 0:
                prize_order_model.del_entity("id=%s", params=prize_order_id)

        prize_order = prize_order.__dict__
        prize_order["prize_list"] = prize_roster_dict_list
        prize_order["pay_order_no"] = pay_order_no

        return self.client_reponse_json_success(prize_order)


class ConfirmReceiptHandler(ClientBaseHandler):
    """
    :description: 确认收货
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :param login_token:用户登录令牌
        :param prize_order_id:奖品订单id
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        login_token = self.get_request_param("login_token")
        prize_order_id = int(self.get_request_param("prize_order_id", 0))

        prize_order_model = PrizeOrderModel(context=self)
        prize_roster_model = PrizeRosterModel(context=self)

        prize_order = prize_order_model.get_entity_by_id(prize_order_id)
        #获取用户信息
        user_info_model = UserInfoModel(context=self)
        user_info = user_info_model.get_dict_by_id(user_id)
        if not user_info:
            return self.client_reponse_json_error("Error", "对不起，用户不存在")
        if user_info["login_token"] != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录,当前无法下单")
        if int(user_info["user_state"]) == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if not prize_order:
            return self.client_reponse_json_error("Error", "对不起，订单不存在")
        if prize_order.order_status != 2:
            return self.client_reponse_json_error("Error", "对不起，当前订单状态不可确认收货")
        if prize_order.user_id != user_id:
            return self.client_reponse_json_error("Error", "对不起，非法操作")
        prize_order.order_status = 5
        now_datetime = self.get_now_datetime()
        prize_order.modify_date = now_datetime

        result = prize_order_model.update_entity(prize_order, "order_status,modify_date")
        if result == False:
            return self.client_reponse_json_error("Error", "对不起，确认收货失败")

        return self.client_reponse_json_success()


class CancelOrderHandler(ClientBaseHandler):
    """
    :description: 取消订单
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,prize_order_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :param login_token:用户登录令牌
        :param prize_order_id:奖品订单id
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        login_token = self.get_request_param("login_token")
        prize_order_id = int(self.get_request_param("prize_order_id", 0))

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        user_info_model = UserInfoModel(db_transaction=db_transaction, context=self)
        prize_order_model = PrizeOrderModel(db_transaction=db_transaction, context=self)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction, context=self)

        #请求太频繁限制
        if self.check_post(f"CancelOrderHandler_Get_{str(user_id)}_{str(prize_order_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")

        #奖品订单信息
        prize_order = prize_order_model.get_entity_by_id(prize_order_id)
        #获取用户信息
        user_info = user_info_model.get_dict_by_id(user_id)
        if not user_info:
            return self.client_reponse_json_error("Error", "对不起，用户不存在")
        if user_info["login_token"] != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录,当前无法下单")
        if int(user_info["user_state"]) == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if not prize_order:
            return self.client_reponse_json_error("Error", "对不起，订单不存在")
        if prize_order.user_id != user_id:
            return self.client_reponse_json_error("Error", "对不起，非法操作")
        if prize_order.order_status != 0:
            return self.client_reponse_json_error("Error", "对不起，当前不可取消订单")
        if not prize_order.freight_pay_order_no:
            return self.client_reponse_json_error("Error", "对不起，订单异常，请联系客服")
        #是否已支付订单
        pay_status = WeiXinPayRequest().get_pay_status(prize_order.freight_pay_order_no)
        if pay_status == "":
            return self.client_reponse_json_error("Error", "对不起，取消订单失败")
        is_paid_order = True if pay_status == "SUCCESS" else False
        try:
            db_transaction.begin_transaction()
            if is_paid_order == False:
                prize_order_model.del_entity("id=%s", params=[prize_order.id])
                prize_roster_model.update_table("prize_status=0,prize_order_no=''", f"prize_order_no='{prize_order.order_no}'")
            else:
                #订单已支付成功
                prize_order.prize_status = 10
                prize_order.modify_date = self.get_now_datetime()
                prize_order_model.update_table(prize_order, "prize_status,modify_date")
                #更新奖品信息
                prize_roster_model.update_table("prize_status=10", f"prize_order_no='{prize_order.order_no}'")

            db_transaction.commit_transaction()
        except Exception as ex:
            db_transaction.rollback_transaction()
            self.logger_info.info("CancelOrderHandler:" + str(ex))
            return self.client_reponse_json_error("Error", "对不起，取消订单失败")

        result = {}
        result["is_paid_order"] = is_paid_order

        return self.client_reponse_json_success(result)


class CompleteOrderPayHandler(ClientBaseHandler):
    """
    :description: 完成奖品订单邮费支付
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,prize_order_id,login_token")
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :param login_token:用户登录令牌
        :param prize_order_id:奖品订单id
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        login_token = self.get_request_param("login_token")
        prize_order_id = int(self.get_request_param("prize_order_id", 0))

        #请求太频繁限制
        if self.check_post(f"CompleteOrderPayHandler_Get_{str(user_id)}_{str(prize_order_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")

        user_info_model = UserInfoModel(context=self)
        prize_order_model = PrizeOrderModel(context=self)
        #奖品订单信息
        prize_order = prize_order_model.get_entity_by_id(prize_order_id)
        #获取用户信息
        user_info = user_info_model.get_dict_by_id(user_id)
        if not user_info:
            return self.client_reponse_json_error("Error", "对不起，用户不存在")
        if user_info["login_token"] != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录,当前无法下单")
        if not prize_order:
            return self.client_reponse_json_error("Error", "对不起，订单不存在")
        if prize_order.user_id != user_id:
            return self.client_reponse_json_error("Error", "对不起，非法操作")
        if prize_order.order_status != 0:
            return self.client_reponse_json_error("Error", "对不起，订单状态异常")
        #更新订单状态为付款中
        prize_order.order_status = 10
        prize_order.modify_date = self.get_now_datetime()
        result = prize_order_model.update_entity(prize_order, "order_status,modify_date")
        if result == False:
            return self.client_reponse_json_error("Error", "对不起，订单更新失败")

        return self.client_reponse_json_success()


class LogisticsHandler(ClientBaseHandler):
    """
    :description: 物流信息查询
    """
    @client_filter_check_head()
    def get_async(self):
        """
        :description: 物流信息查询
        :last_editors: HuangJianYi
        """
        order_no = self.get_request_param("order_no")
        order_type = int(self.get_request_param("order_type", 0))

        express_company = ""
        express_no = ""
        if order_type == 1:
            # 验证发货订单
            exchange_order = ExchangeOrderModel(context=self).get_entity(where="order_no=%s", params=order_no)
            if not exchange_order:
                return self.client_reponse_json_error("抱歉！无法获取发货订单")
            if exchange_order.order_status != 1:
                return self.client_reponse_json_error("抱歉！该发货订单状态无法获取物流信息")

            express_company = exchange_order.express_company
            express_no = exchange_order.express_no
        else:
            # 验证发货订单
            prize_order = PrizeOrderModel(context=self).get_entity(where="order_no=%s", params=order_no)
            if not prize_order:
                return self.client_reponse_json_error("抱歉！无法获取发货订单")
            if prize_order.order_status != 2:
                return self.client_reponse_json_error("抱歉！该发货订单状态无法获取物流信息")
            express_company = prize_order.express_company
            express_no = prize_order.express_no

        url = "https://kuaidi.miniso.cn/index.php"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        param = {
            "com": express_company,
            "num": express_no,
        }
        data = {"customer": "F8623D07D2859EC4EAF3E9BDE0B8FA2B", "sign": CryptoHelper.md5_encrypt(f'{json.dumps(param,ensure_ascii=False,cls=JsonEncoder,separators=(",", ":"))}miniso100KDSF8623D07D2859EC4EAF3E9BDE0B8FA2B').upper(), "param": json.dumps(param, ensure_ascii=False, cls=JsonEncoder, separators=(",", ":"))}
        ret = requests.post(url, data=data, headers=headers)
        ret_json = json.loads(ret.text)
        if 'result' in ret_json.keys():
            return self.client_reponse_json_error(ret_json["message"])

        if ret_json["status"] == "200":
            # 查询成功
            ret_data = {"com": LogisticsType[ret_json["com"]].value, "nu": ret_json["nu"], "data": ret_json["data"]}
            # self.logger_info.info("LogisticsHandler:" + str(ret_data))
            return self.client_reponse_json_success(ret_data)

        # 查询失败
        return self.client_reponse_json_error(ret_json["message"])