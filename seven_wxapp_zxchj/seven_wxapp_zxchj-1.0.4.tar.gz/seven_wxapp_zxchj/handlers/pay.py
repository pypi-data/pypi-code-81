# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-01-08 11:13:53
:LastEditTime: 2021-04-12 18:01:38
:LastEditors: HuangJingCan
@Description: 
"""
import decimal
import xmltodict

from seven_framework.web_tornado.base_handler.base_api_handler import *
from seven_wxapp.handlers.base.client_base import *
from seven_wxapp.handlers.base.behavior_base import *
from seven_wxapp.handlers.base.wechatpay_base import WeiXinPayRequest, WeiXinPayReponse, WeixinError, WeiXinRefundReponse

from seven_wxapp_zxchj.models.enum import *
from seven_wxapp_zxchj.models.ex_model import *
from seven_wxapp_zxchj.models.db_models.pay.pay_order_model import *
from seven_wxapp_zxchj.models.db_models.buy.buy_order_model import *
from seven_wxapp_zxchj.models.db_models.prize.prize_order_model import *
from seven_wxapp_zxchj.models.db_models.prize.prize_roster_model import *
from seven_wxapp_zxchj.models.db_models.machine.machine_prize_model import *
from seven_wxapp_zxchj.models.db_models.surplus.surplus_queue_model import *
from seven_wxapp_zxchj.models.db_models.user.user_info_model import *
from seven_wxapp_zxchj.models.db_models.refund.refund_order_model import *


class WechatCreateOrderHandler(ClientBaseHandler):
    """
    :description: 创建微信预订单
    """
    @client_filter_check_head()
    @client_filter_check_params("user_id,pay_order_no")
    def get_async(self):
        """
        :description: 创建微信预订单
        :param pay_order_no:支付单号
        :param scene:场景值1购买下单2邮费下单
        :param user_id:场景值1购买下单2邮费下单
        :return: 请求微信接口获取客户端需要的支付密钥数据
        :last_editors: HuangJianYi
        """
        user_id = int(self.get_request_param("user_id", 0))
        scene = int(self.get_request_param("scene", 1))
        pay_order_no = self.get_request_param("pay_order_no")

        #请求太频繁限制
        if self.check_post(f"CreateOrder_Post_{str(user_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起,请求太频繁")
        pay_order_model = PayOrderModel(context=self)
        pay_order = pay_order_model.get_entity("pay_order_no=%s", params=[pay_order_no])
        if not pay_order:
            return self.client_reponse_json_error("HintMessage", "抱歉!未查询到订单信息,请联系客服")
        if pay_order.order_status != 0:
            return self.client_reponse_json_error("HintMessage", "抱歉!未查询到订单信息,请联系客服")
        payconfig = config.get_value("wechat_pay")
        demain = payconfig["notify_demain"]
        notify_url = f"{demain}/client/buy_notify" if scene == 1 else f"{demain}/client/freight_notify"

        # 商品说明
        body = pay_order.order_name
        # 金额
        total_fee = pay_order.pay_amount
        # 支付端ip
        spbill_create_ip = self.get_real_ip()
        #交易结束时间,设置1小时
        time_expire = str(SevenHelper.get_now_int(1)) if scene == 1 else ""

        try:
            params = WeiXinPayRequest().create_order(pay_order_no, body, total_fee, spbill_create_ip, notify_url, pay_order.open_id, time_expire)
            if type(params) == WeixinError:
                return self.client_reponse_json_error("Fail", str(params))
            # self.logger_info.info('微信小程序支付返回前端参数:' + str(params))
            return self.client_reponse_json_success(params)
        except Exception as ex:
            self.logger_error.error("【创建微信订单异常】" + str(ex))
            return self.client_reponse_json_error("Fail", "请重新支付")

        return self.client_reponse_json_success()


class WechatBuyNotifyHandler(BaseApiHandler):
    """
    :description: 微信购买下单异步通知
    """
    def post_async(self):
        """
        :description: 微信购买下单异步通知
        :return: 
        :last_editors: HuangJianYi
        """
        self.logger_info.info('微信购买下单异步通知' + str(self.request.body.decode('utf-8')))
        params = self.request.body.decode('utf-8')
        try:
            WeiXinPayReponse(params)  # 判断是否xml数据格式
        except Exception as ex:
            self.logger_error.error(str(ex) + "【微信购买下单异步通知参数解析异常】" + str(params))
            return self.write("False")
        wxpay_params = params  # xml 字符串
        wxpay = WeiXinPayReponse(wxpay_params)  # 创建对象
        wxpay_dict = wxpay.get_data()
        return_code = wxpay_dict.get('return_code')
        result_code = wxpay_dict.get('result_code')
        if return_code == wxpay.FAIL:
            return self.write(wxpay.get_return_data(wxpay_dict.get('return_msg'), False))
        if result_code == wxpay.FAIL:
            return self.write(wxpay.get_return_data(wxpay_dict.get('err_code_des'), False))
        if wxpay.check_sign() != True:  # 校验签名,成功则继续后续操作
            self.logger_error.error('签名验证失败')
            return self.write(wxpay.get_return_data("签名验证失败", False))
        total_fee = wxpay_dict.get('total_fee')
        out_trade_no = wxpay_dict.get('out_trade_no')
        transaction_id = wxpay_dict.get('transaction_id')
        time_string = wxpay_dict.get('time_end')
        # 时间格式转换
        pay_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time_string, "%Y%m%d%H%M%S"))
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        pay_order_model = PayOrderModel(db_transaction=db_transaction, context=self)
        buy_order_model = BuyOrderModel(db_transaction=db_transaction, context=self)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction, context=self)
        machine_prize_model = MachinePrizeModel(db_transaction=db_transaction, context=self)
        surplus_queue_model = SurplusQueueModel(db_transaction=db_transaction, context=self)
        user_info_model = UserInfoModel(db_transaction=db_transaction, context=self)
        pay_order = pay_order_model.get_entity("pay_order_no=%s", params=[out_trade_no])
        if not pay_order:
            return self.write(wxpay.get_return_data("未查询到订单信息", False))
        prize_roster = prize_roster_model.get_entity("pay_order_no=%s", params=[out_trade_no])
        if not prize_roster:
            return self.write(wxpay.get_return_data("未查询到订单信息", False))
        # 判断金额是否匹配
        if float(decimal.Decimal(pay_order.pay_amount) * 100) != float(total_fee):
            self.logger_error.error(f"微信支付订单[{out_trade_no}] 金额不匹配疑似刷单.数据库金额:{str(pay_order.pay_amount)} 平台回调金额:{str(total_fee)};")
            return self.write(wxpay.get_return_data("异常请求", False))

        if pay_order.order_status == 0 or pay_order.order_status == 2:
            try:
                pay_order.wx_order_no = transaction_id
                pay_order.order_status = 1
                pay_order.pay_date = pay_time
                surplus_queue = surplus_queue_model.get_entity("group_id=%s and prize_id=%s", params=[prize_roster.group_id, prize_roster.prize_id])

                db_transaction.begin_transaction()
                pay_order_model.update_entity(pay_order, "wx_order_no,order_status,pay_date")
                buy_order_model.update_table("wx_order_no=%s,order_status=1,pay_date=%s", "pay_order_no=%s", params=[transaction_id, pay_time, out_trade_no])
                prize_roster_model.update_table("pay_status=1", "pay_order_no=%s", params=[out_trade_no])
                #库存处理
                machine_prize_model.update_table("hand_out=hand_out+1,prize_total=prize_total-1", "id=%s", prize_roster.prize_id)
                user_info_model.update_table(f"pay_num=pay_num+1,pay_price=pay_price+{pay_order.pay_amount},removed_count=removed_count+1", "id=%s", params=[prize_roster.user_id])
                if surplus_queue:
                    surplus_queue_model.del_entity("id=%s", params=[surplus_queue.id])
                db_transaction.commit_transaction()

            except Exception as ex:
                db_transaction.rollback_transaction()
                self.logger_error.error("微信购买下单异步通知:数据处理异常:" + str(ex))
                return self.write(wxpay.get_return_data("数据处理异常", False))

            task = TaskModelEx(context=self)
            task.add_task_count(prize_roster.act_id, TaskType.每日参与1次抽盒.value, prize_roster.user_id)
            task.add_task_count(prize_roster.act_id, TaskType.每日参与抽盒N次.value, prize_roster.user_id)
            task.add_task_count(prize_roster.act_id, TaskType.每周参与抽盒N次.value, prize_roster.user_id)

            behavior_model = BehaviorModel(context=self)
            behavior_model.report_behavior_log(prize_roster.act_id, prize_roster.user_id, 'TotalLotteryUserCount', 1)
            behavior_model.report_behavior_log(prize_roster.act_id, prize_roster.user_id, 'TotalLotteryCount', 1)

            behavior_model.report_behavior_log(prize_roster.act_id, prize_roster.user_id, 'TotalPayMoneyCount', pay_order.pay_amount)
            behavior_model.report_behavior_log(prize_roster.act_id, prize_roster.user_id, 'TotalBuyCount', 1)

            behavior_model.report_behavior_log(prize_roster.act_id, prize_roster.user_id, f'BuyUserCount_{prize_roster.machine_id}', 1)
            behavior_model.report_behavior_log(prize_roster.act_id, prize_roster.user_id, f'BuyCount_{prize_roster.machine_id}', 1)
            behavior_model.report_behavior_log(prize_roster.act_id, prize_roster.user_id, f'PayMoneyCount_{prize_roster.machine_id}', pay_order.pay_amount)

            behavior_model.report_behavior_log(prize_roster.act_id, prize_roster.user_id, f'LotteryUserCount_{prize_roster.machine_id}', 1)
            behavior_model.report_behavior_log(prize_roster.act_id, prize_roster.user_id, f'LotteryCount_{prize_roster.machine_id}', 1)
            behavior_model.report_behavior_log(prize_roster.act_id, prize_roster.user_id, f'LotteryAddUserCount_{prize_roster.machine_id}', 1)

        # 返回微信数据
        return self.write(wxpay.get_return_data("SUCCESS", True))


class WechatFreightNotifyHandler(BaseApiHandler):
    """
    :description: 微信邮费下单异步通知
    """
    def post_async(self):
        """
        :description: 微信邮费下单异步通知
        :return: 
        :last_editors: HuangJianYi
        """
        self.logger_info.info('微信邮费下单异步通知' + str(self.request.body.decode('utf-8')))
        params = self.request.body.decode('utf-8')
        try:
            WeiXinPayReponse(params)  # 判断是否xml数据格式
        except Exception as ex:
            self.logger_error.error(str(ex) + "【微信邮费下单异步通知参数解析异常】")
            return self.write("False")
        wxpay_params = params  # xml 字符串
        wxpay = WeiXinPayReponse(wxpay_params)  # 创建对象
        wxpay_dict = wxpay.get_data()
        return_code = wxpay_dict.get('return_code')
        result_code = wxpay_dict.get('result_code')
        if return_code == wxpay.FAIL:
            return self.write(wxpay.get_return_data(wxpay_dict.get('return_msg'), False))
        if result_code == wxpay.FAIL:
            return self.write(wxpay.get_return_data(wxpay_dict.get('err_code_des'), False))
        if wxpay.check_sign() != True:  # 校验签名,成功则继续后续操作
            self.logger_error.error('签名验证失败')
            return self.write(wxpay.get_return_data("签名验证失败", False))
        total_fee = wxpay_dict.get('total_fee')
        out_trade_no = wxpay_dict.get('out_trade_no')
        transaction_id = wxpay_dict.get('transaction_id')
        time_string = wxpay_dict.get('time_end')
        # 时间格式转换
        pay_time = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time_string, "%Y%m%d%H%M%S"))
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        pay_order_model = PayOrderModel(db_transaction=db_transaction, context=self)
        prize_order_model = PrizeOrderModel(db_transaction=db_transaction, context=self)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction, context=self)
        pay_order = pay_order_model.get_entity("pay_order_no=%s", params=[out_trade_no])
        if not pay_order:
            return self.write(wxpay.get_return_data("未查询到订单信息", False))
        prize_order = prize_order_model.get_entity("freight_pay_order_no=%s", params=[out_trade_no])
        if not prize_order:
            return self.write(wxpay.get_return_data("未查询到订单信息", False))
        # 判断金额是否匹配
        if float(decimal.Decimal(pay_order.pay_amount) * 100) != float(total_fee):
            self.logger_error.error(f"微信支付订单[{out_trade_no}] 金额不匹配疑似刷单.数据库金额:{str(pay_order.pay_amount)} 平台回调金额:{str(total_fee)};")
            return self.write(wxpay.get_return_data("异常请求", False))
        if pay_order.order_status == 0 or pay_order.order_status == 2:
            try:
                pay_order.wx_order_no = transaction_id
                pay_order.order_status = 1
                pay_order.pay_date = pay_time
                db_transaction.begin_transaction()
                pay_order_model.update_entity(pay_order, "wx_order_no,order_status,pay_date")
                prize_order_model.update_table("order_status=1", "freight_pay_order_no=%s", params=[out_trade_no])
                prize_roster_model.update_table("prize_status=1", "prize_order_no=%s", params=[prize_order.order_no])
                db_transaction.commit_transaction()

            except Exception as ex:
                db_transaction.rollback_transaction()
                self.logger_error.error("微信邮费下单异步通知:数据处理异常:" + str(ex))
                return self.write(wxpay.get_return_data("数据处理异常", False))
            behavior_model = BehaviorModel(context=self)
            behavior_model.report_behavior_log(prize_order.act_id, prize_order.user_id, 'TotalFreightMoneyCount', pay_order.pay_amount)
            # 返回微信数据
        return self.write(wxpay.get_return_data("SUCCESS", True))


class WechatRefundNotifyHandler(BaseApiHandler):
    """
    :description: 微信退款异步通知
    """
    def post_async(self):
        # self.logger_info.info('微信退款异步通知' + str(self.request.body.decode('utf-8')))
        params = self.request.body.decode('utf-8')
        try:
            WeiXinRefundReponse(params)  # 判断是否xml数据格式
        except Exception as ex:
            self.logger_error.error(str(ex) + "【微信退款异步通知参数解析异常】" + str(params))
            return self.write("False")
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_wxapp"))
        pay_order_model = PayOrderModel(db_transaction=db_transaction, context=self)
        refund_order_model = RefundOrderModel(db_transaction=db_transaction, context=self)
        buy_order_model = BuyOrderModel(db_transaction=db_transaction, context=self)
        prize_roster_model = PrizeRosterModel(db_transaction=db_transaction, context=self)
        prize_order_model = PrizeOrderModel(db_transaction=db_transaction, context=self)
        wxrefund = WeiXinRefundReponse(params)  # 创建对象
        # 解密
        wxrefund_dict = wxrefund.get_data()
        if wxrefund_dict["xml"]["return_code"] == "SUCCESS":
            dict_req_info = wxrefund.decode_req_info(wxrefund_dict["xml"]["req_info"])
            try:
                db_transaction.begin_transaction()
                # 判断是否成功
                if dict_req_info["root"]["refund_status"] == "SUCCESS":
                    self.logger_info.info(f'pay_order_no:{str(dict_req_info["root"]["out_trade_no"])},微信退款异步通知:' + str(dict_req_info["root"]))
                    # 退款成功(相关表处理)
                    # 退款表
                    refund_order_model.update_table(update_sql="refund_status = 3,wx_refund_no = %s,refund_date = %s", where="refund_no = %s", params=[dict_req_info["root"]["refund_id"], dict_req_info["root"]["success_time"], dict_req_info["root"]["out_refund_no"]])
                    # buy_order
                    buy_order_model.update_table(update_sql="order_status=2,refund_date=%s", where="pay_order_no=%s", params=[dict_req_info["root"]["success_time"], dict_req_info["root"]["out_trade_no"]])
                    # pay_order
                    pay_order_model.update_table(update_sql="order_status=20,refund_amount=%s", where="pay_order_no=%s", params=[int(dict_req_info["root"]["settlement_refund_fee"]) / 100, dict_req_info["root"]["out_trade_no"]])
                    # prize_roster
                    prize_roster_model.update_table(update_sql="prize_status=4", where="pay_order_no=%s", params=dict_req_info["root"]["out_trade_no"])
                    # prize_order(需验证是否只有那个退款奖品)
                    prize_roster = PrizeRosterModel(context=self).get_entity(where="pay_order_no=%s", params=dict_req_info["root"]["out_trade_no"])
                    if prize_roster and prize_roster.prize_order_no != "":
                        prize_count = PrizeRosterModel(context=self).get_total(where="prize_order_no=%s and prize_status!=4", params=prize_roster.prize_order_no)
                        if prize_count == 0:
                            prize_order_model.update_table(update_sql="order_status=4", where="order_no=%s", params=prize_roster.prize_order_no)
                else:
                    # 退款失败(只更新退款表)
                    refund_order_model.update_table(update_sql="refund_status=4", where="refund_no=%s", params=dict_req_info["root"]["refund_id"])
                db_transaction.commit_transaction()
            except Exception as ex:
                db_transaction.rollback_transaction()
                self.logger_error.error("微信退款异步通知:数据处理异常:" + str(ex))
                return self.write(wxrefund.get_return_data("数据处理异常", False))

        return self.write(wxrefund.get_return_data("SUCCESS", True))