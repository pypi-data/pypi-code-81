import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin


class RelatedEntity(mongoengine.DynamicEmbeddedDocument):
    disease = mongoengine.ListField(mongoengine.StringField(), verbose_name="疾病")
    insurance_product = mongoengine.ListField(
        mongoengine.StringField(), verbose_name="产品"
    )
    insurance_company = mongoengine.ListField(
        mongoengine.StringField(), verbose_name="公司"
    )
    professional_vocabulary = mongoengine.ListField(
        mongoengine.StringField(), verbose_name="专业词"
    )


class Portrait(mongoengine.DynamicEmbeddedDocument):
    entity = mongoengine.EmbeddedDocumentField(RelatedEntity, verbose_name="实体")
    intent = mongoengine.ListField(mongoengine.StringField(), verbose_name="意图")


class Knowledge(mongoengine.DynamicDocument, MultiDatabaseMixin):
    """
    对接知识中心，通用的knowledge。
    Doc@ https://shimo.im/docs/YpywJpc6DrGVgXGr
    """

    id = mongoengine.StringField(verbose_name="id", primary_key=True, max_length=100)
    title = mongoengine.StringField(verbose_name="标题", default="")
    alias = mongoengine.ListField(
        mongoengine.StringField(), verbose_name="别名", default=list
    )
    type = mongoengine.StringField(verbose_name="类型", default="")
    topic = mongoengine.StringField(verbose_name="空间", default="")
    labels = mongoengine.ListField(mongoengine.StringField(), verbose_name="标签")
    content = mongoengine.StringField(verbose_name="内容")

    continue_page = mongoengine.ListField(
        mongoengine.StringField(), verbose_name="相关页面"
    )

    priority = mongoengine.IntField(verbose_name="访问优先级（人工设置）")
    can_be_copied = mongoengine.BooleanField(verbose_name="是否能被复制")
    heat = mongoengine.IntField(verbose_name="热度（自动统计）")

    is_searchable = mongoengine.BooleanField(verbose_name="是否可被搜索")

    update_time = mongoengine.DateTimeField(verbose_name="更新时间")

    portrait = mongoengine.EmbeddedDocumentField(Portrait, verbose_name="画像信息")

    def __str__(self):
        return self.title

    meta = {
        "collection": "knowledge",
        "abstract": True,
    }
