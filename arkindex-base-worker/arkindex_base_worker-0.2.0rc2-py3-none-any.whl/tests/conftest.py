# -*- coding: utf-8 -*-
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from uuid import UUID

import pytest
import yaml
from peewee import SqliteDatabase

from arkindex.mock import MockApiClient
from arkindex_worker.cache import MODELS, CachedElement, CachedTranscription
from arkindex_worker.git import GitHelper, GitlabHelper
from arkindex_worker.worker import BaseWorker, ElementsWorker

FIXTURES_DIR = Path(__file__).resolve().parent / "data"

__yaml_cache = {}


@pytest.fixture(autouse=True)
def disable_sleep(monkeypatch):
    """
    Do not sleep at all in between API executions
    when errors occur in unit tests.
    This speeds up the test execution a lot
    """
    monkeypatch.setattr(time, "sleep", lambda x: None)


@pytest.fixture
def cache_yaml(monkeypatch):
    """
    Cache all calls to yaml.safe_load in order to speedup
    every test cases that load the OpenAPI schema
    """
    # Keep a reference towards the original function
    _original_yaml_load = yaml.safe_load

    def _cached_yaml_load(yaml_payload):
        # Create a unique cache key for direct YAML strings
        # and file descriptors
        if isinstance(yaml_payload, str):
            yaml_payload = yaml_payload.encode("utf-8")
        if isinstance(yaml_payload, bytes):
            key = hashlib.md5(yaml_payload).hexdigest()
        else:
            key = yaml_payload.name

        # Cache result
        if key not in __yaml_cache:
            __yaml_cache[key] = _original_yaml_load(yaml_payload)

        return __yaml_cache[key]

    monkeypatch.setattr(yaml, "safe_load", _cached_yaml_load)


@pytest.fixture(autouse=True)
def setup_api(responses, monkeypatch, cache_yaml):

    # Always use the environment variable first
    schema_url = os.environ.get("ARKINDEX_API_SCHEMA_URL")
    if schema_url is None:
        # Try to load a local schema as the current developer of base-worker
        # may also work on the backend nearby
        paths = [
            "~/dev/ark/backend/schema.yml",
            "~/dev/ark/backend/output/schema.yml",
        ]
        for path in paths:
            path = Path(path).expanduser().absolute()
            if path.exists():
                monkeypatch.setenv("ARKINDEX_API_SCHEMA_URL", str(path))
                schema_url = str(path)
                break

    # Fallback to prod environment
    if schema_url is None:
        schema_url = "https://arkindex.teklia.com/api/v1/openapi/?format=openapi-json"
        monkeypatch.setenv("ARKINDEX_API_SCHEMA_URL", schema_url)

    # Allow accessing remote API schemas
    responses.add_passthru(schema_url)

    # Force api requests on a dummy server with dummy credentials
    monkeypatch.setenv("ARKINDEX_API_URL", "http://testserver/api/v1")
    monkeypatch.setenv("ARKINDEX_API_TOKEN", "unittest1234")


@pytest.fixture(autouse=True)
def temp_working_directory(monkeypatch, tmp_path):
    def _getcwd():
        return str(tmp_path)

    monkeypatch.setattr(os, "getcwd", _getcwd)


@pytest.fixture(autouse=True)
def give_worker_version_id_env_variable(monkeypatch):
    monkeypatch.setenv("WORKER_VERSION_ID", "12341234-1234-1234-1234-123412341234")


@pytest.fixture
def mock_worker_version_api(responses, mock_user_api):
    """Provide a mock API response to get worker configuration"""
    payload = {
        "id": "12341234-1234-1234-1234-123412341234",
        "configuration": {
            "docker": {"image": "python:3"},
            "configuration": {"someKey": "someValue"},
            "secrets": [],
        },
        "revision": {
            "hash": "deadbeef1234",
            "name": "some git revision",
        },
        "docker_image": "python:3",
        "docker_image_name": "python:3",
        "state": "created",
        "worker": {
            "id": "deadbeef-1234-5678-1234-worker",
            "name": "Fake worker",
            "slug": "fake_worker",
            "type": "classifier",
        },
    }
    responses.add(
        responses.GET,
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        status=200,
        body=json.dumps(payload),
        content_type="application/json",
    )


@pytest.fixture
def mock_user_api(responses):
    """
    Provide a mock API response to retrieve user details
    Workers Activity is disabled in this mock
    """
    payload = {
        "id": 1,
        "email": "bot@teklia.com",
        "display_name": "Bender",
        "features": {
            "workers_activity": False,
            "signup": False,
        },
    }
    responses.add(
        responses.GET,
        "http://testserver/api/v1/user/",
        status=200,
        body=json.dumps(payload),
        content_type="application/json",
    )


@pytest.fixture
def mock_elements_worker(monkeypatch, mock_worker_version_api):
    """Build and configure an ElementsWorker with fixed CLI parameters to avoid issues with pytest"""
    monkeypatch.setattr(sys, "argv", ["worker"])
    monkeypatch.setenv("ARKINDEX_CORPUS_ID", "11111111-1111-1111-1111-111111111111")

    worker = ElementsWorker()
    worker.configure()
    return worker


@pytest.fixture
def mock_base_worker_with_cache(mocker, monkeypatch, mock_worker_version_api):
    """Build a BaseWorker using SQLite cache, also mocking a PONOS_TASK"""
    monkeypatch.setattr(sys, "argv", ["worker"])

    worker = BaseWorker(use_cache=True)
    monkeypatch.setenv("PONOS_TASK", "my_task")
    return worker


@pytest.fixture
def mock_elements_worker_with_cache(monkeypatch, mock_worker_version_api):
    """Build and configure an ElementsWorker using SQLite cache with fixed CLI parameters to avoid issues with pytest"""
    monkeypatch.setattr(sys, "argv", ["worker"])
    monkeypatch.setenv("ARKINDEX_CORPUS_ID", "11111111-1111-1111-1111-111111111111")

    worker = ElementsWorker(use_cache=True)
    worker.configure()
    return worker


@pytest.fixture
def fake_page_element():
    with open(FIXTURES_DIR / "page_element.json", "r") as f:
        return json.load(f)


@pytest.fixture
def fake_ufcn_worker_version():
    with open(FIXTURES_DIR / "ufcn_line_historical_worker_version.json", "r") as f:
        return json.load(f)


@pytest.fixture
def fake_transcriptions_small():
    with open(FIXTURES_DIR / "line_transcriptions_small.json", "r") as f:
        return json.load(f)


@pytest.fixture
def fake_dummy_worker():
    api_client = MockApiClient()
    worker = ElementsWorker()
    worker.api_client = api_client
    return worker


@pytest.fixture
def fake_git_helper(mocker):
    gitlab_helper = mocker.MagicMock()
    return GitHelper(
        "repo_url",
        "/tmp/git_test/foo/",
        "/tmp/test/path/",
        "tmp_workflow_id",
        gitlab_helper,
    )


@pytest.fixture
def fake_gitlab_helper_factory():
    # have to set up the responses, before creating the client
    def run():
        return GitlabHelper(
            "balsac_exporter/balsac-exported-xmls-testing",
            "https://gitlab.com",
            "<GITLAB_TOKEN>",
            "gitlab_branch",
        )

    return run


@pytest.fixture
def mock_cached_elements():
    """Insert few elements in local cache"""
    CachedElement.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        parent_id="12341234-1234-1234-1234-123412341234",
        type="something",
        polygon="[[1, 1], [2, 2], [2, 1], [1, 2]]",
        worker_version_id=UUID("56785678-5678-5678-5678-567856785678"),
    )
    CachedElement.create(
        id=UUID("22222222-2222-2222-2222-222222222222"),
        parent_id=UUID("12341234-1234-1234-1234-123412341234"),
        type="page",
        polygon="[[1, 1], [2, 2], [2, 1], [1, 2]]",
        worker_version_id=UUID("56785678-5678-5678-5678-567856785678"),
    )
    assert CachedElement.select().count() == 2


@pytest.fixture
def mock_cached_transcriptions():
    """Insert few transcriptions in local cache, on a shared element"""
    CachedElement.create(
        id=UUID("12341234-1234-1234-1234-123412341234"),
        type="page",
        polygon="[[1, 1], [2, 2], [2, 1], [1, 2]]",
        worker_version_id=UUID("56785678-5678-5678-5678-567856785678"),
    )
    CachedTranscription.create(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        element_id=UUID("12341234-1234-1234-1234-123412341234"),
        text="Hello!",
        confidence=0.42,
        worker_version_id=UUID("56785678-5678-5678-5678-567856785678"),
    )
    CachedTranscription.create(
        id=UUID("22222222-2222-2222-2222-222222222222"),
        element_id=UUID("12341234-1234-1234-1234-123412341234"),
        text="How are you?",
        confidence=0.42,
        worker_version_id=UUID("90129012-9012-9012-9012-901290129012"),
    )


@pytest.fixture(scope="function")
def mock_databases(tmpdir):
    """
    Initialize several temporary databases
    to help testing the merge algorithm
    """
    out = {}
    for name in ("target", "first", "second", "conflict", "chunk_42"):
        # Build a local database in sub directory
        # for each name required
        filename = "db_42.sqlite" if name == "chunk_42" else "db.sqlite"
        path = tmpdir / name / filename
        (tmpdir / name).mkdir()
        local_db = SqliteDatabase(path)
        with local_db.bind_ctx(MODELS):
            # Create tables on the current local database
            # by binding temporarily the models on that database
            local_db.create_tables(MODELS)
        out[name] = {"path": path, "db": local_db}

    # Add an element in first parent database
    with out["first"]["db"].bind_ctx(MODELS):
        CachedElement.create(
            id=UUID("12341234-1234-1234-1234-123412341234"),
            type="page",
            polygon="[[1, 1], [2, 2], [2, 1], [1, 2]]",
            worker_version_id=UUID("56785678-5678-5678-5678-567856785678"),
        )
        CachedElement.create(
            id=UUID("56785678-5678-5678-5678-567856785678"),
            type="page",
            polygon="[[1, 1], [2, 2], [2, 1], [1, 2]]",
            worker_version_id=UUID("56785678-5678-5678-5678-567856785678"),
        )

    # Add another element with a transcription in second parent database
    with out["second"]["db"].bind_ctx(MODELS):
        CachedElement.create(
            id=UUID("42424242-4242-4242-4242-424242424242"),
            type="page",
            polygon="[[1, 1], [2, 2], [2, 1], [1, 2]]",
            worker_version_id=UUID("56785678-5678-5678-5678-567856785678"),
        )
        CachedTranscription.create(
            id=UUID("11111111-1111-1111-1111-111111111111"),
            element_id=UUID("42424242-4242-4242-4242-424242424242"),
            text="Hello!",
            confidence=0.42,
            worker_version_id=UUID("56785678-5678-5678-5678-567856785678"),
        )

    # Add a conflicting element
    with out["conflict"]["db"].bind_ctx(MODELS):
        CachedElement.create(
            id=UUID("42424242-4242-4242-4242-424242424242"),
            type="page",
            polygon="[[1, 1], [2, 2], [2, 1], [1, 2]]",
            initial=True,
        )
        CachedTranscription.create(
            id=UUID("22222222-2222-2222-2222-222222222222"),
            element_id=UUID("42424242-4242-4242-4242-424242424242"),
            text="Hello again neighbor !",
            confidence=0.42,
            worker_version_id=UUID("56785678-5678-5678-5678-567856785678"),
        )

    # Add an element in chunk parent database
    with out["chunk_42"]["db"].bind_ctx(MODELS):
        CachedElement.create(
            id=UUID("42424242-4242-4242-4242-424242424242"),
            type="page",
            polygon="[[1, 1], [2, 2], [2, 1], [1, 2]]",
            initial=True,
        )

    return out
