
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class ReceivingAddressModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(ReceivingAddressModel, self).__init__(ReceivingAddress, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class ReceivingAddress:

    def __init__(self):
        super(ReceivingAddress, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # act_id
        self.user_id = 0  # user_id
        self.real_name = ""  # 真实姓名
        self.telephone = ""  # 手机号码
        self.is_default = 0  # 是否默认地址（1是0否）
        self.province = ""  # 省
        self.city = ""  # 市
        self.county = ""  # 区
        self.street = ""  # 所在街道
        self.adress = ""  # 收货地址
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'user_id', 'real_name', 'telephone', 'is_default', 'province', 'city', 'county', 'street', 'adress', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "receiving_address_tb"
    