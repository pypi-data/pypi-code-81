import tarfile
import io
import os
import subprocess
from functools import partial


def is_vcs(fname):
    """
    Checks if this path looks like it's a VCS metadata directory
    """
    # TODO: Add more VCSs
    return os.path.basename(fname) in {'.git'}


def is_salt(fname):
    """
    Checks if this path looks like _salt
    """
    return os.path.basename(fname) in {'_salt'}


def parents(fname):
    yield fname
    while True:
        prev = fname
        fname, _ = os.path.split(fname)
        if prev == fname:
            break
        yield fname


def mktarinfo(data, **args):
    """
    Convenience function to synthesize a TarInfo
    """
    ti = tarfile.TarInfo()
    ti.size = len(data)
    ti.type = tarfile.REGTYPE
    for name, value in args.items():
        setattr(ti, name, value)
    return ti, io.BytesIO(data)


def git_describe():
    proc = subprocess.run(['git', 'describe', '--all'], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
    return proc.stdout.strip()


def git_commit():
    proc = subprocess.run(['git', 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
    return proc.stdout.strip()


class TarballBuilder:
    """
    Builds up a deployment bundle.
    >>> with TarballBuilder() as builder:
    ...     ...

    >>> builder.buffer
    """
    def __enter__(self):
        """
        Initialize the buffer and tar metadata
        """
        self.buffer = io.BytesIO()
        self._tf = tarfile.TarFile(fileobj=self.buffer, mode='w')
        self._tf.__enter__()
        return self

    def __exit__(self, *args):
        """
        Close out the tar data and resets the buffer for external user
        """
        rv = self._tf.__exit__(*args)
        self.buffer.seek(0)
        return rv
    
    def add_saltdir(self, dirname):
        """
        Add a salt data directory (_salt)
        """
        for fname in os.listdir(dirname):
            self._tf.add(
                os.path.join(dirname, fname), fname, 
                filter=(lambda ti: None if is_vcs(ti.name) else ti)
            )

    def add_artifact(self, path, name):
        """
        Add a build artifact (into _artifacts)
        """
        self._tf.add(path, os.path.join('_artifacts', name))

    def add_virtual(self, path, data):
        """
        Add a synthesized file
        """
        self._tf.addfile(
            *mktarinfo(data, name=path)
        )

    def add_gitcommit(self, path=None):
        """
        Tag with the git commit data
        """
        info = git_commit() + b'\n' + git_describe()
        if len(info) > 1:  # Contains more than the newline
            self.add_virtual('.gitcommit', info)

    def add_source(self, scanner):
        for fname, fopen in scanner(lambda fn: is_vcs(fn) or is_salt(fn)):
            self.add_virtual('_source/{}'.format(fname), fopen().read())


def git_scanner(should_skip):
    proc = subprocess.run(['git', 'archive', '--format=tar', 'HEAD'], stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
    buf = io.BytesIO(proc.stdout)
    with tarfile.open(fileobj=buf, mode='r') as tf:
        for mem in tf.getmembers():
            if any(should_skip(f) for f in parents(mem.name)):
                continue
            if mem.isfile() or mem.issym():
                yield mem.name, lambda: tf.extractfile(mem)


def fs_scanner(should_skip):
    # This blatently assumes the cwd is the project root
    for dirpath, dirs, files in os.walk('.'):
        dirs[:] = (d for d in dirs if not should_skip(d))

        for f in files:
            if should_skip(f):
                continue
            dpf = os.path.join(dirpath, f)
            yield dpf, partial(open, dpf, 'rb')
