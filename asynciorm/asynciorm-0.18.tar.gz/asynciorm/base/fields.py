from abc import ABC
import inspect
from ..exceptions import ValidateError
import types
from datetime import datetime
from decimal import Decimal

CASCADE = ' CASCADE '
SET_NULL = ' SET NULL '
RESTRICT = ' RESTRICT '


class Field:

    def __init__(self, null=False, default=None, unique=False):
        self._null = null
        self._default = default
        self._unique = unique

    def _to_sql_column(self, column_name):
        return f'{column_name}{self._datatype}{" PRIMARY KEY " if getattr(self, "_primary_key", None) else ""}{"" if self._null else " NOT NULL "}{" UNIQUE " if self._unique else ""}'

    def sql_dump(self, value):
        if callable(value):
            return f"'{value()}'"
        return f"'{value}'"

    def sql_load(self, value):
        return value

    @property
    def default_value(self):
        return self._default

    @property
    def type(self):
        return self.__class__.__name__

    @property
    def is_nullable(self):
        return self._null

    @property
    def is_fk(self):
        return False

    @property
    def is_primary_key(self):
        return False

    @property
    def _datatype(self):
        raise NotImplementedError()


class BaseIntegerField(Field, ABC):

    @property
    def _datatype(self):
        return ' INTEGER '


class BaseAutoIncrementField(BaseIntegerField, ABC):

    def __init__(self, primary_key=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._primary_key = primary_key

    @property
    def _datatype(self):
        return ' INTEGER '

    @property
    def is_primary_key(self):
        return True


class BaseFloatField(Field, ABC):
    
    def sql_load(self, value):
        return float(value) if value is not None else value


class BaseCharField(Field, ABC):

    def __init__(self, max_length=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._max_length = max_length

    @property
    def _datatype(self):
        return f' VARCHAR({self._max_length}) '


class BaseTextField(Field, ABC):

    async def _to_sql_value(self, value):
        return f'"{value}"'

    @property
    def _datatype(self):
        return ' TEXT '


class BaseBooleanField(Field, ABC):
    pass


class BaseDateTimeField(Field, ABC):

    def __init__(self, format='%Y-%d-%m %H:%M:%S', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._format = format

    def sql_load(self, value):
        return datetime.strptime(value, self._format)

    def sql_dump(self, value):
        if callable(value):
            return f"'{value().strftime(self._format)}'"
        return f"'{value.strftime(self._format)}'"


class BaseDateField(BaseDateTimeField, ABC):
    def __init__(self, format='%Y-%d-%m', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._format = format


class BaseTimeField(BaseDateTimeField, ABC):
    def __init__(self, format='%H:%M:%S', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._format = format


class BaseForeignKeyField(Field, ABC):
    def __init__(self, related_model, on_delete=CASCADE, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not inspect.isclass(related_model):
            raise ValueError('Must be class')
        self._related_model = object.__new__(related_model)
        self._on_delete = on_delete

    def _to_sql_column(self, column_name):
        return super()._to_sql_column(column_name + '_id')

    def sql_dump(self, value):
        return str(value) if isinstance(value, int) else str(getattr(value, [key for key, field in value._fields.items() if
                                                                    field.is_primary_key][0]))

    def _get_related_autoincrement_field_name(self):
        for field_name, field in self._related_model._fields.items():
            if field.is_primary_key:
                return field_name

    def _create_fk(self, column_name):
        return f' FOREIGN KEY({column_name + "_id"}) REFERENCES {self._related_model.table_name}({self._get_related_autoincrement_field_name()}) ON DELETE {self._on_delete}'

    @property
    def is_fk(self):
        return True
