from django.db import models
from ...models_base.metadatos.report_builder import *


class ReportBulilderField(ReportBulilderFieldBase):
    def __unicode__(self):
        return u'%s - %s' % (self.table_name, self.field_name)

    def natural_key(self):
        return (self.table_name, self.field_name)


class ReportBulilderTable(ReportBulilderTableBase):
    def __unicode__(self):
        return self.table_name


class ReportBulilderJoin(ReportBulilderJoinBase):
    def __unicode__(self):
        return u'%s - %s' % (self.table_name1, self.table_name2)

    def natural_key(self):
        return (self.table_name1, self.table_name2)
