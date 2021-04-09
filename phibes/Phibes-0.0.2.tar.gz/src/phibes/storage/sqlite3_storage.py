# flake8: noqa
# Built-in library packages
from __future__ import annotations
import base64
from datetime import datetime
from pathlib import Path
import shutil
from typing import List

# Third party packages

# In-project modules
from phibes.crypto import create_crypt, get_crypt
from phibes.lib import phibes_file
from phibes.lib.config import ConfigModel
from phibes.lib.errors import PhibesExistsError
from phibes.lib.errors import PhibesNotFoundError
from phibes.lib.errors import PhibesUnknownError
from phibes.model import FILE_EXT, Item
from phibes.lib.represent import ReprType, todict

# In-package modules
from .storage_impl import StorageImpl


# Sqlite3 connection
CONNECTION = None


class SqlStorage(StorageImpl):

    @classmethod
    def get(cls, name: str = None) -> dict:
        """
        Get a stored object from database
        @param name: The optional locker_id of the entity
        @return: SqlStorage instance
        """
        cur = CONNECTION.cursor()
        if not name:
            name = 'default'
        # fields = salt, crypt_id, timestamp, body
        statement = "SELECT * FROM lockers WHERE locker_id=?", (name,)
        cur.execute(statement)
        rows = cur.fetchall()
        # raise an exception if more than one is returned
        return dict(rows[0])


        # SQL needs to read get:
        # conf.db_path = DB file at configured path, or CWD set in env by CLI
        # - Locker:
        #   - locker_id = hashed locker locker_id
        #   - select by locker_id from LOCKER where locker_id is locker_id or "default"
        # - Item:
        #   - select by item_name, locker_name from ITEM
