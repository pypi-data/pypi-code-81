
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class ActInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(ActInfoModel, self).__init__(ActInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class ActInfo:

    def __init__(self):
        super(ActInfo, self).__init__()
        self.id = 0  # id
        self.act_name = ""  # 活动名称
        self.act_type = 0  # 活动类型
        self.theme_id = 0  # 主题ID
        self.is_open = 0  # 是否发布（1是0否）
        self.close_word = ""  # 关闭小程序文案
        self.share_desc = ""  # 分享内容(json)
        self.skin_desc = ""  # 皮肤内容(json)
        self.menu_desc = ""  # 导航菜单(json)
        self.sort_index = 0  # 排序号
        self.is_del = 0  # 标记删除（1是0否）
        self.shakebox_tips = ""  # 摇盒提示(json)
        self.exceed_tips = ""  # 超出次数提示
        self.shakebox_tips_num = 0  # 摇盒提示次数
        self.freight_price = 0  # 运费价格
        self.deliver_explain = ""  # 发货说明
        self.is_home_page_notice = 0  # 是否开启首页中奖公告（0否1是）
        self.is_prize_retain = 0  # 是否开启奖品保留期
        self.prize_retain_day = 0  # 奖品保留期天数
        self.is_num_free_shipping = 0  # 是否开启满件包邮
        self.free_shipping_count = 0  # 包邮件数
        self.is_amount_free_shipping = 0  # 是否开启满金额包邮
        self.free_shipping_amount = 0  # 包邮金额
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 更新时间

    @classmethod
    def get_field_list(self):
        return ['id', 'act_name', 'act_type', 'theme_id', 'is_open', 'close_word', 'share_desc', 'skin_desc', 'menu_desc', 'sort_index', 'is_del', 'shakebox_tips', 'exceed_tips', 'shakebox_tips_num', 'freight_price', 'deliver_explain', 'is_home_page_notice', 'is_prize_retain', 'prize_retain_day', 'is_num_free_shipping', 'free_shipping_count', 'is_amount_free_shipping', 'free_shipping_amount', 'create_date', 'modify_date']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "act_info_tb"
    