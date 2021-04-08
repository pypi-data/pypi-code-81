import logging
import os
import shutil
import re

from karby.parameter_manager import ParameterManager
from karby.sca_apis import SCAScanTool
from karby.util.helpers import exec_command, project_dir_analyzer, make_zip

FORMAT = "%(asctime)s|%(name)s|%(levelname)s|%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger("snyk-api")


class Scantist(SCAScanTool):
    def __init__(self, param_manager: ParameterManager):
        super().__init__(param_manager)
        self.scantist_email = os.getenv("SCANTIST_EMAIL", "")
        self.scantist_pass = os.getenv("SCANTIST_PSW", "")
        self.scantist_base_url = os.getenv(
            "SCANTIST_BASEURL", "https://api.scantist.io/"
        )
        self.check_auth()
        if not self.project_name:
            self.project_name = project_dir_analyzer(self.project_url)

    def check_auth(self):
        cmd = f"scantist_auth -b {self.scantist_base_url} -e {self.scantist_email} -p {self.scantist_pass}"
        result = exec_command(cmd)
        if result.get("code") != 0:
            logger.error(result.get("error").decode())
            raise

    def scan_with_api(self):
        self.options += " -airgap "
        return self.scan_with_cmd()

    def scan_with_cmd(self):
        if not os.path.exists(self.project_url):
            logger.error(f"trigger_scan|skip, no files found for {self.project_url}")
            raise
        if "-airgap" in self.options:
            make_zip(self.project_url, self.project_url + ".zip")
            cmd = f"scantist_cmd -t source_code -f {self.project_url}.zip -r csv -p {self.output_dir}"
        else:
            cmd = f"scantist_cmd -t source_code -f {self.project_url} -r csv -b -p {self.output_dir}"
        logger.info(f"subprocess: {cmd}")
        result = exec_command(cmd)
        if result.get("code") != 0:
            logger.error(result.get("error").decode())
            raise
        cmd_output = result.get("error").decode()
        logger.info(cmd_output)
        os.remove(self.project_url + ".zip")
        return cmd_output

    def get_report_by_api(self, scan_feedback=None):
        return self.get_report_from_cmd(scan_feedback)

    def get_report_from_cmd(self, scan_feedback=None):
        # get scan id from output
        scan_id = re.search(
            r"^INFO|Scan ([1-9][0-9]+) completed!", scan_feedback
        ).group(1)
        report_path = re.search(
            r"^INFO|report output folder: (.+)\n", scan_feedback
        ).group(1)
        component_list_report = os.path.join(
            report_path, f"scan-{scan_id}-component.csv"
        )
        if not os.path.isfile(component_list_report):
            raise Exception(f"component report not find for {scan_id}")
        vulnerability_list_report = os.path.join(
            report_path, f"scan-{scan_id}-vulnerability.csv"
        )
        if not os.path.isfile(vulnerability_list_report):
            raise Exception(f"issue report not find for {scan_id}")

        # change name to the standard format
        shutil.copy(
            component_list_report,
            os.path.join(self.output_dir, f"scantist-component-{self.project_name}.csv"),
        )
        shutil.copy(
            vulnerability_list_report,
            os.path.join(self.output_dir, f"scantist-issue-{self.project_name}.csv"),
        )
        shutil.rmtree(os.path.dirname(component_list_report))
