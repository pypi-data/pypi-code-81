"""GoodData class definition
"""
import os
import json
from typing import List, Optional
import requests
import re
from datetime import datetime
from time import sleep
from logging import getLogger, INFO, basicConfig
from requests.exceptions import ConnectTimeout, ConnectionError
from urllib3.exceptions import ProtocolError
from http.client import RemoteDisconnected

OBJECT_ID_RE = r".*\/md\/.*\/obj\/(\d+)"
COOLDOWN_SECONDS = 20


class RetrySession:
    def __init__(self, logger=None):
        self.session = requests.Session()
        if logger is None:
            self.logger = getLogger("RetrySession")
        else:
            self.logger = logger

    def get(self, *args, **kwargs):
        retry_count = 0
        retry_timeout = 10
        while True:
            try:
                return self.session.get(*args, **kwargs)
            except (ConnectionError, ConnectTimeout, RemoteDisconnected, ProtocolError) as error:
                self.logger.error(error)
                retry_count += 1
                if retry_count > 5:
                    self.logger.error("Too many retries")
                    raise error
                if retry_count == 3:
                    retry_timeout = 30
                self.logger.error("Retry # %d in %d seconds", retry_count, retry_timeout)
                sleep(retry_timeout)

    def post(self, *args, **kwargs):
        retry_count = 0
        retry_timeout = 10
        while True:
            try:
                return self.session.post(*args, **kwargs)
            except (ConnectionError, ConnectTimeout, RemoteDisconnected, ProtocolError) as error:
                self.logger.error(error)
                retry_count += 1
                if retry_count > 5:
                    self.logger.error("Too many retries")
                    raise error
                if retry_count == 3:
                    retry_timeout = 30
                self.logger.error("Retry # %d in %d seconds", retry_count, retry_timeout)
                sleep(retry_timeout)


def get_object_id(obj_link):
    """Return object id from object link

    Args:
        obj_link (str): Object link (usually `/gdc/md/<project-id>/obj/<object-id>`)

    Returns:
        str: Object id
    """
    return re.findall(OBJECT_ID_RE, obj_link)[0]


def _url(domain, endpoint):
    return "https://{domain}.gooddata.com/{endpoint}".format(domain=domain, endpoint=endpoint)


class ExportJob:
    def __init__(self, token, status_uri, gd, done=False, exported_object=None):
        """ExportJob constructor.

        Args:
            token (str): Token returned from the export job
            status_uri (str): Uri to poll status
            gd (GoodData): GoodData connection object that created the export job
            done (bool, optional): Whether the job is complete. Defaults to False.
            exported_object (str, optional): Exported object's title for better logging.
        """
        self.token = token
        self.status_uri = status_uri
        self.exported_objects = exported_object
        self.done = done
        self.gd = gd

    def wait(self, poll_interval=5):
        """Wait for export job to be completed

        Args:
            poll_interval (int, optional): Number of seconds to wait before polling. Defaults to 5.
        """
        if self.done:
            return
        while True:
            if self.update_status():
                break
            sleep(poll_interval)

    def update_status(self):
        """Update status of the export job and set attribute .done to True if done.
        Returns True if done, False if still running
        """
        if self.done:
            return True
        self.gd.login()
        url = _url(self.gd.domain, self.status_uri[1:])
        response = self.gd.session.get(url, headers=self.gd.headers)
        if response.json()["wTaskStatus"]["status"] == "OK":
            self.done = True
            return True
        if response.json()["wTaskStatus"]["status"] == "ERROR":
            raise Exception(response.text)
        return False


# TODO: Refactor, code repetition
class ExecutionPoller:
    def __init__(self, gd, poll_url):
        self.gd = gd
        self.poll_url = poll_url
        self.done = False
        self.status = None

    def update_status(self):
        """Update status and return .done attribute value"""
        self.gd.login()
        url = _url(self.gd.domain, self.poll_url.lstrip("/"))
        response = self.gd.session.get(url, headers=self.gd.headers)
        status = response.json().get("execution", {}).get("status")
        if status is None:
            raise Exception(response.text)
        self.status = status
        if self.status in ["DONE", "OK"]:
            self.done = True
        elif self.status in ["RUNNING", "SCHEDULED"]:
            self.done = False
        else:
            raise Exception(f"Execution status is prohibited: {self.status}")
        return self.done

    def wait(self, interval=5):
        """Wait until the task is done"""
        if self.done:
            return True
        while not self.done:
            self.update_status()
            sleep(interval)


class GoodData:
    """Main class for interacting with GoodData API."""

    def __init__(self, user, password, domain, pid):
        """Initiate GoodData API and login

        Args:
            user (str): user name (e-mail)
            password (str): user password
            domain (str): GoodData API domain (the part before .gooddata.com (e.g. secure))
            pid (str): project id
        """
        self.last_login = None
        self.session = RetrySession()
        self.user = user
        self.password = password
        self.domain = domain
        self.pid = pid
        self.logger = getLogger(__name__)
        self.profile = None
        self.login()
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.dashboards = []
        self.kpidashboards = []
        self.kpis = []
        self.metrics = []
        self.reports = []
        self.datasets = []
        self.projects = []
        self.datasets_on_dashboard = {}
        self.processed = []
        self.processed_objects = {}
        self.metadata = {}
        self.dataset_members = {}

    def login(self):
        """Login to GoodData and obtain tokens"""
        if self.last_login is not None and (datetime.now() - self.last_login).seconds < 300:
            return
        self.logger.info("Login expired, logging in again")
        payload = {
            "postUserLogin": {
                "login": self.user,
                "password": self.password,
                "verify_level": 0,
            }
        }
        response = self.session.post(_url(self.domain, "gdc/account/login"), json=payload)
        if response.status_code != 200:
            self.logger.error(response.text)
            raise PermissionError("Login not successfull")
        self.profile = response.json()["userLogin"]["profile"]
        self.last_login = datetime.now()

    def list_dashboards(self):
        """List all dashboards

        Returns:
            list: List of dictionaries containing dashboard metadata
        """
        self.login()
        url = _url(self.domain, "gdc/md/{pid}/query/projectdashboards".format(pid=self.pid))
        response = self.session.get(url, headers=self.headers)
        self.dashboards = response.json()["query"]["entries"]
        return self.dashboards

    def list_kpidashboards(self):
        """List all KPI Dashboards

        Returns:
            list: List of dictionaries containing dashboard metadata
        """
        self.login()
        url = _url(
            self.domain,
            "gdc/md/{pid}/query/analyticaldashboard".format(pid=self.pid),
        )
        response = self.session.get(url, headers=self.headers)
        self.kpidashboards = response.json()["query"]["entries"]
        return self.kpidashboards

    def list_reports(self):
        """List all reports

        Returns:
            list: List of dictionaries containing report metadata
        """
        self.login()
        url = _url(self.domain, "gdc/md/{pid}/query/reports".format(pid=self.pid))
        response = self.session.get(url, headers=self.headers)
        self.reports = response.json()["query"]["entries"]
        return self.reports

    def list_kpis(self):
        """List all visualizationobjects

        Returns:
            list: List of dictionaries containing kpi metadata
        """
        self.login()
        url = _url(
            self.domain,
            "gdc/md/{pid}/query/visualizationobjects".format(pid=self.pid),
        )
        response = self.session.get(url, headers=self.headers)
        self.kpis = response.json()["query"]["entries"]
        return self.kpis

    def list_datasets(self):
        """List all project datasets

        Returns:
            list: List of dictionaries containing dataset metadata
        """
        self.login()
        url = _url(self.domain, "gdc/md/{pid}/query/datasets".format(pid=self.pid))
        response = self.session.get(url, headers=self.headers)
        self.datasets = response.json()["query"]["entries"]
        return self.datasets

    def list_metrics(self):
        """List all project metrics

        Returns:
            list: List of dictionaries containing metric metadata
        """
        self.login()
        url = _url(self.domain, "gdc/md/{pid}/query/metrics".format(pid=self.pid))
        response = self.session.get(url, headers=self.headers)
        self.metrics = response.json()["query"]["entries"]
        return self.metrics

    def _find_nested_metric(self, node):
        for subnode in node:
            if "value" in subnode:
                if re.match(OBJECT_ID_RE, subnode["value"]):
                    if "metric" in self.get_object(subnode["value"]):
                        return True
            if "content" in subnode:
                if self._find_nested_metric(subnode["content"]):
                    return True
        return False

    def metric_is_simple(self, object_id: str):
        """Returns True if a metric specified by `object_id` has no nested metrics in the definition.

        Args:
            object_id (str): Object ID of the metric (or object link starting with /gdc/md)
        """
        self.login()
        if "gdc/" in object_id:
            object_id = get_object_id(object_id)
        url = _url(self.domain, "gdc/md/{pid}/obj/{object_id}".format(pid=self.pid, object_id=object_id))
        response = self.session.get(url, headers=self.headers)
        meta = response.json()
        if not "metric" in meta:
            raise ValueError("Object id {} is not a metric".format(object_id))
        node = meta["metric"]["content"]["tree"]["content"]
        # _find_nested_metric returns True if any was found, this means the metric is not simple => return !result
        return not self._find_nested_metric(node)

    def execute_afm(self, afm: dict):
        """Execute afm insight definition and return executionResult to be used with exporter functions.

        Args:
            afm (dict): afm definition, see [GoodData SDK Documentation](https://sdk.gooddata.com/gooddata-ui/docs/4.1.1/afm.html)
        """
        self.login()
        url = _url(self.domain, "gdc/app/projects/{pid}/executeAfm".format(pid=self.pid))
        if "afm" in afm:
            afm = {"execution": afm}
        elif not "execution" in afm:
            raise ValueError("afm should be a dictionary either containing key 'afm' or 'execution' in its root")
        response = self.session.post(url, json=afm, headers=self.headers)
        return response.json()["executionResponse"]["links"]["executionResult"]

    def export_afm_result(self, execution_result: str, fname: str, title: str = "csv export"):
        """Export afm execution as CSV.

        Args:
            execution_result (str): Output of [execute_afm](#gd.GoodData.execute_afm) method.
            fname (str): Output path for the csv.
            title (str, optional): Report title. Defaults to "csv export".
        """
        self.login()
        url = _url(self.domain, "gdc/internal/projects/{pid}/exportResult".format(pid=self.pid))
        data = {
            "resultExport": {
                "executionResult": execution_result,
                "exportConfig": {"format": "csv", "title": title},
            }
        }
        response = self.session.post(url, json=data, headers=self.headers)
        try:
            target_link = response.json()["uri"][1:]
        except json.decoder.JSONDecodeError as error:
            self.logger.error(error)
            self.logger.error(response.text)
            self.logger.error("status_code: %d", response.status_code)
            raise error
        url = _url(self.domain, target_link)

        attempts_count = 60
        while attempts_count:
            sleep(1)
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                self.logger.info("Report returned, status_code: %d", response.status_code)
                break
            elif response.status_code == 204:
                self.logger.info("Empty report returned, status_code: %d", response.status_code)
                break
            else:
                self.logger.info("Report not ready yet, continue polling, status_code: %d", response.status_code)
            attempts_count -= 1

        if response.text.strip():
            with open(fname, "w", encoding="utf-8") as fid:
                fid.write(response.text)

    def get_user(self, user_link: str):
        """Get user details. `user_link` may be either whole link (starting /gdc/account/profile) or user id

        Args:
            user_link (str): User link or user id
        """
        self.login()
        if "/gdc/account/profile" in user_link:
            url = _url(self.domain, user_link[1:])
        else:
            url = _url(self.domain, "gdc/account/profile/{}".format(user_link))
        return self.session.get(url).json()

    def list_projects(self):
        """List all projects authenticated by current user.

        Returns
            list: List of dictionaries containing project metadata
        """
        self.login()
        url = _url(self.domain, "gdc/md")
        response = self.session.get(url, headers=self.headers)
        self.projects = [entry for entry in response.json()["about"]["links"] if entry["category"] == "project"]
        return self.projects

    def get_object(self, object_id, project_id=None):
        """Get object specified by {object_id} from a project specified by {project_id}

        Args:
            object_id (str): Object id or self-link to be returned
            project_id (str, optional): Project to search in. Defaults to current project.
        """
        if project_id is None:
            project_id = self.pid
        if re.match(OBJECT_ID_RE, object_id):
            object_id = get_object_id(object_id)
        self.login()
        url = _url(self.domain, "gdc/md/{}/obj/{}".format(project_id, object_id))
        response = self.session.get(url, headers=self.headers)
        if response.status_code == 404:
            return None
        return response.json()

    def get_using(self, object_id, types=["metric", "attribute", "dimension", "fact"]):
        """Get list of objects of given type that use specified object_id.

        Args:
            object_id (str): numeric object id of the object we are searching for
            types (list, optional): List of types of objects to return. Defaults to ["metric", "attribute", "dimension", "fact"].

        Returns:
            list: list of dictionaries containing resulting dependent objects' metadata
        """
        self.login()
        types_str = ",".join(types)
        url = _url(
            self.domain,
            "gdc/md/{pid}/using2/{object_id}".format(pid=self.pid, object_id=object_id),
        )
        response = self.session.get(url, headers=self.headers, params={"types": types_str})
        return response.json()["entries"]

    def get_used_by(self, object_id, types=["report", "dashboard"]):
        """Get list of objects of given type that are used by specified object_id.

        Args:
            object_id (str): numeric object id of the object we are searching for
            types (list, optional): List of types of objects to return. Defaults to ["metric", "attribute", "dimension", "fact"].

        Returns:
            list: list of dictionaries containing resulting dependent objects' metadata
        """
        self.login()
        types_str = ",".join(types)
        url = _url(
            self.domain,
            "gdc/md/{pid}/usedby2/{object_id}".format(pid=self.pid, object_id=object_id),
        )
        response = self.session.get(url, headers=self.headers, params={"types": types_str})
        return response.json()["entries"]

    def _record(self, kind, obj):
        if not kind in self.processed_objects:
            self.processed_objects[kind] = [obj]
        else:
            if not obj in self.processed_objects[kind]:
                self.processed_objects[kind].append(obj)

    def _find_dataset(self, obj_link):
        for did in self.dataset_members:
            for attribute in self.dataset_members[did]["attributes"]:
                if attribute == obj_link:
                    return did
            for fact in self.dataset_members[did]["facts"]:
                if fact == obj_link:
                    return did
        raise Exception("{} was not found".format(obj_link))

    def _is_processed(self, obj):
        for kind in self.processed_objects:
            if obj in self.processed_objects[kind]:
                return True
        return False

    def process_metric_tree(self, content):
        """Process recursively all objects nested in metric definition

        Args:
            content (dict): Metric .content object
        """
        metrics = []
        if "value" in content and content["type"] not in [
            "function",
            "attributeElement object",
        ]:
            if content["type"] == "attribute object":
                self._record("attribute", content["value"])
            elif content["type"] == "fact object":
                self._record("fact", content["value"])
            elif content["type"] == "metric object":
                metrics.append(content["value"])
            elif content["type"] == "prompt object":
                self._record("prompt", content["value"])
            else:
                if not content["type"] in ["number", "time macro"]:
                    self.logger.warning("Unknown type %s", content["type"])
        if "content" in content:
            if isinstance(content["content"], list):
                for subcontent in content["content"]:
                    metrics.extend(self.process_metric_tree(subcontent))
            else:
                metrics.extend(self.process_metric_tree(content["content"]))
        return metrics

    def process_object(self, object_url):
        """Process object dependency

        Args:
            object_url (str): Object url
        """
        self.login()
        url = _url(self.domain, object_url[1:])
        if object_url in self.processed:
            return
        ## uncomment to speed up testing
        ## if len(self.processed) > 50:
        ##     return
        self.logger.info("Processing %s (total %d processed)", object_url, len(self.processed))
        self.processed.append(object_url)
        response = self.session.get(url, headers=self.headers)
        content = response.json()
        category = list(content.keys())[0]
        children = []
        if category == "metric":
            children.extend(self.process_metric_tree(content["metric"]["content"]["tree"]))
            for child in children:
                if child not in self.processed:
                    self.process_object(child)
        else:
            self._record(category, object_url)

    def get_object_metadata(self, object_url):
        """Get object metadata

        Args:
            object_url (str): Object url
        """
        if object_url in self.metadata:
            return
        self.login()
        url = _url(self.domain, object_url[1:])
        response = self.session.get(url, headers=self.headers)
        content = response.json()
        if "attribute" in content:
            did = self._find_dataset(object_url)
            self.metadata[object_url] = {
                "title": content["attribute"]["meta"]["title"],
                "link": object_url,
                "category": "attribute",
                "dataset": did,
                "dataset_title": self.dataset_members[did]["title"],
            }
        elif "fact" in content:
            did = self._find_dataset(object_url)
            self.metadata[object_url] = {
                "title": content["fact"]["meta"]["title"],
                "link": object_url,
                "category": "fact",
                "dataset": did,
                "dataset_title": self.dataset_members[did]["title"],
            }

    def load_members(self):
        """Load all datasets' members. You can access all members via this object's .dataset_members dictionary."""
        self.login()
        for dataset in self.list_datasets():
            self.logger.info("Loading members for dataset %s", dataset["title"])
            did = dataset["link"]
            url = _url(self.domain, did[1:])
            response = self.session.get(url, headers=self.headers)
            content = response.json()
            attributes = []
            facts = []
            if "attributes" in content["dataSet"]["content"]:
                attributes = content["dataSet"]["content"]["attributes"]
            if "facts" in content["dataSet"]["content"]:
                facts = content["dataSet"]["content"]["facts"]
            self.dataset_members[did] = {
                "title": dataset["title"],
                "facts": facts,
                "attributes": attributes,
            }
            self.logger.debug("Facts %d / Attributes %d", len(facts), len(attributes))

    def translate_prompts(self):
        """Get attribute from prompt"""
        if not "prompt" in self.processed_objects:
            return
        self.login()
        for prompt in self.processed_objects["prompt"]:
            url = _url(self.domain, prompt[1:])
            response = self.session.get(url, headers=self.headers)
            content = response.json()
            if not "prompt" in content or not "content" in content["prompt"]:
                print("WARNING: Prompt could not be translated")
                return
            attribute = content["prompt"]["content"]["attribute"]
            self._record("attribute", attribute)

    def partial_export_async(self, object_id):
        """Create partial export job and return (before the job completes)
        Returns {ExportJob} object

        Args:
            object_id (str): Object id to be exported
        """
        self.login()
        url = _url(self.domain, "gdc/md/{pid}/maintenance/partialmdexport".format(pid=self.pid))
        body = {
            "partialMDExport": {
                "uris": ["/gdc/md/{pid}/obj/{object_id}".format(pid=self.pid, object_id=object_id)],
                "exportAttributeProperties": "0",
                "crossDataCenterExport": "0",
            }
        }
        response = self.session.post(url, headers=self.headers, data=json.dumps(body))
        job_info = response.json()["partialMDArtifact"]
        return ExportJob(job_info["token"], job_info["status"]["uri"], self, exported_object=object_id)

    def partial_export_sync(self, object_id):
        """Create partial export job and wait for it to complete.

        Args:
            object_id (str): Object id to be exported
        """
        export_job = self.partial_export_async(object_id)
        export_job.wait()

    def partial_import_async(self, token, target_pid=None):
        """Create partial import job and return (before job completes)
        Returns ExportJob to enable polling status, None if import failed

        Args:
            token (str): Token of export job to be imported
            target_pid (str): Target project id. Defaults to current pid.
        """
        if target_pid is None:
            target_pid = self.pid
        self.login()
        url = _url(
            self.domain,
            "gdc/md/{pid}/maintenance/partialmdimport".format(pid=target_pid),
        )
        body = {
            "partialMDImport": {
                "token": token,
                "overwriteNewer": "1",
                "updateLDMObjects": "0",
                "importAttributeProperties": "0",
            }
        }
        response = self.session.post(url, headers=self.headers, data=json.dumps(body))
        ## OK
        if response.status_code == 200:
            return ExportJob(None, response.json()["uri"], self)
        ## Too Many Requests
        if response.status_code == 429:
            self.logger.warning(
                "Got status code 429 - Too Many Requests, will try to wait for %d seconds before retrying",
                COOLDOWN_SECONDS,
            )
            sleep(COOLDOWN_SECONDS)
            return self.partial_import_async(token, target_pid)
        self.logger.error("Returned non-200 status code: %d", response.status_code)
        self.logger.error(response.text)
        return None

    def get_report_by_identifier(self, identifier, project_id=None, object_name="reports"):
        """Get report or visualizationobject by identifier.

        Args:
            identifier (str): Report identifier
            project_id (str, optional): Project id. Defaults to current project.
            object_name (str, optional): 'reports' or 'visualizationobjects'. Defaults to 'reports'
        """
        if project_id is None:
            project_id = self.pid
        if object_name == "report":
            object_name = "reports"
        self.login()
        url = _url(
            self.domain,
            "gdc/md/{pid}/query/{object_name}".format(pid=project_id, object_name=object_name),
        )
        response = self.session.get(url, headers=self.headers)
        reports = response.json()["query"]["entries"]
        found = [r for r in reports if r["identifier"] == identifier]
        if found:
            return found[0]
        else:
            return None

    def list_schedules(self, project_id=None):
        """Get schedules for project"""
        project_id = project_id or self.pid
        self.login()
        url = _url(self.domain, f"gdc/projects/{project_id}/schedules")
        response = self.session.get(url, headers=self.headers)
        return response.json().get("schedules", {}).get("items", [])

    def get_schedule(self, schedule_id, project_id=None):
        """Get schedule by its id"""
        project_id = project_id or self.pid
        self.login()
        url = _url(self.domain, f"gdc/projects/{project_id}/schedules/{schedule_id}")
        response = self.session.get(url, headers=self.headers)
        return response.json().get("schedule", {})

    def execute_schedule(self, schedule_id, datasets: Optional[List] = None, project_id=None):
        """Execute a schedule and return polling object"""
        project_id = project_id or self.pid
        self.login()
        url = _url(self.domain, f"gdc/projects/{project_id}/schedules/{schedule_id}/executions")
        sdata = self.get_schedule(schedule_id, project_id)
        if not datasets:
            params = sdata.get("params", {})
        else:
            dset_lst = [{"dataset": dset, "uploadMode": "DEFAULT"} for dset in datasets]
            params = {"GDC_DATALOAD_DATASETS": json.dumps(dset_lst), "GDC_DATALOAD_SINGLE_RUN_LOAD_MODE": "DEFAULT"}
        payload = {"execution": {"params": params}}
        response = self.session.post(url, headers=self.headers, json=payload)
        link = response.json().get("execution", {}).get("links", {}).get("self", None)
        return ExecutionPoller(self, link)

    def get_schedule_execution(self, schedule_id, execution_id, project_id=None):
        """Get schedule execution status"""
        project_id = project_id or self.pid
        self.login()
        url = _url(self.domain, f"gdc/projects/{project_id}/schedules/{schedule_id}/executions/{execution_id}")
