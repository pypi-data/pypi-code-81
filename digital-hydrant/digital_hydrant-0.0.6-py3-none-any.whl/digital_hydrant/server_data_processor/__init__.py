from digital_hydrant.config import config as conf, db_path
from digital_hydrant import logging
import sqlite3


class Processor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.table_name = "unique_ips"

        try:
            self.conn = sqlite3.connect(db_path)
            self.cursor = self.conn.cursor()
        except Exception as err:
            self.logger.critical(f"Failed to connect to the database: {err}")
            exit(1)

    def process_server_data(self, data):
        if data["ips"] and isinstance(data["ips"], list):
            self.process_ips(data["ips"])

    def process_ips(self, data):
        for ip in data:
            try:
                query = f"INSERT INTO {self.table_name}(ip) VALUES('{ip}')"
                self.cursor.execute(query)
            except sqlite3.Error as e:
                if not isinstance(e, sqlite3.IntegrityError):
                    self.logger.critical(f"Failed to insert IP({ip}) into table: {e}")
            finally:
                self.conn.commit()
