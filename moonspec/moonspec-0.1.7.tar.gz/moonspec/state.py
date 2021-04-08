import logging
import os
import pickle
import threading
from typing import List, Dict, Set, Optional, Any, Callable

LOGGER = logging.getLogger('moonspec')


class CaptureDefinition:
    def __init__(self, capture_key: str, function_ref: Callable[[], None], roles: Set[str]) -> None:
        self.capture_key = capture_key
        self.function_ref = function_ref
        self.roles = roles


class SpecCaseDefinition:
    def __init__(self, module: Optional[str], name: str, roles: Set[str], function_ref: Callable[[], None]) -> None:
        self.module = module
        self.name = name
        self.roles = roles
        self.function_ref = function_ref

    def readable_module(self) -> str:
        if self.module is None:
            return '<unknown module>'

        return self.module

    def readable_name(self) -> str:
        return self.name.replace('_', ' ')

    def __str__(self) -> str:
        return '%s[%s]' % (self.readable_module(), self.readable_name())


class CurrentScope(threading.local):
    def __init__(self) -> None:
        self.soft_spec_failures: List[BaseException] = []
        self.scope_desc: Optional[str] = None
        self.scope_roles: Set[str] = set()

    def apply_to_roles(self, roles: Set) -> None:
        self.scope_roles = roles

    def clear_scope_roles(self) -> None:
        self.scope_roles = set()

    def set_scope_description(self, description: Optional['str']) -> None:
        self.scope_desc = description

    def get_and_clear_scope_description(self) -> Optional[str]:
        desc = self.scope_desc
        self.scope_desc = None
        return desc

    def register_soft_failure(self, e: BaseException) -> None:
        self.soft_spec_failures.append(e)

    def clear_soft_failures(self) -> None:
        self.soft_spec_failures = []

    def has_soft_failures(self) -> bool:
        return 0 < len(self.soft_spec_failures)


class State:
    def __init__(self) -> None:
        self.suite_name: str = 'default'
        self.data_dir: Optional[str] = None
        self.debug: bool = os.environ.get('MOONSPEC_DEBUG') is not None
        self.specs: List[SpecCaseDefinition] = []
        self.captures: Dict[str, CaptureDefinition] = {}
        self.facts: Dict[str, Any] = {}
        self.historic_facts: Dict[str, Any] = {}
        self.scope: CurrentScope = CurrentScope()

    def set_test_suite(self, name: str) -> None:
        self.suite_name = name

    def set_data_dir(self, path: str) -> None:
        if os.path.exists(path) and not os.path.isdir(path):
            raise RuntimeError('Data directory exists and is not directory')

        if not os.path.exists(path):
            os.makedirs(path, 0o770)

        self.data_dir = path

    def register_capture(self, capture_key: str, function_ref: Callable[[], None], roles: Set[str]) -> None:
        if capture_key in self.captures:
            raise RuntimeError('Duplicate capture with key "%s"' % capture_key)

        self.captures[capture_key] = CaptureDefinition(
            capture_key,
            function_ref,
            roles
        )

    def register_spec(self, roles: Set[str], function_ref: Callable[[], None]) -> None:
        module = function_ref.__module__ if hasattr(function_ref, '__module__') else None
        self.specs.append(SpecCaseDefinition(
            module,
            function_ref.__name__,
            roles,
            function_ref
        ))

    def load_facts(self, limit_roles: Set[str]) -> None:
        # TODO: multi-threaded
        # TODO: print timing in debug?
        # Load current facts
        for key, definition in self.captures.items():
            if limit_roles is not None and 0 != len(definition.roles) and 0 != len(limit_roles):
                if 0 == len(limit_roles.intersection(definition.roles)):
                    LOGGER.debug('Skipping capture of fact <%s>, role not needed', key)
                    continue

            LOGGER.debug('Loading capture of fact <%s>', key)
            try:
                self.facts[key] = definition.function_ref()
            except Exception as e:
                LOGGER.error('Failed to capture fact <%s>', key, exc_info=e)
                self.facts[key] = None

        if self.data_dir is not None:
            self.load_facts_from_history()

    def load_facts_from_history(self) -> None:
        if self.data_dir is None:
            return

        history_path = os.path.join(self.data_dir, 'facts.%s.bin' % self.suite_name)

        if not os.path.isfile(history_path):
            return

        try:
            with open(history_path, 'rb') as history_res:
                self.historic_facts = pickle.load(history_res)
        except BaseException as e:
            LOGGER.error('Failed to load fact history from file <%s>', history_res, exc_info=e)

    def dump_facts_in_history(self) -> None:
        if self.data_dir is None:
            return

        history_path = os.path.join(self.data_dir, 'facts.%s.bin' % self.suite_name)
        history_path_previous = os.path.join(self.data_dir, 'facts.old.%s.bin' % self.suite_name)

        if os.path.exists(history_path):
            os.replace(history_path, history_path_previous)

        try:
            with open(history_path, 'wb') as history_res:
                pickle.dump(self.facts, history_res, protocol=pickle.HIGHEST_PROTOCOL)
        except BaseException as e:
            LOGGER.error('Failed to dump fact history into file <%s>', history_res, exc_info=e)

    def has_fact(self, key: str) -> bool:
        return key in self.facts

    def get_fact_value(self, key: str) -> Any:
        if not self.has_fact(key):
            return None

        return self.facts[key]

    def has_historic_fact(self, key: str) -> bool:
        return key in self.historic_facts

    def get_historic_fact_value(self, key: str) -> Any:
        if not self.has_historic_fact(key):
            return None

        return self.historic_facts[key]
