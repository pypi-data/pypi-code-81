import hashlib
import os
import shutil
from typing import Dict, Callable, List, Union, Any, Pattern

from moonspec.api._utils import _get_pwd_user_by_name, _get_pwd_group_by_name


class Mount:
    """
    Holds information about a file system mount
    """

    def __init__(
            self,
            dev: str,  #: mount device
            mount: str,  #: mount type
            fstype: str,  #: file system type
            options: Dict[str, Any]  # file system mount options
    ):
        self.dev: str = dev
        self.mount: str = mount
        self.fstype: str = fstype
        self.options: Dict[str, Any] = options

    def __str__(self) -> str:
        return 'Mount<%s, %s, %s, %s>' % (self.dev, self.mount, self.fstype, self.options)

    def __repr__(self) -> str:
        return self.__str__()


class MountCollection:
    def __init__(self, mounts: List[Mount]):
        self.mounts: List[Mount] = mounts

    def has_mount(self, mount_path: str) -> bool:
        for m in self.mounts:
            if m.mount == mount_path:
                return True
        return False

    def has_dev(self, dev: str) -> bool:
        for m in self.mounts:
            if m.dev == dev:
                return True
        return False


class PathApi:
    @staticmethod
    def is_owned_by_uid(path: str, uid: int) -> bool:
        if not PathApi.exists(path):
            raise FileNotFoundError('File not found - <%s>' % path)

        result = FileSystemApi.stat(path)

        return result.st_uid == uid

    @staticmethod
    def is_owned_by_user(path: str, user: str) -> bool:
        pwd_entry = _get_pwd_user_by_name(user)
        if pwd_entry is None:
            return False

        return PathApi.is_owned_by_uid(path, pwd_entry.pw_uid)

    @staticmethod
    def is_owned_by_gid(path: str, gid: int) -> bool:
        if not PathApi.exists(path):
            raise FileNotFoundError('File not found - <%s>' % path)

        result = FileSystemApi.stat(path)

        return result.st_gid == gid

    @staticmethod
    def is_owned_by_group(path: str, group: str) -> bool:
        pwd_entry = _get_pwd_group_by_name(group)

        if pwd_entry is None:
            return False

        return PathApi.is_owned_by_uid(path, pwd_entry.gr_gid)

    @staticmethod
    def exists_owned_by_u(path: str, user: str) -> bool:
        return PathApi.exists(path) and PathApi.is_owned_by_user(path, user)

    @staticmethod
    def exists_owned_by_g(path: str, group: str) -> bool:
        return PathApi.exists(path) and PathApi.is_owned_by_group(path, group)

    @staticmethod
    def exists_owned_by_ug(path: str, user: str, group: str) -> bool:
        return PathApi.exists(path) and PathApi.is_owned_by_user(path, user) and PathApi.is_owned_by_group(path, group)

    @staticmethod
    def can_read(path: str) -> bool:
        return os.access(path, os.R_OK, effective_ids=os.access in os.supports_effective_ids)

    @staticmethod
    def can_write(path: str) -> bool:
        return os.access(path, os.W_OK, effective_ids=os.access in os.supports_effective_ids)

    @staticmethod
    def can_exec(path: str) -> bool:
        return os.access(path, os.X_OK, effective_ids=os.access in os.supports_effective_ids)

    @staticmethod
    def exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def is_file(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def is_link(path: str) -> bool:
        return os.path.islink(path)

    @staticmethod
    def is_mount(path: str) -> bool:
        return os.path.ismount(path)

    @staticmethod
    def is_dir(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def is_empty(path: str) -> bool:
        if not PathApi.exists(path):
            raise FileNotFoundError('File does not exist - <%s>' % path)

        path = os.path.realpath(path)

        if PathApi.is_dir(path):
            return not os.listdir(path)

        return os.path.getsize(path) == 0

    @staticmethod
    def get_size_b(path: str) -> int:
        path = os.path.realpath(path)

        if not PathApi.exists(path) or not PathApi.is_file(path) or not PathApi.can_read(path):
            raise RuntimeError('File <%s> does not exist or is not readable' % path)

        return os.path.getsize(path)

    @staticmethod
    def has_extension(path: str, ext: str) -> bool:
        return path.endswith(ext)

    @staticmethod
    def is_smaller_than(path: str, size_b: int) -> bool:
        path = os.path.realpath(path)

        if not PathApi.exists(path) or not PathApi.is_file(path) or not PathApi.can_read(path):
            raise RuntimeError('File <%s> does not exist or is not readable' % path)

        return os.path.getsize(path) < size_b

    @staticmethod
    def is_larger_than(path: str, size_b: int) -> bool:
        path = os.path.realpath(path)

        if not PathApi.exists(path) or not PathApi.is_file(path) or not PathApi.can_read(path):
            raise RuntimeError('File <%s> does not exist or is not readable' % path)

        return os.path.getsize(path) > size_b

    @staticmethod
    def is_of_size(path: str, size_b: int) -> bool:
        path = os.path.realpath(path)

        if not PathApi.exists(path) or not PathApi.is_file(path) or not PathApi.can_read(path):
            raise RuntimeError('File <%s> does not exist or is not readable' % path)

        return os.path.getsize(path) == size_b


class FileSystemApi:
    """
    :ivar path: PathApi: instance of PathApi
    """

    def __init__(self) -> None:
        self.path = PathApi()

    @staticmethod
    def stat(path: str) -> os.stat_result:
        return os.stat(path)

    @staticmethod
    def hash_file(path: str, *hash_names: str) -> Union[str, Dict[str, str]]:
        if 0 == len(hash_names):
            raise RuntimeError('Requested file hash of <%s> with no hash names' % path)

        path = os.path.realpath(path)

        if not PathApi.exists(path) or not PathApi.is_file(path) or not PathApi.can_read(path):
            raise RuntimeError('File <%s> does not exist or is not readable' % path)

        instances = {}
        for hash_name in hash_names:
            if hash_name not in hashlib.algorithms_available:
                raise RuntimeError('Can not hash <%s>, algorithm not available - <%s>' % (path, hash_name))
            instances[hash_name] = hashlib.new(hash_name)

        with open(path, 'rb') as f:
            while True:
                data = f.read(65536)  # 64k chunks
                if not data:
                    break

                for hash_instance in instances.values():
                    hash_instance.update(data)

        if len(hash_names) == 1:
            return instances[hash_names[0]].hexdigest()

        results = {}

        for key, instance in instances.items():
            results[key] = instance.hexdigest()

        return results

    @staticmethod
    def all_files_in(path: str, matcher: Union[Callable[[str], bool], Pattern]) -> List[str]:
        if not callable(matcher) and not isinstance(matcher, Pattern):
            raise RuntimeError('Matcher is expected to be Callable or Pattern')

        if not PathApi.exists(path):
            raise FileNotFoundError('Path does not exist - <%s>' % path)

        path = os.path.realpath(path)

        files: List[str] = []
        for root, dirs, files in os.walk(path):
            for name in files:
                full_path = os.path.realpath(os.path.join(root, name))

                if isinstance(matcher, Pattern):
                    if matcher.fullmatch(full_path) is not None:
                        files.append(full_path)
                elif matcher(full_path):
                    files.append(full_path)

        return files

    # noinspection DuplicatedCode
    @staticmethod
    def line_in_file(path: str, matcher: Union[Callable[[str], bool], Pattern]) -> Union[bool, str]:
        if not callable(matcher) and not isinstance(matcher, Pattern):
            raise RuntimeError('Matcher is expected to be Callable or Pattern')

        if not PathApi.exists(path):
            raise FileNotFoundError('Path does not exist - <%s>' % path)

        if not PathApi.is_file(path) or not PathApi.can_read(path):
            raise RuntimeError('Path is not a file or can not be read - <%s>' % path)

        path = os.path.realpath(path)

        with open(path, 'r') as f:
            for f_line in f:
                line = f_line.rstrip()

                if isinstance(matcher, Pattern):
                    if matcher.fullmatch(line) is not None:
                        return line
                elif matcher(line):
                    return line

        return False

    # noinspection DuplicatedCode
    @staticmethod
    def lines_in_file(path: str, matcher: Union[Callable[[str], bool], Pattern]) -> List[str]:
        if not callable(matcher) and not isinstance(matcher, Pattern):
            raise RuntimeError('Matcher is expected to be Callable or Pattern')

        if not PathApi.exists(path):
            raise FileNotFoundError('Path does not exist - <%s>' % path)

        if not PathApi.is_file(path) or not PathApi.can_read(path):
            raise RuntimeError('Path is not a file or can not be read - <%s>' % path)

        path = os.path.realpath(path)
        matching_lines = []

        with open(path, 'r') as f:
            for f_line in f:
                line = f_line.rstrip()

                if isinstance(matcher, Pattern):
                    if matcher.fullmatch(line) is not None:
                        matching_lines.append(line)

                elif matcher(line):
                    matching_lines.append(line)

        return matching_lines

    @staticmethod
    def space_free(path: str) -> int:
        if not PathApi.exists(path):
            raise FileNotFoundError('Path does not exist - <%s>' % path)

        return shutil.disk_usage(path).free

    @staticmethod
    def space_used(path: str) -> int:
        if not PathApi.exists(path):
            raise FileNotFoundError('Path does not exist - <%s>' % path)

        return shutil.disk_usage(path).used

    @staticmethod
    def space_total(path: str) -> int:
        if not PathApi.exists(path):
            raise FileNotFoundError('Path does not exist - <%s>' % path)

        return shutil.disk_usage(path).total

    @staticmethod
    def space_gt_threshold(path: str, threshold_percent: Union[float, int]) -> bool:
        if threshold_percent <= 0.0 or threshold_percent > 100.0:
            raise RuntimeError('threshold_percent must be a number larger than 0 and less. or equal to 100')

        if not PathApi.exists(path):
            raise FileNotFoundError('Path does not exist - <%s>' % path)

        usage = shutil.disk_usage(path)

        return (usage.used / usage.total) > threshold_percent / 100

    @staticmethod
    def mounts() -> MountCollection:
        if not PathApi.is_file('/etc/mtab') or not PathApi.can_read('/etc/mtab'):
            raise RuntimeError('/etc/mtab does not exist or is not readable')

        with open('/etc/mtab', 'r') as f:
            mounts = f.readlines()

        result = []
        for mount in mounts:
            parts = mount.strip().split(' ', 5)

            options: Dict[str, Any] = {}
            if '' != parts[3]:
                o_kv_pairs = [x.split('=', 1) for x in parts[3].split(',')]
                for o_pair in o_kv_pairs:
                    if 1 == len(o_pair):
                        options[o_pair[0]] = True
                    else:
                        options[o_pair[0]] = o_pair[1]

            result.append(Mount(
                parts[0],
                parts[1],
                parts[2],
                options
            ))

        return MountCollection(result)
