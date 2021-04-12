# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This utility module contains several shell helpers.

The functions in the module are intentionally and especially
internally not functional-like as the shell functionalities do
inherently not satisfy the requirements of functional-like code.
The functions that do shell calls can also end the execution of
the script on failure.

Nevertheless, the basic principles are preserved, i.e. functions
don't modify their parameters.
"""

from __future__ import print_function

import logging
import os
import pipes
import shutil
import subprocess
import sys
import tarfile
import zipfile

from contextlib import contextmanager

from ..support.platform_names import get_darwin_system_name

from .cache import cached

from .target import current_platform


@cached
def get_dev_null():
    """
    Gives the pipe to which the ignored shell output is put to.
    """
    return getattr(subprocess, "DEVNULL", subprocess.PIPE)


def _quote(arg):
    return pipes.quote(str(arg))


def quote_command(args):
    """Quotes a command for printing it."""
    return " ".join([_quote(a) for a in args])


def _echo_command(dry_run, command, env=None, prompt="+ "):
    """
    Echoes a command to command line. Thus this function isn't
    pure.
    """
    output = []
    if env is not None:
        output.extend(["env"] + [
            _quote("%s=%s" % (k, v)) for (k, v) in sorted(env.items())
        ])
    output.extend([_quote(arg) for arg in command])
    file = sys.stderr
    if dry_run:
        file = sys.stdout
    print(prompt + " ".join(output), file=file)
    file.flush()


def call(command, stderr=None, env=None, dry_run=None, echo=None):
    """Runs the given command."""
    if dry_run or echo:
        _echo_command(dry_run, command, env=env)
    if dry_run:
        return
    _env = None
    if env is not None:
        _env = dict(os.environ)
        _env.update(env)
    try:
        subprocess.check_call(command, env=_env, stderr=stderr)
    except subprocess.CalledProcessError as e:
        logging.critical(
            "Command ended with status %d, stopping",
            e.returncode
        )
        sys.exit(e.returncode)
    except OSError as e:
        logging.critical(
            "Couldn't run '%s': %s",
            quote_command(command),
            e.strerror
        )
        sys.exit(1)


def capture(
    command,
    stderr=None,
    env=None,
    dry_run=None,
    echo=None,
    optional=False,
    allow_non_zero_exit=False
):
    """Runs the given command and returns its output."""
    if dry_run or echo:
        _echo_command(dry_run, command, env=env)
    if dry_run:
        return
    _env = None
    if env is not None:
        _env = dict(os.environ)
        _env.update(env)
    try:
        out = subprocess.check_output(command, env=_env, stderr=stderr)
        # Coerce to 'str' hack. Not py3 'byte', not py2
        # 'unicode'.
        return str(out.decode())
    except subprocess.CalledProcessError as e:
        if allow_non_zero_exit:
            return e.output
        if optional:
            return None
        logging.critical(
            "Command ended with status %d, stopping",
            e.returncode
        )
        sys.exit(e.returncode)
    except OSError as e:
        if optional:
            return None
        logging.critical(
            "Couldn't execute '%s': %s",
            quote_command(command),
            e.strerror
        )
        sys.exit(1)


@contextmanager
def pushd(path, dry_run=None, echo=None):
    """Pushes the directory to the top of the directory stack."""
    old_dir = os.getcwd()
    if dry_run or echo:
        _echo_command(dry_run, ["pushd", path])
    if not dry_run:
        os.chdir(path)
    yield
    if dry_run or echo:
        _echo_command(dry_run, ["popd"])
    if not dry_run:
        os.chdir(old_dir)


def makedirs(path, dry_run=None, echo=None):
    """
    Creates the given directory and the in-between directories.
    """
    if dry_run or echo:
        _echo_command(dry_run, ["mkdir", "-p", path])
    if dry_run:
        return
    if not os.path.isdir(path):
        os.makedirs(path)


def copytree(src, dest, dry_run=None, echo=None):
    """Copies a directory and its contents."""
    if dry_run or echo:
        _echo_command(dry_run, ["cp", "-r", src, dest])
    if dry_run:
        return
    # A workaround
    if os.path.isdir(dest):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)  # , symlinks, ignore)
            else:
                shutil.copy2(s, d)
    else:
        shutil.copytree(src, dest)


def copy(src, dest, dry_run=None, echo=None):
    """Copies a file."""
    if dry_run or echo:
        _echo_command(dry_run, ["cp", "-p", src, dest])
    if dry_run:
        return
    if os.path.islink(src):
        link = os.readlink(src)
        os.symlink(link, dest)
    else:
        shutil.copy2(src, dest)


def rmtree(path, dry_run=None, echo=None):
    """Removes a directory and its contents."""
    if dry_run or echo:
        _echo_command(dry_run, ["rm", "-rf", path])
    if dry_run:
        return
    if os.path.exists(path):
        # TODO Find out if ignore_errors is required
        shutil.rmtree(path, ignore_errors=True)


def rm(file, dry_run=None, echo=None):
    """Removes a file."""
    if dry_run or echo:
        _echo_command(dry_run, ["rm", "-f", file])
    if dry_run:
        return
    if os.path.islink(file):
        os.unlink(file)
    if os.path.exists(file):
        os.remove(file)


def link(src, dest, dry_run=None, echo=None):
    """Creates a symbolic link."""
    if dry_run or echo:
        _echo_command(dry_run, ["ln", "-s", src, dest])
    if dry_run:
        return
    os.symlink(src, dest)


def tar(path, dest=None, dry_run=None, echo=None):
    """Extracts an archive."""
    if dry_run or echo:
        if dest:
            _echo_command(dry_run, ["tar", "-xf", path, "-C", dest])
        else:
            _echo_command(dry_run, ["tar", "-xf", path])
    if dry_run:
        return
    if path.endswith(".zip"):
        with zipfile.ZipFile(path, "r") as archive:
            if dest:
                archive.extractall(dest)
            else:
                archive.extractall()
    else:
        if path.endswith(".tar") or path.endswith(".tar.gz"):
            with tarfile.open(path) as archive:
                if dest:
                    archive.extractall(dest)
                else:
                    archive.extractall()
        else:
            if sys.version_info.major == 2:
                # TODO Use different command for Windows.
                with pushd(os.path.dirname(path)):
                    if dest:
                        call(
                            ["tar", "-xf", os.path.split(path)[1], "-C", dest]
                        )
                    else:
                        call(["tar", "-xf", os.path.split(path)[1]])
            else:
                with tarfile.open(path) as archive:
                    if dest:
                        archive.extractall(dest)
                    else:
                        archive.extractall()


def create_tar(src, dest, dry_run=None, echo=None):
    """Creates a .tar.gz archive."""
    if dry_run or echo:
        _echo_command(dry_run, ["tar", "-czf", dest, src])
    if dry_run:
        return
    dest_file = dest
    if dest_file.endswith(".tar.gz"):
        dest_file = dest_file[:-7]
    shutil.make_archive(dest_file, format="gztar", root_dir=src)


def create_zip(src, dest, dry_run=None, echo=None):
    """Creates a .zip archive."""
    if dry_run or echo:
        _echo_command(dry_run, ["zip", "-r", dest, src])
    if dry_run:
        return
    dest_file = dest
    if dest_file.endswith(".zip"):
        dest_file = dest_file[:-4]
    shutil.make_archive(dest_file, format="zip", root_dir=src)


def curl(url, dest, env=None, dry_run=None, echo=None):
    """Downloads a file."""
    call(
        ["curl", "-o", dest, "--create-dirs", url],
        env=env,
        dry_run=dry_run,
        echo=echo
    )


def chmod(path, mode, dry_run=None, echo=None):
    """Changes the mode of a file."""
    if dry_run or echo:
        _echo_command(dry_run, ["chmod", mode, path])
    if dry_run:
        return
    file_stat = os.stat(path)
    os.chmod(path, file_stat.st_mode | mode)


def caffeinate(command, env=None, dry_run=None, echo=None):
    """Runs a command during which system sleep is disabled."""
    command_to_run = list(command)
    # Disable system sleep, if possible.
    if current_platform() == get_darwin_system_name():
        command_to_run = ["caffeinate"] + list(command)
    call(command_to_run, env=env, dry_run=dry_run, echo=echo)
