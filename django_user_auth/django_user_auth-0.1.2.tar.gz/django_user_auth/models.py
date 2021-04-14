from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.
    Username and password are required. Other fields are optional.
    """
    mobile = models.CharField('手机号',null=True,blank=True, max_length=14)
    is_ad_account = models.BooleanField('启用域用户登录', default=False)
    def __str__(self):
        return self.username+'-'+self.first_name
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
        db_table = "auth_user"



class OperationLog(models.Model):
    qual_name=models.CharField(max_length=200)
    user_id=models.CharField(max_length=200)
    operated=models.DateTimeField(auto_now=True,null=True)
    opeart_contect=models.CharField(max_length=4000,null=True)
    error_code=models.CharField(max_length=4000,null=True)
    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'
        db_table = "Log_Operation"
