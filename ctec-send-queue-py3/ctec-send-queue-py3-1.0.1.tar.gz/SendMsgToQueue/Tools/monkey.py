# coding: utf-8
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.constants import CharacterSet


def patch_mysql_connector():
    """
    兼容ZDAAS，去掉官方connector中设置字符集的代码
    :return:
    """
    MySQLConnectionAbstract.set_charset_collation = _set_charset_collation


def _set_charset_collation(self, charset=None, collation=None):
    if charset:
        if isinstance(charset, int):
            self._charset_id = charset
            (self._charset_id, charset_name, collation_name) = \
                CharacterSet.get_charset_info(charset)
        elif isinstance(charset, str):
            (self._charset_id, charset_name, collation_name) = \
                CharacterSet.get_charset_info(charset, collation)
        else:
            raise ValueError(
                    "charset should be either integer, string or None")
    elif collation:
        (self._charset_id, charset_name, collation_name) = \
            CharacterSet.get_charset_info(collation=collation)

    try:
        # Required for C Extension
        self.set_character_set_name(charset_name)  # pylint: disable=E1101
    except AttributeError:
        # Not required for pure Python connection
        pass

    if self.converter:
        self.converter.set_charset(charset_name)
