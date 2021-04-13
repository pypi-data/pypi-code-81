
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class CarouselMapModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(CarouselMapModel, self).__init__(CarouselMap, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class CarouselMap:

    def __init__(self):
        super(CarouselMap, self).__init__()
        self.id = 0  # id
        self.title = ""  # 标题
        self.ImgIcon = ""  # 图片Icon
        self.act_id = 0  # 活动ID
        self.jump_type = 0  # 跳转类型:1.本小程序2.客服3.其他小程序4.H5页面
        self.app_id = ""  # 小程序ID
        self.jump_url = ""  # 跳转地址
        self.series_id = 0  # 系列Id
        self.machine_id = 0  # 盒子id
        self.sort_index = 0  # 排序号
        self.is_release = 0  # 是否发布（1是0否）
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 更新时间

    @classmethod
    def get_field_list(self):
        return ['id', 'title', 'ImgIcon', 'act_id', 'jump_type', 'app_id', 'jump_url', 'series_id', 'machine_id', 'sort_index', 'is_release', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "carousel_map_tb"
    