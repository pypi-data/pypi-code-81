import math
import re
from enum import Enum
from typing import Callable, Any, Optional, Union, Tuple, Pattern

from moonspec import _MOONSPEC_RUNTIME_STATE


# TODO: what was I thinking...
class ComparatorExpectations(Enum):
    ABSENT = 0
    PRESENT = 1
    EQUAL = 2
    NOT_EQUAL = 3
    NOT_CHANGED = 4
    SELF_IS_NUMBER = 5
    OTHER_IS_NUMBER = 6
    LT = 7
    GT = 8
    LTE = 9
    GTE = 10
    EMPTY = 11
    NOT_EMPTY = 12
    CB = 13
    TYPE = 14
    ANY_OF = 15
    NONE_OF = 16
    CONTAIN_ANY_OF = 17
    CONTAIN_NONE_OF = 18
    CONTAIN_ALL_OF = 19
    HAVE_KEYS = 20
    NOT_HAVE_KEYS = 21
    MATCH = 22
    NOT_MATCH = 23
    CONTAIN_MATCH = 24
    NOT_CONTAIN_MATCH = 25
    LENGTH = 26
    NOT_LENGTH = 27


class SubjectExpectationException(RuntimeError):
    def __init__(self, identity: Optional[str], expected_value: Any, actual_value: Any,
                 expectation: ComparatorExpectations = None) -> None:
        super().__init__()
        self.identity = identity or 'value'
        self.expected_value = expected_value
        self.actual_value = actual_value
        self.expectation = expectation
        self.description = _MOONSPEC_RUNTIME_STATE.scope.get_and_clear_scope_description()

    def __str__(self) -> str:
        if self.description is not None:
            return self.description

        if ComparatorExpectations.EQUAL == self.expectation:
            return 'Expected %s to equal <%s>, actual value is <%s>' % (
                self.identity,
                self.expected_value,
                self.actual_value
            )
        if ComparatorExpectations.NOT_EQUAL == self.expectation:
            return 'Expected %s to not equal <%s>' % (
                self.identity,
                self.expected_value
            )
        if ComparatorExpectations.ABSENT == self.expectation:
            return 'Expected %s to be absent, actual values is <%s>' % (
                self.identity,
                self.actual_value
            )
        if ComparatorExpectations.PRESENT == self.expectation:
            return 'Expected %s to be present, actually absent' % self.identity

        if ComparatorExpectations.NOT_CHANGED == self.expectation:
            return 'Expected %s historic value <%s> to match current value <%s>, values differ' \
                   % (self.identity, self.expected_value, self.actual_value)

        if ComparatorExpectations.SELF_IS_NUMBER == self.expectation:
            return 'Expected %s to be float, integer or numeric string, actual values is <%s> of type %s' % (
                self.identity,
                self.actual_value,
                type(self.actual_value)
            )

        if ComparatorExpectations.OTHER_IS_NUMBER == self.expectation:
            return 'Expected %s opposite value to be float, integer or numeric string, ' \
                   'actual values is <%s> of type %s' % (
                       self.identity,
                       self.actual_value,
                       type(self.actual_value)
                   )

        if ComparatorExpectations.LT == self.expectation:
            return 'Expected %s <%s> to be less than <%s>' \
                   % (self.identity, self.actual_value, self.expected_value)

        if ComparatorExpectations.GT == self.expectation:
            return 'Expected %s <%s> to be greater than <%s>' \
                   % (self.identity, self.actual_value, self.expected_value)

        if ComparatorExpectations.LTE == self.expectation:
            return 'Expected %s <%s> to be less than or equal to <%s>' \
                   % (self.identity, self.actual_value, self.expected_value)

        if ComparatorExpectations.GTE == self.expectation:
            return 'Expected %s <%s> to be greater than or equal to <%s>' \
                   % (self.identity, self.actual_value, self.expected_value)

        if ComparatorExpectations.EMPTY == self.expectation:
            return 'Expected %s to be empty, actual values is <%s>' % (
                self.identity,
                self.actual_value
            )

        if ComparatorExpectations.NOT_EMPTY == self.expectation:
            return 'Expected %s to not be empty, actually empty' % (
                self.identity,
            )

        if ComparatorExpectations.CB == self.expectation:
            return 'Expected %s with value <%s> to match using custom matcher' % (
                self.identity,
                self.actual_value
            )

        if ComparatorExpectations.TYPE == self.expectation:
            return 'Expected %s to be of type <%s>, actual values is <%s>' % (
                self.identity,
                self.expected_value,
                self.actual_value
            )

        if ComparatorExpectations.ANY_OF == self.expectation:
            return 'Expected %s to be any of <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.NONE_OF == self.expectation:
            return 'Expected %s to be none of <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.CONTAIN_ANY_OF == self.expectation:
            return 'Expected %s to contain any of <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.CONTAIN_NONE_OF == self.expectation:
            return 'Expected %s to contain none of <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.CONTAIN_ALL_OF == self.expectation:
            return 'Expected %s to contain all of of <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.HAVE_KEYS == self.expectation:
            return 'Expected %s to have keys <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.NOT_HAVE_KEYS == self.expectation:
            return 'Expected %s to not have keys <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.MATCH == self.expectation:
            return 'Expected %s to match <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.NOT_MATCH == self.expectation:
            return 'Expected %s to not match <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.CONTAIN_MATCH == self.expectation:
            return 'Expected %s to contain match <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.NOT_CONTAIN_MATCH == self.expectation:
            return 'Expected %s not contain match <%s>, actual value is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.LENGTH == self.expectation:
            return 'Expected %s to have length <%s>, actual length is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )
        if ComparatorExpectations.NOT_LENGTH == self.expectation:
            return 'Expected %s to not have length <%s>, actual length is <%s>' % (
                self.identity, self.expected_value, self.actual_value
            )

        raise RuntimeError('Unhandled comparator expectation - %s' % self.expectation)


class Subject:
    def __init__(self, value: Any, identity: str = None) -> None:
        self.value = value
        self._identity = identity

    @staticmethod
    def _get_value(something: Any) -> Any:
        if isinstance(something, Subject):
            return something.value

        return something

    @staticmethod
    def _get_number_value(something: Union[str, int, float, Any]) -> Union[float, int]:
        value = Subject._get_value(something)

        if not isinstance(value, (int, float, str)):
            return math.nan

        if isinstance(value, str):
            if value.isdigit():
                return int(value)

            if value.isdecimal():
                return float(value)

            return math.nan

        return value

    def _get_numeric_comp(self, other: Any) -> Tuple[Union[float, int], Union[float, int]]:
        self_num = self._get_number_value(self.value)
        other_num = self._get_number_value(other)

        if other_num is math.nan:
            raise SubjectExpectationException(self._identity, None, self._get_value(other),
                                              ComparatorExpectations.OTHER_IS_NUMBER)
        if self_num is math.nan:
            raise SubjectExpectationException(self._identity, None, self.value, ComparatorExpectations.SELF_IS_NUMBER)

        return other_num, self_num

    # -> Expectations for values
    def should_be_present(self) -> None:
        if self.value is None:
            raise SubjectExpectationException(self._identity, None, self.value, ComparatorExpectations.PRESENT)

    def should_be_absent(self) -> None:
        if self.value is not None:
            raise SubjectExpectationException(self._identity, None, self.value, ComparatorExpectations.ABSENT)

    def should_equal(self, other: Any) -> None:
        other_value = self._get_value(other)

        if self.value != other_value:
            raise SubjectExpectationException(self._identity, other_value, self.value, ComparatorExpectations.EQUAL)

    def should_not_equal(self, other: Any) -> None:
        other_value = self._get_value(other)
        if self.value == other_value:
            raise SubjectExpectationException(self._identity, other_value, self.value, ComparatorExpectations.NOT_EQUAL)

    def should_be_empty(self) -> None:
        if self.value is None:
            return

        if isinstance(self.value, (str, list, set, bytes, bytearray, tuple, frozenset, range)):
            if 0 != len(self.value):
                raise SubjectExpectationException(self._identity, None, self.value, ComparatorExpectations.EMPTY)
            return

        raise RuntimeError('Value of type %s can not be tested for empty' % type(self.value))

    def should_not_be_empty(self) -> None:
        if self.value is None:
            raise SubjectExpectationException(self._identity, None, self.value, ComparatorExpectations.NOT_EMPTY)

        if isinstance(self.value, (str, list, set, bytes, bytearray, tuple, frozenset, range)):
            if 0 == len(self.value):
                raise SubjectExpectationException(self._identity, None, self.value, ComparatorExpectations.NOT_EMPTY)
            return

        raise RuntimeError('Value of type %s can not be tested for not_empty' % type(self.value))

    def should_be_lt(self, other: Any) -> None:
        other_num, self_num = self._get_numeric_comp(other)

        if other_num <= self_num:
            raise SubjectExpectationException(self._identity, other_num, self_num, ComparatorExpectations.LT)

    def should_be_gt(self, other: Any) -> None:
        other_num, self_num = self._get_numeric_comp(other)

        if other_num >= self_num:
            raise SubjectExpectationException(self._identity, other_num, self_num, ComparatorExpectations.GT)

    def should_be_lte(self, other: Any) -> None:
        other_num, self_num = self._get_numeric_comp(other)

        if other_num < self_num:
            raise SubjectExpectationException(self._identity, other_num, self_num, ComparatorExpectations.LTE)

    def should_be_gte(self, other: Any) -> None:
        other_num, self_num = self._get_numeric_comp(other)

        if other_num > self_num:
            raise SubjectExpectationException(self._identity, other_num, self_num, ComparatorExpectations.GTE)

    def should_be_true(self) -> None:
        if self.value is not None and not isinstance(self.value, bool):
            raise SubjectExpectationException(self._identity, bool, type(self.value), ComparatorExpectations.TYPE)

        if self.value is not True:
            raise SubjectExpectationException(self._identity, True, self.value, ComparatorExpectations.EQUAL)

    def should_be_false(self) -> None:
        if self.value is not None and not isinstance(self.value, bool):
            raise SubjectExpectationException(self._identity, bool, type(self.value), ComparatorExpectations.TYPE)

        if self.value is not False:
            raise SubjectExpectationException(self._identity, False, self.value, ComparatorExpectations.EQUAL)

    def should_be_any_of(self, *args: Any) -> None:
        for it in args:
            if self.value == self._get_value(it):
                return
        raise SubjectExpectationException(self._identity, args, self.value, ComparatorExpectations.ANY_OF)

    def should_be_none_of(self, *args: Any) -> None:
        for it in args:
            if self.value == self._get_value(it):
                raise SubjectExpectationException(self._identity, args, self.value,
                                                  ComparatorExpectations.NONE_OF)

    def should_contain_any_of(self, *args: Any) -> None:
        if isinstance(self.value, dict):
            values = self.value.values()
            for arg in args:
                if arg in values:
                    return
            raise SubjectExpectationException(self._identity, args, self.value,
                                              ComparatorExpectations.CONTAIN_ANY_OF)

        if isinstance(self.value, list) or isinstance(self.value, set):
            for arg in args:
                if arg in self.value:
                    return
            raise SubjectExpectationException(self._identity, args, self.value,
                                              ComparatorExpectations.CONTAIN_ANY_OF)

        raise RuntimeError('Expected set, list or map, can not check against contents of %s' % type(self.value))

    def should_contain_none_of(self, *args: Any) -> None:
        if isinstance(self.value, dict):
            values = self.value.values()
            for arg in args:
                if arg in values:
                    raise SubjectExpectationException(self._identity, args, self.value,
                                                      ComparatorExpectations.CONTAIN_NONE_OF)
            return

        if isinstance(self.value, list) or isinstance(self.value, set):
            for arg in args:
                if arg in self.value:
                    raise SubjectExpectationException(self._identity, args, self.value,
                                                      ComparatorExpectations.CONTAIN_NONE_OF)
            return

        raise RuntimeError('Expected set, list or map, can not check against contents of %s' % type(self.value))

    def should_contain_all_of(self, *args: Any) -> None:
        if isinstance(self.value, dict):
            values = self.value.values()
            for arg in args:
                if arg not in values:
                    raise SubjectExpectationException(self._identity, args, self.value,
                                                      ComparatorExpectations.CONTAIN_ALL_OF)
            return

        if isinstance(self.value, list) or isinstance(self.value, set):
            for arg in args:
                if arg not in self.value:
                    raise SubjectExpectationException(self._identity, args, self.value,
                                                      ComparatorExpectations.CONTAIN_ALL_OF)
            return

        raise RuntimeError('Expected set, list or map, can not check against contents of %s' % type(self.value))

    def should_have_keys(self, *args: str) -> None:
        if not isinstance(self.value, dict):
            raise RuntimeError('Expected dict, can not check against keys of %s' % type(self.value))

        keys = self.value.keys()

        for arg in args:
            if arg not in keys:
                raise SubjectExpectationException(self._identity, args, self.value,
                                                  ComparatorExpectations.HAVE_KEYS)

    def should_not_have_keys(self, *args: str) -> None:
        if not isinstance(self.value, dict):
            raise RuntimeError('Expected dict, can not check against keys of %s' % type(self.value))

        keys = self.value.keys()

        for arg in args:
            if arg in keys:
                raise SubjectExpectationException(self._identity, args, self.value,
                                                  ComparatorExpectations.NOT_HAVE_KEYS)

    def should_match(self, pattern: Union[Pattern, str]) -> None:
        if not isinstance(self.value, str):
            raise RuntimeError('Can not match against type %s, expected value to be string' % type(self.value))

        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        if pattern.fullmatch(self.value) is None:
            raise SubjectExpectationException(self._identity, pattern.pattern, self.value,
                                              ComparatorExpectations.MATCH)

    def should_not_match(self, pattern: Union[Pattern, str]) -> None:
        if not isinstance(self.value, str):
            raise RuntimeError('Can not match against type %s, expected value to be string' % type(self.value))

        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        if pattern.fullmatch(self.value) is not None:
            raise SubjectExpectationException(self._identity, pattern.pattern, self.value,
                                              ComparatorExpectations.NOT_MATCH)

    def should_contain_match(self, pattern: Union[Pattern, str]) -> None:
        if not isinstance(self.value, str):
            raise RuntimeError('Can not match against type %s, expected value to be string' % type(self.value))

        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        if pattern.search(self.value) is None:
            raise SubjectExpectationException(self._identity, pattern.pattern, self.value,
                                              ComparatorExpectations.CONTAIN_MATCH)

    def should_not_contain_match(self, pattern: Union[Pattern, str]) -> None:
        if not isinstance(self.value, str):
            raise RuntimeError('Can not match against type %s, expected value to be string' % type(self.value))

        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        if pattern.search(self.value) is not None:
            raise SubjectExpectationException(self._identity, pattern.pattern, self.value,
                                              ComparatorExpectations.NOT_CONTAIN_MATCH)

    def should_have_length(self, length: int) -> None:
        if len(self.value) != length:
            raise SubjectExpectationException(self._identity, length, len(self.value),
                                              ComparatorExpectations.LENGTH)

    def should_not_have_length(self, length: int) -> None:
        if len(self.value) == length:
            raise SubjectExpectationException(self._identity, length, len(self.value),
                                              ComparatorExpectations.NOT_LENGTH)

    def should(self, matcher: Callable[[Any], bool]) -> None:
        try:
            result = matcher(self.value)
            if not result:
                raise SubjectExpectationException(self._identity, None, self.value, ComparatorExpectations.CB)
        except BaseException as e:
            ex = SubjectExpectationException(self._identity, None, self.value, ComparatorExpectations.CB)
            ex.__cause__ = e
            raise ex

    # <- Expectations for values
    # -> Aliases with to_* for the expectations

    def to_be_present(self) -> None:
        self.should_be_present()

    def to_be_absent(self) -> None:
        self.should_be_absent()

    def to_equal(self, other: Any) -> None:
        self.should_equal(other)

    def to_not_equal(self, other: Any) -> None:
        self.should_not_equal(other)

    def to_be_empty(self) -> None:
        self.should_be_empty()

    def to_not_be_empty(self) -> None:
        self.should_not_be_empty()

    def to_be_lt(self, other: Any) -> None:
        self.should_be_lt(other)

    def to_be_gt(self, other: Any) -> None:
        self.should_be_gt(other)

    def to_be_lte(self, other: Any) -> None:
        self.should_be_lte(other)

    def to_be_gte(self, other: Any) -> None:
        self.should_be_gte(other)

    def to(self, matcher: Callable[[Any], bool]) -> None:
        self.should(matcher)

    def to_be_true(self) -> None:
        self.should_be_true()

    def to_be_false(self) -> None:
        self.should_be_false()

    def to_be_any_of(self, *args: Any) -> None:
        self.should_be_any_of(*args)

    def to_be_none_of(self, *args: Any) -> None:
        self.should_be_none_of(*args)

    def to_contain_any_of(self, *args: Any) -> None:
        self.should_contain_any_of(*args)

    def to_contain_none_of(self, *args: Any) -> None:
        self.should_contain_none_of(*args)

    def to_contain_all_of(self, *args: Any) -> None:
        self.should_contain_all_of(*args)

    def to_have_keys(self, *args: str) -> None:
        self.should_have_keys(*args)

    def to_not_have_keys(self, *args: str) -> None:
        self.should_not_have_keys(*args)

    def to_match(self, pattern: Union[Pattern, str]) -> None:
        self.should_match(pattern)

    def to_not_match(self, pattern: Union[Pattern, str]) -> None:
        self.should_not_match(pattern)

    def to_contain_match(self, pattern: Union[Pattern, str]) -> None:
        self.should_contain_match(pattern)

    def to_not_contain_match(self, pattern: Union[Pattern, str]) -> None:
        self.should_not_contain_match(pattern)

    def to_have_length(self, length: int) -> None:
        self.should_have_length(length)

    def to_not_have_length(self, length: int) -> None:
        self.should_not_have_length(length)

    # <- Aliases with to_*
    # -> Utility methods

    def lookup(self, key: str) -> 'Subject':
        if not isinstance(key, str):
            raise RuntimeError('Non-string value used as lookup key to access %s' % self._identity)

        local_identity = '%s.%s' % (self._identity, key) if self._identity is not None else key

        if not isinstance(self.value, dict):
            return Subject(None, identity=local_identity)

        path = key.split('.')
        num_levels = len(path)
        current_root = self.value

        for i in range(0, num_levels):
            idx = path[i]
            is_last = i == num_levels - 1

            if idx not in current_root:
                return Subject(None, identity=local_identity)

            if is_last:
                return Subject(current_root[idx], local_identity)

            if not isinstance(current_root[idx], dict):
                return Subject(None, identity=local_identity)

            current_root = current_root[idx]

        return Subject(None, identity=local_identity)

    def at(self, index: int) -> 'Subject':
        if not isinstance(index, int):
            raise RuntimeError('Non-integer value used as index to access <%s>' % self._identity)

        local_identity = '%s[%d]' % (self._identity, index) if self._identity is not None else str(index)

        if not isinstance(self.value, list) or index > (len(self.value) - 1):
            return Subject(None, identity=local_identity)

        return Subject(self.value[index], identity=local_identity)
    # <- Utility methods
