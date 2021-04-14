# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
Filesystem decorators.

Used for filtering nodes from existing filesystems, influence access control or other things.
"""

import typing as t

import lawwenda.fs


FilesystemNodePredicate = t.Callable[["Filesystem.Node"], bool]


class AbstractFilesystemDecorator(lawwenda.fs.Filesystem):  # pylint: disable=abstract-method
    """
    TODO.
    """
    # TODO child_nodes broken (e.g. wrong "filesystem")?

    def __init__(self, inner: lawwenda.fs.Filesystem):
        super().__init__()
        self._inner = inner

    def _eval_predicate(self, pred, node):
        return pred(self._inner.node_by_path(node.path))

    def child_nodes(self, handle):
        return [handle.readable_node.child_by_name(n.name) for n
                in self._inner.child_nodes(self._inner.get_readhandle(self._inner.node_by_path(
                handle.readable_node.path)))]

    def __getattribute__(self, item):
        if (item not in ["node_by_path", "rootnode"]) and (not item.startswith("_")) \
                and (not type(self).__dict__.get(item)) and hasattr(self._inner, item):
            return getattr(self._inner, item)
        return super().__getattribute__(item)


class HideNodesFilesystemDecorator(AbstractFilesystemDecorator):  # pylint: disable=abstract-method
    """
    Decorator for filesystems that marks some nodes.
    """

    def __init__(self, inner: lawwenda.fs.Filesystem, pred: FilesystemNodePredicate):
        super().__init__(inner)
        self.__pred = pred

    def is_hidden(self, handle):
        return self._eval_predicate(self.__pred, handle.readable_node) or self._inner.is_hidden(handle)


class ExcludeNodesFilesystemDecorator(AbstractFilesystemDecorator):  # pylint: disable=abstract-method
    """
    Decorator for filesystems that forcefully excludes some nodes.
    """
    # TODO check if all parent dirs are also not excluded?!

    def __init__(self, inner: lawwenda.fs.Filesystem, pred: FilesystemNodePredicate):
        super().__init__(inner)
        self.__pred = pred

    def child_nodes(self, handle):  # TODO noh dedup
        return [handle.readable_node.child_by_name(n.name)
                for n in self._inner.child_nodes(self._inner.get_readhandle(
                    self._inner.node_by_path(handle.readable_node.path)))
                if not self._eval_predicate(self.__pred, n)]

    def get_readhandle(self, node):
        if self._eval_predicate(self.__pred, node):
            raise PermissionError(f"no read access for {node.path}")
        return self._inner.get_readhandle(node)  # TODO noh dangerous trap: must not use super() here (better api?!)

    def get_writehandle(self, node):
        if self._eval_predicate(self.__pred, node):
            raise PermissionError(f"no write access for {node.path}")
        return self._inner.get_writehandle(node)


class ReadOnlyFilesystemDecorator(AbstractFilesystemDecorator):  # pylint: disable=abstract-method
    """
    Decorator for filesystems that blocks all write accesses.
    """

    def get_writehandle(self, node):
        raise PermissionError(f"no write access for {node.path}")
