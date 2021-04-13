
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class MachinePrizeModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(MachinePrizeModel, self).__init__(MachinePrize, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class MachinePrize:

    def __init__(self):
        super(MachinePrize, self).__init__()
        self.id = 0  # 标识
        self.act_id = 0  # 活动标识
        self.machine_id = 0  # 机台ID
        self.prize_name = ""  # 奖品名称
        self.prize_title = ""  # 奖品子标题
        self.prize_pic = ""  # 奖品图
        self.toy_cabinet_pic = ""  # 玩具柜图
        self.goods_code = ""  # 商品编码
        self.prize_type = 0  # 奖品类型（1实物2虚拟物品）
        self.prize_price = 0  # 奖品价格
        self.probability = 0  # 奖品权重
        self.surplus = 0  # 奖品库存
        self.is_prize_notice = 0  # 是否显示中奖公告
        self.prize_limit = 0  # 中奖限制
        self.prize_total = 0  # 奖品总数
        self.hand_out = 0  # 已发出数量
        self.prize_tag = 0  # 奖品标签（1普通款2隐藏款3超级隐藏款）
        self.sort_index = 0  # 排序号
        self.is_release = 0  # 是否发布（1是0否）
        self.is_del = 0  # 标记删除（1是0否）
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 更新时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'machine_id', 'prize_name', 'prize_title', 'prize_pic', 'toy_cabinet_pic', 'goods_code', 'prize_type', 'prize_price', 'probability', 'surplus', 'is_prize_notice', 'prize_limit', 'prize_total', 'hand_out', 'prize_tag', 'sort_index', 'is_release', 'is_del', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "machine_prize_tb"
    