"""
The `moonspec.api` package contains all public APIs useful for writing specifications.

This package also exports global instance of `moonspec.api.Api` as var `api` for you to use in your spec files to
access APIs various APIs useful for host testing using fluent interfaces, for example,
`api.fs.hash_file('/example.txt')`.

**Basic import**

This import contains all the basic members you might need to write your specifications.

.. code-block:: python

    from moonspec.api import (api, any_of, capture,
                              spec, describe, expect,
                              fact, historic_fact, maybe,
                              apply_to_roles)

"""
from typing import List, Any, Callable, Optional

from moonspec import _MOONSPEC_RUNTIME_STATE
from moonspec.api.fact import Fact, HistoricFact
from moonspec.api.interface.fs import FileSystemApi
from moonspec.api.interface.host import HostApi
from moonspec.api.interface.inet import InetApi
from moonspec.api.interface.ssl import SSLApi
from moonspec.api.subject import Subject, SubjectExpectationException, ComparatorExpectations


class Api:
    def __init__(self) -> None:
        self.host: HostApi = HostApi()  #: Access information related to local host
        self.fs: FileSystemApi = FileSystemApi()  #: Access information related to local file systems
        self.net: InetApi = InetApi()  #: Access network resources
        self.ssl: SSLApi = SSLApi()  #: Query various SSL related items


def capture(key: str = None, roles: List[str] = None) -> Callable[[Callable[[], None]], None]:
    """
    Capture a fact to be used in tests or to be checked for state changes when executing
    specifications with state persistence.

    :param key: globally unique identifier of a fact.
    :param roles: list of zero or more roles this fact should be captured for.
    """

    def __capture_imp(function_ref: Callable[[], None]) -> None:
        capture_key = key
        if capture_key is None:
            if function_ref.__name__.startswith('capture_'):
                capture_key = function_ref.__name__[8:]
            else:
                raise RuntimeError('Capture: decorator key must be set or function name must start with capture_')

        _MOONSPEC_RUNTIME_STATE.register_capture(
            capture_key,
            function_ref,
            set(roles or []).union(_MOONSPEC_RUNTIME_STATE.scope.scope_roles)
        )

    return __capture_imp


def spec(roles: List[str] = None) -> Callable[[Callable[[], None]], None]:
    def __spec_imp(function_ref: Callable) -> None:
        _MOONSPEC_RUNTIME_STATE.register_spec(
            set(roles or []).union(_MOONSPEC_RUNTIME_STATE.scope.scope_roles),
            function_ref
        )

    return __spec_imp


def describe(description: str) -> None:
    _MOONSPEC_RUNTIME_STATE.scope.set_scope_description(description)


def fact(key: str) -> Fact:
    if not _MOONSPEC_RUNTIME_STATE.has_fact(key):
        return Fact(key, None)

    return Fact(key, _MOONSPEC_RUNTIME_STATE.get_fact_value(key))


def historic_fact(key: str) -> HistoricFact:
    if not _MOONSPEC_RUNTIME_STATE.has_historic_fact(key):
        return HistoricFact(key, None)

    return HistoricFact(key, _MOONSPEC_RUNTIME_STATE.get_historic_fact_value(key))


def expect(value: Any, identity: Optional[str] = None) -> Subject:
    return Subject(value, identity=identity)


def maybe(assertion: Callable, *assertion_args: Any) -> bool:
    try:
        assertion(*assertion_args)
        return True
    except Exception as e:
        _MOONSPEC_RUNTIME_STATE.scope.register_soft_failure(e)
        return False


def any_of(*assertions: Callable, description: str = None) -> None:
    for callable_ref in assertions:
        # noinspection PyBroadException
        try:
            callable_ref()
            return
        except:
            continue

    if description is not None:
        raise RuntimeError(description)

    scope_desc = _MOONSPEC_RUNTIME_STATE.scope.get_and_clear_scope_description()

    if scope_desc is not None:
        raise RuntimeError(scope_desc)

    raise RuntimeError('All expectations for any_of failed')


def apply_to_roles(*roles: str) -> None:
    """
    Add given roles to all subsequent facts and specifications, in addition to roles defined per-specification
    or per capture, within the current file (module).

    :param roles: one or more roles
    """
    _MOONSPEC_RUNTIME_STATE.scope.apply_to_roles(set(roles))


api: Api = Api()
