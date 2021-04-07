# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

import os
import sqlite3
import unittest

from digital_hydrant.collector_queue import CollectorQueue
from digital_hydrant.config import db_path


class TestCollectorQueue(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS collectors (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, payload TEXT, timestamp TIMESTAMP, uploaded INTEGER DEFAULT 0)"
        )

        self.queue = CollectorQueue()

    def tearDown(self):
        self.cursor.execute("DELETE FROM collectors")
        self.conn.commit()

    def test_put(self):
        timestamp = 123456
        self.queue.put("my type", {"a": "payload"}, timestamp)

        self.cursor.execute(
            "SELECT id, type, payload, timestamp, uploaded FROM collectors"
        )

        (id, type, payload, timestamp, uploaded) = self.cursor.fetchone()

        self.assertEqual(type, "my type")
        self.assertEqual(payload, '{"a": "payload"}')
        self.assertEqual(timestamp, 123456)
        self.assertEqual(uploaded, 0)

    def test_peak(self):
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("another type", "{another: payload}", 654321)'
        )
        self.conn.commit()

        (id, type, payload, timestamp) = self.queue.peak()

        self.assertEqual(type, "another type")
        self.assertEqual(payload, "{another: payload}")
        self.assertEqual(timestamp, 654321)

    def test_remove(self):
        first_id = self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("first type", "{first: payload}", 654321)'
        ).lastrowid
        last_id = self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("another type", "{another: payload}", 654321)'
        ).lastrowid
        self.conn.commit()

        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 2)

        self.queue.remove(first_id)

        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 1)

        (id, uploaded) = self.cursor.execute(
            "SELECT id, uploaded FROM collectors"
        ).fetchone()

        self.assertEqual(uploaded, 0)
        self.queue.remove(last_id, delete=False)
        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 1)

        (id, uploaded) = self.cursor.execute(
            "SELECT id, uploaded FROM collectors"
        ).fetchone()
        self.assertEqual(last_id, id)
        self.assertEqual(uploaded, 1)

    def test_remove_all(self):
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("first type", "{first: payload}", 654321)'
        )
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("another type", "{another: payload}", 654321)'
        )
        self.conn.commit()

        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 2)
        self.queue.remove_all()
        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 0)

    def test_remove_all_no_delete(self):
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("first type", "{first: payload}", 654321)'
        )
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("another type", "{another: payload}", 654321)'
        )
        self.conn.commit()

        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 2)
        self.queue.remove_all(delete=False)
        (count,) = self.cursor.execute("SELECT COUNT(*) FROM collectors").fetchone()
        self.assertEqual(count, 2)

        data = self.cursor.execute("SELECT id, uploaded FROM collectors").fetchall()
        self.assertEqual(data[0][1], 1)
        self.assertEqual(data[1][1], 1)

    def test_fail(self):
        self.cursor.execute(
            'INSERT INTO collectors(type, payload, timestamp) VALUES \
                       ("another type", "{another: payload}", 654321)'
        )
        self.conn.commit()

        id = self.cursor.lastrowid

        self.queue.fail(id)

        (id, uploaded) = self.cursor.execute(
            f"SELECT id, uploaded FROM collectors WHERE id={id}"
        ).fetchone()

        self.assertEqual(uploaded, 2)
