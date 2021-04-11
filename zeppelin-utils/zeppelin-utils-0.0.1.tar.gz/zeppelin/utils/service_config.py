from typing import Dict
from typing import Optional

import os


def is_production() -> bool:
    return _get_environment() == 'prod'


def is_stage() -> bool:
    return _get_environment() == 'stage'


def get_version() -> Optional[str]:
    return os.environ.get('SL_VERSION')


def get_version_short() -> Optional[str]:
    version = get_version()
    if version is None:
        return version
    image = version.split('/')[-1]
    return image


def get_info() -> Dict[str, Optional[str]]:
    return {'version': get_version(), 'environment': _get_environment()}


def _get_environment() -> Optional[str]:
    return os.environ.get('SL_ENVIRONMENT')
