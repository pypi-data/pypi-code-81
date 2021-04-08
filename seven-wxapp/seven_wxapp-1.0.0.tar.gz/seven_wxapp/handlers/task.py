# -*- coding: utf-8 -*-
"""
@Author: WangQiang
@Date: 2021-01-11 14:32:42
:LastEditTime: 2021-02-02 16:52:23
:LastEditors: HuangJianYi
@Description: 
"""

from handlers.base.core_base import *
from handlers.base.behavior_base import *
from handlers.coin import *
import datetime

from models.enum.enum import *

from models.db_models.task.task_info_model import *
from models.db_models.task.task_count_model import *
from models.db_models.user.user_info_model import *
from models.db_models.coin.coin_record_model import *
from models.db_models.invite.invite_log_model import *


class TaskListHandler(ClientBaseHandler):
    """
    :description: 任务列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    @client_filter_check_act_open()
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))

        task_info_model = TaskInfoModel()
        task_count_model = TaskCountModel()
        user_info_model = UserInfoModel()
        invite_log_model = InviteLogModel()

        user_info = user_info_model.get_entity_by_id(user_id)
        if not user_info:
            return self.client_reponse_json_error("NoUser", "对不起，用户不存在")
        #当前时间整形
        now_day = SevenHelper.get_now_day_int()
        #获取任务列表
        task_info_list = task_info_model.get_list("act_id=%s and is_release=1", order_by="sort_index asc", params=[act_id])
        #获取用户任务计算列表
        task_count_list = task_count_model.get_list("act_id=%s and user_id=%s", params=[act_id, user_id])
        #每日任务列表
        day_task_list = []
        #每周任务列表
        week_task_list = []
        for task_info in task_info_list:
            if task_info.complete_type == 1:
                day_task_list.append(task_info)
            else:
                week_task_list.append(task_info)
        #任务列表
        result_task_info = {}
        result_task_info["sign"] = []  #签到任务
        result_task_info["day_list"] = []  #每日任务
        result_task_info["week_list"] = []  #每周任务

        #每日任务遍历
        for task_info in day_task_list:
            #任务json
            task_config = ast.literal_eval(task_info.task_config)
            if not task_config:
                continue
            #任务计数信息
            user_task_count = [task_count for task_count in task_count_list if task_info.task_type == task_count.task_type]
            #是否完成任务
            is_complete = 0
            if not user_task_count:
                user_task_count = TaskCount()
            else:
                user_task_count = user_task_count[0]
            if user_task_count.last_day == now_day:
                if user_task_count.complete_count_value > 0:
                    is_complete = 2
            else:  #每日重置
                user_task_count = TaskCount()
            result = {}
            result["task_id"] = task_info.id
            result["day_limit_count"] = 1  #每日限制次数
            result["status"] = is_complete
            result["count"] = user_task_count.count_value if user_task_count.count_value else 0  #当前计数
            complete_count_value = user_task_count.complete_count_value if user_task_count.complete_count_value else 0  #完成计数
            result["complete_count"] = int(complete_count_value)
            result["task_type"] = task_info.task_type
            if task_info.task_type == 1:  #签到任务
                #用户签到信息
                signin = ast.literal_eval(user_info.signin) if user_info.signin else {"signin_date": "1900-01-01 00:00:00", "signin_value": 0}
                #本周签到天数
                sign_day_count = signin["signin_value"] if TimeHelper.is_this_week(signin["signin_date"]) == True else 0
                result["title"] = "七天签到"
                result["content"] = f"本周已累计签到{sign_day_count}天"
                result["satisfy_count"] = 1
                result["count"] = int(sign_day_count)
                result["text"] = ["签到", "已签到"]
                result["sign_list"] = task_config
                result_task_info["sign"].append(result)
            if task_info.task_type == 2:  #每日参与1次抽盒
                reward_value = int(task_config["reward_value"]) if task_config.__contains__("reward_value") else 0
                result["title"] = "参与抽盒"
                result["satisfy_count"] = int(task_config["satisfy_count"]) if task_config["satisfy_count"] else 1  #满足次数
                result["reward"] = reward_value
                result["text"] = ["去抽盒", "领取", "已完成"]
                result_task_info["day_list"].append(result)
            if task_info.task_type == 3:  #每日参与N次抽盒
                reward_value = int(task_config["reward_value"]) if task_config.__contains__("reward_value") else 0
                satisfy_count = int(task_config["satisfy_count"]) if task_config["satisfy_count"] else 1  #满足次数
                result["title"] = f"每日参与抽盒{satisfy_count}次"
                result["satisfy_count"] = satisfy_count
                result["reward"] = reward_value
                result["text"] = ["去抽盒", "领取", "已完成"]
                result_task_info["day_list"].append(result)
            if task_info.task_type == 7:  #邀请新用户
                reward_value = int(task_config["reward_value"]) if task_config.__contains__("reward_value") else 0
                #获取当日邀请好友数
                invite_log_count = invite_log_model.get_total("act_id=%s and user_id=%s and create_date_int=%s and is_handle=0", params=[act_id, user_id, now_day])
                result["title"] = "邀请新用户"
                result["status"] = 2 if complete_count_value == task_config["day_limit_count"] else 0
                result["satisfy_count"] = task_config["user_num"] if task_config["user_num"] else 1  #满足次数
                result["count"] = invite_log_count
                result["day_limit_count"] = int(task_config["day_limit_count"])  #每日限制次数
                result["reward"] = reward_value
                result["text"] = ["去邀请", "领取", "已完成"]
                result_task_info["day_list"].append(result)
            if task_info.task_type == 4:  #使用1次透视卡
                reward_value = int(task_config["reward_value"]) if task_config.__contains__("reward_value") else 0
                result["title"] = "使用1次透视卡"
                result["satisfy_count"] = int(task_config["satisfy_count"]) if task_config["satisfy_count"] else 1  #满足次数
                result["reward"] = reward_value
                result["text"] = ["去抽盒", "领取", "已完成"]
                result_task_info["day_list"].append(result)
            if task_info.task_type == 5:  #使用1次重抽卡
                reward_value = int(task_config["reward_value"]) if task_config.__contains__("reward_value") else 0
                result["title"] = "使用1次重抽卡"
                result["satisfy_count"] = int(task_config["satisfy_count"]) if task_config["satisfy_count"] else 1  #满足次数
                result["reward"] = reward_value
                result["text"] = ["去抽盒", "领取", "已完成"]
                result_task_info["day_list"].append(result)
            if task_info.task_type == 6:  #使用1次提示卡
                reward_value = int(task_config["reward_value"]) if task_config.__contains__("reward_value") else 0
                result["title"] = "使用1次提示卡"
                result["satisfy_count"] = int(task_config["satisfy_count"]) if task_config["satisfy_count"] else 1  #满足次数
                result["reward"] = reward_value
                result["text"] = ["去抽盒", "领取", "已完成"]
                result_task_info["day_list"].append(result)
        #每周任务遍历
        if len(week_task_list) > 0:
            for task_info in week_task_list:
                #任务json
                task_config = ast.literal_eval(task_info.task_config)
                if not task_config:
                    continue
                if task_info.task_type == 8:  #每周参与抽盒N次
                    if len(task_config) > 0:
                        for i in range(len(task_config)):
                            is_complete = 0
                            #子任务
                            son_task_count = [task_count for task_count in task_count_list if task_info.task_type == task_count.task_type and task_count.task_sub_type == task_config[i]["id"]]
                            #重置每周任务
                            if len(son_task_count) <= 0:
                                son_task_count = TaskCount()
                            else:
                                son_task_count = son_task_count[0]
                            if TimeHelper.is_this_week(son_task_count.last_date) == False:
                                son_task_count = TaskCount()
                            elif son_task_count.complete_count_value > 0:
                                is_complete = 2
                            result = {}
                            result["day_limit_count"] = 1  #每日限制次数
                            result["complete_count"] = son_task_count.complete_count_value  #完成次数
                            result["task_type"] = task_info.task_type
                            satisfy_count = int(task_config[i]["satisfy_count"]) if task_config[i]["satisfy_count"] else 1  #满足次数
                            result["task_id"] = task_info.id
                            result["title"] = f"参与抽盒{str(satisfy_count)}次"
                            result["status"] = is_complete
                            result["satisfy_count"] = satisfy_count
                            result["count"] = son_task_count.count_value if son_task_count else 0
                            result["reward"] = int(task_config[i]["reward_value"]) if task_config[i]["reward_value"] else 0
                            result["text"] = ["去抽盒", "领取", "已完成"]
                            result["task_sub_id"] = task_config[i]["id"]
                            result_task_info["week_list"].append(result)
                else:
                    #任务计数信息
                    user_task_count = [task_count for task_count in task_count_list if task_info.task_type == task_count.task_type]
                    #是否完成任务
                    is_complete = 0
                    #重置每周任务
                    if not user_task_count:
                        user_task_count = TaskCount()
                    else:
                        user_task_count = user_task_count[0]
                    if TimeHelper.is_this_week(user_task_count.last_date) == False:
                        user_task_count = TaskCount()
                    elif user_task_count.complete_count_value > 0:
                        is_complete = 2

                    result = {}
                    result["task_type"] = task_info.task_type
                    result["task_id"] = task_info.id
                    result["day_limit_count"] = 1  #每日限制次数
                    result["status"] = is_complete
                    result["count"] = 1  #当前计数
                    result["complete_count"] = user_task_count.complete_count_value  #完成次数
                    satisfy_count = int(task_config["satisfy_count"]) if task_config["satisfy_count"] else 1  #满足次数
                    reward_value = int(task_config["reward_value"]) if task_config.__contains__("reward_value") else 0
                    if task_info.task_type == 9:  #每周使用N张提示卡
                        result["title"] = f"每周使用{satisfy_count}次提示卡"
                    if task_info.task_type == 10:  #每周使用N张透视卡
                        result["title"] = f"每周使用{satisfy_count}次透视卡"
                    if task_info.task_type == 11:  #每周使用N张重抽卡
                        result["title"] = f"每周使用{satisfy_count}次重抽卡"
                    result["satisfy_count"] = satisfy_count
                    result["count"] = user_task_count.count_value if user_task_count.count_value else 0
                    result["reward"] = reward_value
                    result["text"] = ["去抽盒", "领取", "已完成"]
                    result_task_info["week_list"].append(result)
        self.client_reponse_json_success(result_task_info)


class UserSignHandler(ClientBaseHandler):
    """
    :description: 用户签到
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,task_id")
    @client_filter_check_act_open()
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :param login_token:用户访问令牌
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        task_id = int(self.get_request_param("task_id", 0))
        login_token = self.get_request_param("login_token")
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_cloudapp"))
        task_count_model = TaskCountModel(db_transaction=db_transaction)
        user_info_model = UserInfoModel(db_transaction=db_transaction)
        task_info_model = TaskInfoModel(db_transaction=db_transaction)

        #请求太频繁限制
        if self.check_post(f"UserSignHandler_Get_{str(user_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")

        user_info = user_info_model.get_entity_by_id(user_id)
        if not user_info:
            return self.client_reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if user_info.login_token != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录,当前无法下单")
        task_info = task_info_model.get_entity_by_id(task_id)
        if not task_info:
            return self.client_reponse_json_error("NoUser", "对不起，当前任务不存在")
        if not task_info.task_config:
            return self.client_reponse_json_error("NoUser", "对不起，签到配置异常")
        task_config = ast.literal_eval(task_info.task_config)
        if not task_config:
            return self.client_reponse_json_error("NoUser", "对不起，签到配置异常")
        #当前时间整形
        now_day = SevenHelper.get_now_day_int()
        now_datetime = self.get_now_datetime()
        task_count = task_count_model.get_entity(f"act_id={act_id} AND user_id={user_id} AND task_type=1")
        if not task_count:
            task_count = TaskCount()
        #用户签到信息
        signin = ast.literal_eval(user_info.signin) if user_info.signin else {"signin_date": "1900-01-01 00:00:00", "signin_value": 0}
        #重置每周签到任务
        if TimeHelper.is_this_week(signin["signin_date"]) == False:
            signin = {"signin_date": "1900-01-01 00:00:00", "signin_value": 0}
            task_count.complete_count_value = 0
        #签到奖励
        reward_value = task_config[int(signin["signin_value"])]
        if not reward_value or int(reward_value) <= 0:
            return self.client_reponse_json_error("NoUser", "对不起，签到配置异常")
        try:
            db_transaction.begin_transaction()
            if task_count.id:
                if task_count.last_day == now_day:
                    return self.client_reponse_json_error("NoUser", "对不起，今日已签到")
                task_count.complete_count_value += 1
                signin["signin_value"] += 1
                task_count.last_day = now_day
                task_count.count_value = 0
                task_count.last_date = now_datetime
                task_count_model.update_entity(task_count, "complete_count_value,last_day,count_value,last_date")
            else:
                signin["signin_value"] = 1
                task_count.act_id = act_id
                task_count.user_id = user_id
                task_count.task_type = 1
                task_count.complete_count_value = 1
                task_count.count_value = 0
                task_count.last_date = now_datetime
                task_count.last_day = now_day
                task_count_model.add_entity(task_count)
            #添加T币交易记录
            CoinModel.add_coin_record(act_id, user_info, "签到" + str(task_count.complete_count_value) + "天", 2, 1, int(reward_value))
            #更新用户信息
            signin["signin_date"] = now_datetime
            user_info.signin = signin
            user_info.modify_date = now_datetime
            user_info.surplus_coin += int(reward_value)
            isUpdate = user_info_model.update_entity(user_info, "signin,modify_date,surplus_coin")
            db_transaction.commit_transaction()
        except Exception as ex:
            db_transaction.rollback_transaction()
            self.logger_info.info("UserSignHandler:" + str(ex))
            return self.client_reponse_json_error("NoUser", "对不起，签到异常")

        result = {}
        result["reward_value"] = reward_value
        reward_value = int(reward_value)
        behavior_model = BehaviorModel()
        #签到参与人数
        behavior_model.report_behavior_log(act_id, user_info.id, 'SignUserCount', 1)
        #签到参与次数
        behavior_model.report_behavior_log(act_id, user_info.id, 'SignCount', 1)
        #签到T币发放
        behavior_model.report_behavior_log(act_id, user_info.id, 'SignRewardCount', reward_value)
        #T币发放总量
        behavior_model.report_behavior_log(act_id, user_info.id, 'TotalRewardCount', reward_value)
        self.client_reponse_json_success(result)


class InviteReportHandler(ClientBaseHandler):
    """
    :description: 分享上报
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    @client_filter_check_act_open()
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        behavior_model = BehaviorModel()
        #分享人数
        behavior_model.report_behavior_log(act_id, user_id, 'ShareUserCount', 1)
        #分享次数
        behavior_model.report_behavior_log(act_id, user_id, 'ShareCount', 1)
        self.client_reponse_json_success()


class InviteUserHandler(ClientBaseHandler):
    """
    :description: 邀请用户（被邀请人进入调用）
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,invite_user_id,login_token")
    @client_filter_check_act_open()
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id（受邀请用户）
        :param invite_user_id：邀请用户
        :param login_token:用户访问令牌
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        invite_user_id = int(self.get_request_param("invite_user_id", 0))
        login_token = self.get_request_param("login_token")
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_cloudapp"))
        task_count_model = TaskCountModel(db_transaction=db_transaction)
        user_info_model = UserInfoModel(db_transaction=db_transaction)
        task_info_model = TaskInfoModel(db_transaction=db_transaction)

        task_type = 7  #任务类型
        #请求太频繁限制
        if self.check_post(f"InviteUserHandler_Get_{str(user_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")

        #获取任务信息
        task_info = task_info_model.get_entity("act_id=%s and is_release=1 and task_type=%s", params=[act_id, task_type])
        if not task_info:
            return self.client_reponse_json_error("NoOpen", "对不起，任务未开启")
        task_config = ast.literal_eval(task_info.task_config)
        #获取当前用户
        user_info = user_info_model.get_entity_by_id(user_id)
        if user_id == invite_user_id:
            return self.client_reponse_json_error("Error", "对不起，无效邀请")
        if not user_info:
            return self.client_reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if user_info.login_token != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录,当前无法下单")
        if user_info.is_new == 0:
            return self.client_reponse_json_error("NoUser", "对不起，此用户不是新用户")
        now_day = SevenHelper.get_now_day_int()
        invite_log_model = InviteLogModel()
        invite_count = invite_log_model.get_total("act_id=%s and invite_user_id=%s", params=[act_id, user_id])
        if invite_count > 0:
            return self.client_reponse_json_error("Error", "此用户已经被邀请过")
        #当日邀请新用户总数量
        today_invite_count = invite_log_model.get_total("act_id=%s and user_id=%s and create_date_int=%s", params=[act_id, invite_user_id, now_day])
        user_num = int(task_config["user_num"]) if task_config.__contains__("user_num") else 0
        day_limit_count = int(task_config["day_limit_count"]) if task_config.__contains__("day_limit_count") else 0
        #每日邀请记录上限
        if today_invite_count >= (user_num * day_limit_count):
            return self.client_reponse_json_error("Error", "达到每日邀请好友上限")
        try:
            db_transaction.begin_transaction()
            invite_log = InviteLog()
            invite_log.act_id = act_id
            invite_log.user_id = invite_user_id
            invite_log.invite_user_id = user_id
            invite_log.is_handle = 0
            invite_log.create_date = self.get_now_datetime()
            invite_log.create_date_int = now_day
            invite_log_model.add_entity(invite_log)
            #任务计数
            result = TaskModel.add_task_count(act_id, task_type, invite_user_id)
            db_transaction.commit_transaction()
            if result != "":
                db_transaction.rollback_transaction()
                return self.client_reponse_json_error("Error", "邀请异常")
        except Exception as ex:
            db_transaction.rollback_transaction()
            self.logger_info.info("InviteUserHandler:" + str(ex))

        behavior_model = BehaviorModel()
        #分享访问人数
        behavior_model.report_behavior_log(act_id, user_info.id, 'ActiveUserCount', 1)
        self.client_reponse_json_success()


class ReceiveRewardHandler(ClientBaseHandler):
    """
    :description: 领取奖励处理(不包含签到任务)
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,task_id,login_token")
    @client_filter_check_act_open()
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :param task_id：任务id
        :param task_id：子任务id
        :param login_token:用户访问令牌
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        task_id = int(self.get_request_param("task_id", 0))
        task_sub_id = self.get_request_param("task_sub_id", "")
        login_token = self.get_request_param("login_token", "")
        db_transaction = DbTransaction(db_config_dict=config.get_value("db_cloudapp"))
        task_count_model = TaskCountModel(db_transaction=db_transaction)
        user_info_model = UserInfoModel(db_transaction=db_transaction)
        task_info_model = TaskInfoModel(db_transaction=db_transaction)

        #请求太频繁限制
        if self.check_post(f"ReceiveRewardHandler_Get_{str(user_id)}_{str(task_id)}_{str(task_sub_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")

        task_info = task_info_model.get_entity_by_id(task_id)
        if not task_info or task_info.is_release == False:
            return self.client_reponse_json_error("NoOpen", "对不起，任务未开启")
        #获取当前用户
        user_info = user_info_model.get_entity_by_id(user_id)
        if not user_info:
            return self.client_reponse_json_error("NoUser", "对不起，用户不存在")
        if user_info.user_state == 1:
            return self.client_reponse_json_error("UserState", "账号异常，请联系客服处理")
        if user_info.login_token != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录")
        task_config = ast.literal_eval(task_info.task_config)
        if not task_config:
            return self.client_reponse_json_error("NoOpen", "对不起，任务未配置")
        #当前时间整形
        now_day = SevenHelper.get_now_day_int()
        #当前时间
        current_date = self.get_now_datetime()
        #获取任务计数
        task_count_condition = "act_id=%s and user_id=%s and task_type=%s"
        params = [act_id, user_id, task_info.task_type]
        #子任务领奖
        if task_sub_id:
            if type(task_config) != list:
                return self.client_reponse_json_error("Error", "对不起，任务配置异常")
            task_count_condition += " and task_sub_type=%s"
            params.append(task_sub_id)
        task_count = task_count_model.get_entity(task_count_condition, params=params)
        if not task_count:
            return self.client_reponse_json_error("Error", "对不起，任务数据异常")
        #每日任务重置计数
        if task_info.complete_type == 1 and task_count.last_day != now_day:
            task_count.complete_count_value = 0
            task_count.count_value = 0
        #每周任务重置计数
        elif task_info.complete_type == 2 and TimeHelper.is_this_week(task_count.last_date) == False:
            task_count.complete_count_value = 0
            task_count.count_value = 0

        #奖励T币
        reward_value = 0
        #今日邀请好友数
        days_invite_list = 0
        #获取枚举类型任务名称
        enum = TaskType(task_info.task_type)
        enumValue = enum.name if enum else ""
        if task_info.task_type == 7:
            invite_log_model = InviteLogModel()
            #获取用户今日邀请用户数
            days_invite_list = invite_log_model.get_list("act_id=%s and user_id=%s and create_date_int=%s and is_handle=0", params=[act_id, user_id, now_day])
        #子任务领奖（类型8：每周参与抽盒N次）
        if task_sub_id:
            sub_task_config = [sub_task_config for sub_task_config in task_config if sub_task_config["id"] == task_sub_id]
            if not sub_task_config or len(sub_task_config) <= 0:
                return self.client_reponse_json_error("Error", "对不起，任务不存在，无法领取奖励")
            if task_count.complete_count_value > 0:  #每周、每日任务只能完成一次
                return self.client_reponse_json_error("Error", "对不起，领取奖励已达上限")
            sub_task_config = sub_task_config[0]
            reward_value = int(sub_task_config["reward_value"])
            if sub_task_config.__contains__("satisfy_count"):
                enumValue = enumValue.replace("N", str(sub_task_config["satisfy_count"]))
        #主任务领奖
        else:
            reward_value = int(task_config["reward_value"])
            if task_info.task_type == 7:  #邀请任务
                if len(days_invite_list) < int(task_config["user_num"]):
                    return self.client_reponse_json_error("Error", "对不起，邀请任务未完成，无法领取奖励")
                if task_count.complete_count_value >= int(task_config["day_limit_count"]):
                    return self.client_reponse_json_error("Error", "对不起，领取奖励已达上限")
            else:  #其他类型任务（任务类型8除外）
                if task_count.count_value < int(task_config["satisfy_count"]):
                    return self.client_reponse_json_error("Error", "对不起，任务未完成，无法领取奖励")
                if task_count.complete_count_value > 0:  #每周、每日任务只能完成一次
                    return self.client_reponse_json_error("Error", "对不起，领取奖励已达上限")
            if task_config.__contains__("satisfy_count"):
                enumValue = enumValue.replace("N", str(task_config["satisfy_count"]))

        #发放奖励
        if reward_value <= 0:
            return self.client_reponse_json_error("Error", "对不起，任务奖励配置异常")
        try:
            db_transaction.begin_transaction()
            task_count.complete_count_value += 1
            task_count.count_value = 0
            task_count.last_date = current_date
            task_count.last_day = now_day
            if task_info.task_type == 7:  #邀请任务
                #更新邀请记录表
                for days_invite in days_invite_list:
                    days_invite.is_handle = 1
                result = invite_log_model.update_list(days_invite_list, "is_handle")
            #更新任务计数表
            task_count_model.update_entity(task_count, "complete_count_value,count_value,last_date,last_day")
            #任务类型
            change_type = 2 if task_info.complete_type == 1 else 3
            #添加T币交易记录
            CoinModel.add_coin_record(act_id, user_info, "完成任务：" + enumValue, change_type, 1, reward_value)
            #用户更新
            user_info_model.update_table("surplus_coin=surplus_coin+%s,modify_date=%s", f"id={user_id}", params=[reward_value, current_date])

            db_transaction.commit_transaction()
        except Exception as ex:
            db_transaction.rollback_transaction()
            self.logger_info.info("ReceiveRewardHandler:" + str(ex))
        result = {}
        result["reward_value"] = reward_value
        behavior_model = BehaviorModel()
        #抽盒相关任务上报
        if task_info.task_type == 2 or task_info.task_type == 3 or task_info.task_type == 8:
            #抽盒任务参与人数
            behavior_model.report_behavior_log(act_id, user_info.id, 'TaskLotteryUserCount', 1)
            #抽盒任务参与次数
            behavior_model.report_behavior_log(act_id, user_info.id, 'TaskLotteryCount', 1)
            #抽盒任务T币发放
            behavior_model.report_behavior_log(act_id, user_info.id, 'TaskLotteryRewardCount', reward_value)
            #T币发放总量
            behavior_model.report_behavior_log(act_id, user_info.id, 'TotalRewardCount', reward_value)
        if task_info.task_type == 4 or task_info.task_type == 5 or task_info.task_type == 6 or task_info.task_type == 9 or task_info.task_type == 10 or task_info.task_type == 11:
            #使用道具卡任务参与人数
            behavior_model.report_behavior_log(act_id, user_info.id, 'PropUserCount', 1)
            #使用道具卡任务参与次数
            behavior_model.report_behavior_log(act_id, user_info.id, 'PropCount', 1)
            #使用道具卡任务T币发放
            behavior_model.report_behavior_log(act_id, user_info.id, 'PropRewardCount', reward_value)
            #T币发放总量
            behavior_model.report_behavior_log(act_id, user_info.id, 'TotalRewardCount', reward_value)
        if task_info.task_type==7:
            #邀请好友任务参与人数
            behavior_model.report_behavior_log(act_id, user_info.id, 'InviteUserCount', 1)
            #邀请好友任务参与次数
            behavior_model.report_behavior_log(act_id, user_info.id, 'InviteCount', 1)
            #邀请好友任务T币发放
            behavior_model.report_behavior_log(act_id, user_info.id, 'InviteRewardCount', reward_value)
            #T币发放总量
            behavior_model.report_behavior_log(act_id, user_info.id, 'TotalRewardCount', reward_value)

        self.client_reponse_json_success(result)


class TaskModel:
    """
    :description: 任务公用处理
    """
    @classmethod
    def add_task_count(self, act_id, task_type, user_id):
        """
        :description: 增加任务计数
        
        :param act_id：活动id
        :param task_type：任务类型（参考枚举）
        :param user_id：用户id
        :return: dict
        :last_editors: WangQiang
        """
        task_count_model = TaskCountModel()
        task_info_model = TaskInfoModel()
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
