import datetime
import uuid
from sync import BaseSync2
from classcard_dataclient.client.backbone import BackboneV2
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class ClearSyncV2(BaseSync2):
    def __init__(self, *args, **kwargs):
        super(ClearSyncV2, self).__init__(*args, **kwargs)

    def sync(self):
        backbone = BackboneV2(self.school_id)
        backbone.delete_other_semester([])
