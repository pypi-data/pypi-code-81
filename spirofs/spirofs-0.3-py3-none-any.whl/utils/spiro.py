from __future__ import absolute_import, print_function, unicode_literals

import logging
import os
import hashlib
import contextlib
import tempfile
import shutil
import posixpath
try:
    from urllib import unquote, quote
except ImportError:
    from urllib.parse import unquote, quote

import salt.utils.files
import salt.utils.hashutils
import salt.utils.path
import salt.utils.yamldumper
import salt.utils.yamlloader
from salt.ext import six

log = logging.getLogger(__name__)


def _fsdir(*bits):
    """
    Takes quoted arguments
    """
    # 2018.3: salt.utils.path.join()
    return os.path.join(__opts__['cachedir'], 'spirofs', *bits)


class Deployment(object):
    """
    A single environment.
    """

    def __init__(self, project, deployment):
        self.project = project
        self.deployment = deployment

    @property
    def root(self):
        """
        The root directory of this deployment.
        """
        return _fsdir(
            quote(self.project),
            quote(self.deployment),
        )

    @property
    def saltenv(self):
        """
        The saltenv for this deployment.
        """
        return "%s/%s" % (self.project, self.deployment)

    @property
    def synth_tops(self):
        """
        The name of the synthesized topfile (suitable for salt)
        """
        return __opts__['state_top']

    @property
    def real_tops(self):
        """
        The name of the spiro topfile
        """
        return 'spirotop.sls'

    @classmethod
    def from_env(cls, saltenv):
        """
        Factory: From a saltenv
        """
        if '/' not in saltenv:
            return

        parts = saltenv.rsplit('/', 1)
        self = cls(parts[0], parts[1])
        if self.exists():
            return self

    @classmethod
    def iterdeployments(cls):
        """
        Yield all Deployments
        """
        if not os.path.isdir(_fsdir()):
            return
        for p in os.listdir(_fsdir()):
            for d in os.listdir(_fsdir(p)):
                yield cls(unquote(p), unquote(d))

    def serialize(self):
        """
        Produce a JSON-suitable representation of this object
        """
        return [self.project, self.deployment]

    @classmethod
    def deserialize(cls, data):
        """
        Reverse of .serialize()
        """
        if data:
            return cls(*data)

    def exists(self, fn=None):
        """
        Check that this deployment actually exists in the filesystem.
        """
        if fn is None:
            return os.path.isdir(self.root)
        else:
            return os.path.exists(self.path(fn))

    def ensure_exists(self):
        """
        Create this deployment if it does not exist.
        """
        if not self.exists():
            os.makedirs(self.root)

    def contents(self):
        """
        Yield (name, 'f'|'d') for each filesystem entry
        """
        if not self.exists():
            return

        for path, dirs, files in salt.utils.path.os_walk(self.root):
            relpath = path[len(self.root):].strip('/')
            # FIXME: Return empty dirs
            yield relpath, 'd'
            for f in files:
                # 2018.3: salt.utils.path.join()
                yield posixpath.join(relpath, f), 'f'

    def path(self, fname):
        """
        Returns the real filesystem path for the given item.

        Doesn't actually check the filesystem.
        """
        # Kinda ignoring the fact that salt paths are always / and
        # Windows would like \ because Windows will accept /
        # 2018.3: salt.utils.path.join()
        return os.path.join(self.root, fname)

    def open(self, fname, mode='r'):
        """
        Returns a file.like object for the given itme.
        """
        return salt.utils.files.fopen(self.path(fname), mode)

    def hash_file(self, fname, hashtype):
        """
        Returns a hash for the given item.
        """
        return salt.utils.hashutils.get_hash(
            self.path(fname),
            hashtype,
        )

    def _mkbufferdir(self):
        """
        Make a temporary directory suitable for eventually making the real one
        """
        self.ensure_exists()
        return tempfile.mkdtemp(
            prefix=quote(self.deployment),
            dir=_fsdir(quote(self.project)),
        )

    def _extract(self, tarfile, dir):
        """
        Extract the given TarFile in the directory.
        """
        tarfile.extractall(dir)

    def _generate_topfile(self, dir):
        """
        Examine a staging directory and produce a topfile if a spirotop file
        exists.
        """
        # 2018.3: salt.utils.path.join()
        spirotop_fn = os.path.join(dir, self.real_tops)
        # 2018.3: salt.utils.path.join()
        top_fn = os.path.join(dir, self.synth_tops)
        if os.path.exists(top_fn):
            return
        if not os.path.exists(spirotop_fn):
            return

        with open(spirotop_fn, 'rt') as f:
            # Safe_load in 2018.3
            yaml = salt.utils.yamlloader.load(f, Loader=salt.utils.yamlloader.SaltYamlSafeLoader)

        if not yaml:
            return

        envs = {
            self.saltenv: yaml.get(self.deployment, {}),
        }

        with open(top_fn, 'wt') as f:
            salt.utils.yamldumper.safe_dump(envs, f)

    def _replace_directory(self, stagingdir):
        """
        Replace the environment with the contents of the given directory with as
        little visible intermediate state as possible.
        """
        trashdir = tempfile.mktemp(prefix=self.deployment, dir=_fsdir(quote(self.project)))
        os.rename(self.root, trashdir)
        os.rename(stagingdir, self.root)
        shutil.rmtree(trashdir)

    def deploy_new(self, tarfile):
        """
        Deploy the given TarFile as a new version of this deployment.
        """
        # 1. Set up a staging area in a place most likely to be on the same 
        #    filesystem as the serving directory
        log.debug("Make deployment buffer dir")
        stagingdir = self._mkbufferdir()

        # 2. Examine spirotop and do pre-extraction activities
        # We don't actually have anything here
        log.debug("Deployment pre-extract activities")

        # 3. Extract the tarball
        log.debug("Deployment extraction")
        self._extract(tarfile, stagingdir)

        # 4. Do post-extraction generation/compilation
        log.debug("Deployment post-extract activities")
        self._generate_topfile(stagingdir)

        # 5. Shuffle directories making the staging area the production directory
        # 6. Clean up the old version
        log.debug("Deployment directory shuffle")
        self._replace_directory(stagingdir)


def list_deployments():
    """
    Returns a list of all known Deployments (as Deployment objects).
    """
    return Deployment.iterdeployments()


def from_env(saltenv):
    """
    Gets the Deployment for the given saltenv
    """
    return Deployment.from_env(saltenv)


def from_pd(project, deployment):
    """
    Gets the Deployment for the given project/deployment pair
    """
    return Deployment(project, deployment)


def deserialize(data):
    """
    Turns the results of Deployment.serialize() back into an object.
    """
    return Deployment.deserialize(data)
