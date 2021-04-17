"""Module defining constants used in the project."""

# Standard library:
from pathlib import Path

DOT_ENV_FILE_PATH = Path(__file__).resolve().parents[1] / ".env"
"""Expected path to the location of an environment variable definition file."""


PROJECT_DIR: Path = Path(__file__).resolve().parents[1]
"""Absolute path to the root directory for the project."""


PROJECT_NAME: str = PROJECT_DIR.name
"""Name of the project."""


FRONTEND_DIR: Path = PROJECT_DIR / f"ui/dist/{PROJECT_NAME.replace('_', '-')}"
"""Absolute path to the Angular web application."""


DATA_DIR: Path = PROJECT_DIR / "data"
"""Absolute path to the data directory for the project."""


DATABASE_PATH: Path = DATA_DIR / f"{PROJECT_NAME}.db"
"""Absolute path to a SQLite database for the project."""


LOG_DIR: Path = PROJECT_DIR / "log"
"""Absolute path to the log directory for the project."""


PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
"""Absolute path to the directory for processed data of the project."""


RAW_DATA_DIR: Path = DATA_DIR / "raw"
"""Absolute path to the directory for raw data of the project."""


TMP_DATA_DIR: Path = DATA_DIR / "tmp"
"""Absolute path to the directory for temporary data of the project."""
