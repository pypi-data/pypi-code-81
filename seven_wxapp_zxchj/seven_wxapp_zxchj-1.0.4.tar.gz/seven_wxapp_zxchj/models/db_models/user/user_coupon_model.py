
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class UserCouponModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(UserCouponModel, self).__init__(UserCoupon, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class UserCoupon:

    def __init__(self):
        super(UserCoupon, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # 活动标识
        self.user_id = 0  # 用户标识
        self.coupon_id = 0  # 优惠券标识
        self.pay_order_no = ""  # 支付单号
        self.exchange_id = 0  # 兑换标识
        self.coupon_status = 0  # 优惠劵状态（0未使用1已使用2已失效）
        self.use_date = "1900-01-01 00:00:00"  # 使用时间
        self.access_type = 0  # 获取途径(0人工发送1领取2兑换)
        self.create_date = "1900-01-01 00:00:00"  # 领取时间
        self.create_date_int = 0  # 领取天
        self.is_del = 0  # 标记删除：1是0否

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'user_id', 'coupon_id', 'pay_order_no', 'exchange_id', 'coupon_status', 'use_date', 'access_type', 'create_date', 'create_date_int', 'is_del']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "user_coupon_tb"
    