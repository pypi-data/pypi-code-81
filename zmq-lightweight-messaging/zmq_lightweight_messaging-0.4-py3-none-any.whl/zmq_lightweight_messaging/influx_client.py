from influxdb import InfluxDBClient
import os

class InfluxClient:
    def __init__(self, db):
        host = os.environ["INFLUX_HOST"]
        port = os.environ["INFLUX_PORT"]
        self.client = InfluxDBClient(host=host, port=port)
        self.db = db
    
    def db_exists(self):
        db_list = self.client.get_list_database()

        for db in db_list:
            if db["name"] == self.db:
                return True
            
        return False

    def init_db(self):
        if not self.db_exists():
            self.client.create_database(self.db)

        self.client.switch_database(self.db)

    def insert(self, body):
        self.client.write_points(body)

    