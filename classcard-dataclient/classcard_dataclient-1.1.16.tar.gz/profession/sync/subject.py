import time
from sync import BaseSync
from classcard_dataclient.models.subject import Subject
from utils.code import get_md5_hash
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class SubjectSync(BaseSync):
    def __init__(self, *args, **kwargs):
        super(SubjectSync, self).__init__(*args, **kwargs)
        self.subject_num_map = {}

    def sync(self):
        res = self.nice_requester.get_subject_list()
        res_data = res
        subject_list = []
        for rd in res_data:
            logger.info("subject: {}".format(rd))
            subject_num = get_md5_hash(rd['name'])
            self.subject_num_map[rd['id']] = subject_num
            subject = Subject(number=subject_num, name=rd['name'], school=self.school_id)
            subject_list.append(subject)
        self.client.create_subjects(self.school_id, subject_list)

