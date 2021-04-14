from asynciorm.base.fields import (
    BaseIntegerField,
    BaseAutoIncrementField,
    BaseCharField,
    BaseTextField,
    BaseBooleanField,
    BaseDateTimeField,
    BaseDateField,
    BaseTimeField,
    BaseForeignKeyField,
    BaseFloatField,
)

__all__ = ['IntegerField', 'ForeignKeyField', 'AutoIncrementField', 'FloatField', 'CharField', 'TextField', 'BooleanField', 'DateTimeField', 'TimeField', 'DateField']

class IntegerField(BaseIntegerField):
    pass


class AutoIncrementField(BaseAutoIncrementField):
    pass


class FloatField(BaseFloatField):

    @property
    def _datatype(self):
        return ' REAL '


class CharField(BaseCharField):
    pass


class TextField(BaseTextField):
    pass


class BooleanField(BaseBooleanField):

    def sql_load(self, value):
        return True if value == 'True' else False

    @property
    def _datatype(self):
        return ' INTEGER '


class DateTimeField(BaseDateTimeField):

    @property
    def _datatype(self):
        return ' VARCHAR(255) '

class TimeField(BaseTimeField):

    @property
    def _datatype(self):
        return ' VARCHAR(255) '

class DateField(BaseDateField):
    
    @property
    def _datatype(self):
        return ' VARCHAR(255) '


class ForeignKeyField(BaseForeignKeyField):

    @property
    def _datatype(self):
        return ' INTEGER '
