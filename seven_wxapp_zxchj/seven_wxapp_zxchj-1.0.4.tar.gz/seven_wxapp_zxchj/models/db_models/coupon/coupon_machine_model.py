
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class CouponMachineModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(CouponMachineModel, self).__init__(CouponMachine, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class CouponMachine:

    def __init__(self):
        super(CouponMachine, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # 活动id
        self.coupon_id = 0  # 优惠劵id
        self.machine_id = 0  # 中盒id
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'coupon_id', 'machine_id', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "coupon_machine_tb"
    