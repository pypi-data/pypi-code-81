from pathlib import Path
import zipfile
import tempfile
import pytest

test_dir = Path(__file__).resolve()
SQLITE = test_dir.parent / "sqlite_fixture.zip"


@pytest.fixture(scope="session")
def model_sqlite():
    tmp_path = tempfile.mkdtemp()
    with zipfile.ZipFile(SQLITE, 'r') as zip_ref:
        zip_ref.extractall(tmp_path)
    yield Path(tmp_path) / "tests" / "v2_bergermeer_download.sqlite"
