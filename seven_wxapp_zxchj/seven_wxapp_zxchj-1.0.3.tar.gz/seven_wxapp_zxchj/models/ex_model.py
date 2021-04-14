# -*- coding: utf-8 -*-
"""
@Author: WangQiang
@Date: 2021-01-15 18:12:24
:LastEditTime: 2021-04-13 16:00:42
:LastEditors: HuangJingCan
@Description: 
"""
import ast

from seven_wxapp.handlers.base.seven_helper import *

from seven_wxapp_zxchj.models.enum import *
from seven_wxapp_zxchj.models.db_models.coin.coin_record_model import *
from seven_wxapp_zxchj.models.db_models.user.user_info_model import *
from seven_wxapp_zxchj.models.db_models.coin.coin_exchange_model import *
from seven_wxapp_zxchj.models.db_models.exchange.exchange_record_model import *
from seven_wxapp_zxchj.models.db_models.exchange.exchange_order_model import *
from seven_wxapp_zxchj.models.db_models.task.task_info_model import *
from seven_wxapp_zxchj.models.db_models.task.task_count_model import *


class CoinRecordModelEx:
    """
    :description: T币记录操作
    """
    def __init__(self, context=None):
        self.context = context

    def add_coin_record(self, act_id, user_info, title, change_type, transaction_type, coin_count, db_transaction=""):
        """
        :description: 添加T币记录
        :param act_id：活动id
        :param user_info：用户信息
        :param title：标题
        :param change_type：变动类型:1手动2每日任务3每周任务4兑换
        :param transaction_type：交易类型:1增加2减少
        :param coin_count：T币数量
        :param operation_user_id：操作用户id
        :return: dict
        :last_editors: WangQiang
        """
        coin_record_model = CoinRecordModel(context=self)
        if db_transaction:
            coin_record_model = CoinRecordModel(db_transaction=db_transaction, context=self)
        coin_record = CoinRecord()
        coin_record.act_id = act_id
        coin_record.user_id = user_info.id
        coin_record.title = title
        coin_record.change_type = change_type
        coin_record.transaction_type = transaction_type
        coin_record.coin_count = coin_count
        coin_record.history_coin_count = user_info.surplus_coin
        #coin_record.operation_user_id = user_info.id
        coin_record.create_date = TimeHelper.add_hours_by_format_time(hour=0)
        coin_record.id = coin_record_model.add_entity(coin_record)
        return coin_record


class ExchangeRecordModelEx:
    """
    :description: 兑换操作
    """
    def __init__(self, context=None):
        self.context = context

    def add_exchange_record(self, act_id, user_info, title, goods_type, coin_count, db_transaction=""):
        """
        :description: 添加T币记录
        :param act_id：活动id
        :param user_info：用户信息
        :param title：标题
        :param goods_type:商品类型(1实物2透视卡3提示卡4重抽卡5优惠券)
        :param coin_count：T币数量
        :param db_transaction：事务DB
        :return: dict
        :last_editors: WangQiang
        """
        exchange_record_model = ExchangeRecordModel(context=self)
        if db_transaction:
            exchange_record_model = ExchangeRecordModel(db_transaction=db_transaction, context=self)
        exchange_record = ExchangeRecord()
        exchange_record.act_id = act_id
        exchange_record.user_id = user_info.id
        exchange_record.title = title
        exchange_record.num = 1
        exchange_record.goods_type = goods_type
        exchange_record.use_coin_count = coin_count
        exchange_record.history_coin_count = user_info.surplus_coin
        #coin_record.operation_user_id = user_info.id
        exchange_record.create_date = TimeHelper.add_hours_by_format_time(hour=0)
        exchange_record.id = exchange_record_model.add_entity(exchange_record)
        return exchange_record


class TaskModelEx:
    """
    :description: 任务公用处理
    """
    def __init__(self, context=None):
        self.context = context

    def add_task_count(self, act_id, task_type, user_id):
        """
        :description: 增加任务计数
        :param act_id：活动id
        :param task_type：任务类型（参考枚举）
        :param user_id：用户id
        :return: dict
        :last_editors: WangQiang
        """
        task_count_model = TaskCountModel(context=self)
        task_info_model = TaskInfoModel(context=self)
        now_datetime = TimeHelper.add_hours_by_format_time(hour=0)
        #错误信息
        error_msg = ""
        #当前时间整形
        now_day = SevenHelper.get_now_day_int()
        #获取任务信息
        task_info = task_info_model.get_entity("act_id=%s and is_release=1 and task_type=%s", params=[act_id, task_type])
        if not task_info:
            error_msg = "对不起，任务未开启"
            return error_msg
        #获取任务计数
        task_count_list = task_count_model.get_list("act_id=%s and user_id=%s and task_type=%s", params=[act_id, user_id, task_type])
        task_config = ast.literal_eval(task_info.task_config)
        add_count = 1
        if task_info.task_type == TaskType.每周参与抽盒N次.value:  #每周参与抽盒任务
            add_count = len(task_config)
        for i in range(add_count):
            task_count = None
            if add_count > 1:
                current_task_count_list = [task_count for task_count in task_count_list if task_count.task_sub_type == task_config[i]["id"]]
                if len(current_task_count_list) > 0:
                    task_count = current_task_count_list[0]
            else:
                if len(task_count_list) > 0:
                    task_count = task_count_list[0]
            #添加计数
            if not task_count:
                task_count = TaskCount()
                task_count.act_id = act_id
                task_count.user_id = user_id
                task_count.task_type = task_type
                task_count.complete_count_value = 0
                task_count.count_value = 1
                task_count.last_day = now_day
                task_count.last_date = now_datetime
                if add_count > 1:
                    task_count.task_sub_type = task_config[i]["id"]
                task_count_model.add_entity(task_count)
            else:
                if task_info.complete_type == 1 and task_count.last_day != now_day:  #重置每日任务
                    task_count.complete_count_value = 0
                    task_count.count_value = 0
                elif task_info.complete_type == 2 and TimeHelper.is_this_week(task_count.last_date) == False:  #重置每周任务
                    task_count.complete_count_value = 0
                    task_count.count_value = 0

                task_count.count_value += 1
                task_count.last_day = now_day
                task_count.last_date = now_datetime
                if add_count > 1:
                    task_count.task_sub_type = task_config[i]["id"]
                task_count_model.update_entity(task_count, "count_value,last_day,last_date,task_sub_type,complete_count_value")

        return error_msg
