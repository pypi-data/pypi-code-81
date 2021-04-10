from django.db import models
from django.db import connections
from django.core import management


class ReportBulilderFieldManager(models.Manager):
    def create_simple(self, **kwargs):
        using = kwargs.get('using', None)
        if not 'METADATOS' in using:
            connection_number = using.split('-')[0]
            using = '%s-METADATOS' % connection_number

        table_name = kwargs.get('table_name', '')
        field_name = kwargs.get('field_name', '')
        field_alias = kwargs.get('field_alias', '')
        datatype = kwargs.get('datatype', '')

        curs = connections[using].cursor()
        curs.execute("select count(*) from rb_field where table_name = '%s'  and field_name = '%s'" % (table_name, field_name))
        existe = curs.fetchall()[0][0] > 0

        if not existe:
            sql = """
                INSERT INTO rb_field (table_name, field_name, field_alias, datatype, selectable, searchable, sortable, autosearch, mandatory) \
                        VALUES (%s, %s, %s, %s, 'T', 'T', 'T', 'F', 'F')
                """

            values_data = [table_name, field_name, field_alias, datatype]
            curs = connections[using].cursor()
            curs.execute(sql, values_data)
            management.call_command('syncdb', database=using, interactive=False)

    def get_by_natural_key(self, table_name,  field_name):
        return self.get(table_name=table_name, field_name=field_name)


class ReportBulilderFieldBase(models.Model):
    objects = ReportBulilderFieldManager()
    table_name = models.CharField(max_length=60, db_column='table_name')
    field_name = models.CharField(max_length=60, db_column='field_name')
    field_alias = models.CharField(max_length=60, db_column='field_alias')
    datatype = models.CharField(max_length=60, db_column='datatype')

    selectable = models.CharField(max_length=1, db_column='selectable')
    searchable = models.CharField(max_length=1, db_column='searchable')
    sortable = models.CharField(max_length=1, db_column='sortable')
    autosearch = models.CharField(max_length=1, db_column='autosearch')
    mandatory = models.CharField(max_length=1, db_column='mandatory')

    class Meta:
        db_table = u'rb_field'
        abstract = True
        managed= False
        app_label='models_base'
        unique_together = (('table_name', 'field_name'),)


class ReportBulilderTableManager(models.Manager):
    def create_simple(self, **kwargs):
        using = kwargs.get('using', None)
        if not 'METADATOS' in using:
            connection_number = using.split('-')[0]
            using = '%s-METADATOS' % connection_number

        table_name = kwargs.get('table_name', '')
        table_alias = kwargs.get('table_alias', '')

        curs = connections[using].cursor()
        curs.execute("select count(*) from rb_table where table_name = '%s'" % table_name)
        existe = curs.fetchall()[0][0] > 0

        if not existe:
            sql = """
                INSERT INTO rb_table (table_name, table_alias) \
                        VALUES (%s, %s)
                """

            values_data = [table_name, table_alias]
            curs = connections[using].cursor()
            curs.execute(sql, values_data)
            management.call_command('syncdb', database=using, interactive=False)

    def get_by_natural_key(self, table_name):
        return self.get(table_name=table_name)


class ReportBulilderTableBase(models.Model):
    objects = ReportBulilderTableManager()
    table_name = models.CharField(max_length=60, db_column='table_name')
    table_alias = models.CharField(max_length=60, db_column='table_alias')

    class Meta:
        db_table = u'rb_table'
        abstract = True
        managed= False
        app_label='models_base'
        unique_together = (('table_name'),)


class ReportBulilderJoinManager(models.Manager):
    def create_simple(self, **kwargs):
        using = kwargs.get('using', None)
        if not 'METADATOS' in using:
            connection_number = using.split('-')[0]
            using = '%s-METADATOS' % connection_number

        table_name1 = kwargs.get('table_name1', '')
        table_name2 = kwargs.get('table_name2', '')
        join_type = kwargs.get('join_type', '')
        field_names1 = kwargs.get('field_names1', '')
        operators = kwargs.get('operators', '')
        field_names2 = kwargs.get('field_names2', '')

        curs = connections[using].cursor()
        curs.execute("select count(*) from rb_join where table_name1 = '%s' and table_name2 = '%s'" % (table_name1, table_name2))
        existe = curs.fetchall()[0][0] > 0

        if not existe:
            sql = """
                INSERT INTO rb_join (table_name1, table_name2, join_type, field_names1, operators, field_names2) \
                        VALUES (%s, %s, %s, %s, %s, %s)
                """
            values_data = [table_name1, table_name2, join_type, field_names1, operators, field_names2]
            curs = connections[using].cursor()
            curs.execute(sql, values_data)
            management.call_command('syncdb', database=using, interactive=False)

    def get_by_natural_key(self, table_name1, table_name2):
        return self.get(table_name1=table_name1, table_name2=table_name2)


class ReportBulilderJoinBase(models.Model):
    objects = ReportBulilderJoinManager()
    table_name1 = models.CharField(max_length=60, db_column='table_name1')
    table_name2 = models.CharField(max_length=60, db_column='table_name2')
    field_names1 = models.CharField(max_length=255, db_column='field_names1')
    join_type = models.CharField(max_length=60, db_column='join_type')
    operators = models.CharField(max_length=60, db_column='operators')
    field_names2 = models.CharField(max_length=255, db_column='field_names2')

    class Meta:
        db_table = u'rb_join'
        abstract = True
        managed= False
        app_label='models_base'
        unique_together = (('table_name1', 'table_name2',),)
