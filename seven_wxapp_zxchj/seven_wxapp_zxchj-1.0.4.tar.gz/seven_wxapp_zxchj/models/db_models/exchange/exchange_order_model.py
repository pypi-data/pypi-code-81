
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class ExchangeOrderModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(ExchangeOrderModel, self).__init__(ExchangeOrder, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class ExchangeOrder:

    def __init__(self):
        super(ExchangeOrder, self).__init__()
        self.id = 0  # id
        self.order_no = ""  # 订单号
        self.act_id = 0  # 活动标识
        self.user_id = 0  # 用户标识
        self.exchange_id = 0  # 兑换标识
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
        self.goods_img = ""  # 商品图片
        self.goods_num = 0  # 商品数量
        self.goods_name = ""  # 商品名称
        self.goods_code = ""  # 商品编码
        self.order_status = 0  # 状态（0未发货1已发货2不予发货）
        self.remarks = ""  # 备注
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.create_date_int = 0  # 创建天

    @classmethod
    def get_field_list(self):
        return ['id', 'order_no', 'act_id', 'user_id', 'exchange_id', 'real_name', 'telephone', 'province', 'city', 'county', 'street', 'adress', 'deliver_date', 'express_no', 'express_company', 'goods_img', 'goods_num', 'goods_name', 'goods_code', 'order_status', 'remarks', 'create_date', 'create_date_int']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "exchange_order_tb"
    