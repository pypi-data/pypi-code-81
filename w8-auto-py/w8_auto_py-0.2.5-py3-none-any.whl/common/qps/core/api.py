# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from w8_auto_py.typings import NumberTypes
from w8_auto_py.global_vars import TimeUnit
from w8_auto_py.common.qps import QueryPreSecond


def create_qps(timeout: NumberTypes,
               date_unit: TimeUnit = TimeUnit.MS) -> QueryPreSecond:
    """
    创建 qps
    Args:
        timeout:
        date_unit:

    Returns:

    """
    return QueryPreSecond(timeout, date_unit)
