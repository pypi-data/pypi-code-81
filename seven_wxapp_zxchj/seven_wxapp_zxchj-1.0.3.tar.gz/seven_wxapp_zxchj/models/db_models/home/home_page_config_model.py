
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class HomePageConfigModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(HomePageConfigModel, self).__init__(HomePageConfig, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class HomePageConfig:

    def __init__(self):
        super(HomePageConfig, self).__init__()
        self.id = 0  # id
        self.act_id = 0  # 活动ID
        self.title = ""  # 标题
        self.config_type = 0  # 配置类型:1页签2推荐
        self.img = ""  # 图片
        self.sort_index = 0  # 排序
        self.is_release = 0  # 是否发布（1发布0未发布）
        self.content = ""  # 展示内容(数组json：sort_index(排序),series_id(系列id),machine_id(盒子id))
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'title', 'config_type', 'img', 'sort_index', 'is_release', 'content', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "home_page_config_tb"
    