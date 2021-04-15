import argparse
import json
import logging.config
import os
import subprocess
import tarfile
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Union

import docker

DTFORMAT = "%Y-%m-%dT%H%M%S.%f"
DEFAULT_ROOT_DIRECTOY = "/backups"
DEFAULT_CT_DIRECTORY = "/tmp"
DEFAULT_LABEL_PREFIX = os.environ.get("ARCHIVER_LABEL_PREFIX", "docker-volume-dump")
DEFAULT_SELECTOR = f'{{"label": "{DEFAULT_LABEL_PREFIX}.isactive"}}'

logger = logging.getLogger(__name__)


def backup(testing=False):
    parser = argparse.ArgumentParser(
        description="Backup all targeted containers",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    backup_group = parser.add_argument_group("Backup options")
    backup_group.add_argument(
        "--host-fs",
        dest="host_fs",
        help="In case you are running archiver in a docker container"
        "you probably bind the host system somewhere else than `/` "
        "(ie /hostfs/) this let you choose a parent directory that will be prepend "
        "to the path retreive from container introspection."
        "used with `rsync` driver",
        default="",
    )
    backup_group.add_argument(
        "-d",
        "--backup-directory",
        default=DEFAULT_ROOT_DIRECTOY,
        help="Where backups will be stored",
    )
    backup_group.add_argument(
        "-s",
        "--selector",
        default=DEFAULT_SELECTOR,
        type=json.loads,
        help="A json string to select container to backup. "
        "Likes docker ps --filter option",
    )
    backup_group.add_argument("-r", "--raise-on-failure", action="store_true")
    logging_group = parser.add_argument_group("Logging params")
    logging_group.add_argument(
        "-f",
        "--logging-file",
        type=argparse.FileType("r"),
        help="Logging configuration file, (logging-level and logging-format "
        "are ignored if provide)",
    )
    logging_group.add_argument("-l", "--logging-level", default="INFO")
    logging_group.add_argument(
        "--logging-format",
        default="%(asctime)s - %(levelname)s (%(module)s%(funcName)s): " "%(message)s",
    )
    arguments = parser.parse_args()
    logging.basicConfig(
        level=getattr(logging, arguments.logging_level.upper()),
        format=arguments.logging_format,
    )
    if arguments.logging_file:
        try:
            json_config = json.loads(arguments.logging_file.read())
            logging.config.dictConfig(json_config)
        except json.JSONDecodeError:
            logging.config.fileConfig(arguments.logging_file.name)

    archiver = Archiver(
        selector=arguments.selector,
        root_directory=arguments.backup_directory,
        raise_on_failure=arguments.raise_on_failure,
        host_fs=arguments.host_fs,
    )
    logger.info("Success archived data %r", archiver.backup_all())
    if testing:
        return archiver


class Archiver:
    """Archiver class aims to find containers, create backups
    and move that backups to the expected directory.

    by default select all containers
    """

    _docker = None
    _selector: Dict = None
    _root_directory: str = None
    _container_directory: str = None
    host_fs: str = None
    _raise = None

    def __init__(
        self,
        selector=None,
        root_directory=DEFAULT_ROOT_DIRECTOY,
        container_directory=DEFAULT_CT_DIRECTORY,
        docker_cli=None,
        raise_on_failure=True,
        host_fs=None,
    ):
        """Instantiate

        :param selector:
            a dict used to select containers, it's exactly the same
            as `list() filters params from docker python lib
            <https://docker-py.readthedocs.io/en/stable/
            containers.html#docker.models.containers.ContainerCollection.list
            >`_
        :param root_directory: the root directory where dumps are saved.
        :param container_directory: the root directory where dumps is done
            inside the postgres container.
        :param docker_cli: An instance of `docker.DockerClient <https://
            docker-py.readthedocs.io/en/stable/client.html>`_. Create a new
            one if none
        """

        if not selector:
            selector = dict(label=f"{DEFAULT_LABEL_PREFIX}.isactive")
        if not docker_cli:
            docker_cli = docker.DockerClient()
        self._docker = docker_cli
        self._selector = selector
        self._root_directory = root_directory
        self._container_directory = container_directory
        self._raise = raise_on_failure
        self.host_fs = host_fs

    def backup_all(self) -> List[str]:
        """Backup all targeted containers

        :return: list of created filename
        """

        dumps = []
        containers = self._docker.containers.list(filters=self._selector)
        logger.info(
            "Found %i containers using following selector: %r.",
            len(containers),
            self._selector,
        )
        for container in containers:
            driver = DriverFactory.get_driver(
                container,
                self._container_directory,
                self._root_directory,
                self._raise,
                self.host_fs,
            )
            try:
                driver.retreive_container_labels()
                paths = driver.backup()
            except docker.errors.DockerException as err:
                logger.error(
                    "Docker Exception: Backup fails, "
                    "please figure out what's "
                    "happens: project: %s - container: %r - error: %r",
                    driver.project,
                    container,
                    err,
                )
                if self._raise:
                    raise err
                continue
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as err:
                logger.error(
                    "The following archive fails, please figure out what's "
                    "happen: container name: %s\n"
                    "container labels: %r\n"
                    "selector: %r\n"
                    "error: %s\n"
                    "stdout: %s\n stderr: %s\n output: %s",
                    container.name,
                    container.labels,
                    self._selector,
                    err,
                    (err.stdout or b"").decode(),
                    (err.stderr or b"").decode(),
                    (err.output or b"").decode(),
                )
                if self._raise:
                    raise err
                continue
            except Exception as err:
                logger.error(
                    "The following dump fails, please figure out what's "
                    "happen: container name: %s\n"
                    "container labels: %r\n"
                    "selector: %r\n"
                    "error: %r\n",
                    container.name,
                    container.labels,
                    self._selector,
                    err,
                )
                if self._raise:
                    raise err
                continue
            if paths:
                logger.info(
                    "[%s-%s] Saving data from %s container into %r",
                    driver.project,
                    driver.environment,
                    container.name,
                    paths,
                )
                # Todo: monitor success dump
                # https://github.com/prometheus/client_python#exporting-to-a-pushgateway
                dumps.extend(paths)
        return dumps


class DriverFactory(ABC):

    container = None
    project: str = None
    environment: str = None
    prefix: str = None
    _container_directory: str = None
    _root_directory: str = None
    host_fs: str = None
    _raise: bool = True

    @staticmethod
    def get_driver(
        container,
        container_directory: str,
        root_directory: str,
        raise_on_failure: bool,
        host_fs: str,
    ) -> Union["PgsqlDriver", "RsyncDriver", "MysqlDriver"]:
        drivername = container.labels.get(f"{DEFAULT_LABEL_PREFIX}.driver")
        if drivername == "mysql":
            return MysqlDriver(
                container,
                container_directory=container_directory,
                root_directory=root_directory,
                raise_on_failure=raise_on_failure,
                host_fs=host_fs,
            )
        elif drivername == "rsync":
            return RsyncDriver(
                container,
                container_directory=container_directory,
                root_directory=root_directory,
                raise_on_failure=raise_on_failure,
                host_fs=host_fs,
            )
        return PgsqlDriver(
            container,
            container_directory=container_directory,
            root_directory=root_directory,
            raise_on_failure=raise_on_failure,
            host_fs=host_fs,
        )

    def __init__(
        self,
        container,
        container_directory: str = DEFAULT_CT_DIRECTORY,
        root_directory: str = DEFAULT_ROOT_DIRECTOY,
        host_fs: str = None,
        raise_on_failure: bool = True,
    ):
        self.container = container
        self._container_directory = container_directory
        self._root_directory = root_directory
        self._raise = raise_on_failure
        self.host_fs = host_fs
        if self.host_fs is None:
            self.host_fs = ""

    def untar(self, path):
        tar = tarfile.open(path)
        tar.extractall(path=os.path.dirname(path))
        tar.close()
        os.remove(path)

    def execute_cmd_in_container(self, command):
        res = self.container.exec_run("sh -c '{}'".format(command))
        if res.exit_code:
            raise RuntimeError(
                "The following error happens "
                "(while running: {}) on project {}: {}".format(
                    command, self.project, res.output
                )
            )
        return res

    def retreive_container_labels(self):
        """get intersting container labels for given driver.

        method should probably overloaded to get desired informations
        """
        self.project = self.container.labels.get(f"{DEFAULT_LABEL_PREFIX}.project")
        self.environment = self.container.labels.get(
            f"{DEFAULT_LABEL_PREFIX}.environment", ""
        )
        self.prefix = self.container.labels.get(f"{DEFAULT_LABEL_PREFIX}.prefix", "")
        if not self.project:
            self.project = self.container.name

    @abstractmethod
    def backup(self) -> List[str]:
        """Backup data return list of path of archives file/directory"""


class DatabaseDriverBase(DriverFactory):

    _env_vars_dict = {}
    """Expected database env to be define in sub class"""

    dbname: str = None
    username: str = None
    dbname: str = None
    password: str = None
    dbenvs: Dict = {}

    def retreive_container_labels(self) -> None:
        """get intersting container labels for given driver.

        method should probably overloaded to get desired informations
        """
        super().retreive_container_labels()

        self.dbenvs = {
            env.split("=")[0]: env.split("=")[1]
            for env in self.container.attrs.get("Config", {}).get("Env", [])
            if env.startswith(self._env_vars_dict["env_vars_prefix"])
        }
        self.dbname = self.container.labels.get(f"{DEFAULT_LABEL_PREFIX}.dbname")

        if not self.dbname:
            self.dbname = self.dbenvs.get(self._env_vars_dict["db_name"])

        if not self.dbname:
            raise ValueError(
                "Could not find DB name to dump database in "
                f"'{self.container.name}' docker container."
            )

    def backup(self) -> List[str]:
        """backup a database or files

        ``project``, ``environment`` and ``prefix`` are used to build the
        backup filename ``<project>/[<environment>/]<prefix><dbname><date>``
        """

        logger.info(
            "[%s-%s]dumping %s from %s ct",
            self.project,
            self.environment,
            self.dbname,
            self.container.name,
        )
        filename = "{}{}-{}.sql.gz".format(
            self.prefix, self.dbname, datetime.now().strftime(DTFORMAT)
        )
        container_path = os.path.join(
            self._container_directory, self.project, self.environment, filename
        )
        host_dump_path = os.path.join(
            self._root_directory, self.project, self.environment, filename
        )
        host_tar_path = host_dump_path + ".tar"
        self.execute_cmd_in_container(self.get_dump_command(container_path))
        Path(os.path.dirname(host_tar_path)).mkdir(parents=True, exist_ok=True)
        stream, stat = self.container.get_archive(container_path)
        with open(host_tar_path, "wb") as dump:
            for buffer in stream:
                dump.write(buffer)
        self.untar(host_tar_path)
        if os.path.isfile(host_dump_path):
            self.execute_cmd_in_container(
                "rm -r {}".format(
                    os.path.join(self._container_directory, self.project)
                ),
            )
            return [host_dump_path]
        return []

    @abstractmethod
    def get_dump_command(container_path: str) -> str:
        """Command execute in docker if to let time to create an archive/dump file"""


class PgsqlDriver(DatabaseDriverBase):
    """Archiver subclass for PostgreSQL dumps"""

    _env_vars_dict = {
        "env_vars_prefix": "POSTGRES_",
        "db_name": "POSTGRES_DB",
        "db_username": "POSTGRES_USER",
    }

    def retreive_container_labels(self) -> None:
        super().retreive_container_labels()
        self.username = self.container.labels.get(f"{DEFAULT_LABEL_PREFIX}.username")

        if not self.username:
            self.username = self.dbenvs.get(self._env_vars_dict["db_username"])

        if not self.username:
            # try fallback using postgres role
            self.username = "postgres"

    def get_dump_command(self, container_path):
        command = 'mkdir -p {}; pg_dump -U {} -Fc -O -f "{}" {}'.format(
            os.path.dirname(container_path), self.username, container_path, self.dbname
        )
        return command


class MysqlDriver(DatabaseDriverBase):
    """Archiver subclass for MySQL dumps"""

    _env_vars_dict = {
        "env_vars_prefix": "MYSQL_",
        "db_name": "MYSQL_DATABASE",
        "db_username": "MYSQL_USER",
        "db_password": "MYSQL_PASSWORD",
    }

    def get_dump_command(self, container_path):
        command = "mkdir -p {}; mysqldump -u {} -p{} {} | gzip > {}".format(
            os.path.dirname(container_path),
            self.username,
            self.password,
            self.dbname,
            container_path,
        )
        return command

    def retreive_container_labels(self):
        super().retreive_container_labels()
        self.username = self.container.labels.get(f"{DEFAULT_LABEL_PREFIX}.username")
        if not self.username:
            self.username = self.dbenvs.get(self._env_vars_dict["db_username"])

        if not self.username:
            raise ValueError(
                f"Could not find MYSQL username to dump '{self.dbname}' "
                f"database in '{self.container.name,}' docker container."
            )
        self.password = self.container.labels.get(f"{DEFAULT_LABEL_PREFIX}.password")
        if not self.password:
            self.password = self.dbenvs.get(self._env_vars_dict["db_password"])
        if not self.password:
            raise ValueError(
                f"Could not find MYSQL user password to dump '{self.dbname}' "
                f"database in '{self.container.name,}' docker container."
            )


class RsyncDriver(DriverFactory):

    folders: List[str] = None
    """Folder to dump"""

    rsync_params: str = None
    ro_volumes: bool = None

    def retreive_container_labels(self) -> None:
        super().retreive_container_labels()
        self.rsync_params = self.container.labels.get(
            f"{DEFAULT_LABEL_PREFIX}.rsync-params", ""
        )
        self.ro_volumes = str2bool(
            self.container.labels.get(f"{DEFAULT_LABEL_PREFIX}.ro-volumes", "")
        )
        self.folders = [
            (
                v["Destination"].replace("/", "-")[1:],
                str(Path(self.host_fs + v["Source"])),
            )
            for v in self.container.attrs.get("Mounts", [])
            if v.get("RW", False) or self.ro_volumes
        ]

        if not self.folders:
            raise ValueError(
                "Couldn't find local volume nor bind to rsync introspecting "
                f"{self.container.name} docker container on project "
                f"{self.project}."
            )

    def backup(self) -> List[str]:
        command = "rsync -avhP --delete {params} {source}/ {dest}"
        backup_paths = []
        for name, folder in self.folders:
            backup_dir = Path(self._root_directory).joinpath(
                self.project,
                self.environment,
                self.prefix + name,
            )
            backup_dir.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                command.format(
                    params=self.rsync_params,
                    source=folder,
                    dest=str(backup_dir),
                ),
                shell=True,
                check=True,
                capture_output=True,
            )
            backup_paths.append(str(backup_dir))
        return backup_paths


def str2bool(v):
    return v.lower().strip() in ("yes", "true", "t", "1")
