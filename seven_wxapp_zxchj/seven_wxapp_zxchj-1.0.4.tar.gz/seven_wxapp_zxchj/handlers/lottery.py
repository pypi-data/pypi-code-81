# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2020-05-26 17:51:04
:LastEditTime: 2021-04-14 09:34:20
:LastEditors: HuangJingCan
:Description: 拆盒相关接口
"""
import random
import datetime

from seven_wxapp.handlers.base.client_base import *
from seven_wxapp.handlers.base.behavior_base import *

from seven_wxapp_zxchj.models.enum import *
from seven_wxapp_zxchj.models.ex_model import *
from seven_wxapp_zxchj.models.db_models.act.act_info_model import *
from seven_wxapp_zxchj.models.db_models.user.user_info_model import *
from seven_wxapp_zxchj.models.db_models.user.user_prop_model import *
from seven_wxapp_zxchj.models.db_models.machine.machine_info_model import *
from seven_wxapp_zxchj.models.db_models.machine.machine_prize_model import *
from seven_wxapp_zxchj.models.db_models.prize.prize_roster_model import *
from seven_wxapp_zxchj.models.db_models.surplus.surplus_queue_model import *
from seven_wxapp_zxchj.models.db_models.pay.pay_order_model import *
from seven_wxapp_zxchj.models.db_models.buy.buy_order_model import *
from seven_wxapp_zxchj.models.db_models.user.user_coupon_model import *
from seven_wxapp_zxchj.models.db_models.coupon.coupon_info_model import *


class MachinePrizeListHandler(ClientBaseHandler):
    """
    :description: 每个中盒分配的奖品列表
    """
    @client_filter_check_head()
    @client_filter_check_params("user_id,machine_id")
    def get_async(self):
        """
        :description: 分配的奖品列表
        :param act_id:活动id
        :param user_id:用户id
        :param machine_id:机台id
        :return: 
        :last_editors: HuangJianYi
        """
        user_id = int(self.get_request_param("user_id", 0))
        act_id = int(self.get_request_param("act_id", 1))
        machine_id = int(self.get_request_param("machine_id", 0))

        #请求太频繁限制
        if self.check_post(f"PrizeList_Post_{str(user_id)}_{str(machine_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")

        #入队列
        queue_name = f"PrizeList_Queue_{str(machine_id)}"
        identifier = None
        is_lock = False
        if self.check_lpush(queue_name, user_id) == False:
            identifier = self.acquire_lock(queue_name)
            is_lock = True
        if isinstance(identifier, bool):
            return self.client_reponse_json_error("UserLimit", "当前人数过多,请稍后再来")

        machine_info_model = MachineInfoModel(context=self)
        machine_prize_model = MachinePrizeModel(context=self)
        surplus_queue_model = SurplusQueueModel(context=self)
        machine_info = machine_info_model.get_entity_by_id(machine_id)
        if not machine_info or machine_info.is_release == 0 or machine_info.is_del == 1:
            self.lpop(queue_name)
            self.release_lock(queue_name, identifier)
            return self.client_reponse_json_error("NoMachine", "对不起，找不到该盲盒")
        specs_type = machine_info.specs_type
        if specs_type == 5:
            ran_num = random.randint(3, 5)
        elif specs_type == 6:
            ran_num = random.randint(3, 6)
        elif specs_type == 7:
            ran_num = random.randint(3, 7)
        elif specs_type == 8:
            ran_num = random.randint(4, 8)
        elif specs_type == 9:
            ran_num = random.randint(5, 9)
        elif specs_type == 10:
            ran_num = random.randint(6, 10)
        elif specs_type == 12:
            ran_num = random.randint(7, 12)
        else:
            ran_num = random.randint(9, 16)

        condition = "act_id=%s AND machine_id=%s AND is_release=1 AND is_del=0 AND surplus>0 AND probability>0"
        machine_prize_list = machine_prize_model.get_list(condition, params=[act_id, machine_id])
        if len(machine_prize_list) <= 0:
            self.lpop(queue_name)
            if is_lock:
                self.release_lock(queue_name, identifier)
            return self.client_reponse_json_error("NoPrize", "对不起，该盲盒已售罄")
        if ran_num > len(machine_prize_list):
            ran_num = len(machine_prize_list)
        machine_prize_id_list = []
        random_Prize_dict_list = {}
        for machine_prize in machine_prize_list:
            random_Prize_dict_list[machine_prize.id] = machine_prize.probability
        for i in range(ran_num):
            prize_id = self.random_weight(random_Prize_dict_list)
            machine_prize_id_list.append(prize_id)
            if machine_info.is_repeat_prize == 0:
                del random_Prize_dict_list[prize_id]
        machine_prize_process_list = []
        if len(machine_prize_id_list) > 0:
            if machine_info.is_repeat_prize == 0:
                machine_prize_process_list = [machine_prize for machine_prize in machine_prize_list if machine_prize.id in machine_prize_id_list]
            else:
                for prize_id in machine_prize_id_list:
                    filter_prize = [machine_prize for machine_prize in machine_prize_list if machine_prize.id == prize_id]
                    if len(filter_prize) > 0:
                        machine_prize_process_list.extend(filter_prize)
        else:
            self.lpop(queue_name)
            if is_lock:
                self.release_lock(queue_name, identifier)
            return self.client_reponse_json_error("NoPrize", "对不起，该盲盒已售罄")

        group_id = SevenHelper.create_order_id()
        result_info = {}
        result_list = []
        redis_prize_dict = {}
        serial_no = 0
        for machine_prize in machine_prize_process_list:
            update_result = machine_prize_model.update_table("surplus=surplus-1", "id=%s AND surplus>0", params=[machine_prize.id])
            if update_result == True:
                serial_no = int(serial_no) + 1
                #预扣队列
                surplus_queue = SurplusQueue()
                surplus_queue.act_id = act_id
                surplus_queue.machine_id = machine_id
                surplus_queue.group_id = group_id
                surplus_queue.prize_id = machine_prize.id
                surplus_queue.user_id = user_id
                surplus_queue.withhold_value = 1
                surplus_queue.create_date = self.get_now_datetime()
                surplus_queue.expire_date = TimeHelper.add_minutes_by_format_time(minute=90)
                surplus_queue_model.add_entity(surplus_queue)
                prize_dict = {}
                prize_dict["serial_no"] = serial_no
                result_list.append(prize_dict)

                redis_prize_dict[str(serial_no)] = machine_prize.id

        self.lpop(queue_name)
        if is_lock:
            self.release_lock(queue_name, identifier)
        if len(result_list) <= 0:
            return self.client_reponse_json_error("NoPrize", "对不起，该盲盒已售罄")
        result_info["group_id"] = group_id
        result_info["specs_type"] = specs_type
        result_info["min_machine_list"] = result_list

        self.redis_init().set(f"min_machinelist_{str(user_id)}_{str(group_id)}", self.json_dumps(redis_prize_dict), ex=3600 * 1)

        return self.client_reponse_json_success(result_info)


class GetHorseRaceLampListHandler(ClientBaseHandler):
    """
    :description: 获取跑马灯奖品列表
    """
    @client_filter_check_head()
    def get_async(self):
        """
        :description: 获取跑马灯奖品列表
        :param act_id:活动id
        :param machine_id:机台id
        :param page_index：页索引
        :param page_size：页大小
        :return list
        :last_editors: HuangJianYi
        """
        machine_id = int(self.get_request_param("machine_id", 0))
        act_id = int(self.get_request_param("act_id", 1))
        page_size = int(self.get_request_param("page_size", 30))

        page_list = []
        machine_prize_list_dict = []
        if machine_id == 0:
            condition = "act_id=%s"
            params = [act_id]
            machine_info_list_dict = MachineInfoModel(context=self).get_dict_list("act_id=%s and is_release=1 and is_del=0 and is_prize_notice=0", params=[act_id])
            machine_id_list = [str(i["id"]) for i in machine_info_list_dict]
            if len(machine_id_list) > 0:
                machine_ids = ",".join(machine_id_list)
                condition += " and machine_id not in (" + machine_ids + ")"
            machine_prize_list_dict = MachinePrizeModel(context=self).get_dict_list("act_id=%s and is_release=1 and is_del=0 and is_prize_notice=0", params=[act_id])
        else:
            machine_info_dict = MachineInfoModel(context=self).get_dict("id=%s and is_release=1 and is_del=0 and is_prize_notice=1", params=[machine_id])
            if not machine_info_dict:
                return self.client_reponse_json_success(page_list)
            condition = "act_id=%s and machine_id=%s"
            params = [act_id, machine_id]
            machine_prize_list_dict = MachinePrizeModel(context=self).get_dict_list("act_id=%s and machine_id=%s and is_release=1 and is_del=0 and is_prize_notice=0", params=[act_id, machine_id])

        if machine_prize_list_dict:
            prize_id_list = [str(i["id"]) for i in machine_prize_list_dict]
            if len(prize_id_list) > 0:
                prize_ids = ",".join(prize_id_list)
                condition += " and prize_id not in (" + prize_ids + ")"
        prize_roster_model = PrizeRosterModel(context=self)
        page_list = prize_roster_model.get_dict_list(condition, "", "create_date desc", str(page_size), "user_nick,prize_name,prize_tag,machine_name", params)
        total = int(len(page_list))
        if total > 0:
            for i in range(len(page_list)):
                if page_list[i]["user_nick"]:
                    length = len(page_list[i]["user_nick"])
                    if length > 2:
                        user_nick = page_list[i]["user_nick"][0:length - 2] + "**"
                    else:
                        user_nick = page_list[i]["user_nick"][0:1] + "*"
                    page_list[i]["user_nick"] = user_nick
        return self.client_reponse_json_success(page_list)


class LotteryHandler(ClientBaseHandler):
    """
    :description: 拆盒
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,login_token,serial_no,group_id")
    def get_async(self):
        """
        :description: 抽奖
        :param act_id:活动id
        :param user_id:用户id
        :param login_token:登录令牌
        :param prize_id:奖品id
        :param group_id:用户进入中盒自动分配的唯一标识
        :param user_coupon_id:用户优惠券标识
        :return: 抽奖
        :last_editors: HuangJianYi
        """
        user_id = int(self.get_request_param("user_id", 0))
        login_token = self.get_request_param("login_token")
        group_id = self.get_request_param("group_id", "")
        serial_no = int(self.get_request_param("serial_no", 1))
        act_id = int(self.get_request_param("act_id", 1))
        user_coupon_id = int(self.get_request_param("user_coupon_id", 0))

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        user_info_model = UserInfoModel(db_transaction=db_transaction, context=self)
        machine_prize_model = MachinePrizeModel(db_transaction=db_transaction, context=self)
        surplus_queue_model = SurplusQueueModel(db_transaction=db_transaction, context=self)
        pay_order_model = PayOrderModel(db_transaction=db_transaction, context=self)
        buy_order_model = BuyOrderModel(db_transaction=db_transaction, context=self)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction, context=self)
        user_coupon_model = UserCouponModel(db_transaction=db_transaction, context=self)
        coupon_info_model = CouponInfoModel(context=self)

        #请求太频繁限制
        if self.check_post(f"Lottery_Post_{str(user_id)}_{str(group_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")
        user_info = user_info_model.get_entity("id=%s", params=[user_id])
        if not user_info or user_info.act_id != act_id:
            return self.client_reponse_json_error("Error", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if user_info.login_token != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录,当前无法操作")

        act_info_model = ActInfoModel(context=self)
        act_info = act_info_model.get_entity("id=%s and is_open=1 and is_del=0", params=act_id)
        if not act_info:
            return self.client_reponse_json_error("Error", "对不起，活动不存在")

        redis_minmachinelist_key = f"min_machinelist_{str(user_id)}_{str(group_id)}"
        min_machine_list = self.redis_init().get(redis_minmachinelist_key)
        min_machine_list = json.loads(min_machine_list) if min_machine_list != None else {}
        prize_id = min_machine_list[str(serial_no)] if str(serial_no) in min_machine_list.keys() else 0
        if prize_id <= 0:
            return self.client_reponse_json_error("Error", "超时操作,请重新选择盒子")
        machine_prize = machine_prize_model.get_entity_by_id(prize_id)
        if not machine_prize:
            return self.client_reponse_json_error("Error", "对不起，奖品不存在")
        if machine_prize.is_release == 0 or machine_prize.is_del == 1:
            return self.client_reponse_json_error("Error", "对不起，奖品不存在")

        surplus_queue = surplus_queue_model.get_entity("user_id=%s and group_id=%s and prize_id=%s", params=[user_id, group_id, prize_id])
        if not surplus_queue:
            return self.client_reponse_json_error("Error", "对不起，请重新选择盲盒")

        machine_info_model = MachineInfoModel(context=self)
        machine_info = machine_info_model.get_entity("id=%s and is_release=1 and is_del=0", params=machine_prize.machine_id)
        if not machine_info:
            return self.client_reponse_json_error("Error", "对不起，盒子不存在")

        now_date = self.get_now_datetime()
        buy_amount = decimal.Decimal(machine_info.machine_price)
        pay_amount = decimal.Decimal(machine_info.machine_price)
        discount_amount = 0
        pay_order_no = SevenHelper.create_order_id()
        user_coupon = None
        if pay_amount <= 0:
            return self.client_reponse_json_error("Error", "对不起，盒子配置出错")

        if user_coupon_id > 0:
            user_coupon = user_coupon_model.get_entity_by_id(user_coupon_id)
            if not user_coupon:
                return self.client_reponse_json_error("Error", "优惠券不存在")
            if user_coupon.user_id != user_id:
                return self.client_reponse_json_error("Error", "优惠券不存在")
            if user_coupon.coupon_status == 1:
                return self.client_reponse_json_error("Error", "优惠券已使用")
            elif user_coupon.coupon_status == 2:
                return self.client_reponse_json_error("Error", "优惠券已失效")
            coupon_info = coupon_info_model.get_entity_by_id(user_coupon.coupon_id)
            if not coupon_info or coupon_info.is_release == 0:
                return self.client_reponse_json_error("Error", "优惠券不存在")
            if now_date < coupon_info.effective_start_date:
                return self.client_reponse_json_error("Error", f"{coupon_info.effective_start_date}后才能使用此优惠券")
            if now_date > coupon_info.effective_end_date:
                return self.client_reponse_json_error("Error", "优惠券已失效,超过有效使用时间")
            if coupon_info.coupon_type == 2:
                if buy_amount < decimal.Decimal(coupon_info.use_amount):
                    return self.client_reponse_json_error("Error", f"未达到使用门槛{int(decimal.Decimal(coupon_info.use_amount))}元")
                pay_amount = pay_amount - decimal.Decimal(coupon_info.discount_amount)
                discount_amount = coupon_info.discount_amount
            elif coupon_info.coupon_type == 1:
                pay_amount = pay_amount - decimal.Decimal(coupon_info.discount_amount)
                discount_amount = coupon_info.discount_amount
            else:
                pay_amount = round(pay_amount * (decimal.Decimal(coupon_info.discount_value) / 10), 2)
                discount_amount = buy_amount - pay_amount
            if pay_amount <= 0:
                return self.client_reponse_json_error("Error", "无法使用此优惠券")

            #优惠券
            user_coupon.pay_order_no = pay_order_no
            user_coupon.coupon_status = 1
            user_coupon.use_date = now_date
        #抽奖
        try:
            #支付订单
            pay_order = PayOrder()
            pay_order.open_id = user_info.open_id
            pay_order.pay_order_no = pay_order_no
            pay_order.order_name = "购买盲盒-" + machine_info.machine_name
            pay_order.order_desc = ""
            pay_order.order_status = 0
            pay_order.pay_amount = pay_amount
            pay_order.create_date = now_date
            pay_order.scene = 1

            #购买订单
            buy_order = BuyOrder()
            buy_order.act_id = act_id
            buy_order.user_id = user_id
            buy_order.pay_order_no = pay_order_no
            buy_order.machine_id = machine_info.id
            buy_order.machine_name = machine_info.machine_name
            buy_order.machine_price = machine_info.machine_price
            buy_order.buy_num = 1
            buy_order.buy_amount = buy_amount
            buy_order.pay_amount = pay_amount
            buy_order.discount_amount = discount_amount
            buy_order.order_status = 0
            buy_order.create_date = now_date

            #录入奖品
            prize_roster = PrizeRoster()
            prize_roster.act_id = act_id
            prize_roster.user_id = user_id
            prize_roster.user_nick = user_info.user_nick
            prize_roster.machine_id = machine_info.id
            prize_roster.machine_name = machine_info.machine_name
            prize_roster.machine_price = machine_info.machine_price
            prize_roster.prize_id = machine_prize.id
            prize_roster.prize_name = machine_prize.prize_name
            prize_roster.prize_price = machine_prize.prize_price
            prize_roster.prize_pic = machine_prize.prize_pic
            prize_roster.toy_cabinet_pic = machine_prize.toy_cabinet_pic
            prize_roster.prize_tag = machine_prize.prize_tag
            prize_roster.series_id = machine_info.series_id
            prize_roster.prize_status = 0
            prize_roster.prize_order_no = ""
            prize_roster.order_status = 0
            prize_roster.pay_status = 0
            prize_roster.group_id = group_id
            prize_roster.pay_order_no = pay_order_no
            prize_roster.goods_code = machine_prize.goods_code
            prize_roster.create_date = now_date
            prize_roster.modify_date = now_date
            if act_info.is_prize_retain == 1 and act_info.prize_retain_day > 0:
                prize_roster.expire_date = TimeHelper.add_days_by_format_time(day=act_info.prize_retain_day)
            else:
                prize_roster.expire_date = TimeHelper.add_years_by_format_time(years=100)

            db_transaction.begin_transaction()

            buy_order_model.add_entity(buy_order)
            pay_order_model.add_entity(pay_order)
            prize_roster_model.add_entity(prize_roster)
            surplus_queue.is_lock = 1
            surplus_queue.expire_date = TimeHelper.add_minutes_by_format_time(minute=90)
            surplus_queue_model.update_entity(surplus_queue, "is_lock,expire_date")
            if user_coupon:
                user_coupon_model.update_entity(user_coupon, "pay_order_no,coupon_status,use_date")
            db_transaction.commit_transaction()

            result = {}
            result["pay_order_no"] = pay_order_no
            return self.client_reponse_json_success(result)
        except Exception as ex:
            db_transaction.rollback_transaction()
            return self.logger_info.info("LotteryHandler:" + str(ex))


class LotteryResultHandler(ClientBaseHandler):
    """
    :description: 拆盒结果,用于支付成功后请求
    """
    @client_filter_check_head()
    @client_filter_check_params("user_id,pay_order_no")
    def get_async(self):
        """
        :description: 拆盒结果
        :param user_id:用户id
        :param pay_order_no:支付订单号
        :return: 购买的奖品
        :last_editors: HuangJianYi
        """
        user_id = int(self.get_request_param("user_id", 0))
        pay_order_no = self.get_request_param("pay_order_no")

        prize_roster_model = PrizeRosterModel(context=self)
        buy_order_model = BuyOrderModel(context=self)
        machine_prize_model = MachinePrizeModel(context=self)

        buy_order = buy_order_model.get_entity("pay_order_no=%s and user_id=%s", params=[pay_order_no, user_id])
        if not buy_order:
            return self.client_reponse_json_error("Error", "支付订单不存在")
        if buy_order.order_status == 0:
            return self.client_reponse_json_error("Error", "正在确认收款中")
        if buy_order.order_status == 2:
            return self.client_reponse_json_error("Error", "已退款")

        prize_roster = prize_roster_model.get_entity("pay_order_no=%s and user_id=%s", params=[pay_order_no, user_id])
        if not prize_roster:
            return self.client_reponse_json_error("Error", "没有购买商品")

        result = {}
        result["prize_name"] = prize_roster.prize_name
        result["prize_tag"] = prize_roster.prize_tag
        result["prize_pic"] = prize_roster.prize_pic
        result["prize_price"] = prize_roster.prize_price

        return self.client_reponse_json_success(result)


class UsePerspectiveCardHandler(ClientBaseHandler):
    """
    :description: 使用透视卡
    """
    @client_filter_check_head()
    @client_filter_check_params("user_id,login_token,serial_no,act_id,group_id")
    def get_async(self):
        """
        :description: 使用透视卡
        :param user_id:用户id
        :param login_token:登录令牌
        :param serial_no:小盒子编号
        :param act_id:活动id
        :param group_id:用户进入中盒自动分配的唯一标识
        :return: 奖品名称
        :last_editors: HuangJianYi
        """
        user_id = int(self.get_request_param("user_id", 0))
        login_token = self.get_request_param("login_token")
        serial_no = int(self.get_request_param("serial_no", 1))
        act_id = int(self.get_request_param("act_id", 1))
        group_id = self.get_request_param("group_id")

        user_info_model = UserInfoModel(context=self)
        machine_prize_model = MachinePrizeModel(context=self)
        user_prop_model = UserPropModel(context=self)

        #请求太频繁限制
        if self.check_post(f"Lottery_Post_{str(user_id)}_{str(group_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")
        user_info = user_info_model.get_entity("id=%s", params=[user_id])
        if not user_info or user_info.act_id != act_id:
            return self.client_reponse_json_error("Error", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if user_info.login_token != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录,当前无法操作")
        use_user_prop_total = user_prop_model.get_total("group_id=%s and prop_type=2 and is_use=1", params=[group_id])
        if use_user_prop_total > 0:
            return self.client_reponse_json_error("Error", "只能使用一张透视卡")
        if user_info.perspective_card_count <= 0:
            return self.client_reponse_json_error("Error", "透视卡数量不足")
        user_prop = user_prop_model.get_entity("act_id=%s and user_id=%s and prop_type=2 and is_use=0", params=[act_id, user_id])
        if not user_prop:
            return self.client_reponse_json_error("Error", "透视卡数量不足")
        redis_minmachinelist_key = f"min_machinelist_{str(user_id)}_{str(group_id)}"
        min_machine_list = self.redis_init().get(redis_minmachinelist_key)
        min_machine_list = json.loads(min_machine_list) if min_machine_list != None else {}
        prize_id = min_machine_list[str(serial_no)] if str(serial_no) in min_machine_list.keys() else 0
        if prize_id <= 0:
            return self.client_reponse_json_error("Error", "超时操作,请重新选择盒子")
        machine_prize = machine_prize_model.get_entity_by_id(prize_id)
        if not machine_prize:
            return self.client_reponse_json_error("Error", "对不起，奖品不存在")
        if machine_prize.is_release == 0 or machine_prize.is_del == 1:
            return self.client_reponse_json_error("Error", "对不起，奖品不存在")

        user_prop.is_use = 1
        user_prop.use_date = self.get_now_datetime()
        user_prop.group_id = group_id
        user_prop_dict = {}
        user_prop_dict["machine_id"] = machine_prize.machine_id
        user_prop_dict["prize_id"] = machine_prize.id
        user_prop.remark = user_prop_dict

        update_result = user_info_model.update_table("perspective_card_count=perspective_card_count-1", "id=%s and perspective_card_count>0", params=[user_id])
        if update_result == False:
            return self.client_reponse_json_error("Error", "透视卡数量不足")
        user_prop_model.update_entity(user_prop)

        result = {}
        result["prize_name"] = machine_prize.prize_name
        result["prize_tag"] = machine_prize.prize_tag
        result["prize_pic"] = machine_prize.prize_pic
        result["prize_price"] = machine_prize.prize_price

        task = TaskModelEx(context=self)
        task.add_task_count(user_info.act_id, TaskType.每日使用1张透视卡.value, user_info.id)
        task.add_task_count(user_info.act_id, TaskType.每周使用N张透视卡.value, user_info.id)

        return self.client_reponse_json_success(result)


class UseResetCardHandler(ClientBaseHandler):
    """
    :description: 使用重抽卡
    """
    @client_filter_check_head()
    @client_filter_check_params("user_id,login_token,pay_order_no,act_id,group_id,serial_no")
    def get_async(self):
        """
        :description: 使用重抽卡
        :param user_id:用户id
        :param login_token:登录令牌
        :param pay_order_no:支付单号
        :param act_id:活动id
        :param group_id:用户进入中盒自动分配的唯一标识
        :param serial_no:小盒子编号
        :return: 重抽后的奖品
        :last_editors: HuangJianYi
        """
        user_id = int(self.get_request_param("user_id", 0))
        login_token = self.get_request_param("login_token")
        pay_order_no = self.get_request_param("pay_order_no")
        act_id = int(self.get_request_param("act_id", 1))
        group_id = self.get_request_param("group_id")
        serial_no = int(self.get_request_param("serial_no", 1))

        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        user_info_model = UserInfoModel(db_transaction=db_transaction, context=self)
        user_prop_model = UserPropModel(db_transaction=db_transaction, context=self)
        surplus_queue_model = SurplusQueueModel(db_transaction=db_transaction, context=self)
        machine_prize_model = MachinePrizeModel(db_transaction=db_transaction, context=self)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction, context=self)

        #请求太频繁限制
        if self.check_post(f"Lottery_Post_{str(user_id)}_{str(group_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")
        user_info = user_info_model.get_entity("id=%s", params=[user_id])
        if not user_info or user_info.act_id != act_id:
            return self.client_reponse_json_error("Error", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if user_info.login_token != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录,当前无法操作")
        if user_info.redraw_card_count <= 0:
            return self.client_reponse_json_error("Error", "重抽卡数量不足")
        use_user_prop = user_prop_model.get_entity("prop_type=4 and group_id=%s", params=[group_id])
        if use_user_prop:
            return self.client_reponse_json_error("Error", "只能使用一张重抽卡")
        user_prop = user_prop_model.get_entity("act_id=%s and user_id=%s and prop_type=4 and is_use=0", params=[act_id, user_id])
        if not user_prop:
            return self.client_reponse_json_error("Error", "重抽卡数量不足")
        redis_minmachinelist_key = f"min_machinelist_{str(user_id)}_{str(group_id)}"
        min_machine_list = self.redis_init().get(redis_minmachinelist_key)
        min_machine_list = json.loads(min_machine_list) if min_machine_list != None else {}
        prize_id = min_machine_list[str(serial_no)] if str(serial_no) in min_machine_list.keys() else 0
        if prize_id <= 0:
            return self.client_reponse_json_error("Error", "无法使用重抽卡")
        old_surplus_queue = surplus_queue_model.get_entity("user_id=%s and group_id=%s and prize_id=%s", order_by="RAND()", params=[user_id, group_id, prize_id])
        if not old_surplus_queue:
            return self.client_reponse_json_error("Error", "无法使用重抽卡")
        machine_prize = MachinePrizeModel(context=self).get_entity_by_id(old_surplus_queue.prize_id)
        if not machine_prize:
            return self.client_reponse_json_error("Error", "对不起，奖品不存在")
        if machine_prize.is_release == 0 or machine_prize.is_del == 1:
            return self.client_reponse_json_error("Error", "对不起，奖品不存在")
        old_prize_roster = PrizeRosterModel(context=self).get_entity("pay_order_no=%s and user_id=%s", params=[pay_order_no, user_id])
        if not old_prize_roster:
            return self.client_reponse_json_error("Error", "奖品不存在，无法进行重抽")
        if old_prize_roster.pay_status != 1:
            return self.client_reponse_json_error("Error", "未付款,无法重抽")
        if old_prize_roster.prize_status != 0:
            return self.client_reponse_json_error("Error", "无法重抽，请联系客服处理")

        #录入奖品
        prize_roster = PrizeRoster()
        prize_roster.act_id = act_id
        prize_roster.user_id = user_id
        prize_roster.user_nick = old_prize_roster.user_nick
        prize_roster.series_id = old_prize_roster.series_id
        prize_roster.machine_id = old_prize_roster.machine_id
        prize_roster.machine_name = old_prize_roster.machine_name
        prize_roster.machine_price = old_prize_roster.machine_price
        prize_roster.prize_id = machine_prize.id
        prize_roster.prize_name = machine_prize.prize_name
        prize_roster.prize_price = machine_prize.prize_price
        prize_roster.prize_pic = machine_prize.prize_pic
        prize_roster.toy_cabinet_pic = machine_prize.toy_cabinet_pic
        prize_roster.prize_tag = machine_prize.prize_tag
        prize_roster.series_id = old_prize_roster.series_id
        prize_roster.pay_status = old_prize_roster.pay_status
        prize_roster.group_id = old_prize_roster.group_id
        prize_roster.prize_status = 0
        prize_roster.prize_order_no = ""
        prize_roster.pay_order_no = pay_order_no
        prize_roster.goods_code = machine_prize.goods_code
        prize_roster.create_date = self.get_now_datetime()
        prize_roster.modify_date = self.get_now_datetime()
        prize_roster.expire_date = old_prize_roster.expire_date

        #预扣队列
        surplus_queue = SurplusQueue()
        surplus_queue.act_id = old_surplus_queue.act_id
        surplus_queue.machine_id = old_surplus_queue.machine_id
        surplus_queue.group_id = old_surplus_queue.group_id
        surplus_queue.prize_id = old_surplus_queue.prize_id
        surplus_queue.user_id = user_id
        surplus_queue.withhold_value = 1
        surplus_queue.create_date = self.get_now_datetime()
        surplus_queue.expire_date = old_surplus_queue.expire_date

        user_prop.is_use = 1
        user_prop.use_date = self.get_now_datetime()
        user_prop.group_id = group_id
        user_prop_dict = {}
        user_prop_dict["pay_order_no"] = pay_order_no
        user_prop.remark = user_prop_dict

        try:
            db_transaction.begin_transaction()

            user_prop_model.update_entity(user_prop)
            user_info_model.update_table("redraw_card_count=redraw_card_count-1", "id=%s", params=[user_id])
            machine_prize_model.update_table("hand_out=hand_out-1,prize_total=prize_total+1", "id=%s", old_prize_roster.prize_id)
            machine_prize_model.update_table("hand_out=hand_out+1,prize_total=prize_total-1", "id=%s", prize_roster.prize_id)
            prize_roster_model.del_entity("id=%s", params=[old_prize_roster.id])
            prize_roster_model.add_entity(prize_roster)
            surplus_queue_model.add_entity(surplus_queue)
            surplus_queue_model.del_entity("id=%s", params=[old_surplus_queue.id])

            db_transaction.commit_transaction()
        except Exception as ex:
            db_transaction.rollback_transaction()
            self.logger_error.error("UseResetCardHandler:" + str(ex))

        result = {}
        result["prize_name"] = machine_prize.prize_name
        result["prize_tag"] = machine_prize.prize_tag
        result["prize_pic"] = machine_prize.prize_pic
        result["prize_price"] = machine_prize.prize_price

        task = TaskModelEx(context=self)
        task.add_task_count(prize_roster.act_id, TaskType.每日使用1张重抽卡.value, prize_roster.user_id)
        task.add_task_count(prize_roster.act_id, TaskType.每周使用N张重抽卡.value, prize_roster.user_id)

        return self.client_reponse_json_success(result)


class ShakeItHandler(ClientBaseHandler):
    """
    :description: 摇一摇
    """
    @client_filter_check_head()
    @client_filter_check_params("user_id,serial_no,group_id,login_token")
    def get_async(self):
        """
        :description: 摇一摇
        :param user_id:用户id
        :param serial_no:小盒子编号
        :param group_id:用户进入中盒自动分配的唯一标识
        :param login_token:登录令牌
        :param act_id:活动id
        :param is_use_prop:是否使用道具
        :return: dict
        :last_editors: HuangJianYi
        """
        user_id = int(self.get_request_param("user_id", 0))
        group_id = self.get_request_param("group_id")
        login_token = self.get_request_param("login_token")
        act_id = int(self.get_request_param("act_id", 1))
        is_use_prop = int(self.get_request_param("is_use_prop", 0))
        serial_no = int(self.get_request_param("serial_no", 0))

        user_info_model = UserInfoModel(context=self)
        user_prop_model = UserPropModel(context=self)
        act_info_model = ActInfoModel(context=self)
        machine_prize_model = MachinePrizeModel(context=self)
        surplus_queue_model = SurplusQueueModel(context=self)

        info = {}
        info["prize_name"] = ""
        info["tips"] = ""
        info["is_limit"] = 1

        user_prop = None
        #请求太频繁限制
        if self.check_post(f"Lottery_Post_{str(user_id)}_{str(group_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")
        user_info = user_info_model.get_entity("id=%s", params=[user_id])
        if not user_info or user_info.act_id != act_id:
            return self.client_reponse_json_error("Error", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if user_info.login_token != login_token:
            return self.client_reponse_json_error("ErrorToken", "对不起，已在另一台设备登录,当前无法操作")
        if is_use_prop == 1:
            if user_info.tips_card_count <= 0:
                return self.client_reponse_json_error("Error", "提示卡数量不足")
            user_prop = user_prop_model.get_entity("act_id=%s and user_id=%s and prop_type=3 and is_use=0", params=[act_id, user_id])
            if not user_prop:
                return self.client_reponse_json_error("Error", "提示卡数量不足")

        act_info_model = ActInfoModel(context=self)
        act_info = act_info_model.get_entity("id=%s and is_open=1 and is_del=0", params=[act_id])
        if not act_info:
            return self.client_reponse_json_error("NoAct", "对不起，活动不存在")

        redis_minmachinelist_key = f"min_machinelist_{str(user_id)}_{str(group_id)}"
        min_machine_list = self.redis_init().get(redis_minmachinelist_key)
        if min_machine_list != None:
            min_machine_list = json.loads(min_machine_list)
        else:
            min_machine_list = {}
        prize_id = min_machine_list[str(serial_no)] if str(serial_no) in min_machine_list.keys() else 0
        if prize_id <= 0:
            return self.client_reponse_json_error("Error", "超时操作,请重新选择盒子")
        machine_prize = machine_prize_model.get_entity_by_id(prize_id)
        if not machine_prize:
            return self.client_reponse_json_error("NoPrize", "对不起，奖品不存在")

        surplus_queue = surplus_queue_model.get_entity("act_id=%s and user_id=%s and group_id=%s and prize_id=%s", params=[act_id, user_id, group_id, prize_id])
        if not surplus_queue:
            return self.client_reponse_json_error("Error", "对不起，请重新选择盲盒")

        machine_info_model = MachineInfoModel(context=self)
        machine_info = machine_info_model.get_entity("id=%s and is_release=1 and is_del=0", params=machine_prize.machine_id)
        if not machine_info:
            return self.client_reponse_json_error("NoMachine", "对不起，盒子不存在")
        shakebox_tips_list = ast.literal_eval(act_info.shakebox_tips)
        if len(shakebox_tips_list) <= 0:
            info["tips"] = act_info.exceed_tips
            return self.client_reponse_json_success(info)
        incre_key = str(serial_no)
        redis_num_key = f"shakebox_tipsnumlist_{str(user_id)}_{str(group_id)}"
        shakebox_tipsnumlist = self.redis_init().get(redis_num_key)
        redis_useprop_key = f"shakebox_usepropcount_{str(user_id)}_{str(group_id)}"
        shakebox_useproplist = self.redis_init().get(redis_useprop_key)
        if shakebox_tipsnumlist != None:
            shakebox_tipsnumlist = json.loads(shakebox_tipsnumlist)
        else:
            shakebox_tipsnumlist = {}
        if shakebox_useproplist != None:
            shakebox_useproplist = json.loads(shakebox_useproplist)
        else:
            shakebox_useproplist = {}
        num = shakebox_tipsnumlist[incre_key] if incre_key in shakebox_tipsnumlist.keys() else 0
        useprop_num = shakebox_useproplist[incre_key] if incre_key in shakebox_useproplist.keys() else 0
        if is_use_prop == 0:
            if int(num) >= int(act_info.shakebox_tips_num):
                info["tips"] = act_info.exceed_tips
                return self.client_reponse_json_success(info)
        else:
            prize_count = machine_prize_model.get_total(f"machine_id={machine_prize.machine_id} and is_release=1 and is_del=0 and prize_tag=1")
            if int(num + useprop_num) >= int(prize_count - 2):
                return self.client_reponse_json_error("Error", "使用提示卡数量上限")
        redis_prizelist_key = f"shakebox_tipsprizelist_{str(user_id)}_{str(group_id)}"
        shakebox_tipsprizelist = self.redis_init().get(redis_prizelist_key)
        if shakebox_tipsprizelist != None:
            shakebox_tipsprizelist = json.loads(shakebox_tipsprizelist)
        else:
            shakebox_tipsprizelist = {}
        prize_list = shakebox_tipsprizelist[incre_key] if incre_key in shakebox_tipsprizelist.keys() else []
        cur_prize = None
        exclude_Prizeid_list = [prize_id]
        if len(prize_list) > 0:
            exclude_Prizeid_list.extend(prize_list)
        exclude_Prizeid_ids = ','.join(str(prize_id) for prize_id in exclude_Prizeid_list)
        condition = f"machine_id={machine_prize.machine_id} and id not in ({exclude_Prizeid_ids}) and is_release=1 and is_del=0 and prize_tag=1"
        cur_prize = machine_prize_model.get_entity(condition, order_by="RAND()")
        if cur_prize:
            info["tips"] = shakebox_tips_list[0].replace("XX", cur_prize.prize_name).replace("xx", cur_prize.prize_name)
            info["prize_name"] = cur_prize.prize_name
            info["is_limit"] = 0
            prize_list.append(cur_prize.id)
            if is_use_prop == 0:
                shakebox_tipsnumlist[incre_key] = int(num + 1)
                self.redis_init().set(redis_num_key, self.json_dumps(shakebox_tipsnumlist), ex=3600 * 1)
            else:
                if user_prop:
                    user_prop.is_use = 1
                    user_prop.use_date = self.get_now_datetime()
                    user_prop.group_id = group_id
                    user_prop.remark = info

                    update_result = user_info_model.update_table("tips_card_count=tips_card_count-1", "id=%s and tips_card_count>0", params=[user_id])
                    if update_result == False:
                        return self.client_reponse_json_error("Error", "提示卡数量不足")
                    shakebox_useproplist[incre_key] = int(useprop_num + 1)
                    self.redis_init().set(redis_useprop_key, self.json_dumps(shakebox_useproplist), ex=3600 * 1)
                    user_prop_model.update_entity(user_prop)

                    task = TaskModelEx(context=self)
                    task.add_task_count(user_prop.act_id, TaskType.每日使用1张提示卡.value, user_prop.user_id)
                    task.add_task_count(user_info.act_id, TaskType.每周使用N张提示卡.value, user_info.id)
            shakebox_tipsprizelist[incre_key] = prize_list
            self.redis_init().set(redis_prizelist_key, self.json_dumps(shakebox_tipsprizelist), ex=3600 * 1)
        else:
            info["tips"] = act_info.exceed_tips

        return self.client_reponse_json_success(info)


class ShakeItPrizeListHandler(ClientBaseHandler):
    """
    :description: 摇一摇奖品列表
    """
    @client_filter_check_head()
    @filter_check_params("serial_no,group_id,machine_id")
    def get_async(self):
        """
        :description: 晃一晃奖品列表
        :param prize_id:奖品id
        :param group_id:用户进入中盒自动分配的唯一标识
        :param machine_id:机台id
        :param serial_no:小盒子编号
        :return list
        :last_editors: HuangJianYi
        """
        user_id = int(self.get_request_param("user_id", 0))
        group_id = self.get_request_param("group_id")
        machine_id = int(self.get_request_param("machine_id", 0))
        serial_no = int(self.get_request_param("serial_no", 1))

        machine_info_model = MachineInfoModel(context=self)

        machine_info = machine_info_model.get_entity("id=%s and is_release=1 and is_del=0", params=machine_id)
        if not machine_info:
            return self.client_reponse_json_error("NoMachine", "对不起，盒子不存在")

        redis_minmachinelist_key = f"min_machinelist_{str(user_id)}_{str(group_id)}"
        min_machine_list = self.redis_init().get(redis_minmachinelist_key)
        min_machine_list = json.loads(min_machine_list) if min_machine_list != None else {}
        incre_key = str(serial_no)

        result_machine_prize_list_dict = []

        redis_prizelist_key = f"shakebox_tipsprizelist_{str(user_id)}_{str(group_id)}"
        shakebox_tipsprizelist = self.redis_init().get(redis_prizelist_key)
        if shakebox_tipsprizelist != None:
            shakebox_tipsprizelist = json.loads(shakebox_tipsprizelist)
        else:
            shakebox_tipsprizelist = {}
        exclude_prize_list = shakebox_tipsprizelist[incre_key] if incre_key in shakebox_tipsprizelist.keys() else []

        machine_prize_list_dict = MachinePrizeModel(context=self).get_dict_list("machine_id=%s and is_release=1 and is_del=0", order_by="prize_tag desc,sort_index desc", params=[machine_id])
        for i in range(len(machine_prize_list_dict)):

            exclude_prize_id = [prize_id for prize_id in exclude_prize_list if prize_id == machine_prize_list_dict[i]["id"]]

            result_machine_prize = {}
            result_machine_prize["prize_name"] = machine_prize_list_dict[i]["prize_name"]
            result_machine_prize["prize_pic"] = machine_prize_list_dict[i]["prize_pic"]
            result_machine_prize["prize_tag"] = machine_prize_list_dict[i]["prize_tag"]
            result_machine_prize["is_exclude"] = True if exclude_prize_id else False
            result_machine_prize_list_dict.append(result_machine_prize)

        return self.client_reponse_json_success(result_machine_prize_list_dict)


class RecoverHandler(ClientBaseHandler):
    """
    :description: 回收预分配的奖品
    """
    @client_filter_check_head()
    @filter_check_params("user_id,machine_id,login_token,act_id,group_id")
    def get_async(self):
        """
        :description: 回收预分配的奖品
        :param login_token:登录令牌
        :param act_id:活动id
        :param machine_id:机台id
        :param group_id:用户进入中盒自动分配的唯一标识
        :return reponse_json_success
        :last_editors: HuangJianYi
        """
        user_id = int(self.get_request_param("user_id", 0))
        login_token = self.get_request_param("login_token")
        act_id = int(self.get_request_param("act_id", 1))
        machine_id = int(self.get_request_param("machine_id", 0))
        group_id = self.get_request_param("group_id")

        user_info_model = UserInfoModel(context=self)
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        act_prize_model = MachinePrizeModel(db_transaction=db_transaction, context=self)
        surplus_queue_model = SurplusQueueModel(db_transaction=db_transaction, context=self)

        #请求太频繁限制
        if self.check_post(f"Recover_Post_{str(user_id)}_{str(group_id)}", 60) == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")
        #删除小盒子历史产生的数据
        self.delete_redis(user_id, group_id)
        surplus_queue_list = surplus_queue_model.get_list("user_id=%s and machine_id=%s and group_id=%s and is_lock=0", params=[user_id, machine_id, group_id])
        if len(surplus_queue_list) > 0:
            for surplus_queue in surplus_queue_list:
                try:
                    db_transaction.begin_transaction()
                    act_prize_model.update_table("surplus=surplus+1", "id=%s and (surplus+1)<=prize_total", params=[surplus_queue.prize_id])
                    surplus_queue_model.del_entity("id=%s", params=[surplus_queue.id])
                    db_transaction.commit_transaction()
                except Exception as ex:
                    db_transaction.rollback_transaction()
                    continue

        return self.client_reponse_json_success()

    def delete_redis(self, user_id, group_id):
        """
        :description: 从redis里面删除数据
        :param user_id: 用户id
        :param group_id: group_id
        :return {*}
        :last_editors: HuangJingCan
        """
        redis_num_key = f"shakebox_tipsnumlist_{str(user_id)}_{str(group_id)}"
        redis_prizelist_key = f"shakebox_tipsprizelist_{str(user_id)}_{str(group_id)}"
        redis_minmachinelist_key = f"min_machinelist_{str(user_id)}_{str(group_id)}"
        self.redis_init().delete(redis_num_key)
        self.redis_init().delete(redis_prizelist_key)
        self.redis_init().delete(redis_minmachinelist_key)