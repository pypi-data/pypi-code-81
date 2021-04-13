# -*- coding: utf-8 -*-
"""
:Author: HuangJingCan
:Date: 2020-04-16 14:38:22
:LastEditTime: 2021-04-13 15:59:16
:LastEditors: HuangJingCan
:Description: 在线抽盒机基础路由
"""
# 框架引用
from seven_wxapp_zxchj.handlers import *
from seven_wxapp_zxchj.handlers.base import *


def seven_wxapp_zxchj_route():
    return [
        (r"/", core_base.IndexHandler),
        (r"/client/base_info", core_base.CoreBaseHandler),
        (r"/client/machine_list", machine.MachineInfoListHandler),
        (r"/client/prize_list", machine.MachinePrizeListHandler),
        (r"/client/lottery", lottery.LotteryHandler),
        (r"/client/shakeit", lottery.ShakeItHandler),
        (r"/client/recover", lottery.RecoverHandler),
        (r"/client/use_reset_card", lottery.UseResetCardHandler),
        (r"/client/lottery_result", lottery.LotteryResultHandler),
        (r"/client/shakeit_prize_list", lottery.ShakeItPrizeListHandler),
        (r"/client/use_perspective_card", lottery.UsePerspectiveCardHandler),
        (r"/client/lottery_machineprize_list", lottery.MachinePrizeListHandler),
        (r"/client/get_horseracelamp_List", lottery.GetHorseRaceLampListHandler),
        (r"/client/wechat_pay", pay.WechatCreateOrderHandler),
        (r"/client/buy_notify", pay.WechatBuyNotifyHandler),
        (r"/client/refund_notify", pay.WechatRefundNotifyHandler),
        (r"/client/freight_notify", pay.WechatFreightNotifyHandler),
        (r"/client/login", user.LoginHandler),
        (r"/client/update_user", user.UpdateUserHandler),
        (r"/client/update_user_phone", user.UpdateUserPhoneHandler),
        (r"/client/receiving_address_list", user.ReceivingAddressListHandler),
        (r"/client/save_receiving_address", user.SaveReceivingAddressHandler),
        (r"/client/home_page", home_page.HomePageHandler),
        (r"/client/ip_series_list", home_page.IpSeriesListHandler),
        (r"/client/carousel_map_list", home_page.CarouselMapListHandler),
        (r"/client/home_page_config_list", home_page.HomePageConfigListHandler),
        (r"/client/copywriting_config_list", home_page.CopywritingConfigListHandler),
        (r"/client/home_page_config_details", home_page.HomePageConfigDetailsHandler),
        (r"/client/task_list", task.TaskListHandler),
        (r"/client/user_sign", task.UserSignHandler),
        (r"/client/invite_user", task.InviteUserHandler),
        (r"/client/receive_reward", task.ReceiveRewardHandler),
        (r"/client/invite_report", task.InviteReportHandler),
        (r"/client/logistics", prize_order.LogisticsHandler),
        (r"/client/cancel_order", prize_order.CancelOrderHandler),
        (r"/client/confirm_receipt", prize_order.ConfirmReceiptHandler),
        (r"/client/prize_order_list", prize_order.PrizeOrderListHandler),
        (r"/client/prize_roster_list", prize_order.PrizeRosterListHandler),
        (r"/client/create_prize_order", prize_order.CreatePrizeOrderHandler),
        (r"/client/complete_order_pay", prize_order.CompleteOrderPayHandler),
        (r"/client/cancel_buy_order", buy_order.CancelBuyOrderHandler),
        (r"/client/get_waitpay_order", buy_order.GetWaitPayOrderHandler),
        (r"/client/get_coupon_info", coupon.GetCouponInfo),
        (r"/client/get_coupon_list", coupon.GetCouponList),
        (r"/client/draw_coupon", coupon.DrawCouponHandler),
        (r"/client/get_usercoupon_list", coupon.GetUserCouponListHandler),
        (r"/client/get_enablecoupon_list", coupon.GetEnableCouponListHandler),
        (r"/client/coin_record_list", coin.CoinRecordListHandler),
        (r"/client/new_coin_exchange", coin.NewCoinExchangeHandler),
        (r"/client/new_coin_exchange_list", coin.NewCoinExchangeListHandler),
        (r"/client/exchange_order_list", exchange_order.ExchangeOrderListHandler),
    ]