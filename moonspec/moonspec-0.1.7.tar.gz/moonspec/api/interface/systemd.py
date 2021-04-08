import datetime
import logging
import math
import shutil
import subprocess
from typing import Union, List, Dict, Any

LOGGER = logging.getLogger('moonspec')

_systemd_state_date_val = {
    'ExecMainStartTimestamp',
    'StateChangeTimestamp',
    'InactiveExitTimestamp',
    'ActiveEnterTimestamp',
    'ConditionTimestamp',
    'AssertTimestamp',
}


def _normalize_systemd_value(value: str) -> Union[str, bool, int, float, None, List, Dict]:
    if 'yes' == value or 'success' == value:
        return True

    if 'no' == value or 'failure' == value:
        return False

    if 0 == len(value) or '[not set]' == value or '[no data]' == value or 'none' == value \
            or '[n/a]' == value or '(null)' == value:
        return None

    if 'infinity' == value:
        return math.inf

    if '0' == value:
        return 0

    if value.isdigit() and value[0] != '0':
        return int(value)

    if value.startswith('{'):
        v_lines = value[1:-1].split(' ; ')
        v_object = {}

        for v_line in v_lines:
            (k, v) = v_line.split('=', 1)
            v_object[k.strip()] = _normalize_systemd_value(v.strip())

        return v_object

    return value


def _try_parse_systemd_date(value: str) -> Union[datetime.datetime, str]:
    # noinspection PyBroadException
    try:
        return datetime.datetime.strptime(value, '%a %Y-%m-%d %H:%M:%S %Z')
    except:
        return value


class SystemdApi:
    """
    Interface to SystemD
    """

    @staticmethod
    def is_supported() -> bool:
        """
        Check if SystemD is supported on this host

        :return: True if supported, False otherwise
        """
        return shutil.which('systemctl') is not None

    @staticmethod
    def show(service: str) -> Dict[str, Any]:
        if not SystemdApi.is_supported():
            return {}

        cmd = ['systemctl', 'show', '--all', '--no-page', service]

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE)
        except BaseException as e:
            LOGGER.error('Failed to run systemctl', exc_info=e)
            return {}

        if 0 is not result.returncode:
            return {}

        service_data: Dict[str, Any] = {}

        for line in result.stdout.splitlines(keepends=False):
            (key, value) = line.decode().split('=', maxsplit=1)

            service_data[key] = _normalize_systemd_value(value)

            if key in _systemd_state_date_val:
                service_data[key] = _try_parse_systemd_date(service_data[key])

        return service_data

    @staticmethod
    def is_active(service_name: str) -> bool:
        if not SystemdApi.is_supported():
            return False

        service: Dict[str, Any] = SystemdApi.show(service_name)

        if not service or 'ActiveState' not in service:
            return False

        return service['ActiveState'] == 'active'

    @staticmethod
    def is_enabled(service_name: str) -> bool:
        if not SystemdApi.is_supported():
            return False

        service: Dict[str, Any] = SystemdApi.show(service_name)

        if not service or 'UnitFileState' not in service:
            return False

        return service['UnitFileState'] == 'enabled' or service['UnitFileState'] == 'linked'

    @staticmethod
    def get_service_state(service_name: str) -> Union[None, str]:
        if not SystemdApi.is_supported():
            return None

        service: Dict[str, Any] = SystemdApi.show(service_name)

        if not service or 'ActiveState' not in service:
            return None

        return service['ActiveState']
