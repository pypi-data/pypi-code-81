# Copyright 2021 Sushil Khanchi <sushilkhanchi97@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import grpc
import pytest
from hgitaly.git import (
    EMPTY_TREE_OID,
)
from hgitaly.tests.common import (
    make_empty_repo,
)
from hgitaly.stub.diff_pb2 import (
    RawDiffRequest,
    RawPatchRequest,
)
from mercurial import (
    node,
)
from hgitaly.stub.diff_pb2_grpc import DiffServiceStub
from .. import diff


def test_concat_resplit():
    in_data = iter([b'AAB', b'BCCDD'])
    max_size = 2
    data = diff.concat_resplit(in_data, max_size)
    data = list(data)
    assert data == [b'AA', b'BB', b'CC', b'DD']


def test_raw_diff(grpc_channel, server_repos_root):
    grpc_stub = DiffServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    ctx0 = wrapper.commit_file('foo', content="I am oof\n",
                               message=b'added foo')
    ctx1 = wrapper.commit_file('foo', content="I am foo\n",
                               message=b'changes foo')
    wrapper.command(b'mv', wrapper.repo.root + b'/foo',
                    wrapper.repo.root + b'/zoo')
    wrapper.command(b'ci', message=b"rename foo to zoo")
    ctx2 = wrapper.repo[b'.']
    sha0, sha1, sha2 = ctx0.hex(), ctx1.hex(), ctx2.hex()

    def do_rpc(left_sha, right_sha):
        request = RawDiffRequest(
                    repository=grpc_repo,
                    left_commit_id=left_sha,
                    right_commit_id=right_sha,
                  )
        response = grpc_stub.RawDiff(request)
        return b''.join(resp.data for resp in response)

    # case 1: actual test
    resp = do_rpc(sha0, sha1)
    respheader = (
        b'diff --git a/foo b/foo\n'
    )
    resphunk = (
        b'--- a/foo\n'
        b'+++ b/foo\n'
        b'@@ -1,1 +1,1 @@\n'
        b'-I am oof\n'
        b'+I am foo\n'
    )
    assert resp.startswith(respheader) and resp.endswith(resphunk)

    # case 2: with null node
    resp = do_rpc(node.nullhex, sha0)
    respheader = (
        b'diff --git a/foo b/foo\n'
    )
    resphunk = (
        b'--- /dev/null\n'
        b'+++ b/foo\n'
        b'@@ -0,0 +1,1 @@\n'
        b'+I am oof\n'
    )
    assert resp.startswith(respheader) and resp.endswith(resphunk)

    # case 2bis: with null left node, expressed as empty tree
    # this is really used by the Rails app.
    resp = do_rpc(EMPTY_TREE_OID, sha0)
    assert resp.startswith(respheader) and resp.endswith(resphunk)

    # case 2ter: with null right node, expressed as empty tree
    # this is for completeness
    resp = do_rpc(sha0, EMPTY_TREE_OID)
    resphunk = (
        b'--- a/foo\n'
        b'+++ /dev/null\n'
        b'@@ -1,1 +0,0 @@\n'
        b'-I am oof\n'
    )
    assert resp.startswith(respheader) and resp.endswith(resphunk)

    # case 3: with file renaming
    resp = do_rpc(sha1, sha2)
    assert resp == (
        b'diff --git a/foo b/zoo\n'
        b'similarity index 100%\n'
        b'rename from foo\n'
        b'rename to zoo\n'
    )

    # case 4: when commit_id does not correspond to a commit
    sha_not_exists = b'deadnode' * 5
    # varient 1
    with pytest.raises(grpc.RpcError) as exc_info:
        do_rpc(sha0, sha_not_exists)
    assert exc_info.value.code() == grpc.StatusCode.UNKNOWN
    assert 'exit status 128' in exc_info.value.details()
    # varient 2
    with pytest.raises(grpc.RpcError) as exc_info:
        do_rpc(sha_not_exists, sha0)
    assert exc_info.value.code() == grpc.StatusCode.UNKNOWN
    assert 'exit status 128' in exc_info.value.details()


def test_raw_patch(grpc_channel, server_repos_root):
    grpc_stub = DiffServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    # prepare repo as:
    #
    #   @    3 merge with stable
    #   |\
    #   | o  2 added bar (branch: stable)
    #   | |
    #   o |  1 changes foo (topic: feature)
    #   |/
    #   o  0 added foo
    #
    #
    dayoffset = 86400  # seconds in 24 hours
    ctx0 = wrapper.commit_file('foo', content="I am oof\n",
                               message=b'added foo', user=b'testuser',
                               utc_timestamp=dayoffset)
    ctx1 = wrapper.commit_file('foo', content="I am foo\n", topic=b'feature',
                               message=b'changes foo', user=b'testuser',
                               utc_timestamp=dayoffset*2)
    ctx2 = wrapper.commit_file('bar', content="I am bar\n",
                               message=b'added bar', user=b'testuser',
                               utc_timestamp=dayoffset*3, parent=ctx0,
                               branch=b'stable')
    wrapper.update(ctx1.rev())
    ctx3 = wrapper.merge_commit(ctx2, user=b'testuser',
                                utc_timestamp=dayoffset*4,
                                message=b'merge with stable')
    sha0, sha2, sha3 = ctx0.hex(), ctx2.hex(), ctx3.hex()

    def do_rpc(left_sha, right_sha):
        request = RawPatchRequest(
                    repository=grpc_repo,
                    left_commit_id=left_sha,
                    right_commit_id=right_sha,
                  )
        response = grpc_stub.RawPatch(request)
        return b''.join(resp.data for resp in response)

    # with null revision
    null_node = b"00000" * 5
    assert do_rpc(null_node, sha0) == (
        b'# HG changeset patch\n'
        b'# User testuser\n'
        b'# Date 86400 0\n'
        b'#      Fri Jan 02 00:00:00 1970 +0000\n'
        b'# Node ID f1a2b5b072f5e59abd43ed6982ab428a6149eda8\n'
        b'# Parent  0000000000000000000000000000000000000000\n'
        b'added foo\n'
        b'\n'
        b'diff --git a/foo b/foo\n'
        b'new file mode 100644\n'
        b'--- /dev/null\n'
        b'+++ b/foo\n'
        b'@@ -0,0 +1,1 @@\n'
        b'+I am oof\n'
    )
    # with merge commit
    assert do_rpc(sha2, sha3) == (
        b'# HG changeset patch\n'
        b'# User testuser\n'
        b'# Date 172800 0\n'
        b'#      Sat Jan 03 00:00:00 1970 +0000\n'
        b'# Node ID 0ae85a0d494d9197fd2bf8347d7fff997576f25a\n'
        b'# Parent  f1a2b5b072f5e59abd43ed6982ab428a6149eda8\n'
        b'# EXP-Topic feature\n'
        b'changes foo\n'
        b'\n'
        b'diff --git a/foo b/foo\n'
        b'--- a/foo\n'
        b'+++ b/foo\n'
        b'@@ -1,1 +1,1 @@\n'
        b'-I am oof\n'
        b'+I am foo\n'
        b'# HG changeset patch\n'
        b'# User testuser\n'
        b'# Date 345600 0\n'
        b'#      Mon Jan 05 00:00:00 1970 +0000\n'
        b'# Node ID 2215a964a3245ee4e7c3906f076b14977152a1df\n'
        b'# Parent  0ae85a0d494d9197fd2bf8347d7fff997576f25a\n'
        b'# Parent  c4fa3ef1fc8ba157ed8c26584c13492583bf17e9\n'
        b'# EXP-Topic feature\n'
        b'merge with stable\n'
        b'\n'
        b'diff --git a/bar b/bar\n'
        b'new file mode 100644\n'
        b'--- /dev/null\n'
        b'+++ b/bar\n'
        b'@@ -0,0 +1,1 @@\n'
        b'+I am bar\n'
    )
    # with different branch
    assert do_rpc(sha0, sha2) == (
        b'# HG changeset patch\n'
        b'# User testuser\n'
        b'# Date 259200 0\n'
        b'#      Sun Jan 04 00:00:00 1970 +0000\n'
        b'# Branch stable\n'
        b'# Node ID c4fa3ef1fc8ba157ed8c26584c13492583bf17e9\n'
        b'# Parent  f1a2b5b072f5e59abd43ed6982ab428a6149eda8\n'
        b'added bar\n'
        b'\n'
        b'diff --git a/bar b/bar\n'
        b'new file mode 100644\n'
        b'--- /dev/null\n'
        b'+++ b/bar\n'
        b'@@ -0,0 +1,1 @@\n'
        b'+I am bar\n'
    )
    # when commit_id does not correspond to a commit
    sha_not_exists = b'deadnode' * 5
    # varient 1
    with pytest.raises(grpc.RpcError) as exc_info:
        do_rpc(sha0, sha_not_exists)
    assert exc_info.value.code() == grpc.StatusCode.UNKNOWN
    assert 'exit status 128' in exc_info.value.details()
    # varient 2
    with pytest.raises(grpc.RpcError) as exc_info:
        do_rpc(sha_not_exists, sha0)
    assert exc_info.value.code() == grpc.StatusCode.UNKNOWN
    assert 'exit status 128' in exc_info.value.details()
