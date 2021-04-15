# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Test support for users of heptapod.gitlab
"""
from __future__ import absolute_import
import attr
from copy import deepcopy
import logging
import shutil

from heptapod.gitlab import hooks

from .hg import RepoWrapper
from .git import GitRepo
logger = logging.getLogger(__name__)


def patch_gitlab_hooks(monkeypatch, records, action=None):

    def call(self, changes):
        records.append((self.name, changes))
        if action is not None:
            return action(self.name, changes)
        else:
            return 0, ("hook %r ok" % self.name).encode(), 'no error'

    def init(self, repo, encoding='utf-8'):
        self.repo = repo
        self.encoding = encoding

    monkeypatch.setattr(hooks.Hook, '__init__', init)
    monkeypatch.setattr(hooks.PreReceive, '__call__', call)
    monkeypatch.setattr(hooks.PostReceive, '__call__', call)


@attr.s
class GitLabMirrorFixture:
    """Helper class to create fixtures for GitLab aware hg-git mirroring.

    The pytest fixture functions themselves will have to be provided with
    the tests that use them.

    It is not the role of this class to make decisions about scopes or
    the kind of root directory it operates in.

    There will be later on a fixture for Mercurial-native Heptapod
    repositories, hence GitLab notifications without a Git repository.
    """
    base_path = attr.ib()
    hg_repo_wrapper = attr.ib()
    git_repo = attr.ib()
    gitlab_notifs = attr.ib()
    import heptapod.testhelpers.gitlab

    @classmethod
    def init(cls, base_path, monkeypatch, hg_config=None,
             common_repo_name='repo'):
        if hg_config is None:
            config = {}
        else:
            config = deepcopy(hg_config)

        config.setdefault('extensions', {})['hggit'] = ''
        config['phases'] = dict(publish=False)

        hg_repo_wrapper = RepoWrapper.init(
            base_path / (common_repo_name + '.hg'),
            config=config)
        git_repo = GitRepo.init(base_path / (common_repo_name + '.git'))
        notifs = []
        patch_gitlab_hooks(monkeypatch, notifs)
        return cls(hg_repo_wrapper=hg_repo_wrapper,
                   git_repo=git_repo,
                   gitlab_notifs=notifs,
                   base_path=base_path)

    def clear_gitlab_notifs(self):
        """Forget about all notifications already sent to GitLab.

        Subsequent notifications will keep on being recorded in
        ``self.gitlab_notifs``.
        """
        del self.gitlab_notifs[:]

    def activate_mirror(self):
        """Make mirroring from Mercurial to Git repo automatic.

        This is essential to get the mirroring code to run in-transaction.
        """
        self.hg_repo_wrapper.repo.ui.setconfig(
            b'hooks', b'pretxnclose.testcase',
            b'python:heptapod.hooks.gitlab_mirror.mirror')

    def delete(self):
        git_path = self.git_repo.path
        try:
            shutil.rmtree(git_path)
        except Exception:
            logger.exception("Error removing the Git repo at %r", git_path)

        hg_path = self.hg_repo_wrapper.repo.root
        try:
            shutil.rmtree(hg_path)
        except Exception:
            logger.exception("Error removing the Mercurial repo at %r",
                             hg_path)

    def __enter__(self):
        return self

    def __exit__(self, *exc_args):
        self.delete()
        return False  # no exception handling related to exc_args
