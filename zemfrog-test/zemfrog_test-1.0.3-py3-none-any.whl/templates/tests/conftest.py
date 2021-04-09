from zemfrog.app import create_app
from pytest import fixture

import os

pytest_plugins = "zemfrog_test"

@fixture(scope="session")
def app():
    os.environ["ZEMFROG_ENV"] = "testing"
    app = create_app("{{ import_name }}")
    return app
