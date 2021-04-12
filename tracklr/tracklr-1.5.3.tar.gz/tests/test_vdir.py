from os.path import expanduser
import unittest

from tracklr.vdir import Vdir


class TestVdir(unittest.TestCase):
    def test_vdir(self):

        vdir = Vdir(expanduser("tests/vdir_storage"))

        vdir_list = vdir.list()

        events = []

        for event in vdir_list:
            events.append(event)
            self.assertEqual(event, "3e6c9ccb-a33f-4224-98d6-018704b761e1.ics")

        self.assertEqual(len(events), 1)

        event_data = vdir.get(event)
        self.assertIn("@Tracklr +test #Vdir storage", event_data)

    def test_vdir_does_not_exist(self):

        with self.assertRaises(IOError):
            vdir = Vdir("")
