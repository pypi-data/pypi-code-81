
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class PrizeRosterModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(PrizeRosterModel, self).__init__(PrizeRoster, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class PrizeRoster:

    def __init__(self):
        super(PrizeRoster, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # act_id
        self.user_id = 0  # user_id
        self.user_nick = ""  # 昵称
        self.machine_id = 0  # 机台id
        self.machine_name = ""  # 机台名称
        self.machine_price = 0  # 机台价格
        self.prize_id = 0  # 奖品标识
        self.prize_name = ""  # 奖品名称
        self.prize_price = 0  # 奖品价值
        self.prize_pic = ""  # 奖品图片
        self.toy_cabinet_pic = ""  # 玩具柜图
        self.prize_detail = ""  # 奖品详情图
        self.prize_tag = 0  # 奖品标签（1普通款2隐藏款3超级隐藏款）
        self.series_id = 0  # IP系列id
        self.prize_status = 0  # 奖品状态（0待提货1未发货2已发货3不予发货4已退款10处理中）
        self.pay_status = 0  # 支付状态(0未支付1已支付)
        self.prize_order_no = ""  # 奖品订单号
        self.pay_order_no = ""  # 支付单号
        self.goods_code = ""  # 商品编码
        self.group_id = ""  # 用户进入中盒自动分配的唯一标识
        self.modify_date = "1900-01-01 00:00:00"  # 更新时间
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.expire_date = "1900-01-01 00:00:00"  # 到期时间（到期自动下单）

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'user_id', 'user_nick', 'machine_id', 'machine_name', 'machine_price', 'prize_id', 'prize_name', 'prize_price', 'prize_pic', 'toy_cabinet_pic', 'prize_detail', 'prize_tag', 'series_id', 'prize_status', 'pay_status', 'prize_order_no', 'pay_order_no', 'goods_code', 'group_id', 'modify_date', 'create_date', 'expire_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "prize_roster_tb"
    