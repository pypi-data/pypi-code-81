from .fields import Field
import re
import inflect

engine = inflect.engine()


class Model:
    __tablename__ = None

    @property
    def _fields(self):
        return {key: value for key, value in type(self).__dict__.items() if isinstance(value, Field)}

    @property
    def _names_fields(self):
        return tuple(
            key + '_id' if value.is_fk else key for key, value in type(self).__dict__.items() if
            isinstance(value, Field))

    @property
    def table_name(self):
        return self.__tablename__ if self.__tablename__ else engine.plural('_'.join(
            map(str.lower, re.findall('[A-Z][a-z]*', self.__class__.__name__))))
