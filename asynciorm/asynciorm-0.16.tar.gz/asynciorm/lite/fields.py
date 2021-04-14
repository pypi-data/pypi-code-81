from ..base.fields import (
    BaseIntegerField,
    BaseAutoIncrementField,
    BaseCharField,
    BaseTextField,
    BaseBooleanField,
    BaseDateTimeField,
    BaseForeignKeyField,
    BaseFloatField,
)


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


class ForeignKeyField(BaseForeignKeyField):

    @property
    def _datatype(self):
        return ' INTEGER '
