import os
import sqlite3
import unittest
from unittest.mock import patch

from digital_hydrant.server_data_processor import Processor
from digital_hydrant.config import db_path


class TestServerDataProcessor(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS unique_ips (id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT UNIQUE, last_tested TIMESTAMP, last_nmap_scan TIMESTAMP, open_ports TEXT)"
        )

        self.processor = Processor()

    def tearDown(self):
        self.cursor.execute("DELETE FROM unique_ips")
        self.conn.commit()

    def test_init(self):
        self.cursor.execute(
            """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='unique_ips' """
        )

        self.assertEqual(1, self.cursor.fetchone()[0])

    @patch("digital_hydrant.server_data_processor.Processor.process_ips")
    def test_process_data(self, mock):
        ips = [1, 2, 3, 4]
        self.processor.process_server_data({"ips": ips})

        mock.assert_called_once_with(ips)

    def test_process_ips(self):
        self.processor.process_ips([0, 1, 2, 3, 4, 3])

        self.cursor.execute("SELECT id, ip FROM unique_ips ORDER BY ip ASC")

        ips = self.cursor.fetchall()

        self.assertEqual(5, len(ips))

        for i in range(5):
            self.assertEqual(str(i), ips[i][1])

    def test_process_ips_duplicates(self):
        self.processor.process_ips([0, 1, 2, 3, 4, 3])

        self.cursor.execute("SELECT id, ip FROM unique_ips ORDER BY ip ASC")

        ips = self.cursor.fetchall()

        self.assertEqual(5, len(ips))

        for i in range(5):
            self.assertEqual(str(i), ips[i][1])

        self.processor.process_ips([3, 4, 5, 6])

        self.cursor.execute("SELECT id, ip FROM unique_ips ORDER BY ip ASC")

        ips = self.cursor.fetchall()

        self.assertEqual(7, len(ips))

        for i in range(7):
            self.assertEqual(str(i), ips[i][1])
