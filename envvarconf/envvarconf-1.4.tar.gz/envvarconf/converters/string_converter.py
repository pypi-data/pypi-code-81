from envvarconf.converters.base import ConverterBase
from envvarconf.exceptions import VariableConvertException


class StringConverter(ConverterBase):
    """
    Simple convert string representation to value
    """

    def convert(self, value: str, to_type):
        if to_type == bool:
            if value in ['true', 'True', '1']:
                return True
            elif value in ['false', 'False', '0']:
                return False
            else:
                raise VariableConvertException("Bad value for boolean field: '%s'" % value)

        return to_type(value)
