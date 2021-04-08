"""
This module encapsulates comments into a Tree comments hiearchy that make easy to iterate from a comment tree.
"""

from __future__ import annotations

from typing import Set

from pydecidim.model.comment import Comment


class CommentTreeElement:
    """
    The class CommentTreeElement points to parent and children of a current Tree.
    The root element does not have any parent.
    """

    @property
    def comment(self) -> Comment:
        return self.__comment

    @property
    def parent(self) -> CommentTreeElement or None:
        return self.__parent

    @property
    def childrens(self) -> Set[CommentTreeElement]:
        return self.__children

    def is_root(self) -> bool:
        """
        Checks if the current object is the root node. A root node does not have any parent.
        :return: True if the node is the root one. False otherwise.
        """
        return self.__parent is None

    def __init__(self, comment: Comment or None, parent: CommentTreeElement or None) -> None:
        self.__comment = comment
        self.__parent = parent
        if parent is not None:
            parent.add_children(self)
        self.__children: Set[CommentTreeElement] = set()

    def add_children(self, new_child: CommentTreeElement) -> None:
        """
        Adds a Comment as child.
        :param new_child: The child to be added.
        """
        self.__children.add(new_child)
