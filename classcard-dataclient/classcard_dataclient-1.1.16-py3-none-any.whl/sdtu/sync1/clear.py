import os
from sync1.base import BaseSync
from classcard_dataclient.utils.data_req import edtech_server_url, edtech_server_token
from classcard_dataclient.utils.requestutils import do_delete_request
from classcard_dataclient.client.backbone import Backbone
from classcard_dataclient.requester.nirvana import NirvanaRequester
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class ClearSync(BaseSync):
    def __init__(self):
        super(ClearSync, self).__init__()
        class_card_server_url = os.getenv("CLASS_CARD_SERVER_URL", "http://127.0.0.1:9000")
        self.current_classroom_num = []
        self.current_student_num = []
        self.current_teacher_num = []
        self.current_section_num = []
        self.nirvana_requester = NirvanaRequester(server=class_card_server_url, school_id=self.school_id)

    def delete_classroom_req(self, uid):
        class_card_server_url = os.getenv("CLASS_CARD_SERVER_URL", "http://127.0.0.1:9000")
        class_card_server_token = os.getenv("CLASS_CARD_SERVER_TOKEN", "http://127.0.0.1:9000")
        headers = {"X-Custom-Header-3School": self.school_id,
                   "X-Custom-Header-3App": "classcard",
                   "Authorization": class_card_server_token}
        url = "{}/api/classroom/{}/".format(class_card_server_url, uid)
        resp = do_delete_request(url=url, headers=headers)
        code = resp.code
        data = resp.data.get('data', {}) if not code else resp.msg
        if code:
            logger.error("Error: Request: {}, Detail: {}".format(url, data))
        return code, data

    def delete_teacher_req(self, teacher_id, school_id):
        """ delete teacher from edtech user server"""
        url = "{}/api/v1/schools/{}/teachers/{}/".format(edtech_server_url(), school_id, teacher_id)
        resp = do_delete_request(url=url, token=edtech_server_token())
        code = resp.code
        data = resp.data.get('data', {}) if not code else resp.msg
        if code:
            logger.error("Error: Request: {}, Detail: {}".format(url, data))
        return code, data

    def delete_student_req(self, student_id, school_id):
        """ delete student from edtech user server"""
        url = "{}/api/v1/schools/{}/students/{}/".format(edtech_server_url(), school_id, student_id)
        resp = do_delete_request(url=url, token=edtech_server_token())
        code = resp.code
        data = resp.data.get('data', {}) if not code else resp.msg
        if code:
            logger.error("Error: Request: {}, Detail: {}".format(url, data))
        return code, data

    def delete_section_req(self, section_id, school_id):
        """ delete section from edtech user server"""
        url = "{}/api/v1/schools/{}/sections/{}/".format(edtech_server_url(), school_id, section_id)
        resp = do_delete_request(url=url, token=edtech_server_token())
        code = resp.code
        data = resp.data.get('data', {}) if not code else resp.msg
        if code:
            logger.error("Error: Request: {}, Detail: {}".format(url, data))
        return code, data

    def clear_classroom(self):
        if not self.current_classroom_num:
            return
        result = self.client.get_classroom_num_map(self.school_id)
        for number, uid in result.items():
            if number not in self.current_classroom_num:
                delete_code, delete_data = self.delete_classroom_req(uid)
                print(delete_code, delete_data)

    def clear_student(self):
        if not self.current_student_num:
            return
        result = self.client.get_student_number_map(self.school_id)
        for number, uid in result.items():
            if number not in self.current_student_num:
                delete_code, delete_data = self.delete_student_req(uid, self.school_id)
                print(delete_code, delete_data)

    def clear_teacher(self):
        if not self.current_teacher_num:
            return
        result = self.client.get_teacher_number_map(self.school_id)
        for number, uid in result.items():
            if number not in self.current_teacher_num:
                delete_code, delete_data = self.delete_teacher_req(uid, self.school_id)
                print(delete_code, delete_data)

    def clear_section(self):
        if not self.current_section_num:
            return
        backbone = Backbone(self.school_id)
        result = backbone.wrap_class_map(origin="edtech")
        for number, uid in result.items():
            if number not in self.current_section_num:
                delete_code, delete_data = self.delete_section_req(uid, self.school_id)
                print(delete_code, delete_data)

    def sync(self):
        self.clear_classroom()
        self.clear_section()
        self.clear_teacher()
        self.clear_teacher()
