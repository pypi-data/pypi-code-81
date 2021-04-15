# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import pytest

from mercurial_testhelpers import (
    RepoWrapper,
)

from .. import manifest


@pytest.fixture
def repo_wrapper(tmpdir):
    yield RepoWrapper.init(tmpdir / 'repo')


def test_ls_dir(repo_wrapper):
    wrapper = repo_wrapper
    base_ctx = wrapper.commit_file('foo')

    sub = wrapper.path / 'sub'
    sub.mkdir()
    (sub / 'bar').write('bar content')
    (sub / 'ba2').write('ba2 content')
    deeper = sub / 'deeper'
    deeper.mkdir()
    (deeper / 'ping').write('pong')

    ctx1 = wrapper.commit(rel_paths=['sub/bar', 'sub/ba2', 'sub/deeper/ping'],
                          message="zebar", add_remove=True)

    assert manifest.miner(base_ctx).ls_dir(b'') == ([], [b'foo'])
    # perhaps we'll want an exception there
    assert manifest.miner(base_ctx).ls_dir(b'sub') == ([], [])

    miner1 = manifest.miner(ctx1)
    assert miner1.ls_dir(b'') == ([b'sub'], [b'foo'])
    assert miner1.ls_dir(b'sub') == ([b'sub/deeper'], [b'sub/ba2', b'sub/bar'])
    assert miner1.ls_dir(b'sub/deeper') == ([], [b'sub/deeper/ping'])
