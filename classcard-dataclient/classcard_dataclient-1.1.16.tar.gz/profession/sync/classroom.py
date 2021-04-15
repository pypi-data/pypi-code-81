import os
from sync import BaseSync
from classcard_dataclient.models.classroom import Classroom, RoomType
from classcard_dataclient.requester.nirvana import NirvanaRequester
from utils.loggerutils import logging
from utils.code import get_md5_hash

logger = logging.getLogger(__name__)


class ClassroomSync(BaseSync):
    def __init__(self, *args, **kwargs):
        super(ClassroomSync, self).__init__(*args, **kwargs)
        self.is_walking = True
        self.id_num_map = {}
        self.classroom_class = {}

    def clear_class_relation(self, classroom_nums):
        class_card_server_url = os.getenv("CLASS_CARD_SERVER_URL", "http://127.0.0.1:9000")
        nirvana_requester = NirvanaRequester(server=class_card_server_url, school_id=self.school_id)
        classroom_num_map = self.client.get_classroom_num_map(self.school_id)
        for classroom_num, classroom_id in classroom_num_map.items():
            if classroom_num in classroom_nums:
                nirvana_requester.update_classroom(classroom_id, {"section": None})

    def sync(self):
        total = 0
        res = self.nice_requester.get_classroom_list()
        res_data = res.get('locations', [])
        classroom_list = []
        classroom_nums = []
        logging.info(self.classroom_class)
        for rd in res_data:
            building = rd['building'] or "教学楼"
            try:
                floor = int(rd['building'][-3])
            except (Exception,):
                floor = 0
            number = get_md5_hash(rd['locationName'])
            self.id_num_map[rd['locationID']] = number
            category = RoomType.TYPE_PUBLIC if self.is_walking else RoomType.TYPE_CLASS
            classroom = Classroom(number=number, name=rd['locationName'], building=building,
                                  floor=floor, school=self.school_id)
            if rd['locationID'] in self.classroom_class:
                classroom.section_name = self.classroom_class[rd['locationID']]
                classroom.category = RoomType.TYPE_CLASS
                total += 1
                logger.info("classroom {} class is {}".format(rd['locationName'], classroom.section_name))
            else:
                classroom.category = RoomType.TYPE_PUBLIC
                logger.info("classroom {} has no name".format(rd['locationName']))
            classroom_list.append(classroom)
            classroom_nums.append(classroom.number)
        self.clear_class_relation(classroom_nums)
        try:
            self.client.create_classrooms(self.school_id, classroom_list)
        except (Exception,):
            for classroom_item in classroom_list:
                try:
                    self.client.create_classrooms(self.school_id, [classroom_item])
                except (Exception,):
                    continue
        logging.info("{}/{} has class".format(total, len(classroom_list)))
