# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
User side API for reading and modifying Lawwenda configurations, creating shares, and more.

For most cases, instantiate :py:class:`Configuration` and use some if its methods.
"""

import base64
import datetime
import hashlib
import json
import os
import time
import typing as t

import lawwenda.datafiles
import lawwenda.devserver


# pylint: disable=too-many-locals,too-many-instance-attributes
class Share:
    """
    A directory path together with some parameters (e.g. for access control) for sharing via Lawwenda. Read the
    documentation for more about shares.
    """

    def __init__(self, path: str, *, configuration: "Configuration", name: str, title: str, cachetag: object,
                 readonly: bool = True,
                 hide_by_patterns: t.Iterable[str] = (), hide_by_tags: t.Iterable[str] = (),
                 include_by_patterns: t.Optional[t.Iterable[str]] = None,
                 include_by_tags: t.Optional[t.Iterable[str]] = None,
                 exclude_by_patterns: t.Iterable[str] = (), exclude_by_tags: t.Iterable[str] = (),
                 exclude_hidden: bool = False,
                 password_scrypt: t.Optional[str] = None, password_salt: t.Optional[str] = None,
                 active_until_timestamp: t.Optional[float] = None):
        """
        |dontconstruct|
        """
        self.__path = os.path.abspath(path)
        self.__configuration = configuration
        self.__name = name
        self.__title = title
        self.__cache_tag = cachetag
        self.__readonly = readonly
        self.__hide_by_patterns = hide_by_patterns
        self.__hide_by_tags = hide_by_tags
        self.__include_by_patterns = include_by_patterns
        self.__include_by_tags = include_by_tags
        self.__exclude_by_patterns = exclude_by_patterns
        self.__exclude_by_tags = exclude_by_tags
        self.__exclude_hidden = exclude_hidden
        self.__password_scrypt = password_scrypt or None
        self.__password_salt = password_salt
        self.__active_until_timestamp = active_until_timestamp

    @property
    def path(self) -> str:
        """
        The path of the share's root directory.
        """
        return self.__path

    @property
    def name(self) -> str:
        """
        The share name.

        This usually makes the last part of the url to this share. Is unique in the containing :py:attr:`configuration`.
        """
        return self.__name

    @property
    def configuration(self) -> "Configuration":
        """
        The configuration that contains this share.
        """
        return self.__configuration

    @property
    def title(self) -> str:
        """
        The share title.

        This is an arbitrary text shown in the window title. Should not contain line breaks and should be short.
        """
        return self.__title

    @property
    def readonly(self) -> bool:
        """
        If this share is restricted to only read actions (no removal, copying, uploading, editing, ... of the files and
        directories in :py:attr:`path`).
        """
        return self.__readonly

    @property
    def hide_by_patterns(self) -> t.Iterable[str]:
        """
        A list of regular expressions of paths for hiding.

        A file or directory will be hidden if its path matches at least one of them. Those paths are always relative to
        :py:attr:`path`, always start with a `'/'`, but never end with a one (unless it is the root path).

        Note that hiding is not a security feature unless :py:attr:`exclude_hidden` is set.
        """
        return self.__hide_by_patterns

    @property
    def hide_by_tags(self) -> t.Iterable[str]:
        """
        A list of tags for hiding files and directories.

        A file or directory will be hidden if it is tagged with at least one of them.

        Note that hiding is not a security feature unless :py:attr:`exclude_hidden` is set.
        """
        return self.__hide_by_tags

    @property
    def include_by_patterns(self) -> t.Optional[t.Iterable[str]]:
        """
        A list of regular expressions of paths for including explicitly.

        Those paths are always relative to :py:attr:`path`, always start with a `'/'`, but never end with a one (unless
        it is the root path).

        If this is specified, the share will switch from blacklist to whitelist. Everything that is not considered as
        included is implicitly considered as excluded.
        """
        return self.__include_by_patterns

    @property
    def include_by_tags(self) -> t.Optional[t.Iterable[str]]:
        """
        A list of tags for including files and directories.

        If this is specified, the share will switch from blacklist to whitelist. Everything that is not considered as
        included is implicitly considered as excluded.
        """
        return self.__include_by_tags

    @property
    def exclude_by_patterns(self) -> t.Iterable[str]:
        """
        A list of regular expressions of paths for excluding.

        A file or directory will be excluded if its path matches at least one of them. Those paths are always relative
        to :py:attr:`path`, always start with a `'/'`, but never end with a one (unless it is the root path).

        Exclusions are enforced on backend side and not just a presentation aspect. There is no way for a client to work
        around that (unless there is a software bug).
        """
        return self.__exclude_by_patterns

    @property
    def exclude_by_tags(self) -> t.Iterable[str]:
        """
        A list of tags for excluding files and directories.

        Exclusions are enforced on backend side and not just a presentation aspect. There is no way for a client to work
        around that (unless there is a software bug).
        """
        return self.__exclude_by_tags

    @property
    def exclude_hidden(self) -> bool:
        """
        If to consider 'hidden' flags of files or directories as exclusions.

        Exclusions are enforced on backend side and not just a presentation aspect. There is no way for a client to work
        around that (unless there is a software bug).
        """
        return self.__exclude_hidden

    @property
    def password_scrypt(self) -> t.Optional[str]:
        """
        The scrypt hash of the password for this share.

        Empty or `None` for disabled password protection. See also :py:attr:`password_salt`.
        """
        return self.__password_scrypt

    @property
    def password_salt(self) -> t.Optional[str]:
        """
        The hash salt of the password for this share, if password protected.

        See also :py:attr:`password_scrypt`.
        """
        return self.__password_salt

    @property
    def active_until(self) -> t.Optional[datetime.datetime]:
        """
        The expiration time of this share, or `None` for infinite.
        """
        return datetime.datetime.fromtimestamp(self.active_until_timestamp) if self.active_until_timestamp else None

    @property
    def active_until_timestamp(self) -> t.Optional[float]:
        """
        Same as :py:attr:`active_until`, but as Unix timestamp.
        """
        return self.__active_until_timestamp

    @property
    def is_active(self) -> bool:
        """
        If this share is currently active (e.g. not yet expired; see :py:attr:`active_until`).
        """
        return (not self.is_expired) and self.__cache_tag and (
                self.configuration.peek_share_cache_tag(self.name) == self.__cache_tag)

    @property
    def is_expired(self) -> bool:
        """
        If this share is expired.
        """
        return (self.active_until_timestamp is not None) and (self.active_until_timestamp < time.time())

    def __str__(self):
        return (f"Share {self.name}\n"
                f"- path: {self.path}\n"
                f"- title: {self.title}\n"
                f"- readonly: {self.readonly}\n"
                f"- active until timestamp: {self.active_until_timestamp}\n"
                f"- hide by patterns: {self.hide_by_patterns}\n"
                f"- hide by tags: {self.hide_by_tags}\n"
                f"- include by patterns: {self.include_by_patterns}\n"
                f"- include by tags: {self.include_by_tags}\n"
                f"- exclude by patterns: {self.exclude_by_patterns}\n"
                f"- exclude by tags: {self.exclude_by_tags}\n"
                f"- exclude hidden: {self.exclude_hidden}\n"
                f"- password protected: {bool(self.password_scrypt)}\n")

    def _to_dict(self):
        return {k: getattr(self, k) for k in ["path", "name", "title", "readonly",
                                              "hide_by_patterns", "hide_by_tags", "include_by_patterns",
                                              "include_by_tags", "exclude_by_patterns", "exclude_by_tags",
                                              "exclude_hidden", "password_scrypt", "password_salt",
                                              "active_until_timestamp"]}


class Configuration:
    """
    TODO.
    """

    def __init__(self, cfgpath: t.Optional[str] = None):
        """
        :param cfgpath: The path of the configuration directory. Will be created on demand if it does not exist.
                        Defaults to a location that is usual for your operating system.
        """
        self.__cfgpath = cfgpath or "/etc/lawwenda"
        self.__cfgsharespath = f"{self.__cfgpath}/shares"

    @property
    def path(self) -> str:
        """
        The path of the configuration directory.
        """
        return self.__cfgpath

    def __str__(self):
        return f"Configuration in {self.path!r}"

    def peek_share_cache_tag(self, name: str) -> t.Optional[object]:
        """
        TODO.

        :param name: The share name.
        """
        try:
            return os.stat(f"{self.__cfgsharespath}/{name}").st_mtime
        except OSError:
            return None

    def get_shares(self) -> t.List[Share]:
        """
        Return all shares that are currently part of this configuration.
        """
        if not os.path.isdir(self.__cfgsharespath):
            return []
        result = None
        tnow = time.time()
        itries = 0
        while result is None:
            itries += 1
            try:
                result_ = []
                for name in os.listdir(self.__cfgsharespath):
                    cachetag = self.peek_share_cache_tag(name)
                    if not cachetag:
                        raise OSError("No cachetag.")
                    with open(f"{self.__cfgsharespath}/{name}", "r") as f:
                        sharedict = json.load(f)
                    if cachetag != self.peek_share_cache_tag(name):
                        raise OSError("cachetag changed.")
                    share = Share(**sharedict, configuration=self, cachetag=cachetag)
                    if share.is_expired:
                        self.remove_share(share.name)
                    elif share.is_active:
                        result_.append(share)
                    else:
                        raise OSError("Inactive share.")
                result = result_
            except IOError:
                if (time.time() - tnow > 10) and (itries > 100):
                    raise
        return result

    def get_share_by_name(self, name: str) -> t.Optional[Share]:
        """
        Return the share by a name (or `None` if it does not exist).
        """
        for share in self.get_shares():
            if share.name == name:
                return share
        return None

    def add_share(self, path: str, *, name: str, password: t.Optional[str],
                  title: t.Optional[str] = None, readonly: bool = True,
                  hide_by_patterns: t.Iterable[str] = (), hide_by_tags: t.Iterable[str] = (),
                  include_by_patterns: t.Optional[t.Iterable[str]] = None,
                  include_by_tags: t.Optional[t.Iterable[str]] = None,
                  exclude_by_patterns: t.Iterable[str] = (), exclude_by_tags: t.Iterable[str] = (),
                  exclude_hidden: bool = False,
                  active_until: t.Optional[datetime.datetime] = None) -> Share:
        """
        Add a new share.

        :param path: The directory to share. See :py:attr:`Share.path`.
        :param name: The unique name of the new share. See :py:attr:`Share.name`.
        :param password: The password to protect the share with.
        :param title: The share title. See :py:attr:`Share.title`.
        :param readonly: If to share in a read-only way. See :py:attr:`Share.readonly`.
        :param hide_by_patterns: See :py:attr:`Share.hide_by_patterns`.
        :param hide_by_tags: See :py:attr:`Share.hide_by_tags`.
        :param include_by_patterns: See :py:attr:`Share.include_by_patterns`.
        :param include_by_tags: See :py:attr:`Share.include_by_tags`.
        :param exclude_by_patterns: See :py:attr:`Share.exclude_by_patterns`.
        :param exclude_by_tags: See :py:attr:`Share.exclude_by_tags`.
        :param exclude_hidden: See :py:attr:`Share.exclude_hidden`.
        :param active_until: The optional expiration time of the share. See :py:attr:`Share.active_until`.
        """
        self.__verify_valid_name(name)
        if password:
            pwsalt = os.urandom(16)
            pwscrypt = hashlib.scrypt(password.encode(), salt=pwsalt, n=2**14, r=8, p=1)
            password_scrypt = base64.b64encode(pwscrypt).decode()
            password_salt = base64.b64encode(pwsalt).decode()
        else:
            password_scrypt = password_salt = None
        os.makedirs(self.__cfgsharespath, exist_ok=True)
        # pylint: disable=protected-access
        jshare = json.dumps(Share(path, configuration=self, name=name, title=title or name, readonly=readonly,
                                  hide_by_patterns=hide_by_patterns, hide_by_tags=hide_by_tags,
                                  include_by_patterns=include_by_patterns, include_by_tags=include_by_tags,
                                  exclude_by_patterns=exclude_by_patterns, exclude_by_tags=exclude_by_tags,
                                  exclude_hidden=exclude_hidden,
                                  password_scrypt=password_scrypt, password_salt=password_salt,
                                  active_until_timestamp=active_until.timestamp() if active_until else None,
                                  cachetag=None)._to_dict())
        if self.get_share_by_name(name):
            raise ValueError(f"The name '{name}' is already in use.")
        with open(f"{self.__cfgsharespath}/{name}", "w") as f:
            f.write(jshare)
        return self.get_share_by_name(name)

    def remove_share(self, name: str) -> None:
        """
        Remove a share.

        :param name: The name of the share to remove.
        """
        self.__verify_valid_name(name)
        fpath = f"{self.__cfgsharespath}/{name}"
        try:
            os.unlink(fpath)
        except IOError:
            if os.path.exists(fpath):
                raise

    def run_dev_server(self) -> "lawwenda.devserver._DevServerInfo":
        """
        Start a tiny local server for this configuration.

        Such a server can be used for trying, development, testing, and so on, but is not recommended for real usage.

        It will automatically find a free port and will return a control object that contains the full url, and more.
        """
        svr = lawwenda.devserver.run_dev_server(self)  # TODO noh better text in readme (not blocking)
        print(f"Please browse to the the following base address, appended by a share name:\n"
              f" {svr.url}")
        return svr

    def generate_wsgi(self) -> str:
        """
        Generates a wsgi script for hosting Lawwenda in a web server.

        Read the 'Installation' section of the documentation for more details about what to do with it.
        """
        fwsgi = lawwenda.datafiles.find_data_file("lawwenda.wsgi")
        if not fwsgi:
            raise EnvironmentError("Your installation is not able to generate wsgi.")
        with open(fwsgi, "r") as f:
            return f.read().format(lawwendadir=repr(lawwenda.datafiles.LAWWENDADIR), cfgpath=repr(self.path))

    @staticmethod
    def __verify_valid_name(name: str) -> None:
        if (not name) or name != os.path.basename(name):
            raise ValueError(f"Invalid share name '{name}'")
