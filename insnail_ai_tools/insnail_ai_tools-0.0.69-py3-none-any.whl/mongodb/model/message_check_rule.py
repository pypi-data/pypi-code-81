import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin, StrChoicesMixin
from insnail_ai_tools.mongodb.model.wecom.wecom_personal_messge import UserRoleChoices


class RuleContentTypeChoices(StrChoicesMixin):
    text = "text"
    weapp = "weapp"
    link = "link"
    file = "file"
    image = "image"
    voice = "voice"
    record = "record"
    meeting_voice = "meeting_voice"
    all = "all"


class RuleMeta(mongoengine.EmbeddedDocument):
    rule = mongoengine.StringField(verbose_name="规则")
    note = mongoengine.StringField(verbose_name="备注")


class NotifyModeChoices(StrChoicesMixin):
    """
    选择realtime就是，实时通知到质检，self的那个就是会通知到说话的本人。record就是单纯的记录
    """

    REAL_TIME = "REAL_TIME"
    SELF_NOTIFY = "SELF_NOTIFY"
    RECORD = "RECORD"


class MessageCheckRule(mongoengine.DynamicDocument, MultiDatabaseMixin):
    content_type = mongoengine.StringField(
        verbose_name="内容的类型",
        choices=RuleContentTypeChoices.choices(),
        max_length=50,
        default=RuleContentTypeChoices.all,
        help_text="内容的类型，比如文本，link, 如果填写ALL，则对所有类型对话检查",
    )
    role = mongoengine.StringField(
        verbose_name="检查对象", choices=UserRoleChoices.choices(), help_text="检查对象，即说话的对象"
    )
    level = mongoengine.IntField(
        verbose_name="风险等级", default=1, help_text="风险等级，等级越高越紧急"
    )
    notify_mode = mongoengine.StringField(
        verbose_name="通知方式",
        choices=NotifyModeChoices.choices(),
        default=NotifyModeChoices.RECORD,
    )
    is_legal = mongoengine.BooleanField(
        verbose_name="是否合法", default=False, help_text="如果为True，则相当于白名单"
    )
    illegal_type = mongoengine.StringField(
        verbose_name="违规类型", max_length=100, help_text="违规类型，比如跳单"
    )
    note = mongoengine.StringField(verbose_name="备注")
    notice_text = mongoengine.StringField(verbose_name="通知文本")

    rule_type = mongoengine.StringField(
        verbose_name="规则类型",
        choices=(("REGEX", "REGEX"), ("SUBSTRING", "SUBSTRING")),
    )
    rule_list = mongoengine.ListField(
        mongoengine.EmbeddedDocumentField(RuleMeta), verbose_name="规则列表"
    )
    exclude_rule_list = mongoengine.ListField(
        mongoengine.EmbeddedDocumentField(RuleMeta),
        verbose_name="除外规则列表",
    )
    exclude_black_user_id = mongoengine.BooleanField(
        verbose_name="剔除违禁微信名单", default=False
    )

    meta = {
        "collection": "message_check_rule",
        "indexes": [
            "content_type",
            "role",
            "level",
            "is_legal",
            "illegal_type",
            "rule_type",
            "exclude_black_user_id",
        ],
        "abstract": True,
    }

    def __str__(self):
        return f"{self.content_type}_{self.illegal_type}_{self.role}"


class WecomUserExtraInfo(mongoengine.DynamicDocument, MultiDatabaseMixin):
    """
    用户额外信息的库，一般在质检中用到，比如收集用户个人的微信号、手机号等
    """

    user_id = mongoengine.StringField(verbose_name="用户ID", primary_key=True)
    user_name = mongoengine.StringField(verbose_name="用户名称")
    phone_number = mongoengine.StringField(verbose_name="手机号")
    black_wechat_id = mongoengine.ListField(
        mongoengine.StringField(), verbose_name="违禁微信列表"
    )

    meta = {
        "collection": "wecom_user_extra_info",
        "indexes": ["#user_name", "#phone_number"],
        "abstract": True,
    }
