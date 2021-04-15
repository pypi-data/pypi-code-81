
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class SignRecordModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(SignRecordModel, self).__init__(SignRecord, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class SignRecord:

    def __init__(self):
        super(SignRecord, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # act_id
        self.user_id = 0  # user_id
        self.current_week = 0  # 当前第几周
        self.reward_coin_count = 0  # 奖励T币数量
        self.history_coin_count = 0  # 历史T币数量
        self.sign_date_int = 0  # 签到时间整形(yyyymmdd)
        self.sign_date = "1900-01-01 00:00:00"  # 签到时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'user_id', 'current_week', 'reward_coin_count', 'history_coin_count', 'sign_date_int', 'sign_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "sign_record_tb"
    