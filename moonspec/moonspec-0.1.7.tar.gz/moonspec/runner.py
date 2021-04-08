import importlib
import importlib.util
import logging
import os
import sys
from enum import Enum
from typing import List, Set, Generator

from moonspec import _MOONSPEC_RUNTIME_STATE
from moonspec.output import Output
from moonspec.state import SpecCaseDefinition

LOGGER = logging.getLogger('moonspec')


class SpecResultState(Enum):
    SUCCESS = 0
    FAILURE = 2
    UNSTABLE = 3


class SpecResult:
    def __init__(
            self,
            spec: SpecCaseDefinition,
            state: SpecResultState,
            error: BaseException = None,
            soft_failures: List[BaseException] = None
    ) -> None:
        self.spec = spec
        self.state = state
        self.error = error
        self.soft_failures = soft_failures


class SpecLog:
    def __init__(self, output: Output) -> None:
        self.results: List[SpecResult] = []
        self.any_failed: bool = False
        self.output = output
        pass

    def register_starting(self, spec: SpecCaseDefinition) -> None:
        self.output.on_spec_start(spec)

    def register_success(self, spec: SpecCaseDefinition) -> None:
        self.results.append(SpecResult(spec, SpecResultState.SUCCESS))
        self.output.on_spec_success(spec)

    def register_failure(self, spec: SpecCaseDefinition, e: BaseException, soft_failures: List[BaseException]) -> None:
        self.any_failed = True
        self.results.append(SpecResult(spec, SpecResultState.FAILURE, error=e, soft_failures=soft_failures))
        self.output.on_spec_failure(spec, e, soft_failures)

    def register_unstable(self, spec: SpecCaseDefinition, soft_failures: List[BaseException]) -> None:
        self.results.append(SpecResult(spec, SpecResultState.UNSTABLE, soft_failures=soft_failures))
        self.output.on_spec_unstable(spec, soft_failures)

    def on_complete(self) -> None:
        self.output.on_complete(self.any_failed)


def discover_spec_files_in_path(path: str) -> Generator:
    root_module = os.path.basename(path)

    for root, dirs, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)

            if not os.path.isfile(full_path):
                continue

            if not full_path.endswith('.py') or not name.startswith('spec_'):
                continue

            yield {
                'file': os.path.relpath(full_path, path),
                'root': path,
                'module': '%s.%s' % (root_module, os.path.relpath(full_path, path)[:-3].replace('/', '.'))
            }


def spec_has_role(limit_roles: Set[str], spec: SpecCaseDefinition) -> bool:
    if limit_roles is None or 0 == len(limit_roles):
        return True

    # If spec has no role, it applies to ALL roles
    if 0 == len(spec.roles):
        return True

    intersect = limit_roles.intersection(spec.roles)

    return 0 < len(intersect)


def execute_specs_from_path(path: str, limit_roles: Set[str], log: SpecLog, fail_fast: bool) -> bool:
    # Prevent __pycache__ from being created.
    sys.dont_write_bytecode = True

    parent_path = os.path.dirname(path)

    if sys.path[0] != parent_path:
        sys.path.insert(0, parent_path)

    for spec_file in discover_spec_files_in_path(path):
        LOGGER.debug(
            'Discovered specification file %s/%s (as module %s)',
            spec_file['root'],
            spec_file['file'],
            spec_file['module']
        )
        try:
            importlib.import_module(spec_file['module'], spec_file['root'])
        except Exception as e:
            LOGGER.error('Failed to import specification file', exc_info=e)
            return False
        finally:
            _MOONSPEC_RUNTIME_STATE.scope.clear_scope_roles()

    _MOONSPEC_RUNTIME_STATE.load_facts(limit_roles)

    # TODO multi-threaded?
    # TODO move all the logger stuff to SpecLog

    num_specifications = len(_MOONSPEC_RUNTIME_STATE.specs)
    LOGGER.debug(
        'Discovered %d %s',
        num_specifications,
        'specification' if num_specifications == 1 else 'specifications'
    )

    specs_to_run = [spec for spec in _MOONSPEC_RUNTIME_STATE.specs if spec_has_role(limit_roles, spec)]
    num_specs_to_run = len(specs_to_run)

    if 0 == num_specs_to_run:
        LOGGER.error('0 specs matched, %d specs loaded', len(_MOONSPEC_RUNTIME_STATE.specs))
        return False
    else:
        LOGGER.info('Queued %d %s', num_specs_to_run, 'specification' if num_specs_to_run == 1 else 'specification')

    for spec in specs_to_run:
        _MOONSPEC_RUNTIME_STATE.scope.set_scope_description(None)
        log.register_starting(spec)
        LOGGER.debug('Starting specification <%s>', str(spec))
        try:
            spec.function_ref()

            if _MOONSPEC_RUNTIME_STATE.scope.has_soft_failures():
                log.register_unstable(spec, _MOONSPEC_RUNTIME_STATE.scope.soft_spec_failures)
                if LOGGER.getEffectiveLevel() == logging.DEBUG:
                    for soft_fail in _MOONSPEC_RUNTIME_STATE.scope.soft_spec_failures:
                        LOGGER.debug('Specification <%s> soft fail', str(spec), exc_info=soft_fail)
                else:
                    for soft_fail in _MOONSPEC_RUNTIME_STATE.scope.soft_spec_failures:
                        LOGGER.warning('Specification <%s> unstable - %s', str(spec), str(soft_fail))

                _MOONSPEC_RUNTIME_STATE.scope.clear_soft_failures()
            else:
                LOGGER.info('Specification <%s> successful', str(spec))
                log.register_success(spec)

        except Exception as e:
            if LOGGER.getEffectiveLevel() == logging.DEBUG:
                LOGGER.error('Specification <%s> failed', str(spec), exc_info=e)
            else:
                LOGGER.error('Specification <%s> failed: %s', str(spec), str(e))

            soft_failures = []

            if _MOONSPEC_RUNTIME_STATE.scope.has_soft_failures():
                soft_failures = _MOONSPEC_RUNTIME_STATE.scope.soft_spec_failures
                _MOONSPEC_RUNTIME_STATE.scope.clear_soft_failures()

            log.register_failure(spec, e, soft_failures)

            if fail_fast:
                break

    _MOONSPEC_RUNTIME_STATE.dump_facts_in_history()

    log.on_complete()

    if log.any_failed:
        LOGGER.error('Specification failure')
    else:
        LOGGER.info('%d %s successful', num_specs_to_run, 'specifications' if num_specs_to_run > 1 else 'specification')

    return not log.any_failed
