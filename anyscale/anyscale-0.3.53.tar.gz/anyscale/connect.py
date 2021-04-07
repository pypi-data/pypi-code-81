"""Anyscale connect implementation.

Here's an overview of how a connect call works. It goes through a few steps:
    1. Detecting the project and hashing the files
    2. Getting or creating a session
    3. Acquiring a session lock via the Ray client

Detecting the project: If the user is in a shell, we will create a
"scratch" project by default which is the empty directory. Otherwise, the
project must either be specified explicitly, or we autodetect it based on
the current working directory.

Getting or creating a session: Anyscale connect will look through the list of
sessions for the project and try to find one to connect to. If there are no
active sessions, or the session files hash (generated when the session was
created) is different from the local project hash, a session is
created / updated using "anyscale up".

A new session is 'created' when all other sessions are in-use, otherwise
an existing one is updated. Note that we perform this check while holding the
session lock (below) to avoid race conditions. However note that the
"anyscale up" part is not under the lock (this is a TODO).

Acquiring a session lock via the Ray client: To avoid multiple clients from
connecting to the same session, we acquire an exclusive lock on the session
before returning. This is done by checking that "num_clients" == 1 in the
returned connection info object, which means that we are the first client.
If we are not the first client, we disconnect from the session and try the
next one.
"""

import copy
import getpass
import inspect
import json
import os
import shlex
import subprocess
import sys
import tempfile
import time
from typing import Any, cast, Dict, List, Optional, Tuple, Union
import uuid

import colorama  # type: ignore
import requests
import yaml

from anyscale.client.openapi_client.models.app_config import AppConfig  # type: ignore
from anyscale.client.openapi_client.models.build import Build  # type: ignore
from anyscale.client.openapi_client.models.session import Session  # type: ignore
from anyscale.credentials import load_credentials
import anyscale.project
from anyscale.sdk.anyscale_client.sdk import AnyscaleSDK  # type: ignore
from anyscale.util import get_endpoint

# The default project directory to use, if no project is specified.
DEFAULT_SCRATCH_DIR = "~/.anyscale/scratch_{}".format(getpass.getuser())

# The key used to identify the session's latest file hash.
ANYSCALE_CONFIG_HASH = "anyscale.com/config_hash"

# Max number of auto created sessions.
MAX_SESSIONS = 20

# Default minutes for autosuspend.
DEFAULT_AUTOSUSPEND_TIMEOUT = 120

# The required Ray version on the client side.
REQUIRED_RAY_VERSION = "2.0.0.dev0"
REQUIRED_RAY_COMMIT = "35b45a03cffbedcf5720157060276c9c41bb87c0"

# Pin images to use on the server side.
# NOTE: If these are modified, `frontend/cli/tests/test_connect.py::test_pinned_images` must be run
# to verify that the new images use the right python version, CUDA files & ray commit!
PINNED_IMAGES = {
    "anyscale/ray-ml:nightly-py36-cpu": "anyscale/ray-ml@sha256:3a9f6c1cbb70d69b2af4d44a63f3bac584934083c902a426d5adb46a5f166696",
    "anyscale/ray-ml:nightly-py36-gpu": "anyscale/ray-ml@sha256:b6091ea184cbc63b852c34c44ce8d090848d71efc0d5fe7ebf911391c4fab094",
    "anyscale/ray-ml:nightly-py37-cpu": "anyscale/ray-ml@sha256:a9f1192b4ad6fb5df5adca1b9111ee1f92cde06318661c15e38c527a30ec6bc7",
    "anyscale/ray-ml:nightly-py37-gpu": "anyscale/ray-ml@sha256:3c86665b7d2186e770b8da9a43a27c040cffddfc5bb37cb385f649d8baa593cf",
    "anyscale/ray-ml:nightly-py38-cpu": "anyscale/ray-ml@sha256:b9f982ce854166d556d303f91a7ec19a5c07d4338e279972d28f8022a4b0e280",
    "anyscale/ray-ml:nightly-py38-gpu": "anyscale/ray-ml@sha256:2145a38879995eec14bd5a43352f5131f3f39acf26acf0e9b627d5a2efbf652f",
    "anyscale/ray:nightly-py36-cpu": "anyscale/ray@sha256:6d8b1d91f2e83e1dd7e5982a8a77b19f7c176eb9bb3190186371180b8679415a",
    "anyscale/ray:nightly-py36-gpu": "anyscale/ray@sha256:dd7e34051295465355b85288cf61b0c1dd052a9f2190e7eac0f6dac10263c81a",
    "anyscale/ray:nightly-py37-cpu": "anyscale/ray@sha256:41abf65892ba51fba8c87f704ee1ce77cad42d24bcc4ea11a224a42009f56f7d",
    "anyscale/ray:nightly-py37-gpu": "anyscale/ray@sha256:24e96ac330caed22f97fe03133e87a6eef68296d522a55b9c1b8a7f2c51649ed",
    "anyscale/ray:nightly-py38-cpu": "anyscale/ray@sha256:4d1fac974eaf7c08b5f0f1b2f7bd666c5058be2f693497b1041d5d5b1a003c23",
    "anyscale/ray:nightly-py38-gpu": "anyscale/ray@sha256:325b77b3274632f92ee9a6b7b3740315a6cf6ff30ece40a5384ee4f3b05eb6b2",
}

# Commands used to build Ray from source. Note that intermediate stages will
# be cached by the app config builder.
BUILD_STEPS = [
    "git clone https://github.com/ray-project/ray.git",
    "curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg",
    "sudo mv bazel.gpg /etc/apt/trusted.gpg.d/",
    'echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list',
    "sudo apt-get update && sudo apt-get install -y bazel=3.2.0",
    'cd ray/python && sudo env "PATH=$PATH" python setup.py develop',
    "pip uninstall -y ray",
]


def _get_wheel_url(
    ray_release: str,
    py_version: Optional[str] = None,
    sys_platform: Optional[str] = None,
) -> str:
    """Return S3 URL for the given release spec or 'latest'."""
    if py_version is None:
        py_version = "".join(str(x) for x in sys.version_info[0:2])
    if sys_platform is None:
        sys_platform = sys.platform

    if sys_platform == "darwin":
        if py_version == "38":
            platform = "macosx_10_13_x86_64"
        else:
            platform = "macosx_10_13_intel"
    elif sys_platform == "win32":
        platform = "win_amd64"
    else:
        platform = "manylinux2014_x86_64"

    if py_version == "38":
        py_version_malloc = py_version
    else:
        py_version_malloc = f"{py_version}m"

    return (
        "https://s3-us-west-2.amazonaws.com/ray-wheels/"
        "{}/ray-2.0.0.dev0-cp{}-cp{}-{}.whl".format(
            ray_release, py_version, py_version_malloc, platform
        )
    )


# Default docker images to use for connect sessions.
def _get_base_image(cpu_or_gpu: str = "cpu") -> str:
    py_version = "".join(str(x) for x in sys.version_info[0:2])
    if py_version not in ["36", "37", "38"]:
        raise ValueError("No default docker image for py{}".format(py_version))
    key = "anyscale/ray-ml:nightly-py{}-{}".format(py_version, cpu_or_gpu)
    if "ANYSCALE_NIGHTLY_IMAGES" in os.environ:
        return key
    else:
        return PINNED_IMAGES[key]


# Check whether we're running in a Notebook / shell.
def _in_shell() -> bool:
    fr: Any = inspect.getouterframes(inspect.currentframe())[-1]
    return bool(fr.filename == "<stdin>")


class _ConsoleLog:
    def __init__(self) -> None:
        self.t0 = time.time()

    def zero_time(self) -> None:
        self.t0 = time.time()

    def info(self, *msg: Any) -> None:
        print(
            "{}{}(anyscale +{}){} ".format(
                colorama.Style.BRIGHT,
                colorama.Fore.CYAN,
                self._time_string(),
                colorama.Style.RESET_ALL,
            ),
            end="",
        )
        print(*msg)

    def debug(self, *msg: str) -> None:
        if os.environ.get("ANYSCALE_DEBUG") == "1":
            print(
                "{}{}(anyscale +{}){} ".format(
                    colorama.Style.DIM,
                    colorama.Fore.CYAN,
                    self._time_string(),
                    colorama.Style.RESET_ALL,
                ),
                end="",
            )
            print(*msg)

    def error(self, *msg: str) -> None:
        print(
            "{}{}(anyscale +{}){} ".format(
                colorama.Style.BRIGHT,
                colorama.Fore.RED,
                self._time_string(),
                colorama.Style.RESET_ALL,
            ),
            end="",
        )
        print(*msg)

    def _time_string(self) -> str:
        delta = time.time() - self.t0
        hours = 0
        minutes = 0
        while delta > 3600:
            hours += 1
            delta -= 3600
        while delta > 60:
            minutes += 1
            delta -= 60
        output = ""
        if hours:
            output += "{}h".format(hours)
        if minutes:
            output += "{}m".format(minutes)
        output += "{}s".format(round(delta, 1))
        return output


class SessionBuilder:
    """This class lets you set session options and connect to Anyscale.

    It should not be constructed directly, but instead via anyscale.* methods
    exported at the package level.

    Examples:
        >>> # Raw client, creates new session on behalf of user
        >>> anyscale.connect()

        >>> # Get or create a named session
        >>> anyscale
        ...   .session("my_named_session")
        ...   .connect()

        >>> # Specify a previously created env / app template
        >>> anyscale
        ...   .app_config("prev_created_config:2")
        ...   .autosuspend(hours=2)
        ...   .connect()

        >>> # Create new session from local env / from scratch
        >>> anyscale
        ...   .project_dir("~/dev/my-project-folder")
        ...   .base_docker_image("anyscale/ray-ml:nightly")
        ...   .require("~/dev/my-project-folder/requirements.txt")
        ...   .connect()

        >>> # Ray client connect is setup automatically
        >>> @ray.remote
        ... def my_func(value):
        ...   return value ** 2

        >>> # Remote functions are executed in the Anyscale session
        >>> print(ray.get([my_func.remote(x) for x in range(5)]))
        >>> [0, 1, 4, 9, 16]
    """

    def __init__(
        self,
        scratch_dir: str = DEFAULT_SCRATCH_DIR,
        anyscale_sdk: AnyscaleSDK = None,
        subprocess: Any = subprocess,
        requests: Any = requests,
        _ray: Any = None,
        log: Any = _ConsoleLog(),
        _os: Any = os,
        _in_shell: Any = _in_shell,
        _ignore_version_check: bool = False,
    ) -> None:
        if "IGNORE_VERSION_CHECK" in os.environ:
            _ignore_version_check = True
        # Class dependencies.
        self._log = log
        self._anyscale_sdk: AnyscaleSDK = None
        self._credentials = None
        if anyscale_sdk:
            self._anyscale_sdk = anyscale_sdk
        else:
            self._credentials = load_credentials()
            self._log.debug("Using host {}".format(anyscale.conf.ANYSCALE_HOST))
            self._log.debug("Using credentials {}".format(self._credentials))
            self._anyscale_sdk = AnyscaleSDK(
                self._credentials, os.path.join(anyscale.conf.ANYSCALE_HOST, "ext")
            )
        if not _ray:
            import ray

            _ray = ray
        self._ray: Any = _ray
        self._subprocess: Any = subprocess
        self._os: Any = _os
        self._requests: Any = requests
        self._in_shell: Any = _in_shell
        self._ignore_version_check = _ignore_version_check

        # Builder args.
        self._scratch_dir: str = scratch_dir
        self._ray_release: Optional[str] = None
        self._project_dir: Optional[str] = None
        self._project_name: Optional[str] = None
        self._cloud_name: Optional[str] = None
        self._session_name: Optional[str] = None
        self._base_docker_image: Optional[str] = None
        self._requirements: Optional[str] = None
        self._app_config_name: Optional[str] = None
        self._app_config_revision: Optional[int] = None
        self._initial_scale: List[Dict[str, float]] = []
        self._autosuspend_timeout = DEFAULT_AUTOSUSPEND_TIMEOUT
        self._run_mode: Optional[str] = None
        self._build_commit: Optional[str] = None
        self._build_pr: Optional[int] = None
        self._force_rebuild: bool = False

        # Override default run mode.
        if "ANYSCALE_BACKGROUND" in os.environ:
            self._run_mode = "background"
            self._log.debug(
                "Using `run_mode=background` since ANYSCALE_BACKGROUND is set"
            )
        elif "ANYSCALE_LOCAL_DOCKER" in os.environ:
            self._run_mode = "local_docker"
            self._log.debug(
                "Using `run_mode=local_docker` since ANYSCALE_LOCAL_DOCKER is set"
            )

        # Whether to update the session when connecting to a fixed session.
        self._needs_update: bool = True

    def connect(self) -> None:  # noqa
        """Connect to Anyscale using previously specified options.

        Examples:
            >>> anyscale.connect()
        """
        import ray
        import ray.autoscaler.sdk

        self._check_required_ray_version(ray.__version__, ray.__commit__)
        # TODO(ekl) check for duplicate connections
        self._log.zero_time()

        if ray.util.client.ray.is_connected():
            raise RuntimeError(
                "Already connected to a Ray session, please "
                "run anyscale.connect in a new Python process."
            )

        # Allow the script to be run on the head node as well.
        if "ANYSCALE_SESSION_ID" in os.environ:
            ray.init(address="auto")
            return

        # Re-exec in the docker container.
        if self._run_mode == "local_docker":
            if self._in_shell():
                raise ValueError("Local docker mode is not supported in Python shells.")
            self._exec_self_in_local_docker()

        # Autodetect or create a scratch project.
        if self._project_dir is None:
            self._project_dir = anyscale.project.find_project_root(os.getcwd())
        if self._project_dir:
            self._ensure_project_setup_at_dir(self._project_dir, self._project_name)
        elif self._in_shell():
            self._project_dir = self._get_or_create_scratch_project()
        else:
            raise ValueError(
                "The current working directory is not associated with an "
                "Anyscale project. Please run ``anyscale init`` to setup a "
                "new project or specify ``.project_dir()`` prior to "
                "connecting. Anyscale Connect uses the project directory "
                "to find the Python code dependencies for your script."
            )

        self._job_config = self._ray.job_config.JobConfig(
            runtime_env={
                "working_dir": self._project_dir,
                "exclude": [
                    ".git",
                    "__pycache__",
                    sys.argv[0],
                    os.path.join(self._project_dir, ".anyscale.yaml"),
                    os.path.join(self._project_dir, "session-default.yaml"),
                ],
            }
        )

        proj_def = anyscale.project.ProjectDefinition(self._project_dir)
        project_id = anyscale.project.get_project_id(proj_def.root)
        self._log.info("Using project dir", proj_def.root)

        # TODO(ekl): generate a serverless compute configuraton here.
        cluster_yaml = yaml.safe_load(anyscale.project.CLUSTER_YAML_TEMPLATE)

        if self._build_pr or self._build_commit:
            self._app_config_name = self._build_app_config_from_source(project_id)

        build = (
            self._get_app_config_build(
                project_id, self._app_config_name, self._app_config_revision
            )
            if self._app_config_name
            else None
        )

        cluster_yaml = self._populate_cluster_config(
            cluster_yaml,
            project_id,
            self._anyscale_sdk.get_project(project_id).result.name,
            build=build,
        )

        with open(os.path.join(self._project_dir, "session-default.yaml"), "w+") as f:
            data = yaml.dump(cluster_yaml)
            import hashlib

            hasher = hashlib.sha1()
            hasher.update(data.encode())
            config_hash = hasher.hexdigest().encode()
            f.write(data)
            yaml_filepath = f.name

        if self._session_name is not None:
            sess = self._get_session(project_id, self._session_name)
            if not sess or sess.state != "Running":
                # Unconditionally create the session if it isn't up.
                needs_up = True
            else:
                needs_up = self._needs_update
        else:
            needs_up = False

        # Locate a updated session and update it if needed.
        if self._session_name is None or needs_up:
            self._session_name = self._get_or_create_updated_session(
                config_hash,
                project_id,
                self._session_name,
                build_id=build.id if build else None,
                yaml_filepath=yaml_filepath,
            )

        # Connect Ray client.
        self._check_connection(project_id, self._session_name)

        # Issue request resources call.
        if self._initial_scale:
            self._log.debug("Calling request_resources({})".format(self._initial_scale))
            ray.autoscaler.sdk.request_resources(bundles=self._initial_scale)

        # Define ray in the notebook automatically for convenience.
        try:
            fr: Any = inspect.getouterframes(inspect.currentframe())[-1]
            if fr.filename == "<stdin>" and "ray" not in fr.frame.f_globals:
                self._log.debug("Auto importing Ray into the notebook.")
                fr.frame.f_globals["ray"] = ray
        except Exception as e:
            self._log.error("Failed to auto define `ray` in notebook", e)

        # If in background mode, execute the job in the remote session.
        if self._run_mode == "background":
            if self._in_shell():
                raise ValueError("Background mode is not supported in Python shells.")
            self._exec_self_in_head_node()

    def cloud(self, cloud_name: str) -> "SessionBuilder":
        """Set the name of the cloud to be used.

        This sets the name of the cloud that your connect session will be
        started in. If you do not specify it, it will use the last used cloud
        in this project.

        Args:
            cloud_name (str): Name of the cloud to start the session in.

        Examples:
            >>> anyscale.cloud("aws_test_account").connect()
        """
        self._cloud_name = cloud_name
        return self

    def project_dir(
        self, local_dir: str, name: Optional[str] = None
    ) -> "SessionBuilder":
        """Set the project directory.

        This sets the project code directory that will be synced to all nodes
        in the cluster as required by Ray. If not specified, the project
        directory will be autodetected based on the current working directory.
        If no Anyscale project is found, a "scratch" project will be used.

        Args:
            local_dir (str): path to the project directory.
            name (str): optional name to use if the project doesn't exist.

        Examples:
            >>> anyscale.project_dir("~/my-proj-dir").connect()
        """
        self._project_dir = os.path.abspath(os.path.expanduser(local_dir))
        self._project_name = name
        return self

    def session(self, session_name: str, update: bool = False) -> "SessionBuilder":
        """Set a fixed session name.

        By default, Anyscale connect will pick an idle session updated
        with the connect parameters, creating a new session if no updated
        idle sessions. Setting a fixed session name will force connecting to
        the given named session, creating it if it doesn't exist.

        Args:
            session_name (str): fixed name of the session.
            update (bool): whether to update session configurations when
                connecting to an existing session. Note that this may restart
                the Ray runtime.

        Examples:
            >>> anyscale.session("prod_deployment", update=True).connect()
        """
        if not update:
            self._needs_update = False
        self._session_name = session_name
        return self

    def run_mode(self, run_mode: Optional[str] = None) -> "SessionBuilder":
        """Re-exec the driver program in the remote session or local docker.

        By setting ``run_mode("background")``, you can tell Anyscale connect
        to run the program driver remotely in the head node instead of executing
        locally. This allows you to e.g., close your laptop during development
        and have the program continue executing in the cluster.

        By setting ``run_mode("local_docker")``, you can tell Anyscale connect
        to re-exec the program driver in a local docker image, ensuring the
        driver environment will exactly match that of the remote session.

        You can also change the run mode by setting the ANYSCALE_BACKGROUND=1
        or ANYSCALE_LOCAL_DOCKER=1 environment variables. Changing the run mode
        is only supported for script execution. Attempting to change the run
        mode in a notebook or Python shell will raise an error.

        Args:
            run_mode (str): either None, "background", or "local_docker".

        Examples:
            >>> anyscale.run_mode("background").connect()
        """
        if run_mode not in [None, "background", "local_docker"]:
            raise ValueError("Unknown run mode {}".format(run_mode))
        self._run_mode = run_mode
        return self

    def base_docker_image(self, image_name: str) -> "SessionBuilder":
        """Set the docker image to use for the session.

        IMPORTANT: the Python minor version of the manually specified docker
        image must match the local Python version.

        Args:
            image_name (str): docker image name.

        Examples:
            >>> anyscale.base_docker_image("anyscale/ray-ml:latest").connect()
        """
        self._base_docker_image = image_name
        return self

    def require(self, requirements: Union[str, List[str]]) -> "SessionBuilder":
        """Set the Python requirements for the session.

        Args:
            requirements: either be a list of pip library specifications, or
            the path to a requirements.txt file.

        Examples:
            >>> anyscale.require("~/proj/requirements.txt").connect()
            >>> anyscale.require(["gym", "torch>=1.4.0"]).connect()
        """
        if isinstance(requirements, str):
            with open(requirements, "r") as f:
                data = f.read()
            # Escape quotes
            self._requirements = data.replace('"', r"\"")
        else:
            assert isinstance(requirements, list)
            self._requirements = "\n".join(requirements)
        return self

    def app_config(self, app_config_identifier: str) -> "SessionBuilder":
        """Set the Anyscale app config to use for the session.

        IMPORTANT: the Python minor version of the manually specified app
        config must match the local Python version, and the Ray version must
        also be compatible with the one on the client.

        Args:
            app_config_identifier (str): Name (and optionally revision) of
            the application config, for example "my_app_config:2" where the
            revision would be 2. If no revision is specified, use the latest
            revision.

        Examples:
            >>> anyscale.app_config("prev_created_config:2").connect()
        """
        if self._build_commit or self._build_pr:
            raise ValueError("app_config() conflicts with build_from_source()")
        components = app_config_identifier.rsplit(":", 1)
        self._app_config_name = components[0]
        if len(components) == 1:
            self._app_config_revision = None
        else:
            self._app_config_revision = int(components[1])
        return self

    def download_results(
        self, *, remote_dir: str, local_dir: str, autosync: bool = False
    ) -> "SessionBuilder":
        """Specify a directory to sync down from the cluster head node.

        Args:
            remote_dir (str): the remote result dir on the head node.
            local_dir (str): the local path to sync results to.
            autosync (bool): whether to sync the files continuously. By
                default, results will only be synced on job completion.

        Examples:
            >>> anyscale
            ...   .download_results(
            ...       remote_dir="~/ray_results", remote_dir="~/proj_output",
            ...       autosync=True)
            ...   .connect()
        """
        raise NotImplementedError()

    def autosuspend(
        self,
        enabled: bool = True,
        *,
        hours: Optional[int] = None,
        minutes: Optional[int] = None,
    ) -> "SessionBuilder":
        """Configure or disable session autosuspend behavior.

        The session will be autosuspend after the specified time period. By
        default, sessions auto terminate after one hour of idle.

        Args:
            enabled (bool): whether autosuspend is enabled.
            hours (int): specify idle time in hours.
            minutes (int): specify idle time in minutes. This is added to the
                idle time in hours.

        Examples:
            >>> anyscale.autosuspend(False).connect()
            >>> anyscale.autosuspend(hours=10).connect()
            >>> anyscale.autosuspend(hours=1, minutes=30).connect()
        """
        if enabled:
            if hours is None and minutes is None:
                timeout = DEFAULT_AUTOSUSPEND_TIMEOUT
            else:
                timeout = 0
                if hours is not None:
                    timeout += hours * 60
                if minutes is not None:
                    timeout += minutes
        else:
            timeout = -1
        self._autosuspend_timeout = timeout
        return self

    def nightly_build(self, git_commit: str) -> "SessionBuilder":
        """Use the specified nightly build commit for the session runtime.

        This is an experimental feature.

        Args:
            git_commit (str): git commit of the nightly Ray release.

        Examples:
            >>> anyscale
            ...   .nightly_build("f1e293c6997d1b14d61b8ca05965af42ae59d285")
            ...   .connect()
        """
        if len(git_commit) != 40:
            raise ValueError("Ray git commit hash must be 40 chars long")
        self._ray_release = "master/{}".format(git_commit)
        url = _get_wheel_url(self._ray_release)
        request = self._requests.head(url)
        if request.status_code != 200:
            raise ValueError(
                "Could not locate wheel in S3 (HTTP {}): {}".format(
                    request.status_code, url
                )
            )
        return self

    def build_from_source(
        self,
        *,
        git_commit: Optional[str] = None,
        github_pr_id: Optional[int] = None,
        force_rebuild: bool = False,
    ) -> "SessionBuilder":
        """Build Ray from source for the session runtime.

        This is an experimental feature.

        Note that the first build for a new base image might take upwards of
        half an hour. Subsequent builds will have cached compilation stages.

        Args:
            git_commit (Optional[str]): If specified, try to checkout the exact
                git commit from the Ray master branch. If pull_request_id is
                also specified, the commit may be from the PR branch as well.
            github_pr_id (Optional[int]): Specify the pull request id to use.
                If no git commit is specified, the latest commit from the pr
                will be used.
            force_rebuild (bool): Force rebuild of the app config.

        Examples:
            >>> anyscale
            ...   .build_from_source(git_commit="f1e293c", github_pr_id=12345)
            ...   .connect()
        """
        if self._app_config_name:
            raise ValueError("app_config() conflicts with build_from_source()")
        self._build_commit = git_commit
        self._build_pr = github_pr_id
        self._force_rebuild = force_rebuild
        return self

    def request_resources(
        self,
        *,
        num_cpus: Optional[int] = None,
        num_gpus: Optional[int] = None,
        bundles: Optional[List[Dict[str, float]]] = None,
    ) -> "SessionBuilder":
        """Configure the initial resources to scale to.

        This is an experimental feature.

        The session will immediately attempt to scale to accomodate the
        requested resources, bypassing normal upscaling speed constraints.
        The requested resources are pinned and exempt from downscaling.

        Args:
            num_cpus (int): number of cpus to request.
            num_gpus (int): number of gpus to request.
            bundles (List[Dict[str, float]): resource bundles to
                request. Each bundle is a dict of resource_name to quantity
                that can be allocated on a single machine. Note that the
                ``num_cpus`` and ``num_gpus`` args simply desugar into
                ``[{"CPU": 1}] * num_cpus`` and ``[{"GPU": 1}] * num_gpus``
                respectively.

        Examples:
            >>> anyscale.request_resources(num_cpus=200, num_gpus=30).connect()
            >>> anyscale.request_resources(
            ...     num_cpus=8,
            ...     resource_bundles=[{"GPU": 8}, {"GPU": 8}, {"GPU": 1}],
            ... ).connect()
        """
        to_request: List[Dict[str, float]] = []
        if num_cpus:
            to_request += [{"CPU": 1}] * num_cpus
        if num_gpus:
            to_request += [{"GPU": 1}] * num_gpus
        if bundles:
            to_request += bundles
        self._initial_scale = to_request
        return self

    def _get_or_create_scratch_project(self) -> str:
        """Get or create a scratch project, including the directory."""
        project_dir = os.path.expanduser(self._scratch_dir)
        project_name = os.path.basename(self._scratch_dir)
        if not os.path.exists(project_dir) and self._find_project_id(project_name):
            self._clone_project(project_dir, project_name)
        else:
            self._ensure_project_setup_at_dir(project_dir, project_name)
        return project_dir

    def _find_project_id(self, project_name: str) -> Optional[str]:
        """Return id if a project of a given name exists."""
        resp = self._anyscale_sdk.search_projects({"name": {"equals": project_name}})
        if len(resp.results) > 0:
            return resp.results[0].id  # type: ignore
        else:
            return None

    def _clone_project(self, project_dir: str, project_name: str) -> None:
        """Clone a project into the given dir by name."""
        cur_dir = os.getcwd()
        try:
            parent_dir = os.path.dirname(project_dir)
            os.makedirs(parent_dir, exist_ok=True)
            os.chdir(parent_dir)
            self._subprocess.check_call(["anyscale", "clone", project_name])
        finally:
            os.chdir(cur_dir)

    def _ensure_project_setup_at_dir(
        self, project_dir: str, project_name: Optional[str]
    ) -> None:
        """Get or create an Anyscale project rooted at the given dir."""
        os.makedirs(project_dir, exist_ok=True)
        if project_name is None:
            project_name = os.path.basename(project_dir)

        # If the project yaml exists, assume we're already setup.
        project_yaml = os.path.join(project_dir, ".anyscale.yaml")
        if os.path.exists(project_yaml):
            return

        project_id = self._find_project_id(project_name)
        if project_id is None:
            self._log.info("Creating new project for", project_dir)
            project_response = self._anyscale_sdk.create_project(
                {
                    "name": project_name,
                    "description": "Automatically created by Anyscale Connect",
                }
            )
            project_id = project_response.result.id

        if not os.path.exists(project_yaml):
            with open(project_yaml, "w+") as f:
                f.write(yaml.dump({"project_id": project_id}))

    def _up_session(
        self,
        project_id: str,
        session_name: str,
        cloud_name: str,
        cwd: Optional[str],
        dangerously_set_build_id: Optional[str],
        yaml_filepath: str,
    ) -> None:
        # Non-blocking version of check_call, see
        # https://github.com/python/cpython/blob/64abf373444944a240274a9b6d66d1cb01ecfcdd/Lib/subprocess.py#L363
        command = [
            "anyscale",
            "up",
            "--disable-sync",
            "--idle-timeout",
            str(self._autosuspend_timeout),
            "--config",
            yaml_filepath,
            "--cloud-name",
            cloud_name,
            session_name,
        ] + (
            ["--dangerously-set-build-id", dangerously_set_build_id]
            if dangerously_set_build_id
            else []
        )
        with tempfile.NamedTemporaryFile(delete=False) as output_log_file:
            with self._subprocess.Popen(
                command, cwd=cwd, stdout=output_log_file, stderr=subprocess.STDOUT,
            ) as p:
                # Get session URL:
                session_found = False
                retry_time = 1.0
                while not session_found and retry_time < 10:
                    results = self._list_sessions(project_id=project_id)
                    for session in results:
                        if session.name == session_name:
                            self._log.info(
                                "Updating session, see: {}".format(
                                    get_endpoint(
                                        f"/projects/{project_id}/sessions/{session.id}"
                                    )
                                )
                            )
                            session_found = True
                    time.sleep(retry_time)
                    retry_time = 2 * retry_time
                try:
                    retcode = p.wait()
                except Exception as e:
                    p.kill()
                    raise e
                # Check for errors:
                if retcode:
                    cmd = " ".join(command)
                    msg = "Executing '{}' in {} failed.".format(cmd, self._project_dir)
                    self._log.error(
                        "--------------- Start update logs ---------------\n"
                        "{}".format(open(output_log_file.name).read())
                    )
                    self._log.error("--------------- End update logs ---------------")
                    raise RuntimeError(msg)

    def _get_last_used_cloud(self, project_id: str) -> str:
        """Return the name of the cloud last used in the project.

        Args:
            project_id (str): The project to get the last used cloud for.

        Returns:
            Name of the cloud last used in this project.
        """
        # TODO(pcm): Get rid of this and the below API call in the common case where
        # we can determine the cloud to use in the backend.
        cloud_id = self._anyscale_sdk.get_project(project_id).result.last_used_cloud_id

        # TODO(pcm): Replace this with an API call once the AnyscaleSDK supports it.
        p = self._subprocess.Popen(
            ["anyscale", "list", "clouds", "--json"], stdout=subprocess.PIPE
        )
        clouds = json.loads(p.communicate()[0])

        if len(clouds) == 0:
            msg = "No cloud configured, please set up a cloud with 'anyscale cloud setup'."
            self._log.error(msg)
            raise RuntimeError(msg)

        if not cloud_id:
            # Clouds are sorted in descending order, pick the oldest one as default.
            cloud_id = clouds[-1]["id"]

        cloud_name = {cloud["id"]: cloud["name"] for cloud in clouds}[cloud_id]
        self._log.debug(
            (
                f"Using last active cloud '{cloud_name}'. "
                "Call anyscale.cloud('...').connect() to overwrite."
            )
        )
        return cast(str, cloud_name)

    def _get_or_create_updated_session(  # noqa: C901
        self,
        config_hash: bytes,
        project_id: str,
        session_name: Optional[str],
        build_id: Optional[str],
        yaml_filepath: str,
    ) -> str:
        """Get or create a session updated with the given hash.

        Args:
            config_hash (bytes): The hash value of config
            project_id (str): The project to use.
            session_name (Optional[str]): If specified, the given session
                will be created or updated as needed. Otherwise the session
                name will be picked automatically.

        Returns:
            The name of the session to connect to.
        """
        session_hash = None
        ray_cli = self._ray.util.client.ray
        kv = self._ray.experimental.internal_kv

        if session_name is None:
            self._log.debug("-> Looking for any running session matching hash")
            results = self._list_sessions(project_id=project_id)
            self._log.debug("Session states", [s.state for s in results])
            for session in results:
                if session.state != "Running":
                    continue
                self._log.debug("Trying to acquire lock on", session.name)
                self._acquire_session_lock(
                    session, raise_connection_error=False, connection_retries=0
                )
                if not ray_cli.is_connected():
                    continue
                try:
                    session_hash = kv._internal_kv_get(ANYSCALE_CONFIG_HASH)
                except Exception as e:
                    self._log.debug("Error getting session hash", e)
                    session_hash = None
                if session_hash == config_hash:
                    self._log.debug("Acquired lock on session", session.name)
                    session_name = session.name
                    break
                else:
                    self._ray.util.disconnect()

        session_name_conn_failed = None
        if session_name is None:
            self._log.debug("-> Looking for any running session (ignoring hash)")
            for session in results:
                if session.state != "Running":
                    continue
                self._log.debug("Trying to acquire lock on", session.name)
                try:
                    self._acquire_session_lock(
                        session, raise_connection_error=True, connection_retries=0
                    )
                except Exception:
                    self._log.debug(
                        "Error connecting to session, will revisit", session.name
                    )
                    session_name_conn_failed = session.name
                    continue
                if ray_cli.is_connected():
                    self._log.debug("Acquired lock on session", session.name)
                    session_name = session.name
                    break

        if session_name is None and session_name_conn_failed:
            self._log.debug("-> Fallback to restarting an errored session")
            session_name = session_name_conn_failed

        if session_name is None:
            self._log.debug("-> Fallback to starting a new session")
            used_names = [s.name for s in results if s.state == "Running"]
            for i in range(MAX_SESSIONS):
                name = "session-{}".format(i)
                if name not in used_names:
                    session_name = name
                    self._log.debug("Starting session", session_name)
                    break

        # Should not happen.
        if session_name is None:
            raise RuntimeError("Could not create new session to connect to.")

        if self._cloud_name is None:
            self._cloud_name = self._get_last_used_cloud(project_id)

        self._log.debug("Session hash", session_hash)
        self._log.debug("config hash", config_hash)
        if session_hash != config_hash:
            self._log.debug("Updating the cluster config of", session_name)
            # TODO(ekl): race condition here since "up" breaks the lock.
            if ray_cli.is_connected():
                self._ray.util.disconnect()
            # Update session.
            self._up_session(
                project_id,
                session_name,
                self._cloud_name,
                self._project_dir,
                dangerously_set_build_id=build_id,
                yaml_filepath=yaml_filepath,
            )
            # Need to re-acquire the connection after the update.
            self._acquire_session_lock(
                self._get_session_or_die(project_id, session_name),
                raise_connection_error=True,
                connection_retries=10,
            )
            # TODO(ekl) retry this, might be race condition with another client
            if not ray_cli.is_connected():
                raise RuntimeError("Failed to acquire session we created")
            kv._internal_kv_put(ANYSCALE_CONFIG_HASH, config_hash, overwrite=True)
            self._log.debug(
                "Updated files hash",
                config_hash,
                kv._internal_kv_get(ANYSCALE_CONFIG_HASH),
            )

        return session_name

    def _acquire_session_lock(
        self, session_meta: Any, raise_connection_error: bool, connection_retries: int,
    ) -> None:
        """Connect to and acquire a lock on the session.

        The session lock is released by calling disconnect() on the returned
        Ray connection. This function also checks for Python version
        compatibility, it will not acquire the lock on version mismatch.

        """
        try:
            session_url, secure, metadata = self._get_connect_params(session_meta)
            if connection_retries > 0:
                self._log.debug("Beginning connection attempts")
            # Disable retries when acquiring session lock for fast failure.
            self._log.debug(
                "Info: ",
                session_url,
                secure,
                metadata,
                connection_retries,
                self._job_config,
            )
            info = self._ray.util.connect(
                session_url,
                secure=secure,
                metadata=metadata,
                connection_retries=connection_retries,
                job_config=self._job_config,
            )
            self._log.debug("Connected server info: ", info)
        except Exception as e:
            if raise_connection_error:
                self._log.debug(
                    "Connection error after {} retries".format(connection_retries)
                )
                raise
            else:
                self._log.debug("Ignoring connection error", e)
                return
        if info["num_clients"] > 1:
            self._log.debug(
                "Failed to acquire lock due to too many connections: ",
                info["num_clients"],
            )
            self._ray.util.disconnect()

    def _check_connection(self, project_id: str, session_name: str,) -> None:
        """Check the connected session to make sure it's good"""
        session_found = self._get_session_or_die(project_id, session_name)

        def func() -> str:
            return "Connected!"

        f_remote = self._ray.remote(func)
        ray_ref = f_remote.remote()
        self._log.debug(self._ray.get(ray_ref))
        self._log.info(
            "Connected to {}, see: {}".format(
                session_name,
                get_endpoint(f"/projects/{project_id}/sessions/{session_found.id}"),
            )
        )

    def _get_session_or_die(self, project_id: str, session_name: str) -> Session:
        """Query Anyscale for the given session's metadata."""
        session_found = self._get_session(project_id, session_name)
        if not session_found:
            raise RuntimeError("Failed to locate session: {}".format(session_name))
        return session_found

    def _get_session(self, project_id: str, session_name: str) -> Optional[Session]:
        """Query Anyscale for the given session's metadata."""
        results = self._list_sessions(project_id=project_id)
        session_found: Session = None
        for session in results:
            if session.name == session_name:
                session_found = session
                break
        return session_found

    def _get_connect_params(self, session_meta: Session) -> Tuple[str, bool, Any]:
        """Get the params from the session needed to use Ray client."""
        # TODO(nikita): Use the service_proxy_url once it is fixed for anyscale up with file mounts.
        full_url = session_meta.jupyter_notebook_url
        # like "session-fqsx0p3pzfna71xxxxxxx.anyscaleuserdata.com:8081"
        session_url = full_url.split("/")[2].lower() + ":8081"
        # like "8218b528-7363-4d04-8358-57936cdxxxxx"
        auth_token = full_url.split("?token=")[1].split("&")[0]
        metadata = [("cookie", "anyscale-token=" + auth_token), ("port", "10001")]
        return session_url, False, metadata

    def _populate_cluster_config(
        self,
        cluster_yaml: Dict[str, Any],
        project_id: str,
        project_name: str,
        build: Optional[Build],
    ) -> Dict[str, Any]:
        """Populate cluster config with serverless compute options."""
        cluster_yaml = copy.deepcopy(cluster_yaml)

        base_docker_image_cpu = _get_base_image("cpu")
        base_docker_image_gpu = _get_base_image("gpu")

        # Overwrite base_docker_image with application config if available.
        if build:
            base_docker_image_cpu = (
                base_docker_image_gpu
            ) = self._get_app_config_docker_image(project_id, build_to_use=build)
        elif self._base_docker_image:
            # Overwrite base_docker_image if provided by user.
            base_docker_image_cpu = self._base_docker_image
            base_docker_image_gpu = self._base_docker_image
        self._log.debug("Base docker image {}".format(base_docker_image_cpu))

        # Setup serverless compute template.
        cluster_yaml["available_node_types"] = {
            "anyscale.cpu.medium": {
                "node_config": {"InstanceType": "m5.4xlarge"},
                "max_workers": 20,
                "resources": {},
                "docker": {"worker_image": base_docker_image_cpu},
            },
            "anyscale.cpu.large": {
                "node_config": {"InstanceType": "m5.16xlarge"},
                "max_workers": 10,
                "resources": {},
                "docker": {"worker_image": base_docker_image_cpu},
            },
            "anyscale.gpu.medium": {
                "node_config": {"InstanceType": "g3.4xlarge"},
                "max_workers": 20,
                "resources": {},
                "docker": {"worker_image": base_docker_image_gpu},
            },
            "anyscale.gpu.large": {
                "node_config": {"InstanceType": "g3.16xlarge"},
                "max_workers": 10,
                "resources": {},
                "docker": {"worker_image": base_docker_image_gpu},
            },
        }
        cluster_yaml["max_workers"] = 50
        cluster_yaml["head_node_type"] = "anyscale.cpu.medium"
        cluster_yaml["docker"]["image"] = base_docker_image_cpu

        # Install Ray runtime if specified.
        if self._ray_release:
            cluster_yaml["setup_commands"] = [
                "pip install -U {}".format(_get_wheel_url(self._ray_release))
            ]

        # Install requirements:
        if self._requirements:
            cluster_yaml["setup_commands"].append(
                f'echo "{self._requirements}" | pip install -r /dev/stdin'
            )

        cluster_yaml["head_start_ray_commands"] = [
            "ray stop",
            "ulimit -n 65536; ray start --head --port=6379 "
            "--object-manager-port=8076  --ray-client-server-port=10001",
        ]

        return cluster_yaml

    def _wait_for_app_build(self, project_id: str, build_id: str) -> Build:
        has_logged = False
        while True:
            build = self._anyscale_sdk.get_build(build_id).result
            if build.status in ["pending", "in_progress"]:
                if not has_logged:
                    url = get_endpoint(
                        f"projects/{project_id}/app-config-details/{build_id}"
                    )
                    self._log.info(
                        f"Waiting for app config to be built (see {url} for progress)..."
                    )
                    has_logged = True
                time.sleep(10.0)
            elif build.status in ["failed", "pending_cancellation", "canceled"]:
                raise RuntimeError(
                    "Build status is '{}', please select another revision!".format(
                        build.status
                    )
                )
            else:
                assert build.status == "succeeded"
                return build

    def _get_app_config_build(
        self, project_id: str, app_config_name: str, app_config_revision: Optional[int]
    ) -> Build:
        app_template_id = None
        app_templates = self._list_app_configs(project_id)
        for app_template in app_templates:
            if app_template.name == app_config_name:
                app_template_id = app_template.id
        if not app_template_id:
            raise RuntimeError(
                "Application config '{}' not found. ".format(app_config_name)
                + "Available app configs: {}".format(
                    ", ".join(a.name for a in app_templates)
                )
            )
        builds = self._list_builds(app_template_id)

        build_to_use = None
        if app_config_revision:
            for build in builds:
                if build.revision == app_config_revision:
                    build_to_use = build

            if not build_to_use:
                raise RuntimeError(
                    "Revision {} of app config '{}' not found.".format(
                        app_config_revision, app_config_name
                    )
                )
        else:
            latest_build_revision = -1
            for build in builds:
                if build.revision > latest_build_revision:
                    latest_build_revision = build.revision
                    build_to_use = build
            self._log.debug(
                "Using latest revision {} of {}".format(
                    latest_build_revision, app_config_name
                )
            )
        assert build_to_use  # for mypy
        return build_to_use

    def _build_app_config_from_source(self, project_id: str) -> str:
        config_name = "ray-build-{}-{}".format(self._build_pr, self._build_commit)
        # Force creation of a unique app config.
        if self._force_rebuild:
            config_name += "-{}".format(int(time.time()))
        app_templates = self._list_app_configs(project_id)
        found = any([a.name == config_name for a in app_templates])
        if not found:
            build_steps = BUILD_STEPS.copy()
            # Add a unique command to bust the Makisu cache if needed.
            # Otherwise we could end up caching a previous fetch.
            build_steps.append("echo UNIQUE_ID={}".format(config_name))
            if self._build_pr:
                build_steps.append(
                    "cd ray && git fetch origin pull/{}/head:target && "
                    "git checkout target".format(self._build_pr)
                )
            if self._build_commit:
                build_steps.append(
                    "cd ray && git checkout {}".format(self._build_commit)
                )
            build_steps.append(
                'cd ray/python && sudo env "PATH=$PATH" python setup.py develop'
            )
            self._anyscale_sdk.create_app_config(
                {
                    "name": config_name,
                    "project_id": project_id,
                    "config_json": {
                        "base_image": self._base_docker_image or "anyscale/ray:nightly",
                        "debian_packages": ["curl", "unzip", "zip", "gnupg"],
                        "post_build_cmds": build_steps,
                    },
                }
            )
        return config_name

    def _get_app_config_docker_image(self, project_id: str, build_to_use: Build) -> str:
        # Wait for build to complete:
        build_to_use = self._wait_for_app_build(project_id, build_to_use.id)
        return "localhost:5555/{}".format(build_to_use.docker_image_name)

    def _exec_self_in_head_node(self) -> None:
        """Run the current main file in the head node."""
        cur_file = os.path.abspath(sys.argv[0])
        # TODO(ekl) it would be nice to support keeping the original file name,
        # but "anyscale push" isn't escaping e.g., spaces correctly.
        tmp_file = "/tmp/anyscale-connect-{}.py".format(uuid.uuid4().hex)
        cur_dir = os.getcwd()
        try:
            os.chdir(self._project_dir)  # type: ignore
            command = [
                "anyscale",
                "push",
                self._session_name,
                "-s",
                cur_file,
                "-t",
                tmp_file,
            ]
            self._log.debug("Running", command)
            self._subprocess.check_output(
                command, stderr=subprocess.STDOUT,
            )
            command = (
                [
                    "anyscale",
                    "exec",
                    "--session-name",
                    self._session_name,
                    "python",
                    tmp_file,
                ]
                + sys.argv[1:]  # type: ignore
            )
            self._log.debug("Running", command)
            self._subprocess.check_call(command)
        finally:
            os.chdir(cur_dir)
        self._os._exit(0)

    def _exec_self_in_local_docker(self) -> None:
        """Run the current main file in a local docker image."""
        cur_file = os.path.abspath(sys.argv[0])
        docker_image = self._base_docker_image or _get_base_image("cpu")
        command = [
            "docker",
            "run",
            "--env",
            "ANYSCALE_HOST={}".format(anyscale.conf.ANYSCALE_HOST),
            "--env",
            "ANYSCALE_CLI_TOKEN={}".format(self._credentials),
            "-v",
            "{}:/user_main.py".format(cur_file),
            "--entrypoint=/bin/bash",
            docker_image,
            "-c",
            "python /user_main.py {}".format(
                " ".join([shlex.quote(x) for x in sys.argv[1:]])
            ),
        ]
        self._log.debug("Running", command)
        self._subprocess.check_call(command)
        self._os._exit(0)

    def _get_project_name(self, project_id: str) -> str:
        return self._anyscale_sdk.get_project(project_id).result.name  # type: ignore

    def _list_entities(self, list_function: Any, container_id: str) -> List[Any]:
        entities = []
        has_more = True
        paging_token = None
        while has_more:
            resp = list_function(container_id, count=50, paging_token=paging_token)
            entities.extend(resp.results)
            paging_token = resp.metadata.next_paging_token
            has_more = paging_token is not None
        return entities

    def _list_sessions(self, project_id: str) -> List[Session]:
        return self._list_entities(self._anyscale_sdk.list_sessions, project_id)

    def _list_app_configs(self, project_id: str) -> List[AppConfig]:
        return self._list_entities(self._anyscale_sdk.list_app_configs, project_id)

    def _list_builds(self, application_template_id: str) -> List[Build]:
        return self._list_entities(
            self._anyscale_sdk.list_builds, application_template_id
        )

    def _check_required_ray_version(self, ray_version: str, ray_commit: str) -> None:
        if ray_version != REQUIRED_RAY_VERSION or ray_commit != REQUIRED_RAY_COMMIT:
            msg = (
                "The local Ray installation has version {} (commit {}), but "
                "{} (commit {}) is required. Please install the required "
                "Ray version by running `pip uninstall ray -y && pip install -U {}`. To unsafely "
                "ignore this check, set IGNORE_VERSION_CHECK=1.".format(
                    ray_version,
                    ray_commit,
                    REQUIRED_RAY_VERSION,
                    REQUIRED_RAY_COMMIT,
                    _get_wheel_url("master/{}".format(REQUIRED_RAY_COMMIT)),
                )
            )
            if self._ignore_version_check:
                self._log.debug(msg)
            else:
                raise ValueError(msg)


# This implements the following utility function for users:
# $ pip install -U `python -m anyscale.connect required_ray_version`
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "required_ray_version":
        print(_get_wheel_url("master/{}".format(REQUIRED_RAY_COMMIT)))
    else:
        raise ValueError("Unsupported argument.")
