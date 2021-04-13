
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PrizeOrderModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(PrizeOrderModel, self).__init__(PrizeOrder, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PrizeOrder:

    def __init__(self):
        super(PrizeOrder, self).__init__()
        self.id = 0  # id
        self.order_no = ""  # 订单号
        self.act_id = 0  # act_id
        self.user_id = 0  # user_id
        self.real_name = ""  # 真实姓名
        self.telephone = ""  # 手机号码
        self.province = ""  # 所在省
        self.city = ""  # 所在市
        self.county = ""  # 所在区
        self.street = ""  # 所在街道
        self.adress = ""  # 收货地址
        self.deliver_date = "1900-01-01 00:00:00"  # 发货时间
        self.express_no = ""  # 快递单号
        self.express_company = ""  # 快递公司
        self.order_status = 0  # 订单状态（0未付款1未发货2已发货3不予发货4已退款5已完成10付款中）
        self.is_auto_deliver = 0  # 是否自动发货：0否1是
        self.freight_price = 0  # 运费价格
        self.is_free_shipping = 0  # 是否包邮
        self.freight_pay_order_no = ""  # 运费支付订单id
        self.remarks = ""  # 备注
        self.sync_status = 0  # 订单同步状态（0-未同步，1-同步成功，2-同步失败）
        self.sync_date = "1900-01-01 00:00:00"  # 订单同步时间
        self.sync_count = 0  # 订单同步次数
        self.sync_result = ""  # 订单同步结果
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'order_no', 'act_id', 'user_id', 'real_name', 'telephone', 'province', 'city', 'county', 'street', 'adress', 'deliver_date', 'express_no', 'express_company', 'order_status', 'is_auto_deliver', 'freight_price', 'is_free_shipping', 'freight_pay_order_no', 'remarks', 'sync_status', 'sync_date', 'sync_count', 'sync_result', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "prize_order_tb"
    