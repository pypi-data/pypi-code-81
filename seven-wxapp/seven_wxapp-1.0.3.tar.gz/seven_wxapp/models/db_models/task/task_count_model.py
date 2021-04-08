
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class TaskCountModel(BaseModel):
    def __init__(self, db_connect_key='db_cloudapp', sub_table=None, db_transaction=None):
        super(TaskCountModel, self).__init__(TaskCount, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction

    #方法扩展请继承此类
    
class TaskCount:

    def __init__(self):
        super(TaskCount, self).__init__()
        self.id = 0  # 标识
        self.act_id = 0  # 活动标识
        self.user_id = 0  # user_id
        self.task_type = 0  # 任务类型(1签到2每日参与1次抽盒3每日参与抽盒N次4使用透视卡5使用重抽卡6使用提示卡7邀请8每周参与抽盒N次9每周使用N张提示卡10每周使用N张透视卡11每周使用N张重抽卡)
        self.task_sub_type = ""  # 任务子类型(用于指定任务里的再细分)
        self.complete_count_value = 0  # 完成计数值
        self.count_value = 0  # 计数值（完成任务后重置）
        self.last_date = "1900-01-01 00:00:00"  # 最后完成修改时间
        self.last_day = 0  # 修改日期整形(yyyymmdd)

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'user_id', 'task_type', 'task_sub_type', 'complete_count_value', 'count_value', 'last_date', 'last_day']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "task_count_tb"
    