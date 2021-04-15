
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class UserInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(UserInfoModel, self).__init__(UserInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class UserInfo:

    def __init__(self):
        super(UserInfo, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # act_id
        self.open_id = ""  # open_id
        self.union_id = ""  # UnionID
        self.user_nick = ""  # 用户昵称
        self.user_nick_base64 = ""  # 用户昵称Base64
        self.avatar = ""  # 头像
        self.e_mail = ""  # 邮箱
        self.is_new = 0  # 是否新用户
        self.telephone = ""  # 手机号
        self.gender = 0  # 性别:1男 2女
        self.age = 0  # 年龄
        self.birthday = "1900-01-01 00:00:00"  # 生日
        self.province = ""  # 省
        self.city = ""  # 市
        self.county = ""  # 区
        self.last_ip = ""  # 最后登录IP
        self.pay_price = 0  # 累计支付金额
        self.pay_num = 0  # 累计支付笔数
        self.removed_count = 0  # 已拆次数
        self.login_token = ""  # 登录令牌
        self.signin = ""  # 签到信息
        self.surplus_coin = 0  # 剩余T币
        self.tips_card_count = 0  # 提示卡数量
        self.perspective_card_count = 0  # 透视卡数量
        self.redraw_card_count = 0  # 重抽卡数量
        self.user_state = 0  # 用户状态（0-正常，1-黑名单）
        self.relieve_date = "1900-01-01 00:00:00"  # 解禁时间
        self.last_login_date = "1900-01-01 00:00:00"  # 最后登录时间
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'open_id', 'union_id', 'user_nick', 'user_nick_base64', 'avatar', 'e_mail', 'is_new', 'telephone', 'gender', 'age', 'birthday', 'province', 'city', 'county', 'last_ip', 'pay_price', 'pay_num', 'removed_count', 'login_token', 'signin', 'surplus_coin', 'tips_card_count', 'perspective_card_count', 'redraw_card_count', 'user_state', 'relieve_date', 'last_login_date', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "user_info_tb"
    