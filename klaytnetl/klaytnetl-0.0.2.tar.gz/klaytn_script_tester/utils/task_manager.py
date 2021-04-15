# %%
import pymongo
from pymongo import ReplaceOne
from bson.codec_options import CodecOptions

from datetime import datetime, timezone, timedelta
from typing import List, Any, Union, Iterator, Dict
from copy import deepcopy
from utils.commons import timestamp_chunk

# %%
TaskIDs = {
    "BLOCKS_AND_TRANSACTIONS": "klaytn_raw_blocks_and_transactions",
    "RECEIPTS_AND_LOGS": "klaytn_raw_receipts_and_logs",
    "CONTRACTS": "klaytn_raw_contracts",
    "TOKENS": "klaytn_raw_tokens",
    "TOKEN_TRANSFERS": "klaytn_raw_token_transfers",
    "TRACES": "klaytn_raw_traces",
    "ALL": "klaytn_all"
}

# %%
class TaskManager:
    ALLOWED_STAGES = ["raw", "enrich"]

    _connection_uri:str = None
    _client:pymongo.MongoClient = None
    _db:pymongo.database.Database = None
    _min_timestamp:datetime = None
    _max_timestamp:datetime = None

    def __init__(self, mongodb_connection_uri:str, min_timestamp:datetime, max_timestamp:datetime=None):

        if mongodb_connection_uri is not None:
            self._connection_uri = mongodb_connection_uri
            self._client = pymongo.MongoClient(
                self._connection_uri
            )
            self._db = self._client["klaytn_etl"]

        self._min_timestamp = min_timestamp
        if max_timestamp is not None:
            self._max_timestamp = max_timestamp
        else:
            self._max_timestamp = datetime.now(tz=timezone.utc) - timedelta(minutes=3)

    def get_client(self):
        return self._client

    def get_db(self):
        return self._db

    def initialize_db(self, task_id, stage):
        options = CodecOptions(tz_aware=True)
        get_last_tasks = list(self._db.get_collection(f"tasks_{stage}", codec_options=options).find({
            "task_id": task_id,
        }, {
            "_id": 0,
            "end_timestamp": 1
        }).sort([('start_timestamp', -1)]).limit(1))

        if (len(get_last_tasks) > 0):
            _min_timestamp = get_last_tasks[0]["end_timestamp"]
        else:
            _min_timestamp = self._min_timestamp

        job_ranges = timestamp_chunk(
            start_timestamp=max(self._min_timestamp, _min_timestamp),
            end_timestamp=self._max_timestamp,
            interval=timedelta(hours=1))

        tasks = ({
            "_id": f"""{task_id}_{int(start_timestamp.timestamp())}_{int(end_timestamp.timestamp())}""",
            "task_id": task_id,
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
        } for start_timestamp, end_timestamp in job_ranges)

        upserts=[ReplaceOne({'_id':x['_id']}, x, upsert=True) for x in tasks]

        if len(upserts) > 0:
            options = CodecOptions(tz_aware=True)
            self._db.get_collection(f"tasks_{stage}", codec_options=options).bulk_write(upserts)


    def get_todos(self, task_id:str, stage:str, limit:int=48):
        options = CodecOptions(tz_aware=True)
        return list(self._db.get_collection(f"tasks_{stage}", codec_options=options).find({
            "task_id": task_id,
            "finished_at": { "$exists": False }
        }, {
            "_id": 0,
            "start_timestamp": 1,
            "end_timestamp": 1
        }).sort([('start_timestamp', -1)]).limit(limit))


    def task_finished(self,
                      task_id:str,
                      stage:str,
                      start_timestamp:datetime,
                      end_timestamp:datetime):
        options = CodecOptions(tz_aware=True)
        self._db.get_collection(f"tasks_{stage}", codec_options=options).find_one_and_update({
                "_id": f"""{task_id}_{int(start_timestamp.timestamp())}_{int(end_timestamp.timestamp())}"""
            }, {
                "$set": {
                    "finished_at": datetime.now(tz=timezone.utc)
                }
            })

    def task_started(self,
                      task_id:str,
                      stage:str,
                      start_timestamp:datetime,
                      end_timestamp:datetime):

        options = CodecOptions(tz_aware=True)
        self._db.get_collection(f"tasks_{stage}", codec_options=options).find_one_and_replace({
                "_id": f"""{task_id}_{int(start_timestamp.timestamp())}_{int(end_timestamp.timestamp())}""",
            }, {
                "_id": f"""{task_id}_{int(start_timestamp.timestamp())}_{int(end_timestamp.timestamp())}""",
                "task_id": task_id,
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "started_at": datetime.now(tz=timezone.utc)
            }, upsert=True)

    def get_latest_job_result(self, task_id:str):
        # TODO: get from MongoDB
        return {
            "task_id": task_id,
            "start_timestamp": datetime(2021, 3, 1, 23, 0, 0, tzinfo=timezone.utc),
            "end_timestamp": datetime(2021, 3, 2, 0, 0, 0, tzinfo=timezone.utc),
            "started_at": datetime(2021, 3, 2, 0, 3, 0, tzinfo=timezone.utc),
            "finished_at": datetime(2021, 3, 2, 0, 5, 32, tzinfo=timezone.utc)
        }


    def set_latest_job_result(
            self,
            task_id:str,
            start_timestamp:datetime,
            end_timestamp:datetime,
            started_at:Union[None, datetime]=None,
            finished_at:Union[None, datetime]=None):

        # TODO: set to MongoDB
        if started_at is not None and isinstance(started_at, datetime):
            print({
                "_id": f"""{task_id}_{int(start_timestamp)}_{int(end_timestamp)}""",
                "task_id": task_id,
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "started_at": datetime.now(tz=timezone.utc)
            })
        elif started_at is not None and isinstance(started_at, datetime):
            print({
                "_id": f"""{task_id}_{int(start_timestamp)}_{int(end_timestamp)}""",
                "task_id": task_id,
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "finished_at": finished_at.replace(tz=timezone.utc)
            })
        else:
            print({})
