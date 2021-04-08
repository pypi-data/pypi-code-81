
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class TaskInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None):
        super(TaskInfoModel, self).__init__(TaskInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction

    #方法扩展请继承此类
    
class TaskInfo:

    def __init__(self):
        super(TaskInfo, self).__init__()
        self.id = 0  # 标识
        self.act_id = 0  # 活动标识
        self.complete_type = 0  # 完成类型:1每日任务2每周任务
        self.task_type = 0  # 任务类型(1签到2每日参与1次抽盒3每日参与抽盒N次4使用透视卡5使用重抽卡6使用提示卡7邀请8每周参与抽盒N次9每周使用N张提示卡10每周使用N张透视卡11每周使用N张重抽卡)
        self.task_config = ""  # 任务配置（json字符串）
            # 每日签到包含字段（reward_value奖励值）
            # 邀请好友包含字段（reward_value奖励值，user_num邀请用户数，day_limit_count每日限制次数）
            # 使用道具卡及参与抽盒字段（satisfy_count满足数量，reward_value奖励值）
            # 每周抽盒任务字段（数组结果：id唯一值，satisfy_count满足数量，reward_value奖励值）
            # 任务配置(json字符串，枚举TaskType里面的注释都有详细例子)
            
        self.sort_index = 0  # 排序
        self.is_release = 0  # 是否发布
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 更新时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'complete_type', 'task_type', 'task_config', 'sort_index', 'is_release', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "task_info_tb"
    