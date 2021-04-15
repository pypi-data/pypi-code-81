
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class ExchangeRecordModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(ExchangeRecordModel, self).__init__(ExchangeRecord, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class ExchangeRecord:

    def __init__(self):
        super(ExchangeRecord, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # act_id
        self.user_id = 0  # user_id
        self.title = ""  # 标题
        self.num = 0  # 数量
        self.use_coin_count = 0  # 使用T币数
        self.history_coin_count = 0  # 历史T币数量
        self.goods_type = 0  # 商品类型(1实物2透视卡3提示卡4重抽卡5优惠券)
        self.create_date = "1900-01-01 00:00:00"  # 创建时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'user_id', 'title', 'num', 'use_coin_count', 'history_coin_count', 'goods_type', 'create_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "exchange_record_tb"
    