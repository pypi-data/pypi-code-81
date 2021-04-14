import platform
from contextlib import contextmanager

from .impl_registry import get_implementation

__all__ = ("adrenaline", "is_sleep_prevented", "prevent_sleep")

_impl = get_implementation()

adrenaline = _impl.prevent_sleep
prevent_sleep = _impl.prevent_sleep
is_sleep_prevented = _impl.is_sleep_prevented
