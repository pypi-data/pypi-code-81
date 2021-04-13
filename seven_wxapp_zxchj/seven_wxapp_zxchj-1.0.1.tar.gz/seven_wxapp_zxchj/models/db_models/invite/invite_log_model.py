
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class InviteLogModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(InviteLogModel, self).__init__(InviteLog, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class InviteLog:

    def __init__(self):
        super(InviteLog, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # 活动标识
        self.user_id = 0  # 邀请人userid
        self.invite_user_id = 0  # 受邀人userid
        self.is_handle = 0  # 是否处理（1处理0未处理）
        self.create_date_int = 0  # 创建时间整形（yyymmdd）
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'user_id', 'invite_user_id', 'is_handle', 'create_date_int', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "invite_log_tb"
    