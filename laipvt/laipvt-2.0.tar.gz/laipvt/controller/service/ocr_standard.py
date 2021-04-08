from __future__ import absolute_import
from __future__ import unicode_literals

from laipvt.interface.serviceinterface import ServiceInterface
from laipvt.sysutil.util import path_join


class OcrStandardController(ServiceInterface):
    def __init__(self, check_result, service_path):
        super(OcrStandardController, self).__init__(check_result, service_path)
        self.project = "mage"

        self.ocr_ctpn_model_data_src = path_join(self.data_dir, "ocr-ctpn-tf-server")
        self.ocr_ctpn_model_data_remote = path_join(self.deploy_dir, "ocr-ctpn-tf-server")
        self.ocr_text_recognition_data_src = path_join(self.data_dir, "ocr-text-recognition-tf-server")
        self.ocr_text_recognition_data_remote = path_join(self.deploy_dir, "ocr-text-recognition-tf-server")

    def prepare_ocr(self):
        self._send_file(src=self.ocr_ctpn_model_data_src, dest=self.ocr_ctpn_model_data_remote)
        self._send_file(src=self.ocr_text_recognition_data_src, dest=self.ocr_text_recognition_data_remote)

    def run(self):
        self.prepare_ocr()
        self.push_images(project=self.project)
        self.start_service(project=self.project, version=self.private_deploy_version)
