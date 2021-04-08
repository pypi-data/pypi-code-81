# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-01-05 17:16:17
:LastEditTime: 2021-03-29 15:07:51
:LastEditors: HuangJianYi
@Description: 
"""
import json
from handlers.base.erp_base import *
from models.enum.enum import *
from models.db_models.prize.prize_order_model import *
from models.db_models.prize.prize_roster_model import *
from models.db_models.machine.machine_prize_model import *


class DeliverHandler(ErpBaseHandler):
    """
    :description: 发货单接口
    :last_editors: XiaoYongChun
    """
    def post_async(self):
        if not self.check_erp_sign():
            self.response_error_msg(333, "签名错误")
            return

        out_order_id = self.get_erp_params("out_order_id")
        logi_no = self.get_erp_params("logi_no")
        logi_name = self.get_erp_params("logi_name")
        t_begin = self.get_erp_params("t_begin")
        prize_order_model = PrizeOrderModel()
        prize_roster_model = PrizeRosterModel()
        prize_order_entity = prize_order_model.get_entity("order_no=%s", params=out_order_id)
        if not prize_order_entity:
            self.response_error_msg(334, "不存在的订单!")
            return

        prize_order_entity.deliver_date = t_begin
        prize_order_entity.express_no = logi_no
        prize_order_entity.express_company = self.get_express_company(logi_name)
        prize_order_entity.order_status = 2

        try:
            prize_order_model.update_entity(prize_order_entity)
            prize_roster_model.update_table("prize_status=2", "prize_order_no=%s and prize_status=1", params=[out_order_id])
        except:
            error_msg = f"erp发货状态更新时产生异常[{out_order_id}]异常,错误信息[{traceback.print_exc()}]"
            self.logger_error.error(error_msg)
            self.response_error_msg(335, "发货信息记录失败!")
            return

        response_data = {}
        response_data["code"] = 200
        response_data["msg"] = "success"
        response_data["result"] = {"out_order_id": out_order_id, "action_result": True, "action_msg": "处理成功"}

        self.http_reponse(JsonHelper.json_dumps(response_data))

    def get_express_company(self, express_company):
        """
        :param express_company：物流公司（拼音）
        :return list
        :last_editors: XiaoYongChun
        """
        express_company_name = ""
        if express_company:
            for enum in LogisticsType:
                if enum.value == express_company:
                    express_company_name = enum.name
                    break
        return express_company_name


class ProductListHandler(ErpBaseHandler):
    """
    :description: 商品列表接口
    :last_editors: XiaoYongChun
    """
    def post_async(self):
        if not self.check_erp_sign():
            self.response_error_msg(333, "签名错误")
            return

        page_no = self.get_erp_params("page_no")
        page_size = self.get_erp_params("page_size")
        start_time = self.get_erp_params("start_time")
        end_time = self.get_erp_params("end_time")
        product_bn = self.get_erp_params("product_bn")

        condition = "1=1"
        order = "id asc"
        param_list = []

        if start_time:
            condition += " and modify_date>=%s"
            param_list.append(start_time)
        if end_time:
            condition += " and modify_date<=%s"
            param_list.append(end_time)
        if product_bn:
            condition += " and goods_code=%s"
            param_list.append(product_bn)

        machine_prize_list, total = MachinePrizeModel().get_dict_page_list("goods_code,prize_name,prize_price", page_no - 1, page_size, condition, "", order, param_list)

        if not machine_prize_list:
            self.response_error_msg(336, "没有可获取的商品列表")
            return

        response_data = {}
        response_data["code"] = 200
        response_data["msg"] = "success"
        response_data["result"] = {}

        response_data["result"]["page_no"] = page_no
        response_data["result"]["page_size"] = page_size
        response_data["result"]["count"] = total
        response_data["result"]["items"] = []

        for machine_prize_item in machine_prize_list:

            response_data["result"]["items"].append({"product_bn": machine_prize_item["goods_code"], "product_name": machine_prize_item["prize_name"], "price": machine_prize_item["prize_price"]})

        self.http_reponse(JsonHelper.json_dumps(response_data))


class StockHandler(ErpBaseHandler):
    """
    :description: 更新库存接口
    :last_editors: XiaoYongChun
    """
    def post_async(self):

        if not self.check_erp_sign():
            return self.response_error_msg(333, "签名错误")
        body_json = self.request.body
        if str(body_json, "utf-8") != "":
            param_info = json.loads(body_json)
        if not param_info:
            return self.response_error_msg(337, "数据格式错误")
        machine_prize_model = MachinePrizeModel()
        response_data = {}
        response_data["code"] = 200
        response_data["msg"] = "success"
        response_data["result"] = []
        for param_info_item in param_info:
            product_bn = param_info_item["product_bn"]
            stock = param_info_item["stock"]

            machine_prize_entity = machine_prize_model.get_entity(where="goods_code=%s", params=[product_bn])
            if not machine_prize_entity:
                stock_data = {}
                stock_data["product_bn"] = product_bn
                stock_data["action_result"] = False
                stock_data["action_msg"] = "没有找到此商品"
                response_data["result"].append(stock_data)
                continue
            try:
                machine_prize_entity.surplus = stock
                machine_prize_entity.prize_total = stock
                result = machine_prize_model.update_entity(machine_prize_entity)
                if result == False:
                    stock_data = {}
                    stock_data["product_bn"] = product_bn
                    stock_data["action_result"] = False
                    stock_data["action_msg"] = "更新商品库存失败"
                    response_data["result"].append(stock_data)
                    continue
            except:
                error_msg = f"更新商品库存时产生异常[product_bn]异常,错误信息[{traceback.print_exc()}]"
                self.logger_error.error(error_msg)
                stock_data = {}
                stock_data["product_bn"] = product_bn
                stock_data["action_result"] = False
                stock_data["action_msg"] = "更新商品库存时产生异常"
                response_data["result"].append(stock_data)
                continue

            stock_data = {}
            stock_data["product_bn"] = product_bn
            stock_data["action_result"] = True
            stock_data["action_msg"] = "处理成功"
            response_data["result"].append(stock_data)

        self.http_reponse(JsonHelper.json_dumps(response_data))
