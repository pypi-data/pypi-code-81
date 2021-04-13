
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class UserPropModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(UserPropModel, self).__init__(UserProp, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class UserProp:

    def __init__(self):
        super(UserProp, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # act_id
        self.user_id = 0  # user_id
        self.is_use = 0  # 是否使用
        self.use_date = "1900-01-01 00:00:00"  # 使用时间
        self.prop_type = 0  # 道具类型(2透视卡3提示卡4重抽卡)
        self.group_id = ""  # 用户进入中盒自动分配的唯一标识
        self.remark = ""  # 备注
        self.create_date_int = 0  # 创建时间整形
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'user_id', 'is_use', 'use_date', 'prop_type', 'group_id', 'remark', 'create_date_int', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "user_prop_tb"
    