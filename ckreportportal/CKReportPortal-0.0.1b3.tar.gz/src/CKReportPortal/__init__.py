# encoding: utf-8
import os
import logging
from time import time
from mimetypes import guess_type
from robot.api.deco import keyword
from reportportal_client import ReportPortalService

dir_file = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class CKReportPortal(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logger = logging.getLogger(__name__)

    @keyword('RP Config')
    def RPConfig(self, rp_endpoint, rp_project, rp_uuid):
        """
        Examples
        | RP Config  |  http://localhost:8080  |  Examples  |  0f687fbd-5563-4f01-9a17-123d20ce7e8e |
        """
        global service
        service = ReportPortalService(endpoint=rp_endpoint, project=rp_project, token=rp_uuid)

    @keyword('RP Start Bulid')
    def RPStartBulid(self, rp_launch_name):
        """
        Examples
        | RP Start Bulid  |  Bulid Name |
        """
        launch = service.start_launch(name=rp_launch_name, start_time=str(int(time()*1000)))

    @keyword('RP Start Test')
    def RPStartTest(self, rp_testname, rp_description=None, rp_parameters={'':''}):
        """
        Examples
        | ${ReturnID}  |  RP Start Test  |  TEST  |                   |                     |
        | ${ReturnID}  |  RP Start Test  |  TEST  | Test description  |                     |
        | ${ReturnID}  |  RP Start Test  |  TEST  | Test description  |  {'key' : 'value'}  |
        """
        item_id = service.start_test_item(name=rp_testname, description=rp_description, start_time=str(int(time()*1000)), item_type="STEP", parameters=rp_parameters)
        return item_id

    @keyword('RP Start Test Step')
    def RPStartLog(self, item_id, rp_message, rp_attachment=''):
        """
        Examples
        | ${ReturnID}           |  RP Start Test  |  TEST  |                |       
        | `RP Start Test Step`  |  ${ReturnID}    |  TEST  |                | 
        | `RP Start Test Step`  |  ${ReturnID}    |  TEST  |  D:/test.jpeg  | 
        """
        if '' == rp_attachment:
            service.log(time=str(int(time()*1000)), message=rp_message, level="Debug", item_id=item_id)
        else:
            with open(rp_attachment, "rb") as fh:
                attachment = {
                    "name": os.path.basename(rp_attachment),
                    "data": fh.read(),
                    "mime": guess_type(rp_attachment)[0] or "application/octet-stream"
                }
                service.log(time=str(int(time()*1000)), message=rp_message, level="Debug", item_id=item_id, attachment=attachment)

    @keyword('RP Finish Test')
    def RPFinishTest(self, item_id, rp_status='PASSED'):
        """
        Examples
        | ${ReturnID}         |  RP Start Test  |  TEST  |
        | RP Start Test Step  |  ${ReturnID}    |  TEST  |                | 
        | `RP Finish Test`    |  ${ReturnID}    |        |
        """
        if 'PASS' in rp_status:
            service.finish_test_item(item_id=item_id, end_time=str(int(time()*1000)), status="PASSED")
        elif 'FAIL' in rp_status:
            service.finish_test_item(item_id=item_id, end_time=str(int(time()*1000)), status="FAILED")
        else:
            service.finish_test_item(item_id=item_id, end_time=str(int(time()*1000)), status="SKIPPED")

    @keyword('RP Finish Bulid')
    def RPFinishBulid(self):
        """
        Examples
        | ${ReturnID}         |  RP Start Test  |  TEST  |
        | RP Start Test Step  |  ${ReturnID}    |  TEST  |                | 
        | RP Finish Test      |  ${ReturnID}    |        |
        | `RP Finish Bulid`   |                 |        |
        """
        service.finish_launch(end_time=str(int(time()*1000)))
        service.terminate()
