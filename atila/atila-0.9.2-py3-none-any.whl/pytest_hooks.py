import pytest
from rs4.webkit import apidoc

def pytest_addoption (parser):
    parser.addoption (
        "--run-slow", action="store_true", default=False, help="run inckuding slow marked tests"
    )
    parser.addoption (
        "--generate-doc", action='store', default=None, dest="output_path", help="generate API document into file"
    )

def pytest_collection_modifyitems (config, items):
    if config.getoption ("--run-slow"):
        return
    skip_slow = pytest.mark.skip (reason = "need --run-slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker (skip_slow)

def pytest_sessionstart (session):
    if session.config.getoption ("--generate-doc"):
        apidoc.truncate_log_dir ()

def pytest_sessionfinish (session, exitstatus):
    apidoc_output = session.config.getoption ("--generate-doc")
    if apidoc_output and exitstatus == 0:
        apidoc.build_doc (apidoc_output)
