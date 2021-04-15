from sync import BaseSync
from classcard_dataclient.models.clas import Class
from classcard_dataclient.client.backbone import Backbone
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


class ClassSync(BaseSync):
    def __init__(self, *args, **kwargs):
        super(ClassSync, self).__init__(*args, **kwargs)
        self.class_entrance = {}
        self.classroom_class = {}
        backbone = Backbone(self.school_id)
        backbone.wrap_teacher_map(origin="edtech")
        self.teacher_map = backbone.teacher_map

    def sync(self):
        study_year = {"小学": 6, "初中": 3, "高中": 3}
        res = self.nice_requester.get_class_list()
        code, res_sections = self.client.get_section_list(school_id=self.school_id)
        if code or not isinstance(res_sections, list):
            logger.error("Error: get section info, Detail: {}".format(res_sections))
            res_sections = []
        section_dict = {d["number"]: d['uuid'] for d in res_sections if d.get("number")}
        res_data = res.get('classes', [])
        sections = []
        for index, rd in enumerate(res_data):
            try:
                principal_number = rd['classTeacher']['teacherEID']
                principal_id = self.teacher_map.get(principal_number)
            except (Exception,):
                principal_number, principal_id = None, None
            if rd['locationID']:
                self.classroom_class[rd['locationID']] = rd['classFullName']
            section = Class(number=rd['qualifiedClassID'], name=rd['classFullName'], grade=rd['gradeName'],
                            principal_number=principal_number, principal_id=principal_id, school=self.school_id)
            section.uid = section_dict.get(section.number, None)
            section.principal_id = principal_id
            if rd['entranceYear'] and rd['entranceYear'].isdigit():
                entrance_info = {"classof": int(rd['entranceYear']),
                                 "graduateat": int(rd['entranceYear']) + study_year[rd["eduStage"]]}
            else:
                entrance_info = {"classof": None, "graduateat": None}
            self.class_entrance[rd['qualifiedClassID']] = entrance_info
            sections.append(section)
        code, data = self.client.create_section(sections)
        if code:
            logger.error("Code: {}, Msg: {}".format(code, data))
