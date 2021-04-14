
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class MachineInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(MachineInfoModel, self).__init__(MachineInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class MachineInfo:

    def __init__(self):
        super(MachineInfo, self).__init__()
        self.id = 0  # 
        self.act_id = 0  # act_id
        self.machine_name = ""  # 机台名称
        self.machine_long_name = ""  # 机台长名称
        self.machine_type = 0  # 机台类型：1消耗积分2消耗次数
        self.skin_id = 0  # 主题皮肤id
        self.sort_index = 0  # 排序
        self.is_release = 0  # 是否发布：1发布0-未发布
        self.machine_price = 0  # 机台价格
        self.is_repeat_prize = 0  # 是否奖品不重复：0-不重复1-重复
        self.is_prize_notice = 0  # 是否显示中奖公告
        self.series_id = 0  # IP系列id
        self.specs_type = 0  # 中盒规格(5.6,7.8.9.10.12)
        self.index_pic = ""  # 首页主图
        self.machine_bg_pic = ""  # 中盒背景图
        self.goods_detail = ""  # 商品详情(多张图)
        self.carousel_map_img = ""  # 轮播图
        self.box_style_detail = ""  # 盲盒样式详情(json)
        self.is_del = 0  # 标记删除：1是0否
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'machine_name', 'machine_long_name', 'machine_type', 'skin_id', 'sort_index', 'is_release', 'machine_price', 'is_repeat_prize', 'is_prize_notice', 'series_id', 'specs_type', 'index_pic', 'machine_bg_pic', 'goods_detail', 'carousel_map_img', 'box_style_detail', 'is_del', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "machine_info_tb"
    