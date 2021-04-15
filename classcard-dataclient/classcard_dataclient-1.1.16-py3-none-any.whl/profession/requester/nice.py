import uuid
import datetime
from copy import deepcopy
from requester.base import Requester
from config import NICE_SECRET_KEY, NICE_APP_KEY
from utils.code import get_md5_hash


class NiceRequester(Requester):
    def __init__(self, school_number, *args, **kwargs):
        base_data = kwargs.pop("base_data", {})
        super(NiceRequester, self).__init__(*args, **kwargs)
        self.school_number = school_number
        self.base_data = {"schoolID": self.school_number, "login": "banpai_01",
                          "token": "d0df559761fdd8ad0db754def2f56954"}
        self.base_data.update(base_data)

    def get_sign_data(self):
        sys_time = int(datetime.datetime.now().timestamp())
        random_str = str(uuid.uuid4()).replace('-', "")[:6]
        if self.school_number:
            sign_str = "randomStr={}&schoolID={}&sysTime={}&secretKey={}".format(random_str, self.school_number,
                                                                                 sys_time, NICE_SECRET_KEY)
        else:
            sign_str = "randomStr={}&sysTime={}&secretKey={}".format(random_str, sys_time, NICE_SECRET_KEY)
        sign = get_md5_hash(sign_str).lower()
        sign_data = {"appKey": NICE_APP_KEY, "sysTime": sys_time, "randomStr": random_str,
                     "sign": sign}
        if self.school_number:
            sign_data['schoolID'] = self.school_number
        return sign_data

    @property
    def sign_data(self):
        # sign_data = self.base_data
        sign_data = self.get_sign_data()
        print(sign_data)
        return sign_data

    def check_res(self, data):
        if data['status'] != 'success':
            raise ConnectionError(data['errorMessage'])
        return data['result'], True

    def get_teach_class_list(self):
        route = "/scheduler/getTeachingClasses"
        res = self._post_method(route, self.sign_data)
        return res

    def get_table(self, current=True):
        route = "/scheduler/getSchedule" if current else "/scheduler/getNextSchedule"
        res = self._post_method(route, self.sign_data)
        return res

    def get_student_class(self):
        route = "/scheduler/getStudentClasses"
        res = self._post_method(route, self.sign_data)
        return res

    def get_teacher_list(self):
        route = "/scheduler/getTeachers"
        res = self._post_method(route, self.sign_data)
        return res

    def get_class_list(self):
        route = "/scheduler/getClasses"
        res = self._post_method(route, self.sign_data)
        return res

    def get_student_list(self):
        route = "/scheduler/getStudentInfos"
        res = self._post_method(route, self.sign_data)
        return res

    def get_subject_list(self):
        route = "/scheduler/getSubjects"
        res = self._post_method(route, self.sign_data)
        return res

    def get_classroom_list(self):
        route = "/scheduler/getLocations"
        res = self._post_method(route, self.sign_data)
        return res

    def get_school_info(self):
        route = "/scheduler/getSchoolInfo"
        base_data = deepcopy(self.sign_data)
        res = self._post_method(route, base_data)
        return res

    def get_school_list(self):
        route = "/scheduler/getSchools"
        base_data = deepcopy(self.sign_data)
        res = self._post_method(route, base_data)
        return res


classroom_class = {}
nice_requester = NiceRequester("3550", host="xgk.lanzhou.edu.cn/schoolscheduleserv/integration", protocol="https")
class_number_map = {}
res_data = nice_requester.get_class_list()
for index, rd in enumerate(res_data["classes"]):
    try:
        principal_number = rd['classTeacher']['teacherEID']
    except (Exception,):
        principal_number = None
    class_number_map[rd['classFullName']] = rd['qualifiedClassID']
    if rd['locationID']:
        if rd['locationID'] not in classroom_class:
            classroom_class[rd['locationID']] = []
        classroom_class[rd['locationID']].append(rd['classFullName'])
section_classroom = {}
room_data = nice_requester.get_classroom_list()
for rd in room_data["locations"]:
    if rd['locationID'] in classroom_class:
        section_classroom[classroom_class[rd['locationID']][0]] = rd['locationName']
course_class_list = set()
response = nice_requester.get_table(current=True)
for course_info in response['schedule']:
    is_walking = course_info['classType'] in ["教学班", "选修班"]
    if not is_walking:
        course_class_list.add(course_info['qualifiedClassID'])
print(res_data)
