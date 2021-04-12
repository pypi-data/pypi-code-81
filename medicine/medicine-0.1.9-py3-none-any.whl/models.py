import logging

from DjangoAppCenter.extensions.fields.snowflake import SnowFlakeField
from django.db import models
from pypinyin import Style, lazy_pinyin

logger = logging.getLogger('db-monitor')


class SnowFlakeIdentifiedModel(models.Model):
    id = SnowFlakeField(primary_key=True, db_column="id", editable=False)

    class Meta:
        abstract = True

    def to_dict(self):
        _dict = dict.copy(self.__dict__)
        del _dict["_state"]
        _dict["id"] = str(_dict["id"])
        return _dict


class MetaBasic(SnowFlakeIdentifiedModel):
    """
    身份标识模型，mid作为全局的统一UUID
    名称，通用名称，缩写，全拼
    """
    REQUIRED_KEYS = ('name', 'abbreviation', 'spec', 'dosage_unit',
                     'pack_unit', 'manufacture',
                     'approval_number', 'barcode', 'ro', 'function', 'brand')

    name = models.CharField(verbose_name="名称", max_length=255)
    abbreviation = models.CharField(
        verbose_name="首字母缩写", max_length=255, null=True, blank=True, editable=False)
    pinyin = models.CharField(
        verbose_name="拼音全拼", max_length=255, null=True, blank=True, editable=False)
    data_source = models.CharField(
        verbose_name="数据来源", null=True, blank=True, max_length=512, editable=False)
    update_time = models.DateTimeField(verbose_name="数据更新时间", auto_now=True)
    data_completion = models.FloatField(verbose_name="数据完整度", default=0, null=True, blank=True, editable=False)

    class Meta:
        abstract = True

    def compute_pinyin(self):
        """
        计算拼音缩写及拼音全拼，用于对数据进行搜索相关的处理
        """
        if not self.name:
            return

        self.abbreviation = ''.join(lazy_pinyin(
            self.name, style=Style.FIRST_LETTER, errors='ignore')).upper()[0:255]  # 0-255截断 以防太长
        self.pinyin = ''.join(lazy_pinyin(self.name, errors='ignore'))[0:255]

        if not self.abbreviation:
            self.abbreviation = self.name

        if not self.pinyin:
            self.pinyin = self.name

    def save(self):
        self.compute_pinyin()
        if hasattr(self, 'data_source'):
            if not self.data_source:
                self.data_source = "人工录入"
        try:
            super().save()
        except Exception as e:
            logger.error(f"{str(e)}")


class Medicine(MetaBasic):
    """基础药品信息描述 
    基础字段 不可或缺: 名规厂号剂类码功图书
    """
    spec = models.CharField(
        verbose_name="规格", max_length=255, null=True, blank=True)

    # 最小规格理论上是可计算的, 可以由spec生成
    dosage_unit = models.CharField(
        verbose_name="剂量单位", max_length=255, null=True, blank=True)

    preparation = models.CharField(
        verbose_name="剂型", max_length=255, null=True, blank=True)
    pack_unit = models.CharField(
        verbose_name="包装单位", max_length=255, null=True, blank=True)
    manufacture = models.CharField(
        verbose_name="生产厂家", max_length=255, null=True, blank=True)
    approval_number = models.CharField(
        verbose_name="批准文号", max_length=255, null=True, blank=True)
    barcode = models.CharField(
        verbose_name="条形码", max_length=255, null=True, blank=True)
    # 处方与非处方分类
    ro = models.CharField(verbose_name="处方级别", max_length=64, default='尚不明确',
                          choices=(('处方', '处方'), ('非处方', '非处方'),
                                   ('甲类非处方', '甲类非处方'),
                                   ('乙类非处方', '乙类非处方'), ('尚不明确', '尚不明确')), null=True)

    function = models.TextField(verbose_name="功能主治", null=True, blank=True)

    brand = models.CharField(
        verbose_name="品牌", max_length=255, null=True, blank=True)
    brand_abbreviation = models.CharField(
        verbose_name="首字母缩写", max_length=255, null=True, blank=True, editable=False)
    brand_pinyin = models.CharField(
        verbose_name="拼音全拼", max_length=255, null=True, blank=True, editable=False)

    storage = models.CharField(
        verbose_name="贮藏", max_length=255, null=True, blank=True)
    origin = models.CharField(
        verbose_name="产地", max_length=255, null=True, blank=True)

    # 药品的分类标签, 用逗号分隔
    tag = models.CharField(verbose_name="标签", null=True, blank=True, max_length=512)

    # 商品名称字段在主题定义中已被移除!
    # 商品名称往往是 通用名称+品牌名称 的组合, 或者 奇怪的自定义名字
    prod_name = models.CharField(
        verbose_name="商品名称", max_length=255, null=True, blank=True)

    expiration = models.CharField(
        verbose_name="有效期", max_length=255, null=True, blank=True)

    dosage = models.TextField(verbose_name="用法用量", max_length=600, null=True, blank=True)

    def __str__(self):
        return self.name

    def compute_brand_pinyin(self):
        """
        计算品牌拼音缩写及拼音全拼，用于对数据进行搜索相关的处理
        """
        if not self.brand:
            return

        self.brand_abbreviation = ''.join(lazy_pinyin(
            self.brand, style=Style.FIRST_LETTER, errors='ignore')).upper()[0:255]  # 0-255截断 以防太长
        self.brand_pinyin = ''.join(lazy_pinyin(self.brand, errors='ignore'))[0:255]

        if not self.brand_abbreviation:
            self.brand_abbreviation = self.brand

        if not self.brand_pinyin:
            self.brand_pinyin = self.brand

    def compute_completion(self):
        """计算基础信息完整度及丰富度
        """
        # 计算数据完整度
        empty_key = 0
        for key in self.REQUIRED_KEYS:
            value = self.__dict__.get(key, None)
            if not value:
                empty_key += 1

        if self.images.all().count() == 0:
            empty_key += 1

        if self.instructions.all().count() == 0:
            empty_key += 1

        completion = 1 - empty_key / (len(self.REQUIRED_KEYS) + 2)

        self.data_completion = round(completion, 2)

    def save(self):
        self.compute_brand_pinyin()
        self.compute_completion()
        super().save()

    class Meta:
        verbose_name = "药品"
        verbose_name_plural = "药品"
        db_table = "medicine"
        app_label = "medicine"


class Image(SnowFlakeIdentifiedModel):
    medicine = models.ForeignKey(Medicine,
                                 verbose_name="关联药品",
                                 related_name="images",
                                 related_query_name="medicine",
                                 db_constraint=False,
                                 to_field="id",
                                 db_column="medicine_id",
                                 on_delete=models.CASCADE)
    file = models.ImageField(verbose_name="文件")
    url = models.CharField(verbose_name="图片链接", editable=False, max_length=512)
    order = models.IntegerField(verbose_name="排序", default=0)
    description = models.CharField(verbose_name="描述", max_length=32, blank=True, null=True)

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.url = self.file.url
        super().save(*args, **kwargs)
        self.medicine.save()

    class Meta:
        verbose_name = "药品图片"
        verbose_name_plural = "药品图片"
        db_table = "image"
        app_label = "medicine"


class Instruction(SnowFlakeIdentifiedModel):
    medicine = models.ForeignKey(Medicine,
                                 verbose_name="关联药品",
                                 related_name="instructions",
                                 related_query_name="medicine",
                                 db_constraint=False,
                                 to_field="id",
                                 db_column="medicine_id",
                                 on_delete=models.CASCADE)
    key = models.CharField(verbose_name="选项名称", null=False, blank=False, max_length=64)
    value = models.TextField(verbose_name="选项内容", null=False, blank=False)
    order = models.IntegerField(verbose_name="排序编号", default=0)

    def __str__(self):
        return f"{self.key} [{self.id}]"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.medicine.save()

    class Meta:
        verbose_name = "药品说明书"
        verbose_name_plural = "药品说明书"
        db_table = "instruction"
        app_label = "medicine"
