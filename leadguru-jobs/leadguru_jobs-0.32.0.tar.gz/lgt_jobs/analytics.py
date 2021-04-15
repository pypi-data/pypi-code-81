from abc import ABC
import datetime
from typing import Optional

from pydantic import BaseModel, conlist
from pymongo import MongoClient
from lgt.common.python.lgt_logging import log

from . import BaseBackgroundJobData, BaseBackgroundJob
from .env import mongo_connection_string

"""
Track analytics
"""
class TrackAnalyticsJobData(BaseBackgroundJobData, BaseModel):
    data: str
    name: str
    event: str
    attributes: conlist(Optional[str], min_items = 1)
    created_at: datetime.datetime

class TrackAnalyticsJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return TrackAnalyticsJobData

    def exec(self, data: TrackAnalyticsJobData):
        with MongoClient(mongo_connection_string) as client:
            db = client.lgt_analytics
            type = data.event
            if type == 'message-received':
                collection_name = 'received_messages'
            elif type == 'message-filtered-in':
                collection_name = 'filtered_messages'
            else:
                collection_name = type

            analytics_id = db[collection_name].insert_one(data.dict()).inserted_id
            log.info(f'entry with id {analytics_id} has been recorded into {collection_name}')