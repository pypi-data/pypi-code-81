from datetime import datetime
import os
from pathlib import Path
import subprocess
import tempfile
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    List,
    Tuple,
)
from unittest.mock import ANY, Mock

import pytest
import yaml

import anyscale
from anyscale.client.openapi_client.models.app_config import AppConfig  # type: ignore
from anyscale.client.openapi_client.models.build import Build  # type: ignore
from anyscale.client.openapi_client.models.project import Project  # type: ignore
from anyscale.client.openapi_client.models.project_response import ProjectResponse  # type: ignore
from anyscale.client.openapi_client.models.session import Session  # type: ignore
from anyscale.connect import (
    _get_wheel_url,
    PINNED_IMAGES,
    REQUIRED_RAY_COMMIT,
    REQUIRED_RAY_VERSION,
)
from anyscale.connect import SessionBuilder


def _make_session(i: int, state: str) -> Session:
    return Session(
        id="session_id",
        name="session-{}".format(i),
        created_at=datetime.now(),
        snapshots_history=[],
        idle_timeout=120,
        tensorboard_available=False,
        project_id="project_id",
        state=state,
        service_proxy_url="http://session-{}.userdata.com/auth?token=value&bar".format(
            i
        ),
        jupyter_notebook_url="http://session-{}.userdata.com/jupyter/lab?token=value".format(
            i
        ),
        access_token="value",
    )


def _make_app_template() -> AppConfig:
    return AppConfig(
        project_id="project_id",
        id="application_template_id",
        name="test-app-config",
        creator_id="creator_id",
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
    )


def _make_build() -> Build:
    return Build(
        id="build_id",
        revision=0,
        application_template_id="application_template_id",
        config_json="",
        creator_id="creator_id",
        status="succeeded",
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
        docker_image_name="docker_image_name",
    )


def _connected(ray: Mock, ret: Dict[str, Any],) -> Callable[[Any, Any], Dict[str, Any]]:
    def connected(*a: Any, **kw: Any) -> Dict[str, Any]:
        ray.util.client.ray.is_connected.return_value = True
        return ret

    return connected


def _make_test_builder(
    tmp_path: Path,
    session_states: List[str] = ["Running"],
    setup_project_dir: bool = True,
) -> Tuple[Any, Any, Any, Any]:
    scratch = tmp_path / "scratch"
    sdk = Mock()
    sess_resp = Mock()
    ray = Mock()

    def disconnected(*a: Any, **kw: Any) -> None:
        ray.util.client.ray.is_connected.return_value = False

    # Emulate session lock failure.
    ray.util.connect.side_effect = _connected(ray, {"num_clients": 1})
    ray.util.disconnect.side_effect = disconnected

    job_config_mock = Mock()
    ray.job_config.JobConfig.return_value = job_config_mock
    sess_resp.results = [
        _make_session(i, state) for i, state in enumerate(session_states)
    ]
    sess_resp.metadata.next_paging_token = None
    sdk.list_sessions.return_value = sess_resp
    proj_resp = Mock()
    proj_resp.result.name = "scratch"
    sdk.get_project.return_value = proj_resp
    subprocess = Mock()
    _os = Mock()
    builder = SessionBuilder(
        scratch_dir=scratch.absolute().as_posix(),
        anyscale_sdk=sdk,
        subprocess=subprocess,
        _ray=ray,
        _os=_os,
        _ignore_version_check=True,
    )
    if setup_project_dir:
        builder.project_dir(scratch.absolute().as_posix())
    else:
        builder._in_shell = lambda: True
    builder._find_project_id = lambda _: None  # type: ignore
    setattr(builder, "_up_session", Mock())
    setattr(
        builder, "_get_last_used_cloud", Mock(return_value="anyscale_default_cloud")
    )
    return builder, sdk, subprocess, ray


def test_new_proj_connect_params(tmp_path: Path, project_test_data: Project) -> None:
    project_dir = (tmp_path / "my_proj").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file
    builder.project_dir(project_dir).connect()

    assert anyscale.project.get_project_id(project_dir)
    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "anyscale_default_cloud",
        project_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )

    # Also check connection params in this test.
    ray.util.connect.assert_called_with(
        "session-0.userdata.com:8081",
        metadata=[("cookie", "anyscale-token=value"), ("port", "10001")],
        secure=False,
        connection_retries=10,
        job_config=ray.job_config.JobConfig(),
    )


def test_detect_existing_proj(tmp_path: Path) -> None:
    nested_dir = (tmp_path / "my_proj" / "nested").absolute().as_posix()
    parent_dir = os.path.dirname(nested_dir)
    os.makedirs(nested_dir)
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, setup_project_dir=False
    )

    # Setup project in parent dir
    project_yaml = os.path.join(parent_dir, ".anyscale.yaml")
    with open(project_yaml, "w+") as f:
        f.write(yaml.dump({"project_id": 12345}))

    # Should detect the parent project dir
    cwd = os.getcwd()
    try:
        os.chdir(nested_dir)
        builder.connect()
    finally:
        os.chdir(cwd)

    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "anyscale_default_cloud",
        parent_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_fallback_scratch_dir(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.connect()

    assert anyscale.project.get_project_id(scratch_dir)
    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_background_run_mode(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.run_mode("background").connect()

    assert anyscale.project.get_project_id(scratch_dir)
    builder._subprocess.check_output.assert_called_with(
        ["anyscale", "push", "session-0", "-s", ANY, "-t", ANY], stderr=ANY
    )
    builder._subprocess.check_call.assert_called_with(ANY)
    builder._os._exit.assert_called_once_with(0)


def test_local_docker_run_mode(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.run_mode("local_docker").connect()

    assert anyscale.project.get_project_id(scratch_dir)
    builder._subprocess.check_call.assert_called_with(
        [
            "docker",
            "run",
            "--env",
            ANY,
            "--env",
            ANY,
            "-v",
            ANY,
            "--entrypoint=/bin/bash",
            ANY,
            "-c",
            ANY,
        ]
    )
    builder._os._exit.assert_called_once_with(0)


def test_connect_with_cloud(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.cloud("test_cloud").connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "test_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_clone_scratch_dir(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, setup_project_dir=False
    )
    builder._find_project_id = lambda _: "foo"
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def clone_project(*a: Any, **kw: Any) -> None:
        os.makedirs(scratch_dir, exist_ok=True)
        project_yaml = os.path.join(scratch_dir, ".anyscale.yaml")
        with open(project_yaml, "w+") as f:
            f.write(yaml.dump({"project_id": 12345}))

    builder._subprocess.check_call.side_effect = clone_project

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.connect()

    builder._subprocess.check_call.assert_called_once_with(
        ["anyscale", "clone", "scratch"]
    )
    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_new_session(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    # Should create a new session.
    builder.connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_base_docker_image(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    yaml_filepath = None

    def get_yaml_filepath(*n: Any, **kw: Any) -> None:
        nonlocal yaml_filepath
        yaml_filepath = kw["yaml_filepath"]

    builder._up_session.side_effect = get_yaml_filepath
    builder.project_dir(scratch_dir).base_docker_image(
        "anyscale/ray-ml:custom"
    ).connect()

    with open(cast(str, yaml_filepath)) as f:
        data = yaml.safe_load(f)

    assert data["docker"]["image"] == "anyscale/ray-ml:custom"
    for nodes_type, node_config in data["available_node_types"].items():
        assert node_config["docker"]["worker_image"] == "anyscale/ray-ml:custom"


def test_requirements_list(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    yaml_filepath = None

    def create_session(*a: Any, **kw: Any) -> None:
        nonlocal yaml_filepath
        yaml_filepath = kw["yaml_filepath"]
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    # Create a new session with a list of requirements.
    builder.project_dir(scratch_dir).require(["pandas", "wikipedia"]).connect()

    with open(cast(str, yaml_filepath)) as f:
        data = yaml.safe_load(f)

    assert (
        'echo "pandas\nwikipedia" | pip install -r /dev/stdin' in data["setup_commands"]
    )


def test_requirements_file(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    yaml_filepath = None

    def create_session(*a: Any, **kw: Any) -> None:
        nonlocal yaml_filepath
        yaml_filepath = kw["yaml_filepath"]
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    with open("/tmp/requirements.txt", "w") as f:
        f.write("pandas\nwikipedia\ndask")
    # Create a new session with a requiremttns file.
    builder.project_dir(scratch_dir).require("/tmp/requirements.txt").connect()

    with open(cast(str, yaml_filepath)) as f:
        data = yaml.safe_load(f)

    assert (
        'echo "pandas\nwikipedia\ndask" | pip install -r /dev/stdin'
        in data["setup_commands"]
    )


def test_new_session_lost_lock(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    # Emulate session lock failure.
    ray.util.connect.side_effect = _connected(ray, {"num_clients": 999999})

    # Should create a new session.
    with pytest.raises(RuntimeError):
        builder.connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_reuse_session_hash_match(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Create fake cluster yaml for fingerprinting.
    os.makedirs(scratch_dir)
    builder.require(["wikipedia", "dask"]).project_dir(scratch_dir)
    cluster_yaml = yaml.safe_load(anyscale.project.CLUSTER_YAML_TEMPLATE)
    cluster_yaml = builder._populate_cluster_config(
        cluster_yaml, "project_id", "scratch", build=None
    )
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(yaml.dump(cluster_yaml))
    import hashlib

    hasher = hashlib.sha1()
    hasher.update(yaml.dump(cluster_yaml).encode())
    local_config_hash = hasher.hexdigest().encode()

    # Emulate session hash code match.
    ray.util.connect.return_value = {"num_clients": 1}
    ray.experimental.internal_kv._internal_kv_get.return_value = local_config_hash

    # Hash code match, no update needed.
    builder.require(["wikipedia", "dask"]).connect()

    builder._up_session.assert_not_called()

    # Hash code doesn't match, update needed.
    builder.require(["wikipedia", "dask", "celery"]).connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_reuse_session_hash_mismatch(
    tmp_path: Path, project_test_data: Project
) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    local_config_hash = b"wrong-hash-code"

    # Emulate session hash code mismatch.
    ray.experimental.internal_kv._internal_kv_get.return_value = local_config_hash

    # Should connect and run 'up'.
    builder.connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_reuse_session_lock_failure(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [
            _make_session(0, "Running"),
            _make_session(1, "Running"),
        ]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp
        ray.util.connect.side_effect = _connected(ray, {"num_clients": 1})

    builder._up_session.side_effect = create_session

    cluster_yaml = yaml.safe_load(anyscale.project.CLUSTER_YAML_TEMPLATE)
    builder._populate_cluster_config(cluster_yaml, "project_id", "scratch", build=None)
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(yaml.dump(cluster_yaml))
    import hashlib

    hasher = hashlib.sha1()
    hasher.update(yaml.dump(cluster_yaml).encode())
    local_config_hash = hasher.hexdigest().encode()
    # Emulate session hash code match but lock failure.
    ray.util.connect.side_effect = _connected(ray, {"num_clients": 9999999})
    ray.experimental.internal_kv._internal_kv_get.return_value = local_config_hash

    # Creates new session-1.
    builder.connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-1",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_restart_session_conn_failure(
    tmp_path: Path, project_test_data: Project
) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def fail_first_session(url: str, *a: Any, **kw: Any) -> Any:
        raise ConnectionError("mock connect failure")

    # Emulate session hash code match but conn failure.
    ray.util.connect.side_effect = fail_first_session

    # Tries to restart it, but fails.
    with pytest.raises(ConnectionError):
        builder.connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_skip_session_conn_failure(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def fail_first_session(url: str, *a: Any, **kw: Any) -> Any:
        if "session-0" in url:
            raise ConnectionError("mock connect failure")
        else:
            ray.util.client.ray.is_connected.return_value = True
            return {"num_clients": 1}

    # Emulate session hash code match but conn failure.
    ray.util.connect = fail_first_session

    # Skips session-0, updates session-1.
    builder.connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-1",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_fixed_session(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should connect and run 'up'.
    builder.session("session-1", update=True).connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-1",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_fixed_session_not_running(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Stopped"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should connect and run 'up'.
    builder.session("session-1").connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-1",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


def test_fixed_session_no_update(tmp_path: Path, project_test_data: Project) -> None:
    builder, sdk, subprocess, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should connect and run 'up'.
    builder.session("session-1", update=False).connect()

    builder._up_session.assert_not_called()


def test_new_fixed_session(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(i, "Running") for i in range(3)]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    # Should create a new session.
    builder.session("session-2").connect()

    builder._up_session.assert_called_once_with(
        ANY,
        "session-2",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=None,
        yaml_filepath=ANY,
    )


class MockPopen(object):
    def __init__(self) -> None:
        pass

    def communicate(self) -> Tuple[str, str]:
        return (
            '[{"id": "cloud2", "name": "second cloud"}, {"id": "cloud1", "name": "first cloud"}]',
            "",
        )


def test_get_default_cloud(tmp_path: Path, project_test_data: Project) -> None:
    subprocess = Mock()
    subprocess.Popen.return_value = MockPopen()
    sdk = Mock()
    project_test_data.last_used_cloud_id = None
    sdk.get_project.return_value = ProjectResponse(result=project_test_data)
    builder = SessionBuilder(anyscale_sdk=sdk, subprocess=subprocess,)
    # Check that we get the "default cloud" (cloud first created)
    # if there is no last used cloud.
    assert builder._get_last_used_cloud("prj_1") == "first cloud"
    project_test_data.last_used_cloud_id = "cloud2"
    # If there is a last used cloud, use that instead.
    assert builder._get_last_used_cloud("prj_1") == "second cloud"


def test_app_config(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    app_templates_resp = Mock()
    app_templates_resp.results = [_make_app_template()]
    app_templates_resp.metadata.next_paging_token = None
    sdk.list_app_configs.return_value = app_templates_resp

    build = _make_build()
    builds_resp = Mock()
    builds_resp.results = [build]
    builds_resp.metadata.next_paging_token = None
    sdk.list_builds.return_value = builds_resp

    get_build_resp = Mock()
    get_build_resp.result = build
    sdk.get_build.return_value = get_build_resp

    yaml_filepath = None

    def create_session(*a: Any, **kw: Any) -> None:
        nonlocal yaml_filepath
        yaml_filepath = kw["yaml_filepath"]
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._up_session.side_effect = create_session

    with pytest.raises(RuntimeError):
        builder.app_config("non-existent-app-config").connect()

    builder.app_config("test-app-config").connect()

    with open(cast(str, yaml_filepath)) as f:
        data = yaml.safe_load(f)

    assert data["docker"]["image"] == "localhost:5555/docker_image_name"
    for nodes_type, node_config in data["available_node_types"].items():
        assert (
            node_config["docker"]["worker_image"] == "localhost:5555/docker_image_name"
        )

    builder._up_session.assert_called_once_with(
        ANY,
        "session-0",
        "anyscale_default_cloud",
        scratch_dir,
        dangerously_set_build_id=build.id,
        yaml_filepath=ANY,
    )


def test_get_wheel_url() -> None:
    wheel_prefix = (
        "https://s3-us-west-2.amazonaws.com/ray-wheels/master/COMMIT_ID/ray-2.0.0.dev0"
    )
    assert (
        _get_wheel_url("master/COMMIT_ID", "36", "darwin")
        == f"{wheel_prefix}-cp36-cp36m-macosx_10_13_intel.whl"
    )
    assert (
        _get_wheel_url("master/COMMIT_ID", "37", "darwin")
        == f"{wheel_prefix}-cp37-cp37m-macosx_10_13_intel.whl"
    )
    assert (
        _get_wheel_url("master/COMMIT_ID", "38", "darwin")
        == f"{wheel_prefix}-cp38-cp38-macosx_10_13_x86_64.whl"
    )

    assert (
        _get_wheel_url("master/COMMIT_ID", "36", "linux")
        == f"{wheel_prefix}-cp36-cp36m-manylinux2014_x86_64.whl"
    )
    assert (
        _get_wheel_url("master/COMMIT_ID", "37", "linux")
        == f"{wheel_prefix}-cp37-cp37m-manylinux2014_x86_64.whl"
    )
    assert (
        _get_wheel_url("master/COMMIT_ID", "38", "linux")
        == f"{wheel_prefix}-cp38-cp38-manylinux2014_x86_64.whl"
    )

    assert (
        _get_wheel_url("master/COMMIT_ID", "36", "win32")
        == f"{wheel_prefix}-cp36-cp36m-win_amd64.whl"
    )
    assert (
        _get_wheel_url("master/COMMIT_ID", "37", "win32")
        == f"{wheel_prefix}-cp37-cp37m-win_amd64.whl"
    )
    assert (
        _get_wheel_url("master/COMMIT_ID", "38", "win32")
        == f"{wheel_prefix}-cp38-cp38-win_amd64.whl"
    )


def test_version_mismatch() -> None:
    sdk = Mock()
    connect_instance = SessionBuilder(anyscale_sdk=sdk)
    connect_instance_ignore = SessionBuilder(
        anyscale_sdk=sdk, _ignore_version_check=True
    )

    both_wrong = ["1.1.0", "fake_commit"]
    commit_is_wrong = [REQUIRED_RAY_VERSION, REQUIRED_RAY_COMMIT[2:]]
    version_is_wrong = ["1.0.0", REQUIRED_RAY_COMMIT]
    for attempt in [both_wrong, version_is_wrong, commit_is_wrong]:
        with pytest.raises(ValueError):
            connect_instance._check_required_ray_version(*attempt)
        connect_instance_ignore._check_required_ray_version(*attempt)

    both_correct = [REQUIRED_RAY_VERSION, REQUIRED_RAY_COMMIT]
    connect_instance_ignore._check_required_ray_version(*both_correct)
    connect_instance._check_required_ray_version(*both_correct)


@pytest.mark.skip(
    "This test is very, very long, and should only be run if connect.py::PINNED_IMAGES are updated"
)
def test_pinned_images() -> None:
    """
    This test should be run every time PINNED_IMAGES is changed in connect.py.
    This test ensures:
    - Python versions match.
    - Ray commits match.
    - CUDA is present for GPU images (determined by the presence of the file /usr/local/cuda)
    """
    for image, pinned_image in PINNED_IMAGES.items():
        cmd = "-c \"python --version; python -c 'import ray; print(ray.__commit__)'; ls -l 2>&1 /usr/local/cuda\""
        print(f"Checking: {image} with SHA: {pinned_image} ")
        output = subprocess.run(  # noqa: B1
            f"docker run --rm -it --entrypoint=/bin/bash {pinned_image} {cmd}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        py_version, ray_commit, cuda_info, _ = output.stdout.decode("UTF-8").split("\n")

        _, desired_py_version, desired_arch = image.split(":")[-1].split("-")
        assert (
            desired_py_version[-1] in py_version
        ), f"Wrong python version found in {pinned_image}!"

        if desired_arch == "gpu":
            assert ("ls: cannot access" not in cuda_info) and (
                "cuda-" in cuda_info
            ), f"CUDA install incorrect in {pinned_image}"
        else:
            assert (
                "ls: cannot access"
            ) in cuda_info, f"CUDA found in CPU image {pinned_image}"

        assert (
            ray_commit.strip() == REQUIRED_RAY_COMMIT
        ), f"Wrong ray commit installed in {pinned_image}"
