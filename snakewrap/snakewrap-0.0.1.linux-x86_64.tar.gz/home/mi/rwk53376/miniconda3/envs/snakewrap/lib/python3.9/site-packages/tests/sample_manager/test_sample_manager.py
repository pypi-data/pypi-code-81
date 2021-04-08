import pytest

from snakewrap.sample_manager import *


class TestDummyManager():

    def test_class_creation(self):
        smanager = DummySampleManager()

    def test_class_parse_samples(self):
        smanager = DummySampleManager()
        smanager.parse_samples(None)
        smanager.parse_samples([None])
        smanager.parse_samples("folder")

    def test_class_process_samples(self):
        smanager = DummySampleManager()
        smanager.parse_samples("folder")
        smanager.process_samples()
        assert smanager.samples_processed is True

    def test_write_to_file(self):
        smanager = DummySampleManager()
        smanager.parse_samples("folder")
        smanager.process_samples()
        smanager.write_to_file("some_file.yaml")

    def test_load_from_file(self):
        smanager = DummySampleManager()
        smanager.load_from_file("some_file.yaml")
