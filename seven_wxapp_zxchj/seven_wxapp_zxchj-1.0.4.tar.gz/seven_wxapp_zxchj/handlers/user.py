# -*- coding: utf-8 -*-
"""
@Author: WangQiang
@Date: 2021-01-07 16:07:42
:LastEditTime: 2021-04-12 18:16:46
:LastEditors: HuangJingCan
@Description: 
"""
from seven_wxapp.handlers.base.client_base import *
from seven_wxapp.handlers.base.wechatpay_base import *
from seven_wxapp.handlers.base.behavior_base import *

from seven_wxapp_zxchj.models.db_models.user.user_info_model import *
from seven_wxapp_zxchj.models.db_models.receiving.receiving_address_model import *


class LoginHandler(ClientBaseHandler):
    """
    :description: 登录处理
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户标识
        :return: dict
        :last_editors: WangQiang
        """
        code = self.get_request_param("code")
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))

        if user_id <= 0 and not code:
            return self.client_reponse_json_error("NoParameter", "对不起，缺少参数")

        user_info_model = UserInfoModel(context=self)

        user_info = None
        open_id = ""
        if user_id > 0:
            user_info = user_info_model.get_entity_by_id(user_id)
            if not user_info:
                return self.client_reponse_json_error("NoUser", "对不起，找不到此用户")
        else:
            open_id = WeiXinHelper().get_open_id(code)
            if not open_id:
                return self.client_reponse_json_error("NoUser", "对不起，获取用户信息异常")
            user_info = user_info_model.get_entity("act_id=%s and open_id=%s", params=[act_id, open_id])
        if not user_info:
            user_info = UserInfo()
            user_info.open_id = open_id
            user_info.act_id = act_id
            user_info.is_new = 1
            user_info.create_date = self.get_now_datetime()
            user_info.modify_date = self.get_now_datetime()
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.last_login_date = self.get_now_datetime()
            user_info.last_ip = self.get_real_ip()
            user_info.id = user_info_model.add_entity(user_info)
        else:
            user_info.modify_date = self.get_now_datetime()
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.last_login_date = self.get_now_datetime()
            user_info.is_new = 0
            user_info.last_ip = self.get_real_ip()
            user_info_model.update_entity(user_info, "modify_date,login_token,is_new,last_login_date,last_ip")

        if user_info.user_nick:
            user_info.user_nick = self.emoji_base64_to_emoji(user_info.user_nick)
        user_info_dict = {}
        user_info_dict["id"] = user_info.id
        user_info_dict["act_id"] = user_info.act_id
        user_info_dict["open_id"] = user_info.open_id
        user_info_dict["union_id"] = user_info.union_id
        user_info_dict["user_nick"] = user_info.user_nick
        user_info_dict["avatar"] = user_info.avatar
        user_info_dict["is_new"] = user_info.is_new
        user_info_dict["telephone"] = user_info.telephone
        user_info_dict["gender"] = user_info.gender
        user_info_dict["birthday"] = user_info.birthday
        user_info_dict["login_token"] = user_info.login_token
        user_info_dict["surplus_coin"] = user_info.surplus_coin
        user_info_dict["tips_card_count"] = user_info.tips_card_count
        user_info_dict["perspective_card_count"] = user_info.perspective_card_count
        user_info_dict["redraw_card_count"] = user_info.redraw_card_count
        user_info_dict["user_coupon_count"] = self.get_user_coupon_count(user_info.act_id, user_info.id)
        user_info_dict["user_state"] = user_info.user_state

        behavior_model = BehaviorModel(context=self)
        #访问次数
        behavior_model.report_behavior_log(act_id, user_info.id, 'VisitCountEveryDay', 1)
        #访问人数
        behavior_model.report_behavior_log(act_id, user_info.id, 'VisitManCountEveryDay', 1)
        if user_info.is_new == 1:
            #新增用户数
            behavior_model.report_behavior_log(act_id, user_info.id, 'VisitManCountEveryDayIncrease', 1)

        return self.client_reponse_json_success(user_info_dict)

    def get_user_coupon_count(self, act_id, user_id):
        """
        description 获取优惠券数量
        :param act_id：活动标识
        :param user_id：用户标识
        """
        now = self.get_now_datetime()
        where = "a.act_id=%s and a.user_id=%s and a.coupon_status=%s and a.`coupon_id`=b.`id` and b.is_del=0" + f" and '{now}'<b.effective_end_date"
        params = [act_id, user_id, 0]
        sql = f"SELECT COUNT(a.id) AS count FROM user_coupon_tb as a,coupon_info_tb as b where {where};"
        db = MySQLHelper(config.get_value("db_wxapp"))
        row = db.fetch_one_row(sql, params)
        row_count = 0
        if row and 'count' in row and int(row['count']) > 0:
            row_count = int(row["count"])
        return row_count

    def get_wx_login_url(self, code):
        """
        description 获取登录接口
        :param code：微信登录code
        """
        app_id = config.get_value("app_id")
        app_secret = config.get_value("app_secret")
        wx_login_url = f"https://api.weixin.qq.com/sns/jscode2session?appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code"
        return wx_login_url


class UpdateUserHandler(ClientBaseHandler):
    """
    :description: 更新用户
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,user_nick,avatar")
    def get_async(self):
        """
        :param user_id：用户id
        :param act_id：活动id
        :param user_nick：用户昵称
        :param avatar：头像
        :param gender：性别
        :param birthday：生日
        :param province：省
        :param city：市
        :param county：区
        :return: dict
        :last_editors: WangQiang
        """
        user_id = int(self.get_request_param("user_id", 0))
        act_id = int(self.get_request_param("act_id", 0))
        user_nick = self.get_request_param("user_nick")  #用户昵称
        avatar = self.get_request_param("avatar")  #头像
        gender = int(self.get_request_param("gender", 0))  #性别
        birthday = self.get_request_param("birthday")  #生日
        province = self.get_request_param("province")  #省`
        city = self.get_request_param("city")  #市
        county = self.get_request_param("county")  #区

        user_info_model = UserInfoModel(context=self)

        user_info = user_info_model.get_entity("id=%s and act_id=%s", params=[user_id, act_id])
        if not user_info:
            return self.client_reponse_json_error("NoUser", "对不起，用户不存在")

        user_info.user_nick = self.emoji_to_emoji_base64(user_nick)
        user_info.user_nick_base64 = self.base64_encode(user_nick)
        user_info.avatar = avatar
        user_info.gender = gender
        if birthday:
            user_info.birthday = birthday
        user_info.province = province
        user_info.city = city
        user_info.county = county
        user_info_model.update_entity(user_info, "user_nick,user_nick_base64,avatar,gender,birthday,province,city,county")

        #输出新的字典
        user_info_dict = {}
        user_info_dict["id"] = user_info.id
        user_info_dict["act_id"] = user_info.act_id
        user_info_dict["open_id"] = user_info.open_id
        user_info_dict["union_id"] = user_info.union_id
        user_info_dict["user_nick"] = user_info.user_nick
        user_info_dict["avatar"] = user_info.avatar
        user_info_dict["is_new"] = user_info.is_new
        user_info_dict["telephone"] = user_info.telephone
        user_info_dict["gender"] = user_info.gender
        user_info_dict["birthday"] = user_info.birthday
        user_info_dict["login_token"] = user_info.login_token
        user_info_dict["surplus_coin"] = user_info.surplus_coin
        user_info_dict["tips_card_count"] = user_info.tips_card_count
        user_info_dict["perspective_card_count"] = user_info.perspective_card_count
        user_info_dict["redraw_card_count"] = user_info.redraw_card_count
        user_info_dict["user_state"] = user_info.user_state

        return self.client_reponse_json_success(user_info_dict)


class UpdateUserPhoneHandler(ClientBaseHandler):
    """
    :description: 更新用户手机号
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,open_id,encryptedData,iv")
    def get_async(self):
        """
        :param user_id：用户id
        :param act_id：活动id
        :param open_id：open_id
        :param telephone：手机号
        :return: dict
        :last_editors: WangQiang
        """
        user_id = int(self.get_request_param("user_id", 0))
        act_id = int(self.get_request_param("act_id", 0))
        open_id = self.get_request_param("open_id", "", False)
        encryptedData = self.get_request_param("encryptedData", "", False)  #密文
        iv = self.get_request_param("iv", "", False)  #iv
        code = self.get_request_param("code")  #code

        user_info_model = UserInfoModel(context=self)
        decrypted_data = WeiXinHelper().decrypted_data(open_id, code, encryptedData, iv)
        if not decrypted_data or not decrypted_data.__contains__("phoneNumber"):
            return self.client_reponse_json_error("NoUser", "对不起，获取手机号失败")
        # self.logger_info.info("[decrypted_data]" + json.dumps(decrypted_data))
        result = user_info_model.update_table("telephone=%s", f"id={user_id}", params=[str(decrypted_data["phoneNumber"])])

        return self.client_reponse_json_success(str(decrypted_data["phoneNumber"]))


class ReceivingAddressListHandler(ClientBaseHandler):
    """
    :description: 收货地址列表
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id")
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))

        receiving_address_model = ReceivingAddressModel(context=self)

        field = "user_id,real_name,telephone,is_default,province,city,county,street,adress"

        receiving_address_dict_list = receiving_address_model.get_dict_list("act_id=%s and user_id=%s", field=field, params=[act_id, user_id])

        return self.client_reponse_json_success(receiving_address_dict_list)


class SaveReceivingAddressHandler(ClientBaseHandler):
    """
    :description: 保存收货地址
    """
    @client_filter_check_head()
    @client_filter_check_params("act_id,user_id,login_token,real_name,telephone")
    def get_async(self):
        """
        :param act_id：活动id
        :param user_id：用户id
        :param user_id：用户id
        :param is_default：是否默认地址（1是0否）
        :param login_token：用户登录令牌
        :param real_name：真实姓名
        :param telephone：手机号码
        :param province：省
        :param city：市
        :param county：区
        :param street：街道
        :param adress：地址
        :return: dict
        :last_editors: WangQiang
        """
        act_id = int(self.get_request_param("act_id", 0))
        user_id = int(self.get_request_param("user_id", 0))
        login_token = self.get_request_param("login_token")
        real_name = self.get_request_param("real_name")
        telephone = self.get_request_param("telephone")
        province = self.get_request_param("province")
        city = self.get_request_param("city")
        county = self.get_request_param("county")
        street = self.get_request_param("street")
        adress = self.get_request_param("adress")

        #请求太频繁限制
        if self.check_post(f"AddReceivingAddress_Get_{str(user_id)}") == False:
            return self.client_reponse_json_error("HintMessage", "对不起，请求太频繁")

        #获取用户信息
        user_info_model = UserInfoModel(context=self)
        user_info = user_info_model.get_dict_by_id(user_id)
        if not user_info:
            return self.client_reponse_json_error("Error", "对不起，用户不存在")
        if user_info["login_token"] != login_token:
            return self.client_reponse_json_error("Error", "对不起，已在另一台设备登录,当前无法添加地址")

        result = 0
        receiving_address_model = ReceivingAddressModel(context=self)
        receiving_address = receiving_address_model.get_entity("user_id=%s and is_default=1", params=[user_id])
        if not receiving_address:
            receiving_address = ReceivingAddress()
        receiving_address.real_name = real_name
        receiving_address.telephone = telephone
        receiving_address.province = province
        receiving_address.city = city
        receiving_address.county = county
        receiving_address.street = street
        receiving_address.adress = adress
        if receiving_address.id <= 0:
            receiving_address.act_id = act_id
            receiving_address.user_id = user_id
            receiving_address.is_default = 1
            receiving_address.create_date = self.get_now_datetime()
            result = receiving_address_model.add_entity(receiving_address)
        else:
            updateResult = receiving_address_model.update_entity(receiving_address, "real_name,telephone,province,city,county,street,adress")
            result = 1
        if result == 0:
            return self.client_reponse_json_error("Error", "对不起，保存地址失败")

        return self.client_reponse_json_success(receiving_address)