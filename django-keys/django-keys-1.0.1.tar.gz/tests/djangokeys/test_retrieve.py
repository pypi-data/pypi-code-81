#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Contains unit tests for functionality related to retrieving keys.

import os
import pytest
import unittest

from tempfile import TemporaryDirectory
from unittest.mock import patch

from djangokeys.retrieve import retrieve_key_from_file
from djangokeys.settings import DJANGO_DEFAULT_KEY_LENGTH
from djangokeys.settings import DJANGO_DEFAULT_SYMBOLS
from djangokeys.exceptions import KeyNotFound
from djangokeys.exceptions import KeyNotGenerated
from djangokeys.exceptions import CouldNotAccessKey


class RetrieveKeyFromFileTests(unittest.TestCase):
    """ Contains tests for retrieve_key_from_file() function.
    """

    def setUp(self):
        """ Sets up clean test fixture.
        """
        # generate temporary directory
        self._temp_dir = TemporaryDirectory()
        # path of existing secret
        self.OLD_SECRET = "OLD_SECRET"
        self.OLD_SECRET_PATH = os.path.join(self._temp_dir.name, "old.key")
        with open(self.OLD_SECRET_PATH, "w") as f:
            f.write(self.OLD_SECRET)
        # path of new secret
        self.NEW_SECRET_PATH = os.path.join(self._temp_dir.name, "new.key")

    def tearDown(self):
        """ Cleans up test fixture.
        """
        self._temp_dir.cleanup()

    def test__strict__exists__accessible(self):
        """ Test that we can successfully retrieve a key in strict mode from
            an accessible file.
        """
        key = retrieve_key_from_file(self.OLD_SECRET_PATH, strict=True)
        assert key == self.OLD_SECRET

    def test__strict__exists__inaccessible(self):
        """ Test that exception is raised when trying to retrieve a key in
            strict mode from an inaccessible file.
        """
        with patch("djangokeys.retrieve._read_from_file") as mock:
            mock.side_effect = IOError("could not read")
            with pytest.raises(CouldNotAccessKey):
                retrieve_key_from_file(self.OLD_SECRET_PATH, strict=True)

    def test__strict__does_not_exist(self):
        """ Test that exception is raised when trying to retrieve a key in
            strict mode from a file that does not exist.
        """
        with pytest.raises(KeyNotFound):
            retrieve_key_from_file(self.NEW_SECRET_PATH, strict=True)

    def test__lax__exists__accessible(self):
        """ Test that we can successfully retrieve key from file in lax mode.
        """
        key = retrieve_key_from_file(self.OLD_SECRET_PATH, strict=False)
        assert key == self.OLD_SECRET

    def test__lax__exists__inaccessible(self):
        """ Test that exception is raised when key cannot be read from file.
        """
        with patch("djangokeys.retrieve._read_from_file") as mock:
            mock.side_effect = IOError("could not read")
            with pytest.raises(CouldNotAccessKey):
                retrieve_key_from_file(self.OLD_SECRET_PATH, strict=False)

    def test_lax__does_not_exist__accessible__file_created(self):
        """ Test that file is created with newly generated key in lax mode.
        """
        _ = retrieve_key_from_file(self.NEW_SECRET_PATH, strict=False)
        assert os.path.isfile(self.NEW_SECRET_PATH)

    def test_lax__does_not_exist__accessible__key_created(self):
        """ Test that new key is generated in lax mode if file did not exist yet.
        """
        key = retrieve_key_from_file(self.NEW_SECRET_PATH, strict=False)
        assert isinstance(key, str)
        assert len(key) == DJANGO_DEFAULT_KEY_LENGTH
        assert all([ch in DJANGO_DEFAULT_SYMBOLS for ch in key])

    def test_lax__does_not_exist__inaccessible__cannot_write(self):
        """ Test that exception is raised when key cannot be written to file.
        """
        with patch("djangokeys.retrieve._write_to_file") as mock:
            mock.side_effect = IOError("could not write")
            with pytest.raises(KeyNotGenerated):
                retrieve_key_from_file(self.NEW_SECRET_PATH, strict=False)

    def test_lax__does_not_exist__inaccessible__cannot_read(self):
        """ Test that exception is raised when newly generated key cannot be
            read back from file.
        """
        with patch("djangokeys.retrieve._read_from_file") as mock:
            mock.side_effect = IOError("could not read")
            with pytest.raises(CouldNotAccessKey):
                retrieve_key_from_file(self.NEW_SECRET_PATH, strict=False)
