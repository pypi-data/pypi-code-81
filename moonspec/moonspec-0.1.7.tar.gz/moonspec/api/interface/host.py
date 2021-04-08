import multiprocessing
import os
import socket
from grp import struct_group
from pwd import struct_passwd
from typing import List, Optional, Tuple

from moonspec.api._utils import _get_pwd_group_by_name, _get_pwd_user_by_name, _get_pwd_users, _get_pwd_groups
from moonspec.api.interface.libvirtd import LibvirtApi
from moonspec.api.interface.osqueryd import OSQueryApi
from moonspec.api.interface.systemd import SystemdApi


class HostUser:
    def __init__(self) -> None:
        self.name: Optional[str] = None
        self.uid: Optional[int] = None
        self.gid: Optional[int] = None
        self.home: Optional[str] = None
        self.shell: Optional[str] = None

    @staticmethod
    def _from_pwd_entry(it: struct_passwd) -> 'HostUser':
        user = HostUser()
        user.name = it[0]
        user.uid = it[2]
        user.gid = it[3]
        user.home = it[5]
        user.shell = it[6]
        return user

    def __str__(self) -> str:
        return 'HostUser<%s, %s, %s, %s, %s>' % (
            self.name,
            self.uid,
            self.gid,
            self.home,
            self.shell
        )

    def __repr__(self) -> str:
        return self.__str__()


class HostGroup:
    def __init__(self) -> None:
        self.name: Optional[str] = None
        self.gid: Optional[int] = None
        self.members: List = []

    @staticmethod
    def _from_pwd_entry(it: struct_group) -> 'HostGroup':
        group = HostGroup()
        group.name = it[0]
        group.gid = it[2]
        group.members = it[3]
        return group

    def __str__(self) -> str:
        return 'HostGroup<%s, %s, %s>' % (
            self.name,
            self.gid,
            self.members
        )

    def __repr__(self) -> str:
        return self.__str__()


class HostApi:
    def __init__(self) -> None:
        self.systemd: SystemdApi = SystemdApi()
        self.osquery: OSQueryApi = OSQueryApi()
        self.libvirt: LibvirtApi = LibvirtApi()

    @staticmethod
    def username() -> str:
        return os.getlogin()

    @staticmethod
    def fqdn() -> str:
        return socket.getfqdn()

    @staticmethod
    def name() -> str:
        return socket.gethostname()

    @staticmethod
    def user_exists(user: str) -> bool:
        u = _get_pwd_user_by_name(user)
        return u is not None and u.pw_name is not None

    @staticmethod
    def group_exists(group: str) -> bool:
        g = _get_pwd_group_by_name(group)
        return g is not None and g.gr_name is not None

    @staticmethod
    def users() -> List[HostUser]:
        # noinspection PyProtectedMember
        return [HostUser._from_pwd_entry(it) for it in _get_pwd_users()]

    @staticmethod
    def groups() -> List[HostGroup]:
        # noinspection PyProtectedMember
        return [HostGroup._from_pwd_entry(it) for it in _get_pwd_groups()]

    @staticmethod
    def cpu_count() -> int:
        return multiprocessing.cpu_count()

    @staticmethod
    def load_avg() -> Tuple[float, float, float]:
        return os.getloadavg()

    @staticmethod
    def load_avg_percent() -> Tuple[float, float, float]:
        cpu_count = HostApi.cpu_count()
        l1, l5, l15 = HostApi.load_avg()
        return (l1 / cpu_count) * 100, (l5 / cpu_count) * 100, (l15 / cpu_count) * 100

    @staticmethod
    def load_1_above(percent_threshold: float) -> bool:
        l1p, _, _ = HostApi.load_avg_percent()
        return l1p > percent_threshold

    @staticmethod
    def load_5_above(percent_threshold: float) -> bool:
        _, l5p, _ = HostApi.load_avg_percent()
        return l5p > percent_threshold

    @staticmethod
    def load_15_above(percent_threshold: float) -> bool:
        _, _, l15p = HostApi.load_avg_percent()
        return l15p > percent_threshold
