# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Interaction with Git repos.

It is not expected that the rise of the HGitaly project would remove
all interesting things to do with Git.
"""
from __future__ import absolute_import

from hggit.git_handler import GitHandler
from heptapod.gitlab.branch import (
    gitlab_branch_from_ref as git_branch_from_ref,
)
from mercurial import (
    hg,
)
import re

from .branch import (
    GITLAB_TYPED_REFS_MISSING,
    set_default_gitlab_branch,
    gitlab_branches,
    gitlab_tags,
    write_gitlab_branches,
    write_gitlab_tags,
)
from .special_ref import (
    special_refs,
    write_special_refs
)
from .keep_around import (
    iter_keep_arounds,
    init_keep_arounds,
)
from .state_maintainer import GitLabStateMaintainer


class HeptapodGitHandler(GitHandler, GitLabStateMaintainer):

    def __init__(self, *args, **kwargs):
        super(HeptapodGitHandler, self).__init__(*args, **kwargs)

        main_repo = hg.sharedreposource(self.repo)
        if main_repo is None:
            main_repo = self.repo

        self.gitdir = re.sub(br'\.hg$', b'', main_repo.root) + b'.git'
        self.unfiltered_repo = self.repo.unfiltered()
        self._default_git_ref = None

        self.gitlab_refs = self.git.refs

    def get_default_gitlab_ref(self):
        # HEAD is the source of truth for GitLab default branch
        # For native projects, it's going to be the one stored
        # in Mercurial, returned by get_default_gitlab_branch(), and we are
        # maintaining consistency until we reach the HGitaly2 milestone
        # (i.e., as long as hg-git is used even for native projects)
        res = self._default_git_ref
        if res is None:
            res = self.git.refs.get_symrefs().get(b'HEAD')
            self._default_git_ref = res
        return res

    def set_default_gitlab_ref(self, new_default_ref):
        new_gl_branch = git_branch_from_ref(new_default_ref)
        self.repo.ui.note(
            b"Setting Git HEAD to %s and Hg default "
            b"GitLab branch to %s" % (new_default_ref, new_gl_branch))
        self.git.refs.set_symbolic_ref(b'HEAD', new_default_ref)
        set_default_gitlab_branch(self.repo, new_gl_branch)

        # cache invalidation
        self._default_git_ref = None

    hg_sha_from_gitlab_sha = GitHandler.map_hg_get
    gitlab_sha_from_hg_sha = GitHandler.map_git_get

    def extract_all_gitlab_refs(self):
        """Heptapod version of GitHandler.get_exportable().

        This rewraps :meth:`GitHandler.get_exportable` to add named branches
        and topics to the returned Git refs
        """
        git_refs = super(HeptapodGitHandler, self).get_exportable()
        self.extract_current_gitlab_branches(git_refs)
        return git_refs

    def export_commits(self):
        try:
            self.export_git_objects()
            self.update_gitlab_references()
        finally:
            self.save_map(self.map_file)

    def ensure_gitlab_branches(self):
        """Init GitLab branches state file from Git repository if needed.

        Nothing happens if the file is already present.

        :returns: ``None` if the file was already present. Otherwise,
           new GitLab branches :class:`dict`, same as
           ``gitlab_branches(self.repo)`` would.
        """
        repo = self.repo
        if gitlab_branches(repo) is not GITLAB_TYPED_REFS_MISSING:
            return

        self.ui.note(b"Initializing GitLab branches state file "
                     b"for repo at '%s'" % repo.root)

        gl_branches = self.gitlab_branches_hg_shas(self.git.refs.as_dict())
        write_gitlab_branches(repo, gl_branches)
        return gl_branches

    def ensure_gitlab_tags(self):
        """Init GitLab tags state file from Git repository if needed.

        Nothing happens if the file is already present.

        :returns: ``None` if the file was already present. Otherwise,
           new GitLab tags :class:`dict`, same as
           ``gitlab_tags(self.repo)`` would.
        """
        repo = self.repo
        if gitlab_tags(repo) is not GITLAB_TYPED_REFS_MISSING:
            return

        self.ui.note(b"Initializing GitLab tags state file "
                     b"for repo at '%s'" % repo.root)

        gl_tags = self.gitlab_tags_hg_shas(self.git.refs)
        write_gitlab_tags(repo, gl_tags)
        return gl_tags

    def ensure_gitlab_special_refs(self):
        """Init GitLab special refs file from Git repository if needed.

        Nothing happens if the file is already present.

        :returns: ``None` if the file was already present. Otherwise,
           new GitLab special refs :class:`dict`, same as
           ``special_refs(self.repo)`` would.
        """
        repo = self.repo
        if special_refs(repo) is not GITLAB_TYPED_REFS_MISSING:
            return

        self.ui.note(b"Initializing GitLab special refs state file "
                     b"for repo at '%s'" % repo.root)

        srefs = self.gitlab_special_refs_hg_shas(self.git.refs)
        write_special_refs(repo, srefs)
        return srefs

    def ensure_gitlab_keep_arounds(self):
        """Init GitLab keep arounds file from Git repository if needed.

        Nothing happens if the file is already present.

        :returns: ``None` if the file was already present. Otherwise,
           new GitLab keep-arounds :class:`set`.
        """
        repo = self.repo
        try:
            if next(iter_keep_arounds(repo)) is not GITLAB_TYPED_REFS_MISSING:
                return
        except StopIteration:
            return

        self.ui.note(b"Initializing GitLab keep-arounds state file "
                     b"for repo at '%s'" % repo.root)

        kas = self.gitlab_keep_arounds(self.git.refs)
        init_keep_arounds(repo, kas)
        return kas
