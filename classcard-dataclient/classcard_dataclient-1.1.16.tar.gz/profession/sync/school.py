import uuid
from copy import deepcopy
from sync import BaseSync
from classcard_dataclient.models.school import School
from utils.loggerutils import logging
from classcard_dataclient.utils.data_req import edtech_server_url, do_get_request, edtech_server_token, \
    update_school_req
from config import SCHOOL_NAME

logger = logging.getLogger(__name__)


class SchoolSync(BaseSync):
    def __init__(self, *args, **kwargs):
        super(SchoolSync, self).__init__(*args, **kwargs)
        self.school_map = {}
        self.special_number = kwargs.get('special_number', None)

    def get_code_map(self):
        url = "{}/api/v1/schools/".format(edtech_server_url())
        resp = do_get_request(url=url, token=edtech_server_token())
        data = resp.data.get('data', [])
        code_map = {}
        for item in data:
            code_map[item["code"]] = item
        return code_map

    def map_name(self, code):
        code_name = {"1153": "北京市第一六六中学(QA)",
                     "1165": "北京市第二中学(QA)",
                     "1481": "深圳市福田区外国语高级中学(QA)",
                     "3400": "好专业大数据（QA）",
                     "3532": "班牌对接测试"}
        return code_name[code]

    def sync(self):
        res = self.nice_requester.get_school_list()
        res_data = res.get('schools', [])
        logger.info(res_data)
        for index, rd in enumerate(res_data):
            # school_res = self.nice_requester.get_school_info(rd['schoolID'])
            # school_info = school_res['schoolInfo']
            name, number = rd['schoolName'], rd['schoolID']
            # name = self.map_name(number)
            if self.special_number and number != self.special_number:
                continue
            phone_number = "123456{}".format(number)
            email_number = "{}@edt.com".format(str(uuid.uuid4())[:7])
            school = School(name=name, number=number, description=name, phone=phone_number,
                            province="甘肃省", area='市辖区', city="兰州市", address=name, motto=name,
                            principal_name="兰州电教馆", principal_email=email_number, principal_phone=phone_number)
            logger.info(">>> Already add {}/{} school".format(index + 1, len(res_data)))
            print(">>> Already add {}/{} school".format(index + 1, len(res_data)))
            code_map = self.get_code_map()
            if number in code_map and name != code_map[number].get("name"):
                update_data = deepcopy(school.sso_data)
                update_data.pop('principal_email', None)
                update_school_req(code_map[number].get('uuid'), update_data)
            self.client.create_school(school)
            self.school_map[name] = number
