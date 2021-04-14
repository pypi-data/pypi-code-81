
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class CoinRecordModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(CoinRecordModel, self).__init__(CoinRecord, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class CoinRecord:

    def __init__(self):
        super(CoinRecord, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # act_id
        self.user_id = 0  # user_id
        self.title = ""  # 标题
        self.change_type = 0  # 变动类型:1手动2每日任务3每周任务4兑换
        self.transaction_type = 0  # 交易类型:1增加2减少
        self.coin_count = 0  # T币数量
        self.history_coin_count = 0  # 历史T币数量
        self.operation_user_id = ""  # 操作用户id
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'user_id', 'title', 'change_type', 'transaction_type', 'coin_count', 'history_coin_count', 'operation_user_id', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "coin_record_tb"
    