import hashlib

import mongoengine

from insnail_ai_tools.mongodb.mixin import MultiDatabaseMixin


class OntologyDisease(mongoengine.DynamicDocument, MultiDatabaseMixin):
    """
    疾病库
    """

    id = mongoengine.StringField(verbose_name="ID", primary_key=True)
    is_audited = mongoengine.BooleanField(verbose_name="是否审核过", default=False)
    name = mongoengine.StringField(verbose_name="名称")
    alias = mongoengine.ListField(mongoengine.StringField(), verbose_name="别称")
    alias_search = mongoengine.StringField(verbose_name="用来搜索的别称")

    class_first = mongoengine.StringField(verbose_name="疾病大类")
    class_second = mongoengine.StringField(verbose_name="疾病中类")

    description = mongoengine.StringField(verbose_name="疾病介绍")

    questions = mongoengine.ListField(mongoengine.StringField(), verbose_name="询问问题")
    recommend_product_list = mongoengine.ListField(
        mongoengine.StringField(), verbose_name="推荐产品列表"
    )
    recommend_reason = mongoengine.StringField(verbose_name="推荐理由")

    meta = {
        "collection": "ontology_disease",
        "indexes": ["name", "alias", "is_audited", "#class_first", "#class_second"],
        "unique": [("class_first", "class_second", "name")],
        "verbose_name": "疾病核保库",
        "abstract": True,
    }

    def __str__(self):
        return f"{self.class_first}-{self.class_second}-{self.name}"

    def save(self, **kwargs):
        self.alias_search = ",".join(self.alias)
        super().save(**kwargs)

    @classmethod
    def gen_id(cls, name: str):
        hash_name = hashlib.md5(name.encode()).hexdigest()
        return f"disease_{hash_name}"
