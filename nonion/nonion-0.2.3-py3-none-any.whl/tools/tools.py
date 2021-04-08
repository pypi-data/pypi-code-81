from typing import Callable, Dict, Iterable, Iterator, List, Tuple, TypeVar, Union

import operator

from functools import partial
from functools import reduce
from itertools import chain
from itertools import compress
from itertools import islice
from itertools import product
from itertools import repeat
from itertools import starmap

X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")

Option = Union[Tuple[X], Tuple[()]]
Either = Tuple[Option[X], Option[Y]]

AnyFunction = Callable[[Tuple[object, ...], Dict[str, object]], Y]
OptionFunction = Callable[[Tuple[object, ...], Dict[str, object]], Option[Y]]
EitherFunction = Callable[[Tuple[object, ...], Dict[str, object]], Either[Z, Y]]

def binary_compose(f: Callable[[Y], Z], g: Callable[[X], Y]) -> Callable[[X], Z]:
  return lambda x: f(g(x))

def curry(f: AnyFunction[Y]) -> AnyFunction[Y]:
  return lambda *args, **kwargs: partial(f, *args, **kwargs)

lift = curry(map)

def fmap(f: Callable[[X], Y], x: Iterable[X]) -> Tuple[Y, ...]:
  return binary_compose(tuple, lift(f))(x)

def bind(f: Callable[[X], Iterable[Y]], x: Iterable[X]) -> Tuple[Y, ...]:
  ys: Iterable[Iterable[Y]] = map(f, x)
  y: Iterable[Y] = chain.from_iterable(ys)

  return tuple(y)

def wraptry(f: AnyFunction[Y]) -> OptionFunction[Y]:
  def g(*args: object, **kwargs: object) -> Option[Y]:
    try:
      return (f(*args, **kwargs),)
    except:
      return ()

  return g

def wrapexcept(f: AnyFunction[Y]) -> EitherFunction[Exception, Y]:
  def g(*args: object, **kwargs: object) -> Either[Exception, Y]:
    try:
      y = f(*args, **kwargs)
      return ((), (y,))
    except Exception as e:
      return ((e,), ())

  return g

def maptry(f: Callable[[X], Y], xs: Iterable[X]) -> Iterable[Y]:
  ys: Iterable[Option[Y]] = map(wraptry(f), xs)
  return chain.from_iterable(ys)

wrapnext: Callable[[Iterator[X]], Option[X]] = wraptry(next)

def wrapeek(xs: Iterable[X]) -> Tuple[Option[X], Iterable[X]]:
  xs = iter(xs)
  x = wrapnext(xs)

  return x, chain(x, xs)

def iterfind(ps: Iterable[Callable[[X], bool]], xs: Iterable[X]) -> Iterable[Option[X]]:
  xs = iter(xs)
  buffer = []

  for p in ps:
    x = find(p, buffer)

    if not x:
      x, buffer = find_and_collect(p, xs, buffer)

    yield x

def find(p: Callable[[X], bool], xs: Iterable[X]) -> Option[X]:
  xs = filter(p, xs)
  return wrapnext(xs)

def find_and_collect(
    p: Callable[[X], bool],
    xs: Iterator[X],
    buffer: List[X]
    ) -> Tuple[Option[X], List[X]]:

  x = wrapnext(xs)

  while x:
    buffer.extend(x)

    if p(*x):
      return x, buffer

    x = wrapnext(xs)

  return (), buffer

def findindex(p: Callable[[X], bool], xs: Iterable[X]) -> Option[int]:
  yxs = enumerate(xs)

  g: Callable[[Tuple[int, X]], bool] = binary_compose(p, second)
  yx: Option[Tuple[int, X]] = find(g, yxs)

  return fmap(first, yx)

def first(xy: Tuple[X, Y]) -> X:
  return xy[0]

def second(xy: Tuple[X, Y]) -> Y:
  return xy[1]

def mapexplode(f: Callable[[X, Y], Z], x: X, ys: Iterable[Y]) -> Iterable[Z]:
  xs_and_ys: Iterable[Tuple[X, Y]] = explode(x, ys)
  return starmap(f, xs_and_ys)

def explode(x: X, ys: Iterable[Y]) -> Iterable[Tuple[X, Y]]:
  return zip(repeat(x), ys)

def slide(xs: Iterable[X], length: int = 2, step: int = 1) -> Iterable[Tuple[X, ...]]:
  xs = iter(xs)

  window = islice(xs, length)
  window = tuple(window)

  while len(window) > 0:
    yield window

    window = chain(window[step:], islice(xs, step))
    window = tuple(window)

def take(n: int) -> Callable[[Iterable[X]], Iterable[X]]:
  return lambda xs: islice(xs, n)

def drop(n: int) -> Callable[[Iterable[X]], Iterable[X]]:
  return lambda xs: islice(xs, n, None)

def cachepartial(f: AnyFunction[Y], *args: object, **kwargs: object) -> AnyFunction[Y]:
  f = partial(f, *args, **kwargs)
  return cache(f)

def cache(f: AnyFunction[Y]) -> AnyFunction[Y]:
  def cached() -> Iterable[Y]:
    args, kwargs = yield
    y = f(*args, **kwargs)

    while True:
      yield y

  cached = cached()
  next(cached)

  def g(*args: object, **kwargs: object) -> Y:
    return cached.send((args, kwargs))

  return g

def shift(f: AnyFunction[Y], *args: object, **kwargs: object) -> AnyFunction[Y]:
  return lambda *args_, **kwargs_: f(*args_, *args,  **{**kwargs_, **kwargs})

def key(f: Callable[[X], Z]) -> Callable[[Tuple[X, Y]], Tuple[Z, Y]]:
  g: Callable[[Tuple[X, Y]], Z] = binary_compose(f, first)
  return lambda xy: (g(xy), second(xy))

def value(f: Callable[[Y], Z]) -> Callable[[Tuple[X, Y]], Tuple[X, Z]]:
  g: Callable[[Tuple[X, Y]], Z] = binary_compose(f, second)
  return lambda xy: (first(xy), g(xy))

def flip(f: Callable[[Y, X], Z]) -> Callable[[X, Y], Z]:
  return lambda x, y: f(y, x)

def fold(f: Callable[[Y, X], Y], acc: Y) -> Callable[[Iterable[X]], Y]:
  return lambda xs: reduce(f, xs, acc)

def fold1(f: Callable[[Y, X], Y]) -> Callable[[Iterable[X]], Y]:
  return lambda xs: reduce(f, xs)

def zipl(xs: Iterable[X]) -> Callable[[Iterable[Y]], Iterable[Tuple[X, Y]]]:
  return lambda ys: zip(xs, ys)

def zipr(ys: Iterable[Y]) -> Callable[[Iterable[X]], Iterable[Tuple[X, Y]]]:
  return lambda xs: zip(xs, ys)

def flatten(xyz: Tuple[Tuple[X, Y], Z]) -> Tuple[X, Y, Z]:
  (x, y), z = xyz
  return x, y, z

def zipmapl(f: Callable[[X], Y]) -> Callable[[Iterable[X]], Iterable[Tuple[Y, X]]]:
  return lambda xs: map(lambda x: (f(x), x), xs)

def zipmapr(f: Callable[[X], Y]) -> Callable[[Iterable[X]], Iterable[Tuple[X, Y]]]:
  return lambda xs: map(lambda x: (x, f(x)), xs)

def call(fx: Tuple[Callable[[Tuple[object, ...]], Y], Tuple[object, ...]]) -> Y:
  f, *x = fx
  return f(*x)

def as_function(xys: Iterable[Tuple[X, Y]]) -> Callable[[X], Option[Y]]:
  x_to_y = dict(xys)

  def lookup(x: X) -> Option[Y]:
    if x in x_to_y:
      return (x_to_y[x],)
    else:
      return ()

  return lookup

def match(*fs: Callable[[X], Option[Y]]) -> Callable[[X], Option[Y]]:
  def g(x: X) -> Option[Y]:
    wrapped_ys = map(lambda f: f(x), fs)
    filtered_ys = filter(lambda y: y, wrapped_ys)
    ys = map(first, filtered_ys)

    return wrapnext(ys)

  return g

def catch(*fs: Callable[[X], Option[Y]], default: Callable[[X], Y]) -> Callable[[X], Y]:
  f = match(*fs)

  def g(x: X) -> Y:
    y, *_ = f(x) or (default(x),)
    return y

  return g

def stripby(f: Callable[[X, X], bool]) -> Callable[[Iterable[X]], Iterable[X]]:
  return binary_compose(lift(first), groupby(f))

def groupby(f: Callable[[X, X], bool]) -> Callable[[Iterable[X]], Iterable[Tuple[X, ...]]]:
  z: Callable[[X], Callable[[X], bool]] = curry(f)

  def g(xs: Iterable[X]) -> Iterable[Tuple[X, ...]]:
    xs = iter(xs)
    wrapped_p = wrapnext(xs)

    while wrapped_p:
      p, *_ = wrapped_p

      group, xs = span(z(p))(xs)
      yield wrapped_p + group

      wrapped_p = wrapnext(xs)

  return g

@curry
def span(p: Callable[[X], bool], xs: Iterable[X]) -> Tuple[Tuple[X, ...], Iterable[X]]:
  xs = iter(xs)
  x = wrapnext(xs)

  matched = []

  while x:
    if p(*x):
      matched.extend(x)
      x = wrapnext(xs)
    else:
      break

  return tuple(matched), chain(x, xs)

strip: Callable[[Iterable[X]], Iterable[X]] = stripby(operator.eq)
group: Callable[[Iterable[X]], Iterable[Tuple[X, ...]]] = groupby(operator.eq)

def on(f: Callable[[Y, Y], Z], g: Callable[[X], Y]) -> Callable[[X, X], Z]:
  return lambda p, n: f(g(p), g(n))

@curry
def partition(p: Callable[[X], bool], xs: Iterable[X]) -> Tuple[Tuple[X, ...], Tuple[X, ...]]:
  ts, fs = [], []

  for x in xs:
    if p(x): ts.append(x)
    else: fs.append(x)

  return tuple(ts), tuple(fs)

def powerset(xs: Tuple[X, ...]) -> Iterable[Iterable[X]]:
  ys = map(lambda _: range(2), range(len(xs)))
  return map(partial(compress, xs), product(*ys))

def between(left: float, right: float) -> Callable[[float], bool]:
  return lambda x: left <= x and x <= right

def in_(xs: Tuple[X, ...]) -> Callable[[X], bool]:
  return lambda x: x in xs

length: Callable[[Iterable[X]], int] = fold(lambda acc, _: acc + 1, 0)

def not_(p: AnyFunction[bool], *args: object, **kwargs: object) -> AnyFunction[bool]:
  return lambda *args_, **kwargs_: not p(*args, *args_, **{**kwargs, **kwargs_})

def zipflatl(f: Callable[[X], Option[Y]]) -> Callable[[Iterable[X]], Iterable[Tuple[Y, X]]]:
  def g(xs: Iterable[X]) -> Iterable[Tuple[Y, X]]:
    ys = zipmapl(f)(xs)
    zs = filter(first, ys)

    return map(key(first), zs)

  return g

def zipflatr(f: Callable[[X], Option[Y]]) -> Callable[[Iterable[X]], Iterable[Tuple[X, Y]]]:
  def g(xs: Iterable[X]) -> Iterable[Tuple[X, Y]]:
    ys = zipmapr(f)(xs)
    zs = filter(second, ys)

    return map(value(first), zs)

  return g

@curry
def as_catch(default: Callable[[X], Y], xys: Iterable[Tuple[X, Y]]) -> Callable[[X], Y]:
  return catch(as_function(xys), default=default)
