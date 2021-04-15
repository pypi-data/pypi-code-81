
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class SurplusQueueModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(SurplusQueueModel, self).__init__(SurplusQueue, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class SurplusQueue:

    def __init__(self):
        super(SurplusQueue, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # 活动ID
        self.machine_id = 0  # 机台id
        self.prize_id = 0  # 奖品id
        self.group_id = ""  # 用户进入中盒自动分配的唯一标识
        self.is_lock = 0  # 是否锁定(1是0否)
        self.user_id = 0  # 用户id
        self.withhold_value = 0  # 计数
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.expire_date = "1900-01-01 00:00:00"  # 过期回收时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'machine_id', 'prize_id', 'group_id', 'is_lock', 'user_id', 'withhold_value', 'create_date', 'expire_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "surplus_queue_tb"
    