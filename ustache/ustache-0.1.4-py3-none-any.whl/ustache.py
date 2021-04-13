"""
ustache module.

This module alone implements the entire ustache library, including its
minimal command line interface.

The main functions are considered to be :func:`cli`, :func:`render` and
:func:`stream`, as they expose different approaches to template rendering.

Other functionality will be considered as **advanced**, exposing
implementation-specific complexity and potentially introducing non-standard
mustache behavior.

"""
"""
ustache, Mustache for Python
============================

See `README.md`_ provided as part of source distributions or available online
at the `project repository`_.

.. _README.md: https://gitlab.com/ergoithz/ustache/-/blob/master/README.md
.. _project repository: https://gitlab.com/ergoithz/ustache


License
-------

Copyright (c) 2021, Felipe A Hernandez.

MIT License (see `LICENSE`_).

.. _LICENSE: https://gitlab.com/ergoithz/ustache/-/blob/master/LICENSE

"""

import codecs
import collections
import collections.abc
import functools
import typing

try:
    import xxhash
    _cache_hash = next(filter(None, (
        getattr(xxhash, name, None)
        for name in (
            'xxh3_128_intdigest',
            'xxh128_intdigest',
            'xxh64_intdigest',
            )
        )))
    """Generate template hash using the fastest algorithm available."""
except (ImportError, StopIteration):
    def _cache_hash(template: str) -> str:
        """Get template itself as hash fallback."""
        return template

__author__ = 'Felipe A Hernandez'
__email__ = 'ergoithz@gmail.com'
__license__ = 'MIT'
__version__ = '0.1.4'
__all__ = (
    # api
    'tokenize',
    'stream',
    'render',
    'cli',
    # exceptions
    'TokenException',
    'ClosingTokenException',
    'UnclosedTokenException',
    'DelimiterTokenException',
    # defaults
    'default_resolver',
    'default_getter',
    'default_stringify',
    'default_escape',
    'default_lambda_render',
    'default_tags',
    'default_cache',
    'default_virtuals',
    # types
    'TString',
    'PartialResolver',
    'PropertyGetter',
    'StringifyFunction',
    'EscapeFunction',
    'LambdaRenderFunctionFactory',
    'LambdaRenderFunctionConstructor',
    'CompiledTemplate',
    'CompiledToken',
    'CompiledTemplateCache',
    'TagsTuple',
    )

T = typing.TypeVar('T')
"""Generic."""

TString = typing.TypeVar('TString', str, bytes)
"""String/bytes generic."""

PartialResolver = typing.Callable[[bytes], bytes]
"""Template partial tag resolver function interface."""

PropertyGetter = typing.Callable[
    [typing.Any, typing.Sequence[typing.Any], bytes],
    bytes,
    ]
"""Template property getter function interface."""

StringifyFunction = typing.Callable[[bytes, bool], bytes]
"""Template variable general stringification function interface."""

EscapeFunction = typing.Callable[[bytes], bytes]
"""Template variable value escape function interface."""

LambdaRenderFunctionConstructor = typing.Callable[
    ...,
    typing.Callable[..., typing.AnyStr],
    ]
"""Lambda render function constructor interface."""

LambdaRenderFunctionFactory = LambdaRenderFunctionConstructor
"""
.. deprecated:: 0.1.3
    Use :attr:`LambdaRenderFunctionConstructor` instead.

"""

VirtualPropertyFunction = typing.Callable[[typing.Any], typing.Any]
"""Virtual property implementation callable interface."""

VirtualPropertyMapping = typing.Mapping[str, VirtualPropertyFunction]
"""Virtual property mapping interface."""

TagsTuple = typing.Tuple[bytes, bytes]
"""Mustache tag tuple interface."""

CompiledToken = typing.Tuple[
    int,  # type
    # 0. end
    # 1. echo
    # 2. variable
    # 3. block
    # 4. close
    # 5. partial
    # 6. tags
    # 7. comment
    typing.Optional[slice],  # token name slice
    typing.Optional[slice],  # token content slice
    int,  # flag
    # - variable: 0. unescaped, 1. escape
    # - block: 0. falsy, 1. truthy
    # - close: block.index
    ]
"""Compiled template token interface."""

CompiledTemplate = typing.List[CompiledToken]
"""Compiled template interface."""

CompiledTemplateCache = typing.Mapping[
    typing.Tuple[typing.Union[bytes, int], bytes, bytes, bool],
    CompiledTemplate,
    ]
"""Cache mapping interface."""


class LRUCache(collections.OrderedDict, typing.Generic[T]):
    """Capped mapping discarding least recently used elements."""

    def __init__(self, maxsize: int, *args, **kwargs) -> None:
        """
        Initialize.

        :param maxsize: maximum number of elements will be kept

        Any parameter excess will be passed straight to dict constructor.

        """
        self.maxsize = maxsize
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: typing.Hashable) -> T:
        """
        Get value for given key.

        :param key: hashable
        :returns: value if any matching key
        :raises KeyError: if given key is not found

        """
        self.move_to_end(key)
        return super().__getitem__(key)

    def __setitem__(self, key: typing.Hashable, value: T) -> None:
        """
        Set value for given key.

        :param key: hashable will be used to retrieve values later on
        :param value: value for given key

        """
        super().__setitem__(key, value)
        try:
            self.move_to_end(key)
            while len(self) > self.maxsize:
                self.popitem(last=False)
        except KeyError:  # race condition
            pass


class DefaultVirtualProperties(collections.abc.Mapping):
    """
    Immutable mapping with default virtual properties.

    The following virtual properties are implemented:

    - **length**, for non-mapping sized objects, returning ``len(ref)``.

    """

    _keys = (
        'length',
        )
    __len__ = staticmethod(_keys.__len__)
    __iter__ = staticmethod(_keys.__iter__)

    @classmethod
    def _virtual_length(cls, ref: typing.Any) -> int:
        """
        Resolve virtual length property.

        :param ref: any non-mapping object implementing `__len__`
        :returns: number of items
        :raises TypeError: if ref is mapping or has no `__len__` method

        """
        if not isinstance(ref, collections.abc.Mapping):
            return len(ref)
        raise TypeError

    @classmethod
    def __getitem__(cls, name):
        """Get self[name]."""
        try:
            return getattr(cls, f'_virtual_{name}')
        except AttributeError:
            raise KeyError(name)


default_tags = (b'{{', b'}}')
"""Tuple of default mustache tags (in bytes)."""

default_cache: CompiledTemplateCache = LRUCache(1024)
"""
Default template cache mapping, keeping the 1024 most recently used
compiled templates (LRU expiration).

If `xxhash`_ is available, template data won't be included in cache.

.. _xxhash: https://pypi.org/project/xxhash/

"""

default_virtuals: VirtualPropertyMapping = DefaultVirtualProperties()
"""
Immutable mapping with default virtual properties.

The following virtual properties are implemented:

- **length**, for non-mapping sized objects, returning ``len(ref)``.

"""


class TokenException(SyntaxError):
    """Invalid token found during tokenization."""

    message = 'Invalid tag {tag} at line {row} column {column}'

    @classmethod
    def from_template(
            cls: typing.Type[T],
            template: bytes,
            start: int,
            end: int,
            ) -> T:
        """
        Create exception instance from parsing data.

        :param template: template bytestring
        :param start: character position where the offending tag starts at
        :param end: character position where the offending tag ends at
        :returns: exception instance

        """
        tag = template[start:end].decode()
        row = 1 + template[:start].count(b'\n')
        column = 1 + start - max(0, template.rfind(b'\n', 0, start))
        return cls(cls.message.format(tag=tag, row=row, column=column))


class ClosingTokenException(TokenException):
    """Non-matching closing token found during tokenization."""

    message = 'Non-matching tag {tag} at line {row} column {column}'


class UnclosedTokenException(ClosingTokenException):
    """Unclosed token found during tokenization."""

    message = 'Unclosed tag {tag} at line {row} column {column}'


class DelimiterTokenException(TokenException):
    """
    Invalid delimiters token found during tokenization.

    .. versionadded:: 0.1.1

    """

    message = 'Invalid delimiters {tag} at line {row} column {column}'


def default_stringify(
        data: typing.Any,
        text: bool = False,
        ) -> typing.Generator[bytes, None, None]:
    """
    Convert arbitrary data to bytes.

    :param data: value will be serialized
    :param text: whether running in text mode or not (bytes mode)
    :returns: bytes generator

    """
    if isinstance(data, collections.abc.ByteString) and not text:
        yield data
    elif isinstance(data, str):
        yield data.encode()
    else:
        yield f'{data}'.encode()


def replay(
        recording: CompiledTemplate,
        start: int = 0,
        ) -> typing.Generator[typing.Optional[CompiledToken], int, None]:
    """
    Yield template tokenization from cached data.

    Returned generator accepts sending back an index, which will yield None,
    and will make the generator to restart yielding tokens from that position.

    :param recording: token list
    :param start: starting index
    :returns: token tuple generator

    """
    size = len(recording)
    token = recording.__getitem__
    while True:
        for item in map(token, range(start, size)):
            start = yield item
            if start is not None:
                yield
                break
        else:
            break


def default_escape(data: bytes) -> bytes:
    """
    Convert bytes conflicting with HTML to their escape sequences.

    :param data: bytestring containing text
    :returns: escaped text bytes

    """
    return (
        data
        .replace(b'&', b'&amp;')
        .replace(b'<', b'&lt;')
        .replace(b'>', b'&gt;')
        .replace(b'"', b'&quot;')
        .replace(b'\'', b'&#x60;')
        .replace(b'`', b'&#x3D;')
        )


def default_resolver(name: typing.AnyStr) -> bytes:
    """
    Mustache partial resolver function (stub).

    :param name: partial template name
    :returns: empty bytes

    """
    return b''


def default_getter(
        scope: typing.Any,
        scopes: typing.Sequence[typing.Any],
        key: typing.AnyStr,
        default: typing.Any = None,
        *,
        virtuals: VirtualPropertyMapping = default_virtuals,
        ) -> typing.Any:
    """
    Extract property value from scope hierarchy.

    :param scope: uppermost scope (corresponding to '.')
    :param scopes: parent scope sequence
    :param key: property key
    :param default: value will be used as default when missing
    :param virtuals: mapping of virtual property callables
    :return: value from scope or default

    .. versionadded:: 0.1.3
       *virtuals* parameter.

    Both :class:`AttributeError` and :class:`TypeError` exceptions
    raised by virtual property implementations will be handled as if
    that property doesn't exist, which can be useful to filter out
    incompatible types.

    """
    if key in (b'.', '.'):
        return scope

    binary_mode = not isinstance(key, str)
    components = key.split(b'.' if binary_mode else '.')
    for source in ((scope,), reversed(scopes)):
        for ref in source:
            for name in components:
                if binary_mode:
                    try:
                        ref = ref[name]
                        continue
                    except (KeyError, TypeError, AttributeError):
                        pass
                    try:
                        ref = virtuals[name](ref)
                        continue
                    except (KeyError, TypeError, AttributeError):
                        pass
                    try:
                        name = name.decode()
                    except UnicodeDecodeError:
                        break
                try:
                    ref = ref[name]
                    continue
                except (KeyError, TypeError, AttributeError):
                    pass
                try:
                    ref = (
                        ref[int(name)]
                        if name.isdigit() else
                        getattr(ref, name)
                        )
                    continue
                except (KeyError, TypeError, AttributeError, IndexError):
                    pass
                try:
                    ref = virtuals[name](ref)
                    continue
                except (KeyError, TypeError, AttributeError):
                    pass
                break
            else:
                return ref
    return default


def default_lambda_render(
        scope: typing.Any,
        **kwargs,
        ) -> typing.Callable[[TString], TString]:
    r"""
    Generate a template-only render function with fixed parameters.

    :param scope: current scope
    :param \**kwargs: parameters forwarded to :func:`render`
    :returns: template render function

    """

    def lambda_render(template: TString) -> TString:
        """
        Render given template to string/bytes.

        :param template: template text
        :returns: rendered string or bytes (depending on template type)

        """
        return render(template, scope, **kwargs)

    return lambda_render


def slicestrip(template: bytes, start: int, end: int) -> slice:
    """
    Strip slice from whitespace on bytes.

    :param template: bytes where whitespace should be stripped
    :param start: substring slice start
    :param end: substring slice end
    :returns: resulting stripped slice

    """
    c = template[start:end]
    return slice(end - len(c.lstrip()), start + len(c.rstrip()))


def tokenize(
        template: bytes,
        *,
        tags: TagsTuple = default_tags,
        comments: bool = False,
        cache: CompiledTemplateCache = default_cache,
        ) -> typing.Generator[typing.Optional[CompiledToken], int, None]:
    """
    Generate token tuples from mustache template.

    Returned generator accepts sending back an index, which will cause tokens
    to replay starting from it (up to current position) and then will resume
    token generation (but be aware of send call itself yields None).

    :param template: template as utf-8 encoded bytes
    :param tags: mustache tag tuple (open, close)
    :param comments: whether yield comment tokens or not (ignore comments)
    :param cache: mutable mapping for compiled template cache
    :return: token tuple generator (type, name slice, content slice, option)

    """
    tokenization_key = _cache_hash(template), *tags, comments

    if tokenization_key in cache:
        yield from replay(cache[tokenization_key])
        return

    template_find = template.find

    stack = []
    stack_append = stack.append
    stack_pop = stack.pop
    scope_label = slice(None)
    scope_head = 0
    scope_start = 0
    scope_index = 0

    start_tag, end_tag = tags
    end_literal, end_switch = b'}' + end_tag, b'=' + end_tag
    start_len, end_len, end_literal_len, end_switch_len = map(len, (
        start_tag,
        end_tag,
        end_literal,
        end_switch,
        ))

    t = slice
    s = functools.partial(slicestrip, template)
    cursor = 0
    recording = []
    record = recording.append
    while True:
        # text
        text_start, text_end = cursor, template_find(start_tag, cursor)
        if text_end == -1:
            if stack:
                raise UnclosedTokenException.from_template(
                    template=template,
                    start=scope_head,
                    end=scope_start,
                    )
            value = 0, None, t(text_start, None), -1
            record(value)
            cache[tokenization_key] = recording
            yield value
            break

        if text_start < text_end:
            value = 1, None, t(text_start, text_end), -1
            record(value)
            yield value

        cursor = text_end + start_len
        tag_type = template[cursor]

        if 47 == tag_type:  # b'/' - {{/closing}}
            cursor += 1
            tag_start, tag_end = cursor, template_find(end_tag, cursor)
            cursor = tag_end + end_len

            if template[scope_label] != template[tag_start:tag_end].strip():
                raise ClosingTokenException.from_template(
                    template=template,
                    start=text_end,
                    end=cursor,
                    )

            index = scope_index + 1
            value = 4, scope_label, s(scope_start, text_end), index
            scope_label, scope_head, scope_start, scope_index = stack_pop()

        elif 35 == tag_type:  # b'#' - {{#truthy}}{{.}}{{/turthy}}
            cursor += 1
            tag_start, tag_end = cursor, template_find(end_tag, cursor)
            cursor = tag_end + end_len

            stack_append((scope_label, text_end, scope_start, scope_index))
            scope_label = s(tag_start, tag_end)
            scope_head = text_end
            scope_start = cursor
            scope_index = len(recording)
            value = 3, scope_label, None, 1

        elif 94 == tag_type:  # b'^' - {{^falsy}}falsy{{/falsy}}
            cursor += 1
            tag_start, tag_end = cursor, template_find(end_tag, cursor)
            cursor = tag_end + end_len

            stack_append((scope_label, text_end, scope_start, scope_index))
            scope_label = s(tag_start, tag_end)
            scope_head = text_end
            scope_start = cursor
            scope_index = len(recording)
            value = 3, scope_label, None, 0

        elif 62 == tag_type:  # b'>' - {{>partial}}
            cursor += 1
            tag_start, tag_end = cursor, template_find(end_tag, cursor)
            cursor = tag_end + end_len
            value = 5, s(tag_start, tag_end), None, -1

        elif 123 == tag_type:  # b'&' = {{{ unescaped }}}
            cursor += 1
            tag_start, tag_end = cursor, template_find(end_literal, cursor)
            cursor = tag_end + end_literal_len
            value = 2, s(tag_start, tag_end), None, 0

        elif 38 == tag_type:  # b'&' = {{& unescaped }}
            cursor += 1
            tag_start, tag_end = cursor, template_find(end_tag, cursor)
            cursor = tag_end + end_len
            value = 2, s(tag_start, tag_end), None, 0

        elif 33 == tag_type:  # b'!' - {{! comment }}
            if not comments:
                cursor = template_find(end_tag, cursor + 1) + end_len
                continue

            cursor += 1
            tag_start, tag_end = cursor, template_find(end_tag, cursor)
            cursor = tag_end + end_len
            value = 7, None, s(tag_start, tag_end), -1

        elif 61 == tag_type:  # b'=' - {{=START-DELIMITER END-DELIMITER=}}
            cursor += 1
            tag_start, tag_end = cursor, template_find(end_switch, cursor)
            cursor = tag_end + end_switch_len

            try:
                start_tag, end_tag = template[tag_start:tag_end].split(b' ')
                if not (start_tag and end_tag):
                    raise ValueError
            except ValueError:
                raise DelimiterTokenException.from_template(
                    template=template,
                    start=text_end,
                    end=cursor,
                    )

            end_literal = b'}' + end_tag
            end_switch = b'=' + end_tag
            start_len, end_len, end_literal_len, end_switch_len = map(len, (
                start_tag,
                end_tag,
                end_literal,
                end_switch,
                ))
            start_end = tag_start + start_len
            end_start = tag_end - end_len
            value = 6, s(tag_start, start_end), s(end_start, tag_end), -1

        else:  # {{variable}}
            tag_start, tag_end = cursor, template_find(end_tag, cursor)
            cursor = tag_end + end_len
            value = 2, s(tag_start, tag_end), None, 1

        if tag_end < 0:
            raise UnclosedTokenException.from_template(
                template=template,
                start=tag_start,
                end=tag_end,
                )

        record(value)
        rewind = yield value
        if rewind is not None:
            yield
            yield from replay(recording, rewind)


def process(
        template: typing.AnyStr,
        scope: typing.Any,
        *,
        scopes: typing.Iterable[typing.Any] = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter = default_getter,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        ) -> typing.Generator[bytes, int, None]:
    """
    Generate rendered mustache template byte chunks.

    :param template: mustache template string
    :param scope: root object used as root mustache scope
    :param scopes: iterable of parent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: lambda render function constructor
    :param tags: mustache tag tuple (open, close)
    :param cache: mutable mapping for compiled template cache
    :return: byte chunk generator

    """
    text_mode = isinstance(template, str)

    # encoding
    template = (
        template.encode()
        if text_mode else
        template
        )
    tags = tuple(
        tag.encode() if isinstance(tag, str) else tag
        for tag in tags
        )

    # current context
    silent = False
    siblings = None
    callback = None

    # context stack
    stack = []
    stack_append = stack.append
    stack_pop = stack.pop

    # scope stack
    scopes = list(scopes)
    scopes_append = scopes.append
    scopes_pop = scopes.pop

    # locals
    t = template.__getitem__
    d = (lambda x: template[x].decode()) if text_mode else t
    missing = object()
    falsy_primitives = None, False, 0, float('nan'), float('-nan')
    TIterable = collections.abc.Iterable
    TNonLooping = (
        str,
        collections.abc.ByteString,
        collections.abc.Mapping,
        )
    TSequence = collections.abc.Sequence

    tokens = tokenize(template, tags=tags, cache=cache)
    while True:
        token_type, token_name, token_content, token_option = next(tokens)

        if 4 == token_type:  # closing/loop
            closing_scope = scope
            closing_siblings, closing_callback, _ = (
                siblings,
                callback,
                silent,
                )

            scope = scopes_pop()
            siblings, callback, silent = stack_pop()

            if not silent:
                if closing_callback:
                    yield from stringify(
                        closing_scope(
                            d(token_content),
                            lambda_render(
                                scope=scope,
                                scopes=scopes,
                                resolver=resolver,
                                escape=escape,
                                tags=tags,
                                cache=cache,
                                ),
                            ),
                        text_mode,
                        )

                if closing_siblings:
                    try:
                        sibling_scope = next(closing_siblings)

                        scopes_append(scope)
                        stack_append((siblings, silent, callback))

                        scope = sibling_scope
                        siblings = closing_siblings
                        silent = callback
                        callback = callable(sibling_scope)

                        tokens.send(token_option)
                    except StopIteration:
                        pass

        elif 3 == token_type:  # block
            scopes_append(scope)
            stack_append((siblings, callback, silent))

            if not silent:
                value = getter(scope, scopes, d(token_name).strip())
                falsy = (  # emulate JS falseness
                    value in falsy_primitives
                    or isinstance(value, TSequence) and not value
                    )
                if not token_option:  # falsy block
                    siblings = None
                    # scope = None
                    callback = False
                    silent = not falsy
                elif falsy:  # truthy block with falsy value
                    siblings = None
                    # scope = scope
                    callback = False
                    silent = True
                elif (
                        isinstance(value, TIterable)
                        and not isinstance(value, TNonLooping)
                        ):  # loop block
                    try:
                        siblings = iter(value)
                        scope = next(siblings)
                        callback = callable(scope)
                        silent = callback
                    except StopIteration:
                        siblings = None
                        scope = None
                        callback = False
                        silent = True
                else:  # truthy block with truthy value
                    siblings = None
                    scope = value
                    callback = callable(scope)
                    silent = callback

        elif token_type == 0:  # final text
            yield t(token_content)
            break

        elif not silent:
            if 1 == token_type:  # text
                yield t(token_content)

            elif 2 == token_type:  # variable
                value = getter(scope, scopes, d(token_name).strip(), missing)
                if value is not missing:
                    yield from (
                        map(escape, stringify(value, text_mode))
                        if token_option else
                        stringify(value, text_mode)
                        )

            elif 5 == token_type:  # partial
                value = resolver(d(token_name))
                if value:
                    yield from process(
                        template=value,
                        scope=scope,
                        scopes=scopes,
                        resolver=resolver,
                        escape=escape,
                        tags=tags,
                        cache=cache,
                        )

            elif 6 == token_type:  # tags
                tags = t(token_name), t(token_content)


def stream(
        template: TString,
        scope: typing.Any,
        *,
        scopes: typing.Iterable[typing.Any] = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter = default_getter,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        ) -> typing.Generator[TString, None, None]:
    """
    Generate rendered mustache template chunks.

    :param template: mustache template (str or bytes)
    :param scope: current rendering scope (data object)
    :param scopes: list of precedent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: lambda render function constructor
    :param tags: tuple (start, end) specifying the initial mustache delimiters
    :param cache: mutable mapping for compiled template cache
    :returns: generator of bytes/str chunks (type depends on template)

    """
    chunks = process(
        template=template,
        scope=scope,
        scopes=scopes,
        resolver=resolver,
        getter=getter,
        stringify=stringify,
        escape=escape,
        lambda_render=lambda_render,
        tags=tags,
        cache=cache,
        )
    yield from (
        codecs.iterdecode(chunks, 'utf8')
        if isinstance(template, str) else
        chunks
        )


def render(
        template: TString,
        scope: typing.Any,
        *,
        scopes: typing.Iterable[typing.Any] = (),
        resolver: PartialResolver = default_resolver,
        getter: PropertyGetter = default_getter,
        stringify: StringifyFunction = default_stringify,
        escape: EscapeFunction = default_escape,
        lambda_render: LambdaRenderFunctionConstructor = default_lambda_render,
        tags: TagsTuple = default_tags,
        cache: CompiledTemplateCache = default_cache,
        ) -> TString:
    """
    Render mustache template.

    :param template: mustache template
    :param scope: current rendering scope (data object)
    :param scopes: list of precedent scopes
    :param resolver: callable will be used to resolve partials (bytes)
    :param getter: callable will be used to pick variables from scope
    :param stringify: callable will be used to render python types (bytes)
    :param escape: callable will be used to escape template (bytes)
    :param lambda_render: lambda render function constructor
    :param tags: tuple (start, end) specifying the initial mustache delimiters
    :param cache: mutable mapping for compiled template cache
    :returns: rendered bytes/str (type depends on template)

    """
    data = b''.join(process(
        template=template,
        scope=scope,
        scopes=scopes,
        resolver=resolver,
        getter=getter,
        stringify=stringify,
        escape=escape,
        lambda_render=lambda_render,
        tags=tags,
        cache=cache,
        ))
    return data.decode() if isinstance(template, str) else data


def cli(argv: typing.Optional[typing.Sequence[str]] = None) -> None:
    """
    Render template from command line.

    Use `python -m ustache --help` to check available options.

    :param argv: command line arguments, :attr:`sys.argv` when None

    """
    import argparse
    import json
    import sys

    arguments = argparse.ArgumentParser(
        description='Render mustache template.',
        )
    arguments.add_argument(
        'template',
        metavar='PATH',
        type=argparse.FileType('r'),
        help='template file',
        )
    arguments.add_argument(
        '-j', '--json',
        metavar='PATH',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='JSON file, default: stdin',
        )
    arguments.add_argument(
        '-o', '--output',
        metavar='PATH',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='output file, default: stdout',
        )
    args = arguments.parse_args(argv)
    try:
        args.output.write(render(args.template.read(), json.load(args.json)))
    finally:
        args.template.close()
        if args.json is not sys.stdin:
            args.json.close()
        if args.output is not sys.stdout:
            args.output.close()


if __name__ == '__main__':
    cli()
