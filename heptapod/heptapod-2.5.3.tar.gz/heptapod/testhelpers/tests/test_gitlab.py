# Copyright 2019 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import shutil
from ..gitlab import GitLabMirrorFixture


def test_fixture_hg_teardown_error(tmpdir, monkeypatch):
    """Trigger a cleanup error by removing the Mercurial repo early."""
    with GitLabMirrorFixture.init(tmpdir, monkeypatch) as fixture:
        shutil.rmtree(fixture.hg_repo_wrapper.repo.root)


def test_fixture_git_teardown_error(tmpdir, monkeypatch):
    """Trigger a cleanup error by removing the Git repo early."""
    with GitLabMirrorFixture.init(tmpdir, monkeypatch) as fixture:
        shutil.rmtree(str(fixture.git_repo.path))
