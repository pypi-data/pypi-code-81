# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from contextlib import contextmanager
from io import BytesIO
import grpc
import shutil
import tarfile

import pytest

from hgext3rd.heptapod.branch import read_gitlab_typed_refs
from hgext3rd.heptapod.keep_around import (
    create_keep_around,
    iter_keep_arounds,
)

from hgitaly.tests.common import make_empty_repo

from hgitaly.stub.repository_service_pb2 import (
    GetArchiveRequest,
    HasLocalBranchesRequest,
    RepositoryExistsRequest,
    WriteRefRequest,
)
from hgitaly.stub.repository_service_pb2_grpc import RepositoryServiceStub


def test_repository_exists(grpc_channel, server_repos_root):
    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    def exists(repo):
        return repo_stub.RepositoryExists(
            RepositoryExistsRequest(repository=repo)).exists

    assert exists(grpc_repo)

    # directory exists but is not a Mercurial repo
    shutil.rmtree(wrapper.path / '.hg')
    assert not exists(grpc_repo)

    # directory does not exist
    grpc_repo.relative_path = 'does/not/exist'
    assert not exists(grpc_repo)


def test_has_local_branches(grpc_channel, server_repos_root):
    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    def has_local_branches():
        return repo_stub.HasLocalBranches(
            HasLocalBranchesRequest(repository=grpc_repo)).value

    assert not has_local_branches()
    wrapper.write_commit('foo')
    assert has_local_branches()

    wrapper.command('commit', message=b"closing the only head!",
                    close_branch=True)

    assert not has_local_branches()


def test_write_ref(grpc_channel, server_repos_root):
    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)
    repo = wrapper.repo

    for ref, revision in ((b'refs/heads/something', b'dead01234cafe'),
                          (b'HEAD', b'topic/default/wont-last'),
                          (b'refs/keep-around/not-a-sha', b'not-a-sha'),
                          (b'refs/keep-around/feca01eade', b'cafe01dead'),
                          ):
        with pytest.raises(grpc.RpcError) as exc_info:
            repo_stub.WriteRef(WriteRefRequest(
                repository=grpc_repo,
                ref=ref,
                revision=revision
            ))
        assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    changeset = wrapper.commit_file('foo')

    to_write = {b'refs/merge-requests/12/head': changeset.hex(),
                b'refs/pipelines/98192': b'refs/heads/branch/default',
                b'refs/environments/13/deployments/9826': b'branch/default',
                }
    for ref_path, target in to_write.items():
        repo_stub.WriteRef(WriteRefRequest(
            repository=grpc_repo,
            ref=ref_path,
            revision=target))

    # read without any caching
    assert read_gitlab_typed_refs(wrapper.repo, 'special-refs') == {
        ref_path[5:]: changeset.hex() for ref_path in to_write.keys()
    }

    # Keep-arounds. let's have a pre-existing one for good measure
    existing_ka = b'c8c3ae298f5549a0eb0c28225dcc4f6937b959a8'
    create_keep_around(repo, existing_ka)

    repo_stub.WriteRef(WriteRefRequest(
        repository=grpc_repo,
        ref=b'refs/keep-around/' + changeset.hex(),
        revision=changeset.hex()))

    assert set(iter_keep_arounds(repo)) == {changeset.hex(), existing_ka}


def test_write_special_refs_exceptions(
        grpc_channel, server_repos_root, monkeypatch):
    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)
    wrapper.commit_file('foo')

    (wrapper.path / '.hg' / 'store' / 'gitlab.special-refs').write_text(
        'invalid')

    repo_stub.WriteRef(WriteRefRequest(
        repository=grpc_repo,
        ref=b'refs/merge-requests/12/head',
        revision=b'76ac23fe' * 5))


@contextmanager
def get_archive_tarfile(stub, grpc_repo, commit_id, path=b''):
    with BytesIO() as fobj:
        for chunk_index, chunk_response in enumerate(
                stub.GetArchive(GetArchiveRequest(
                    repository=grpc_repo,
                    format=GetArchiveRequest.Format.Value('TAR'),
                    commit_id=commit_id,
                    path=path,
                    prefix='archive-dir',
                ))):
            fobj.write(chunk_response.data)

        fobj.seek(0)
        with tarfile.open(fileobj=fobj) as tarf:
            yield tarf, chunk_index + 1


def test_get_archive(grpc_channel, server_repos_root, tmpdir):
    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    ctx = wrapper.write_commit('foo', content="Foo")
    (wrapper.path / 'sub').mkdir()
    ctx2 = wrapper.write_commit('sub/bar', content="Bar")

    node_str = ctx.hex().decode()
    with get_archive_tarfile(repo_stub, grpc_repo, node_str) as (tarf, _nb):
        assert set(tarf.getnames()) == {'archive-dir/.hg_archival.txt',
                                        'archive-dir/foo'}

        extract_dir = tmpdir.join('extract')
        tarf.extractall(path=extract_dir)

        metadata_lines = extract_dir.join('archive-dir',
                                          '.hg_archival.txt').readlines()

        assert 'node: %s\n' % node_str in metadata_lines
        assert extract_dir.join('archive-dir', 'foo').read() == "Foo"

    node2_str = ctx2.hex().decode()
    with get_archive_tarfile(repo_stub, grpc_repo, node2_str) as (tarf, _nb):
        assert set(tarf.getnames()) == {'archive-dir/.hg_archival.txt',
                                        'archive-dir/foo',
                                        'archive-dir/sub/bar'}

        extract_dir = tmpdir.join('extract-2')
        tarf.extractall(path=extract_dir)

        metadata_lines = extract_dir.join('archive-dir',
                                          '.hg_archival.txt').readlines()

        assert 'node: %s\n' % node2_str in metadata_lines
        assert extract_dir.join('archive-dir', 'sub', 'bar').read() == "Bar"

    with get_archive_tarfile(
            repo_stub, grpc_repo, node2_str, path=b'sub') as (tarf, _nb):
        assert tarf.getnames() == ['archive-dir/sub/bar']

        extract_dir = tmpdir.join('extract-sub')
        tarf.extractall(path=extract_dir)
        assert extract_dir.join('archive-dir', 'sub', 'bar').read() == "Bar"

    with pytest.raises(grpc.RpcError) as exc_info:
        get_archive_tarfile(
            repo_stub, grpc_repo, node2_str,
            path=b'/etc/passwd'
        ).__enter__()  # needed to actually perform the RPC call
    assert exc_info.value.code() == grpc.StatusCode.INVALID_ARGUMENT


def test_get_archive_multiple_chunks(grpc_channel, server_repos_root,
                                     tmpdir, monkeypatch):

    repo_stub = RepositoryServiceStub(grpc_channel)
    wrapper, grpc_repo = make_empty_repo(server_repos_root)

    # we can't just override the environment variable: it's read at module
    # import time.
    large_content = "Foo" * 200000
    ctx = wrapper.write_commit('foo', content=large_content)
    node_str = ctx.hex().decode()
    with get_archive_tarfile(repo_stub, grpc_repo, node_str) as (tarf, count):
        assert count > 1
        assert set(tarf.getnames()) == {'archive-dir/.hg_archival.txt',
                                        'archive-dir/foo'}

        extract_dir = tmpdir.join('extract')
        tarf.extractall(path=extract_dir)

        metadata_lines = extract_dir.join('archive-dir',
                                          '.hg_archival.txt').readlines()

        assert 'node: %s\n' % node_str in metadata_lines
        assert extract_dir.join('archive-dir', 'foo').read() == large_content

    del large_content
