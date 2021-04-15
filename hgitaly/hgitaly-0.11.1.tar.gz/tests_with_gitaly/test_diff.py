# Copyright 2021 Sushil Khanchi <sushilkhanchi97@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import pytest
import grpc
import re
from hgitaly.git import EMPTY_TREE_OID
from hgitaly.stub.diff_pb2 import (
    RawDiffRequest,
)
from hgitaly.stub.diff_pb2_grpc import DiffServiceStub

from . import skip_comparison_tests
if skip_comparison_tests():  # pragma no cover
    pytestmark = pytest.mark.skip

INDEX_LINE_REGEXP = re.compile(br'^index \w+\.\.\w+( \d+)?$')


def test_compare_raw_diff(gitaly_comparison):
    fixture = gitaly_comparison
    hgitaly_repo = fixture.hgitaly_repo
    gitaly_repo = fixture.gitaly_repo
    git_repo = fixture.git_repo
    wrapper = fixture.hg_repo_wrapper

    gl_branch = b'branch/default'
    ctx0 = wrapper.commit_file('bar', content="I am in\nrab\n",
                               message="Some bar")
    git_sha0 = git_repo.branches()[gl_branch]['sha']
    ctx1 = wrapper.commit_file('bar', content="I am in\nbar\n",
                               message="Changes bar")
    git_sha1 = git_repo.branches()[gl_branch]['sha']
    ctx2 = wrapper.commit_file('zoo', content="I am in\nzoo\n",
                               message="Added zoo")
    git_sha2 = git_repo.branches()[gl_branch]['sha']
    wrapper.command(b'mv', wrapper.repo.root + b'/bar',
                    wrapper.repo.root + b'/zar')
    wrapper.command(b'ci', message=b"Rename bar to zar")
    ctx3 = wrapper.repo[b'.']
    git_sha3 = git_repo.branches()[gl_branch]['sha']
    # Repo structure:
    #
    # @  3 Rename bar to zar
    # |
    # o  2 Added zoo
    # |
    # o  1 Changes bar
    # |
    # o  0 Some bar
    #

    def do_rpc_hgitaly(left_cid, right_cid):
        hgitaly_request = RawDiffRequest(
                            repository=hgitaly_repo,
                            left_commit_id=left_cid,
                            right_commit_id=right_cid,
                        )
        hgitaly_diff_stub = DiffServiceStub(fixture.hgitaly_channel)
        response = hgitaly_diff_stub.RawDiff(hgitaly_request)
        return b''.join(resp.data for resp in response)

    def do_rpc_gitaly(left_cid, right_cid):
        gitaly_request = RawDiffRequest(
                            repository=gitaly_repo,
                            left_commit_id=left_cid,
                            right_commit_id=right_cid,
                        )
        gitaly_diff_stub = DiffServiceStub(fixture.gitaly_channel)
        response = gitaly_diff_stub.RawDiff(gitaly_request)
        return b''.join(resp.data for resp in response)

    # case 1: when indexline doesn't contain <mode>
    hg_resp_lines = do_rpc_hgitaly(left_cid=ctx1.hex(),
                                   right_cid=ctx2.hex()).split(b'\n')
    git_resp_lines = do_rpc_gitaly(left_cid=git_sha1,
                                   right_cid=git_sha2).split(b'\n')
    INDEX_LINE_POSITION = 2
    hg_indexline = hg_resp_lines[INDEX_LINE_POSITION]
    git_indexline = git_resp_lines[INDEX_LINE_POSITION]
    # check that index line has the correct format
    assert INDEX_LINE_REGEXP.match(hg_indexline) is not None
    assert INDEX_LINE_REGEXP.match(git_indexline) is not None
    # actual comparison
    del hg_resp_lines[INDEX_LINE_POSITION]
    del git_resp_lines[INDEX_LINE_POSITION]
    assert hg_resp_lines == git_resp_lines

    # case 2: when indexline has <mode> (it happens when mode didn't change)
    hg_resp_lines = do_rpc_hgitaly(left_cid=ctx0.hex(),
                                   right_cid=ctx1.hex()).split(b'\n')
    git_resp_lines = do_rpc_gitaly(left_cid=git_sha0,
                                   right_cid=git_sha1).split(b'\n')
    INDEX_LINE_POSITION = 1
    hg_indexline = hg_resp_lines[INDEX_LINE_POSITION]
    git_indexline = git_resp_lines[INDEX_LINE_POSITION]
    # check the mode
    assert INDEX_LINE_REGEXP.match(hg_indexline).group(1) == b' 100644'
    assert INDEX_LINE_REGEXP.match(git_indexline).group(1) == b' 100644'

    # case 3: test with file renaming
    hg_resp = do_rpc_hgitaly(left_cid=ctx2.hex(),
                             right_cid=ctx3.hex())
    git_resp = do_rpc_gitaly(left_cid=git_sha2,
                             right_cid=git_sha3)
    assert hg_resp is not None
    assert hg_resp == git_resp

    # case 4: when commit_id does not correspond to a commit
    sha_not_exists = b'deadnode' * 5
    with pytest.raises(grpc.RpcError) as exc_info:
        do_rpc_hgitaly(sha_not_exists, ctx2.hex())
    assert exc_info.value.code() == grpc.StatusCode.UNKNOWN
    with pytest.raises(grpc.RpcError) as exc_info:
        do_rpc_gitaly(sha_not_exists, git_sha2)
    assert exc_info.value.code() == grpc.StatusCode.UNKNOWN

    # case 5: EMPTY_TREE_OID to represent null commit on the left
    hg_resp_lines = do_rpc_hgitaly(left_cid=EMPTY_TREE_OID,
                                   right_cid=ctx0.hex()).split(b'\n')
    git_resp_lines = do_rpc_gitaly(left_cid=EMPTY_TREE_OID,
                                   right_cid=git_sha0).split(b'\n')
    INDEX_LINE_POSITION = 2
    assert (hg_resp_lines[INDEX_LINE_POSITION].split(b'..')[0]
            ==
            git_resp_lines[INDEX_LINE_POSITION].split(b'..')[0])
    del hg_resp_lines[INDEX_LINE_POSITION]
    del git_resp_lines[INDEX_LINE_POSITION]
    assert hg_resp_lines == git_resp_lines

    # case 6: EMPTY_TREE_OID to represent null commit on the right
    git_resp_lines = do_rpc_gitaly(right_cid=EMPTY_TREE_OID,
                                   left_cid=git_sha0).split(b'\n')
    hg_resp_lines = do_rpc_hgitaly(right_cid=EMPTY_TREE_OID,
                                   left_cid=ctx0.hex()).split(b'\n')
    INDEX_LINE_POSITION = 2
    assert (hg_resp_lines[INDEX_LINE_POSITION].rsplit(b'..')[-1]
            ==
            git_resp_lines[INDEX_LINE_POSITION].rsplit(b'..')[-1])
    del hg_resp_lines[INDEX_LINE_POSITION]
    del git_resp_lines[INDEX_LINE_POSITION]
    assert hg_resp_lines == git_resp_lines


def test_compare_raw_patch(gitaly_comparison):
    fixture = gitaly_comparison
    gitaly_repo = fixture.gitaly_repo
    git_repo = fixture.git_repo
    wrapper = fixture.hg_repo_wrapper

    gl_branch = b'branch/default'
    ctx0 = wrapper.commit_file('bar', content="I am in\nrab\n",
                               message="Some bar")
    git_sha0 = git_repo.branches()[gl_branch]['sha']

    def do_rpc(vcs, left_cid, right_cid):
        request = RawDiffRequest(
            repository=gitaly_repo,
            left_commit_id=left_cid,
            right_commit_id=right_cid,
        )
        diff_stubs = dict(
            git=DiffServiceStub(fixture.gitaly_channel),
            hg=DiffServiceStub(fixture.hgitaly_channel)
        )
        response = diff_stubs[vcs].RawDiff(request)
        return b''.join(resp.data for resp in response)

    # Here we are only comparing for error cases, as HGitaly returns Hg patches
    # and Gitaly returns Git pataches. For more, look at diff.RawPatch()
    sha_not_exists = b'deadnode' * 5
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', sha_not_exists, ctx0.hex())
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', sha_not_exists, git_sha0)
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert exc_info_hg.value.details() == exc_info_git.value.details()
