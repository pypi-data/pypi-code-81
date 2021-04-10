#encoding:utf-8
from django.db import models
from datetime import datetime

class BancoBase(models.Model):
    BANCO_ID = models.AutoField(primary_key=True, db_column='BANCO_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    rfc = models.CharField(max_length=30, db_column='RFC')

    class Meta:
        db_table = u'bancos'
        abstract = True
        managed= False
        app_label='models_base'