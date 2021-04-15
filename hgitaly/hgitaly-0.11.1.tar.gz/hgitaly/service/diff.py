# Copyright 2021 Sushil Khanchi <sushilkhanchi97@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
import io

from ..errors import (
    not_implemented,
    unknown_error,
)
from ..oid import (
    blob_oid,
)
from ..git import (
    NULL_BLOB_OID,
    EMPTY_TREE_OID,
)
from mercurial import (
    node,
    patch,
    pycompat,
    diffutil,
    cmdutil,
)
from ..stub.diff_pb2 import (
    CommitDiffRequest,
    CommitDiffResponse,
    CommitDeltaRequest,
    CommitDeltaResponse,
    RawDiffRequest,
    RawDiffResponse,
    RawPatchRequest,
    RawPatchResponse,
    DiffStatsRequest,
    DiffStatsResponse,
)
from ..stub.diff_pb2_grpc import DiffServiceServicer

from ..servicer import HGitalyServicer
from ..revision import gitlab_revision_changeset
from ..stream import (
    concat_resplit,
    WRITE_BUFFER_SIZE,
)


logger = logging.getLogger(__name__)
# Copied from mercurial/patch.py
gitmode = {b'l': b'120000', b'x': b'100755', b'': b'100644'}
nullid = node.nullid
nullhex = node.nullhex
nullrev = node.nullrev
hex = node.hex


class DiffServicer(DiffServiceServicer, HGitalyServicer):
    """DiffService implementation.

    Note: There is a case where we can have differences in HGitaly's and
    Gitaly's DiffService responses. This happens with the renames when the
    similarity index is less than 50% in that case Git doesn't consider it
    a 'rename' but Hg does (as Hg has explicit tracking of copies and renames).
    """
    def CommitDiff(self, request: CommitDiffRequest,
                   context) -> CommitDiffResponse:
        return not_implemented(context, CommitDiffResponse,
                               issue=38)  # pragma no cover

    def CommitDelta(self, request: CommitDeltaRequest,
                    context) -> CommitDeltaResponse:
        return not_implemented(context, CommitDeltaResponse,
                               issue=39)  # pragma no cover

    def RawDiff(self, request: RawDiffRequest,
                context) -> RawDiffResponse:
        parsed_request = parse_diff_request(self, request, context)
        _parsed, repo, ctx_from, ctx_to = parsed_request
        if not _parsed:
            return unknown_error(context, RawDiffResponse, "exit status 128")
        opts = {b'git': True}
        overrides = {
            (b'experimental', b'extendedheader.similarity'): True,
        }
        with repo.ui.configoverride(overrides):
            diffopts = diffutil.diffallopts(repo.ui, opts)
            diffchunks = ctx_to.diff(ctx_from, opts=diffopts)

        # generator func to yield hunks
        def in_chunks():
            for chunk in patch.parsepatch(diffchunks):
                header = _insert_blob_index(chunk, ctx_from, ctx_to)
                yield header
                for hunk in chunk.hunks:
                    with io.BytesIO() as extracted:
                        hunk.write(extracted)
                        yield extracted.getvalue()
        for data in concat_resplit(in_chunks(), WRITE_BUFFER_SIZE):
            yield RawDiffResponse(data=data)

    def RawPatch(self, request: RawPatchRequest,
                 context) -> RawPatchResponse:
        """Yields raw patches between two csets.

        Note: Here, patches are in `hg` format instead of `git`. We decided
        this on the basis of "response is not being parsed at Rails side, and
        directly sent to UI" so that users can import the hg patches.
        """
        parsed_request = parse_diff_request(self, request, context)
        _parsed, repo, ctx_from, ctx_to = parsed_request
        if not _parsed:
            return unknown_error(context, RawPatchResponse, "exit status 128")
        opts = {b'git': True}
        diffopts = diffutil.diffallopts(repo.ui, opts)
        ui = repo.ui
        fm = ui.formatter(b'RawPatch', opts={})
        revs = repo.revs(b'only(%s, %s)', ctx_to, ctx_from)

        def in_chunks():
            for seqno, rev in enumerate(revs):
                ctx = repo[rev]
                itr_data = _exportsingle(repo, ctx, fm, seqno, diffopts)
                for data in itr_data:
                    yield data
        for data in concat_resplit(in_chunks(), WRITE_BUFFER_SIZE):
            yield RawPatchResponse(data=data)

    def DiffStats(self, request: DiffStatsRequest,
                  context) -> DiffStatsResponse:
        return not_implemented(context, DiffStatsResponse,
                               issue=42)  # pragma no cover


def parse_diff_request_cid(cid):
    """Perform the conversions from a request commit_id to a usable revision.
    """
    if cid == EMPTY_TREE_OID:
        return nullhex
    return pycompat.sysbytes(cid)


def parse_diff_request(servicer, request, context):
    repo = servicer.load_repo(request.repository, context)

    left_cid = parse_diff_request_cid(request.left_commit_id)
    right_cid = parse_diff_request_cid(request.right_commit_id)

    ctx_from = gitlab_revision_changeset(repo, left_cid)
    ctx_to = gitlab_revision_changeset(repo, right_cid)
    if ctx_from is None:
        logger.warning(
            "%s: left_commit_id %r "
            "could not be found", request.__class__.__name__, left_cid)
        return (False, repo, ctx_from, ctx_to)
    if ctx_to is None:
        logger.warning(
            "%s: right_commit_id %r "
            "could not be found", request.__class__.__name__, right_cid)
        return (False, repo, ctx_from, ctx_to)
    return (True, repo, ctx_from, ctx_to)


def old_new_blob_oids(header, old_ctx, new_ctx):
    """Return a tuple of (old, new) blob oids."""
    old_path, new_path = old_new_file_path(header)
    old_bid = new_bid = NULL_BLOB_OID
    if old_path in old_ctx:
        cid = pycompat.sysstr(old_ctx.hex())
        old_bid = blob_oid(None, cid, old_path)
    if new_path in new_ctx:
        cid = pycompat.sysstr(new_ctx.hex())
        new_bid = blob_oid(None, cid, new_path)
    return old_bid, new_bid


def old_new_file_mode(header, old_ctx, new_ctx):
    """Return a tuple of (old, new) file mode."""
    old_path, new_path = old_new_file_path(header)
    old_mode, new_mode = b'0', b'0'
    if old_path in old_ctx:
        old_fctx = old_ctx[old_path]
        old_mode = gitmode[old_fctx.flags()]
    if new_path in new_ctx:
        new_fctx = new_ctx[new_path]
        new_mode = gitmode[new_fctx.flags()]
    return old_mode, new_mode


def old_new_file_path(header):
    """Return a tuple of (old, new) file path."""
    fname = header.filename()
    from_path, to_path = fname, fname
    if len(header.files()) > 1:
        # file is renamed
        from_path, to_path = header.files()
    return from_path, to_path


def _insert_blob_index(chunk, ctx_from, ctx_to):
    fname = chunk.filename()
    old_bid, new_bid = old_new_blob_oids(chunk, ctx_from, ctx_to)
    indexline = 'index %s..%s' % (old_bid, new_bid)
    indexline = pycompat.sysbytes(indexline)

    # Note: <mode> is required only when it didn't change between
    # the two changesets, otherwise it has a separate line
    if fname in ctx_from and fname in ctx_to:
        oldmode, mode = old_new_file_mode(chunk, ctx_from, ctx_to)
        if mode == oldmode:
            indexline += b' ' + mode
    indexline += b'\n'
    headerlines = chunk.header

    for index, line in enumerate(headerlines[:]):
        if line.startswith(b'--- '):
            headerlines.insert(index, indexline)
            break
    return b''.join(headerlines)


def _exportsingle(repo, ctx, fm, seqno, diffopts):
    """Generator method which yields a bytes stream of exporting `ctx` data.

    This method overwrite upstream mercurial's cmdutil._exportsingle(), as
    the upstream version directly writes the data to stdout and concatenates
    the diff chunks instead of yielding them.
    """
    node = ctx.node()
    parents = [p.node() for p in ctx.parents() if p]
    branch = ctx.branch()

    if parents:
        p1 = parents[0]
    else:
        p1 = nullid

    textlines = []
    textlines.append(b'# HG changeset patch\n')
    textlines.append(b'# User %s\n' % ctx.user())
    textlines.append(b'# Date %d %d\n' % ctx.date())
    textlines.append(b'#      %s\n' % fm.formatdate(ctx.date()))
    if branch and branch != b'default':
        textlines.append(b'# Branch %s\n' % branch)
    textlines.append(b'# Node ID %s\n' % hex(node))
    textlines.append(b'# Parent  %s\n' % hex(p1))
    if len(parents) > 1:
        textlines.append(b'# Parent  %s\n' % hex(parents[1]))

    for headerid in cmdutil.extraexport:
        header = cmdutil.extraexportmap[headerid](seqno, ctx)
        if header is not None:
            textlines.append(b'# %s\n' % header)

    textlines.append(b'%s\n' % ctx.description().rstrip())
    textlines.append(b'\n')
    yield b''.join(textlines)

    chunkiter = patch.diff(repo, p1, node, opts=diffopts)
    for chunk in chunkiter:
        yield chunk
