# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
Creating Lawwenda filesystems.
"""

import re
import typing as t

import lawwenda.fs.decorators
import lawwenda.fs.local


class _PredicateFactory:
    """
    Used by :py:func:`create_filesystem` for translating its arguments into filter predicates.
    """

    @staticmethod
    def false(node):  # pylint: disable=unused-argument
        """
        Return `False` for each node.
        """
        return False

    @staticmethod
    def excludehidden(node):
        """
        Return `True` for a hidden node.
        """
        return node.is_hidden

    @staticmethod
    def p_or(*preds):
        """
        Return a predicate that returns `True` iff at least one of the input predicates return `True`.

        :param preds: The input predicates.
        """
        def npred(node):
            for pred in preds:
                if pred(node):
                    return True
            return False
        return npred

    @staticmethod
    def p_not(pred):
        """
        Return a predicate that inverts the input predicate.

        :param pred: The input predicate.
        """
        def npred(node):
            return not pred(node)
        return npred

    @staticmethod
    def p_descending(pred):
        """
        Return a predicate that returns `True` iff the input predicate returns `True` for the input node and/or some
        nodes in its subtree (if it is a directory).

        :param pred: The input predicate.
        """
        def npred(node):  # TODO cache
            for ccn, _ in node.traverse_dir(raise_on_circle=False):
                if pred(ccn):
                    return True
            return False
        return npred

    @staticmethod
    def p_regexp(restr):
        """
        Return a predicate that returns `True` for input nodes whose :py:attr:`Filesystem.Node.path` matches the given
        regular expression.

        :param restr: The regular expression string.
        """
        repat = re.compile(restr)
        def npred(node):
            return bool(repat.fullmatch(node.path))
        return npred

    @staticmethod
    def p_tag(tag):
        """
        Return a predicate that returns `True` for input nodes whose :py:attr:`Filesystem.Node.tags` contain the given
        tag.

        :param tag: The tag to look for.
        """
        def npred(node):
            return tag in node.tags
        return npred


def decorate_filesystem(filesystem: lawwenda.fs.Filesystem, *, readonly: bool = False,
                        hide_by_patterns: t.Iterable[str] = (), hide_by_tags: t.Iterable[str] = (),
                        include_by_patterns: t.Optional[t.Iterable[str]] = None,
                        include_by_tags: t.Optional[t.Iterable[str]] = None,
                        exclude_by_patterns: t.Iterable[str] = (), exclude_by_tags: t.Iterable[str] = (),
                        exclude_hidden: bool = False) -> lawwenda.fs.Filesystem:  # TODO to new module?!
    """
    Decorates a filesystem with some access control and more.

    :param filesystem: The filesystem to decorate.
    :param readonly: Whether it should block write accesses.
    :param hide_by_patterns: TODO.
    :param hide_by_tags: TODO.
    :param include_by_patterns: TODO.
    :param include_by_tags: TODO.
    :param exclude_by_patterns: TODO.
    :param exclude_by_tags: TODO.
    :param exclude_hidden: TODO.
    """
    # pylint: disable=too-many-locals
    preds = _PredicateFactory
    if readonly:
        filesystem = lawwenda.fs.decorators.ReadOnlyFilesystemDecorator(filesystem)
    hidepred = preds.false
    for hide_by_pattern in hide_by_patterns:
        hidepred = preds.p_or(hidepred, preds.p_regexp(hide_by_pattern))
    for hide_by_tag in hide_by_tags:
        hidepred = preds.p_or(hidepred, preds.p_tag(hide_by_tag))
    if hidepred is not preds.false:
        filesystem = lawwenda.fs.decorators.HideNodesFilesystemDecorator(filesystem, hidepred)
    excludepred = preds.false
    for exclude_by_pattern in exclude_by_patterns:
        excludepred = preds.p_or(excludepred, preds.p_regexp(exclude_by_pattern))
    for exclude_by_tag in exclude_by_tags:
        excludepred = preds.p_or(excludepred, preds.p_tag(exclude_by_tag))
    if (include_by_patterns is not None) or (include_by_tags is not None):
        includepred = preds.false
        for include_by_pattern in include_by_patterns or []:
            includepred = preds.p_or(includepred, preds.p_regexp(include_by_pattern))
        for include_by_tag in include_by_tags or []:
            includepred = preds.p_or(includepred, preds.p_tag(include_by_tag))
        excludepred = preds.p_or(excludepred, preds.p_not(preds.p_descending(includepred)))
    if exclude_hidden:
        excludepred = preds.p_or(excludepred, _PredicateFactory.excludehidden)
    if excludepred is not preds.false:
        filesystem = lawwenda.fs.decorators.ExcludeNodesFilesystemDecorator(filesystem, excludepred)
    return filesystem


def create_filesystem(rootpath: str, **kwargs) -> lawwenda.fs.Filesystem:
    """
    Create a :py:class:`Filesystem` resembling a particular subtree of your real local filesystem, with some
    configuration for access control and more.

    See :py:func:`decorate_filesystem` for details about the parameters.

    :param rootpath: The path from your real local filesystem to consider as the root directory.
    """
    # TODO xx refactor and test all this scariness
    return decorate_filesystem(lawwenda.fs.local.LocalFilesystem(rootpath), **kwargs)
