from django.db import models


class WeChatResponseMaterial(models.Model):
    user_name = models.CharField(max_length=32, null=True, blank=True)

    """
    {1: 文字链接}
    """
    material_type = models.IntegerField()
    title = models.CharField(max_length=255, null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    state = models.BooleanField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_response_material'


class WeChatResponseEvent(models.Model):
    material_id = models.IntegerField()
    user_name = models.CharField(max_length=32, null=True, blank=True)

    """
    {1: 文本, 2: 参数二维码}
    """
    event_type = models.IntegerField()

    title = models.CharField(max_length=255)
    event_key = models.CharField(max_length=100)
    qrcode_ticket = models.TextField(null=True, blank=True)
    qrcode_url = models.TextField(null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    state = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_response_event'


class WeChatQrcode(models.Model):
    unionid = models.CharField(max_length=32)
    scene_str = models.JSONField()
    ticket = models.TextField(null=True, default='')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wechat_qrcode'
