
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class BuyOrderModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(BuyOrderModel, self).__init__(BuyOrder, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class BuyOrder:

    def __init__(self):
        super(BuyOrder, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # act_id
        self.user_id = 0  # user_id
        self.wx_order_no = ""  # 微信交易单号
        self.pay_order_no = ""  # 支付单号
        self.machine_id = 0  # 机台id
        self.machine_name = ""  # 机台名称
        self.machine_price = 0  # 机台价格
        self.buy_num = 0  # 购买数量
        self.buy_amount = 0  # 购买金额（单位:元）
        self.pay_amount = 0  # 支付金额（单位:元）
        self.discount_amount = 0  # 优惠金额（单位:元）
        self.order_status = 0  # 订单状态:0未支付1已支付2已退款
        self.refund_date = "1900-01-01 00:00:00"  # 退款时间
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.pay_date = "1900-01-01 00:00:00"  # 支付时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'user_id', 'wx_order_no', 'pay_order_no', 'machine_id', 'machine_name', 'machine_price', 'buy_num', 'buy_amount', 'pay_amount', 'discount_amount', 'order_status', 'refund_date', 'create_date', 'pay_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "buy_order_tb"
    