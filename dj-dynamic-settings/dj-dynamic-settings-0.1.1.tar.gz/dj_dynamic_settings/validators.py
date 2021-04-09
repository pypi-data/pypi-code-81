from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.module_loading import import_string
from rest_framework.utils.humanize_datetime import humanize_strptime


class TypeValidator(object):
    message = "'{value}' not an instance of one of classes '{types}'."

    def __init__(self, *types):
        assert types, "At least one class has to be provided."
        self.types = types

    def __call__(self, value):
        if not isinstance(value, self.types):
            raise ValidationError(self.message.format(value=value, types=self.types))


class ModulePathValidator(object):
    message = "{path} not a valid module path."

    def __call__(self, value):
        try:
            import_string(value)
        except ImportError:
            raise ValidationError(self.message.format(path=value))


class DateTimeValidator(object):
    message = "DateTime format does not match. DateTime: {value} Format: {dformat}"

    def __init__(self, date_time_format):
        assert date_time_format, "Datetime format has to be provided."
        self.date_time_format = date_time_format

    def __call__(self, value):
        try:
            datetime.strptime(value, self.date_time_format)
        except ValueError:
            date_time_format = humanize_strptime(self.date_time_format)
            raise ValidationError(
                self.message.format(value=value, dformat=date_time_format)
            )


class SerializerValidator(object):
    def __init__(self, serializer_class, serializer_kwargs=None):
        self.serializer_class = serializer_class
        self.serializer_kwargs = serializer_kwargs or {}

    def __call__(self, value):
        serializer = self.serializer_class(data=value, **self.serializer_kwargs)
        serializer.is_valid(raise_exception=True)
