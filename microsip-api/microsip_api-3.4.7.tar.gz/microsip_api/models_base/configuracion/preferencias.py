#encoding:utf-8
from django.db import models

class RegistryBase(models.Model):
    id = models.AutoField(primary_key=True, db_column='ELEMENTO_ID')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    tipo = models.CharField(max_length=1, db_column='TIPO')
    padre = models.ForeignKey('self', related_name='padre_a',on_delete=models.CASCADE)
    valor = models.CharField(default='', blank = True, null = True, max_length=100, db_column='VALOR')

    class Meta:
        db_table = u'registry'
        abstract = True
        managed= False
        app_label='models_base'

    def __unicode__(self):
        return u'%s' % self.nombre
    
    def get_value(self):
        if self.valor == '':
            return None
        return u"%s"%self.valor
        