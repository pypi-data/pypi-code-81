# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Git test helpers based on the actual Git

This module does not depend on the dulwich library, hence avoiding
a Python dependency and potential tautology problems in the testing
of code that relies on dulwich.

The price to pay for that is to assume the non-Python dependency on Git,
typically solved by installing Git system-wide.
"""
import subprocess
from mercurial import pycompat

ZERO_SHA = b'0' * 40
"""Git null commit.

Used notably to represent creation and deletion of Git refs.

It is actually identical to Mercurial's `nullid`, but that could change
at some point.

It is also identical to ``dulwich.protocol.ZERO_SHA``, but we don't want
to depend on dulwich here.
"""


def extract_git_branch_titles(branches):
    return {ref: info['title'] for ref, info in branches.items()}


class GitRepo(object):
    """Represent a Git repository, relying on the Git executable.

    The ``git`` command is expected to be available on the ``PATH``.
    """

    def __init__(self, path):
        self.path = path

    @classmethod
    def init(cls, path):
        subprocess.call(('git', 'init', '--bare', str(path)))
        return cls(path)

    def branch_titles(self):
        return extract_git_branch_titles(self.branches())

    def branches(self):
        out = subprocess.check_output(('git', 'branch', '-v', '--no-abbrev'),
                                      cwd=str(self.path))
        split_lines = (l.lstrip(b'*').strip().split(None, 2)
                       for l in out.splitlines())
        return {sp[0]: dict(sha=sp[1], title=sp[2]) for sp in split_lines}

    def tags(self):
        out = subprocess.check_output(('git', 'tag'), cwd=str(self.path))
        return set(l.strip() for l in out.splitlines())

    def commit_hash_title(self, revspec):
        out = subprocess.check_output(
            ('git', 'log', '-n1', revspec, r'--pretty=format:%H|%s'),
            cwd=str(self.path))
        return out.strip().split(b'|')

    def get_symref(self, name):
        return self.path.join(name).read().strip().split(':', 1)[1].strip()

    def set_symref(self, name, target_ref):
        self.path.join(name).write('ref: %s\n' % target_ref)

    def set_branch(self, name, sha):
        sha = pycompat.sysstr(sha)
        self.path.join('refs', 'heads', name).ensure().write(sha + '\n')

    def get_branch_sha(self, name):
        if isinstance(name, bytes):
            name = name.decode()
        return self.path.join('refs', 'heads', name).read().strip()

    def write_ref(self, ref_path, value):
        """Call git to write a ref.

        symbolic refs are taken at face value, hence
        ``write_git_ref(repo, b'HEAD', b'refs/heads/mybranch')`` will move
        ``HEAD`` to ``mybranch``, instead of moving whatever ``HEAD``
        points to.
        """
        subprocess.check_call(('git', 'update-ref',
                               b'--no-deref', ref_path, value),
                              cwd=str(self.path))

    def all_refs(self):
        """Call git to return all refs.

        :return: a :class:`dict` whose keys are full ref paths and values are
           Git commit SHAs, both as :class:`bytes`.
        """
        lines = subprocess.check_output(('git', 'show-ref'),
                                        cwd=str(self.path)).splitlines()
        return {split[1]: split[0]
                for split in (line.split(b' ', 1) for line in lines)}
