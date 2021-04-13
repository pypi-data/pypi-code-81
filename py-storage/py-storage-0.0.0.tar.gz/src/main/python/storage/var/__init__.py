from __future__ import annotations

import abc
import operator
from functools import reduce, wraps
from typing import Callable, Sequence, Any
from typing import Tuple

from storage import V
from storage.api import Predicate, E, Var


def force_var(func):
    @wraps(func)
    def decorated(self, arg):
        if not isinstance(arg, (Var,)):
            arg = Const(arg)
        return func(self, arg)

    return decorated


class BaseVar(Var[E, V]):

    @force_var
    def __eq__(self, other: Var) -> Predicate[Any]:
        return EqualComparison(self, other)

    @force_var
    def __ne__(self, other):
        return NotEqualComparison(self, other)

    @force_var
    def __gt__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.gt)

    @force_var
    def __ge__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.ge)

    @force_var
    def __lt__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.lt)

    @force_var
    def __le__(self, other: Var) -> Predicate[Any]:
        return Comparison(self, other, operator.le)

    @force_var
    def __contains__(self, item: Var) -> Predicate[Any]:
        return Comparison(self, item, operator.contains)

    @force_var
    def __mul__(self, other: Var) -> Var:
        return ReduceOperator((self, other,), operator.mul)

    @force_var
    def __add__(self, other: Var) -> Var:
        return ReduceOperator((self, other,), operator.add)

    @force_var
    def __sub__(self, other: Var) -> Var:
        return ReduceOperator((self, other,), operator.sub)

    @force_var
    def __truediv__(self, other: Var) -> Var:
        return ReduceOperator((self, other,), operator.truediv)

    @force_var
    def __pow__(self, power, modulo=None) -> Var:
        return ReduceOperator((self, power,), operator.pow)

    def __invert__(self) -> Var:
        return NotOperator(self)

    @force_var
    def __and__(self, other: Var) -> Var:
        return AndOperator((self, other,))

    @force_var
    def __or__(self, other: Var) -> Var:
        return OrOperator((self, other,))

    def cast(self, cast_fn: Callable):
        return CastOperator(cast_fn, self)

    @abc.abstractmethod
    def __call__(self, item: E) -> V:
        raise NotImplementedError()

    def optimize(self) -> Var[E]:
        return self

    def equals(self, other: Var) -> bool:
        if self.__class__ != other.__class__:
            return False
        for self_item, other_item in zip(self.__dict__.items(), other.__dict__.items()):
            if self_item != other_item:
                return False
        return True


class Comparison(BaseVar):

    def __init__(self, var_a: Var, var_b: Var, op: Callable[[Any, Any], bool]):
        self.var_a = var_a
        self.var_b = var_b
        self.op = op

    def __call__(self, item: E) -> bool:
        return self.op(self.var_a(item), self.var_b(item))

    def __repr__(self):
        return f'("{self.op.__name__}", {self.var_a}, {self.var_b})'


class EqualComparison(BaseVar[Any, bool]):
    def __init__(self, var_a: Var, var_b: Var):
        self.var_a = var_a
        self.var_b = var_b

    def __call__(self, item: E) -> bool:
        return self.var_a(item) == self.var_b(item)

    def optimize(self) -> Var[E]:
        opt_var_a = self.var_a.optimize()
        opt_var_b = self.var_b.optimize()
        if opt_var_a.equals(opt_var_b):
            return Vars.const(True)
        return EqualComparison(opt_var_a, opt_var_b)

    def __repr__(self):
        return f'("eq", {self.var_a}, {self.var_b})'


class NotEqualComparison(BaseVar[Any, bool]):
    def __init__(self, var_a: Var, var_b: Var):
        self.var_a = var_a
        self.var_b = var_b

    def __call__(self, item: E) -> bool:
        return self.var_a(item) != self.var_b(item)

    def optimize(self) -> Var[E]:
        opt_var_a = self.var_a.optimize()
        opt_var_b = self.var_b.optimize()
        if opt_var_a.equals(opt_var_b):
            return Vars.const(False)
        return NotEqualComparison(opt_var_a, opt_var_b)

    def __repr__(self):
        return f'("ne", {self.var_a}, {self.var_b})'


class CastOperator(BaseVar[E, V]):

    def __init__(self, cast_fn: Callable[[Any], V], inner_var: Var[E, Any]):
        self.cast_fn = cast_fn
        self.inner_var = inner_var

    def __call__(self, item: E) -> V:
        return self.cast_fn(self.inner_var(item))

    def cast(self, cast_fn: Callable):
        if self.cast_fn == cast_fn:
            return self
        return CastOperator(cast_fn, self)


class NotOperator(BaseVar[E, V]):

    def __init__(self, inner_var: Var[E, V]):
        self.inner_var = inner_var

    def __invert__(self):
        return self.inner_var

    def __call__(self, item: E) -> V:
        return not self.inner_var(item)

    def optimize(self) -> Var[E]:
        inner_var = self.inner_var.optimize()
        if Const.is_const(inner_var):
            return Const(not inner_var.const)
        return self


class OrOperator(BaseVar[E, Any]):

    def __init__(self, inner_vars: Tuple[Var[E, Any], ...]):
        self.inner_vars = inner_vars

    @force_var
    def __or__(self, other: Var):
        return OrOperator(self.inner_vars + (other,))

    def __call__(self, item: E) -> Any:
        for var in self.inner_vars:
            val = var(item)
            if val:
                return val
        return False

    def optimize(self) -> Var[E]:
        inner_vars = []
        for var in self.inner_vars:
            optimized_var = var.optimize()
            if Const.is_true(optimized_var):
                return optimized_var
            inner_vars.append(optimized_var)
        return OrOperator(tuple(inner_vars))

    def __repr__(self):
        return f'("or",{",".join(map(repr, self.inner_vars))})'


class AndOperator(BaseVar[E, Any]):
    def __init__(self, inner_vars: Tuple[Var[E, Any], ...]):
        self.inner_vars = inner_vars

    def __and__(self, other: Predicate[E]):
        return AndOperator(self.inner_vars + (other,))

    def __call__(self, item: E) -> bool:
        for var in self.inner_vars:
            if not var(item):
                return False
        return True

    def optimize(self) -> Var[E]:
        inner_vars = []
        for var in self.inner_vars:
            optimized_var = var.optimize()
            if Const.is_false(optimized_var):
                return optimized_var
            inner_vars.append(optimized_var)
        return AndOperator(tuple(inner_vars))

    def __repr__(self):
        return f'("and",{",".join(map(repr, self.inner_vars))})'


class ReduceOperator(BaseVar[Any, Any]):

    def __init__(self, inner_vars: Tuple[Any, ...], op: Callable[[Any, Any], Any]):
        self.inner_vars = inner_vars
        self.op = op

    def __repr__(self):
        return f'("{self.op.__name__}",{",".join(map(repr, self.inner_vars))})'

    @force_var
    def __mul__(self, other: Var) -> Var:
        if self.op == operator.mul:
            return ReduceOperator(self.inner_vars + (other,), self.op)
        return ReduceOperator((self, other,), operator.mul)

    @force_var
    def __add__(self, other: Var) -> Var:
        if self.op == operator.add:
            return ReduceOperator(self.inner_vars + (other,), self.op)
        return ReduceOperator((self, other,), operator.add)

    @force_var
    def __sub__(self, other: Var) -> Var:
        if self.op == operator.sub:
            return ReduceOperator(self.inner_vars + (other,), self.op)
        return ReduceOperator((self, other,), operator.sub)

    @force_var
    def __truediv__(self, other: Var) -> Var:
        if self.op == operator.truediv:
            return ReduceOperator(self.inner_vars + (other,), self.op)
        return ReduceOperator((self, other,), operator.truediv)

    @force_var
    def __pow__(self, power, modulo=None) -> Var:
        if self.op == operator.pow:
            return ReduceOperator(self.inner_vars + (power,), self.op)
        return ReduceOperator((self, power,), operator.pow)

    def __call__(self, item: E) -> V:
        return reduce(self.op, [var(item) for var in self.inner_vars])


class Const(BaseVar[Any, V]):

    @classmethod
    def is_const(cls, instance):
        return isinstance(instance, (cls,))

    @classmethod
    def is_true(cls, instance):
        if cls.is_const(instance):
            return instance.const
        return False

    @classmethod
    def is_false(cls, instance):
        if cls.is_const(instance):
            return not instance.const
        return False

    def __init__(self, const: V):
        self.const = const

    def __invert__(self) -> Var:
        return Const(not self.const)

    def __repr__(self):
        return f'{repr(self.const)}'

    @force_var
    def __and__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const & other.const)
        return AndOperator((self, other,))

    @force_var
    def __or__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const | other.const)
        return OrOperator((self, other,))

    @force_var
    def __mul__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const * other.const)
        return ReduceOperator((self, other,), operator.mul)

    @force_var
    def __add__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const + other.const)
        return ReduceOperator((self, other,), operator.add)

    @force_var
    def __sub__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const - other.const)
        return ReduceOperator((self, other,), operator.sub)

    @force_var
    def __truediv__(self, other: Var) -> Var:
        if isinstance(other, (Const,)):
            return Const(self.const / other.const)
        return ReduceOperator((self, other,), operator.truediv)

    @force_var
    def __pow__(self, power, modulo=None) -> Var:
        if isinstance(power, (Const,)):
            return Const(self.const ** power.const)
        return ReduceOperator((self, power,), operator.pow)

    def cast(self, cast_fn: Callable):
        if isinstance(cast_fn, (type,)) and isinstance(self.const, cast_fn):
            return self
        return Const(cast_fn(self.const))

    def __call__(self, item: Any = None) -> V:
        return self.const


class Func(BaseVar):

    def __init__(self, func: Callable[[E], bool]):
        self.func = func

    def __call__(self, item: E) -> bool:
        return self.func(item)

    @classmethod
    def from_lambda(cls, func: Callable[[E], bool]) -> Predicate[E]:
        return cls(func)


class Keys(BaseVar):

    def __init__(self, keys: Sequence[str] = ()):
        self.keys = keys

    def __call__(self, item):
        for key in self.keys:
            if item is None:
                return None
            item = item.get(key, None)
        return item

    def __repr__(self) -> str:
        return f'${{{".".join(self.keys)}}}'


class Vars:

    @staticmethod
    def key(key: str) -> Var[Any, Any]:
        return Keys((key,))

    @staticmethod
    def keys(keys: Sequence[str]) -> Var[Any, Any]:
        return Keys(keys)

    @staticmethod
    def const(value: E) -> Var[Any, E]:
        return Const(value)
