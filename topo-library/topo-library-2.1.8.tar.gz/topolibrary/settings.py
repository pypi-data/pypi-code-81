from __future__ import absolute_import, unicode_literals
import os


from mongoengine import connect
from mongoengine.connection import disconnect
from celery import Celery
import motor.motor_asyncio
import redis


class MongoSettings():
    ''' mongop settings '''
    def __init__(self, db_name=None, host=None, port=None):
        self.mongo_user = os.environ.get("MONGO_USER")
        self.mongo_pass = os.environ.get("MONGO_PASS")
        self.mongo_port = port if port is not None else os.environ.get("MONGO_PORT", 27017)
        self.mongo_host = host if host is not None else os.environ.get("MONGO_HOST", "host.docker.internal")
        self.mongo_db = db_name if db_name is not None else os.environ.get("MONGO_DB", "topograph")
        self.host = f"mongodb://{self.mongo_host}:{self.mongo_port}"
        self.client = connect(self.mongo_db, host=self.host, port=self.mongo_port, alias='default', connect=False)

    def connect(self):
        return self.client

    def save(self, document):
        document.save()

    def close(self):
        disconnect()


class CelerySettings():
    ''' celery settings '''
    def __init__(self, broker_url=None, proj_name=None):
        self.celery_broker = broker_url if broker_url is not None else os.environ.get("REDIS_URL", "redis://redis:6379/1")
        # self.temp_folder = temp_celery_folder if temp_celery_folder is not None else os.environ.get("TEMP_CELERY_FOLDER", "/tmp/celery-linter")
        self.proj_name = proj_name if proj_name is not None else os.environ.get("CELERY_PROJECT_NAME", "topo_celery_proj")
        self.app = Celery(self.proj_name, broker=self.celery_broker, backend=self.celery_broker)

    def get_app(self):
        return self.app

    # def get_temp_folder(self):
        # return self.temp_folder

    def add_autodiscover(self, task_name):
        self.app.autodiscover_tasks([
            task_name
        ], force=True)


class MotorClient:
    ''' motor client '''
    client = None
    db = None

    def __new__(cls, host=None, port=None, db_name=None):
        port = port if port else os.environ.get("MONGO_PORT", 27017)
        host = (
            host if host else os.environ.get("MONGO_HOST", "host.docker.internal")
        )
        db_name = (
            db_name if db_name else os.environ.get("MONGO_DB", "topograph")
        )

        client = motor.motor_asyncio.AsyncIOMotorClient(
            host=host,
            port=port,
            uuidRepresentation="standard"
        )

        db = client[db_name]

        return db


class RedisClient:
    client = None

    def __new__(cls, host=None, port=None):
        port = port if port else os.environ.get("REDIS_PORT", 6379)
        host = (
            host if host else os.environ.get("REDIS_HOST", "host.docker.internal")
        )

        client = redis.Redis(host=host, port=port)

        return client
