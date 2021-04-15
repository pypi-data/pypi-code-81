# Copyright 2021 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""High level utilities for Mercurial manifest handling.

The purpose is both to provide exactly what the HGitaly services need
and to abstract away from the actual manifest implementation: we might
at some point switch to some version of Tree Manifest if one appears that
fills our basic needs (namely to be a peer implementation detail, having no
effect on changeset IDs).

The module is meant to harbour several classes, according to the
underlying Mercurial core implementations. The dispatching is done by
the :func:`miner` fatory function.

It is legitimate to optimize each class according to the (stable) properties
of the core manifest object it works on.
"""
import attr


@attr.s
class ManifestMiner:
    """High level data extraction for basic Mercurial manifest.
    """
    changeset = attr.ib()

    def ls_dir(self, path):
        """List directory contents of path at given changeset.

        Anything from inside subdirectories of ``path`` is ignored.

        :param changeset: a :class:`changectx` instance
        :param bytes path: path in the repository of the directory to list.
           Can be empty for the root directory, but not ``b'/'``.
        :returns: a pair ``(subdirs, filepaths)`` of lists, where
          ``subdirs`` contains the sub directories and ``filepaths`` the direct
          file entries within ``path``.
          Both lists are lexicographically sorted.
          All elements are given by their full paths from the root.
        """
        subtrees = set()
        file_paths = []
        prefix = path.rstrip(b'/') + b'/' if path else path
        prefix_len = len(prefix)
        for file_path in self.changeset.manifest().iterkeys():
            if not file_path.startswith(prefix):
                continue
            split = file_path[prefix_len:].split(b'/', 1)
            if len(split) > 1:
                subtrees.add(prefix + split[0])
            else:
                file_paths.append(file_path)
        file_paths.sort()
        return sorted(subtrees), file_paths


def miner(changeset):
    """Return an appropriate manifest extractor for the given changeset.

    This factory function abstracts over possible future manifest
    types, for which we might write different implementations
    """
    return ManifestMiner(changeset)
