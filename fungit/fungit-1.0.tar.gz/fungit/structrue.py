from typing import Dict, List

from .shared import GitType, GitActionStatus, TREE


class Selected(GitType):
    selects: List = []
    selects_len: int = 0

    selected: Dict = {}
    change: Dict = {}
    action: GitActionStatus = GitActionStatus.NONE

    full = False
    tip: str = ''

    @classmethod
    def initial(cls) -> None:
        cls.selected['old_selected'] = 0
        cls.selected['selected'] = cls.STATUS
        cls.selected[cls.STATE] = 0
        cls.selected[cls.STATUS] = 0
        cls.selected[cls.BRANCH] = 0
        cls.selected[cls.COMMIT] = 0
        cls.selected[cls.STASH] = 0
        cls.selected[cls.CONTENT] = 0

        cls.selects = [cls.STATE, cls.STATUS,
                       cls.BRANCH, cls.COMMIT, cls.STASH]

        cls.selects_len = 5

        cls.change = {}
        for i in cls.selects:  # Mark whether a category has changed
            cls.change[i] = False

        cls.change[cls.CONTENT] = False

    @classmethod
    @property
    def old(cls):
        return cls.selected['old_selected']

    @classmethod
    @property
    def current(cls):
        return cls.selected['selected']

    @classmethod
    @property
    def state(cls):
        return 0

    @classmethod
    @property
    def status(cls):
        return cls.selected[cls.STATUS]

    @classmethod
    @property
    def branch(cls):
        return cls.selected[cls.BRANCH]

    @classmethod
    @property
    def commit(cls):
        return cls.selected[cls.COMMIT]

    @classmethod
    @property
    def content(cls):
        return cls.selected[cls.CONTENT]
