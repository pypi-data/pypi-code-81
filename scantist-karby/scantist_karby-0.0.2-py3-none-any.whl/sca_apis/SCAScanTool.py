import os
import pathlib
from abc import abstractmethod, ABC

from karby.parameter_manager import ParameterManager
from karby.util.constants import SCAN_TYPE
from karby.util.settings import error_exit


class SCAScanTool(ABC):
    def __init__(self, param_manager: ParameterManager):
        self.scan_type = param_manager.get_param("scan_type")
        self.project_url = param_manager.get_param("url")
        if os.path.exists(self.project_url):
            self.project_url = os.path.abspath(self.project_url)
        self.project_name = param_manager.get_param("name")
        self.output_dir = param_manager.get_param("output")
        self.options = param_manager.get_param("options")

    @abstractmethod
    def check_auth(self):
        pass

    @abstractmethod
    def scan_with_api(self):
        pass

    @abstractmethod
    def scan_with_cmd(self):
        pass

    @abstractmethod
    def get_report_by_api(self, scan_feedback=None):
        pass

    @abstractmethod
    def get_report_from_cmd(self, scan_feedback=None):
        pass

    def scan_project(self):
        if self.scan_type == "cmd":
            return self.scan_with_cmd()
        elif self.scan_type == "upload":
            return self.scan_with_api()
        else:
            error_exit(f"scan type should only in {SCAN_TYPE}")

    def get_result(self, scan_feedback):
        if not os.path.isdir(self.output_dir):
            pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        if self.scan_type == "cmd":
            return self.get_report_from_cmd(scan_feedback)
        elif self.scan_type == "upload":
            return self.get_report_by_api(scan_feedback)
        else:
            error_exit(f"scan type should only in {SCAN_TYPE}")
