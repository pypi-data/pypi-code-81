#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of nt2dc
# (see https://github.com/carstencodes/nt2dc).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#
"""Replacements for generic types built in python 3.8 or earlier.
"""

import typing
import collections
import collections.abc
import contextlib
import re

BuiltInReplacements: typing.Dict[typing.Type, typing.Type] = {
    tuple: typing.Tuple,
    collections.abc.Callable: typing.Callable,
    type: typing.Type,
    dict: typing.Dict,
    list: typing.List,
    set: typing.Set,
    frozenset: typing.FrozenSet,
    collections.defaultdict: typing.DefaultDict,
    collections.OrderedDict: typing.OrderedDict,
    collections.ChainMap: typing.ChainMap,
    collections.Counter: typing.Counter,
    collections.deque: typing.Deque,
    re.Pattern: typing.Pattern,
    re.Match: typing.Match,
    collections.abc.Set: typing.Set,
    collections.abc.ByteString: typing.ByteString,
    collections.abc.Collection: typing.Collection,
    collections.abc.Container: typing.Container,
    collections.abc.ItemsView: typing.ItemsView,
    collections.abc.KeysView: typing.KeysView,
    collections.abc.Mapping: typing.Mapping,
    collections.abc.MappingView: typing.MappingView,
    collections.abc.MutableMapping: typing.MutableMapping,
    collections.abc.MutableSequence: typing.MutableSequence,
    collections.abc.MutableSet: typing.MutableSet,
    collections.abc.Sequence: typing.Sequence,
    collections.abc.ValuesView: typing.ValuesView,
    collections.abc.Iterable: typing.Iterable,
    collections.abc.Iterator: typing.Iterator,
    collections.abc.Generator: typing.Generator,
    collections.abc.Reversible: typing.Reversible,
    collections.abc.Coroutine: typing.Coroutine,
    collections.abc.AsyncGenerator: typing.AsyncGenerator,
    collections.abc.AsyncIterable: typing.AsyncIterable,
    collections.abc.AsyncIterator: typing.AsyncIterator,
    collections.abc.Awaitable: typing.Awaitable,
    contextlib.AbstractContextManager: typing.ContextManager,
    contextlib.AbstractAsyncContextManager: typing.AsyncContextManager,
}

BuiltInNames: typing.Dict[typing.Type, str] = {
    typing.Tuple: "typing.Tuple",
    typing.Callable: "typing.Callable",
    typing.Type: "typing.Type",
    typing.Dict: "typing.Dict",
    typing.List: "typing.List",
    typing.FrozenSet: "typing.FrozenSet",
    typing.DefaultDict: "typing.DefaultDict",
    typing.OrderedDict: "typing.OrderedDict",
    typing.ChainMap: "typing.ChainMap",
    typing.Counter: "typing.Counter",
    typing.Deque: "typing.Deque",
    typing.Pattern: "typing.Pattern",
    typing.Match: "typing.Match",
    typing.Set: "typing.Set",
    typing.ByteString: "typing.ByteString",
    typing.Collection: "typing.Collection",
    typing.Container: "typing.Container",
    typing.ItemsView: "typing.ItemsView",
    typing.KeysView: "typing.KeysView",
    typing.Mapping: "typing.Mapping",
    typing.MappingView: "typing.MappingView",
    typing.MutableMapping: "typing.MutableMapping",
    typing.MutableSequence: "typing.MutableSequence",
    typing.MutableSet: "typing.MutableSet",
    typing.Sequence: "typing.Sequence",
    typing.ValuesView: "typing.ValuesView",
    typing.Iterable: "typing.Iterable",
    typing.Iterator: "typing.Iterator",
    typing.Generator: "typing.Generator",
    typing.Reversible: "typing.Reversible",
    typing.Coroutine: "typing.Coroutine",
    typing.AsyncGenerator: "typing.AsyncGenerator",
    typing.AsyncIterable: "typing.AsyncIterable",
    typing.AsyncIterator: "typing.AsyncIterator",
    typing.Awaitable: "typing.Awaitable",
    typing.ContextManager: "typing.ContextManager",
    typing.AsyncContextManager: "typing.AsyncContextManager",
}
