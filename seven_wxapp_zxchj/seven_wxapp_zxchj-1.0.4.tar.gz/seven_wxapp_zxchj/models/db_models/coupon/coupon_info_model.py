
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class CouponInfoModel(BaseModel):
    def __init__(self, db_connect_key='db_wxapp', sub_table=None, db_transaction=None, context=None):
        super(CouponInfoModel, self).__init__(CouponInfo, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction
        self.db.context = context

    #方法扩展请继承此类
    
class CouponInfo:

    def __init__(self):
        super(CouponInfo, self).__init__()
        self.id = 0  # 优惠券标识
        self.act_id = 0  # 活动标识
        self.coupon_name = ""  # 优惠券名称
        self.scene_type = 0  # 使用场景(1普发2兑换)
        self.coupon_type = 0  # 优惠券类型(1无门槛劵2满减劵3折扣劵)
        self.discount_amount = 0  # 优惠金额（单位：元）
        self.use_amount = 0  # 使用门槛（单位：元）
        self.discount_value = 0  # 折扣力度(几折)
        self.effective_start_date = "1900-01-01 00:00:00"  # 有效开始时间
        self.effective_end_date = "1900-01-01 00:00:00"  # 有效结束时间
        self.rule_desc = ""  # 规则说明
        self.total_num = 0  # 发放数量
        self.draw_num = 0  # 领取数量
        self.get_limit = 0  # 领取限制数量
        self.is_appoint_machine = 0  # 是否指定中盒 0 否 1 是
        self.remarks = ""  # 备注
        self.is_release = 0  # 是否发布（1发布0未发布）
        self.create_date = "1900-01-01 00:00:00"  # 创建时间
        self.modify_date = "1900-01-01 00:00:00"  # 修改时间
        self.is_del = 0  # 是否删除 0 否 1 是
        self.qrcode_img = ""  # 小程序二维码图

    @classmethod
    def get_field_list(self):
        return ['id', 'act_id', 'coupon_name', 'scene_type', 'coupon_type', 'discount_amount', 'use_amount', 'discount_value', 'effective_start_date', 'effective_end_date', 'rule_desc', 'total_num', 'draw_num', 'get_limit', 'is_appoint_machine', 'remarks', 'is_release', 'create_date', 'modify_date', 'is_del', 'qrcode_img']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "coupon_info_tb"
    