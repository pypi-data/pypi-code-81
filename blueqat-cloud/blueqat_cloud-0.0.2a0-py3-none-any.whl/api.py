"""Module for manage API"""
import json
import os
import urllib.request
import typing
from typing import Any, List, Optional, Type

from .annealing import AnnealingTask, AnnealingResult
from .data import ExecutionRequest, ExecutionRequestEncoder, TaskListData
from .device import Device
from .task import Task, TaskIter, TaskList

from .taskdatafactory import make_executiondata

if typing.TYPE_CHECKING:
    from blueqat import Circuit

API_ENDPOINT = "https://cloudapi.blueqat.com/"


class Api:
    """Manage API and post request."""
    def __init__(self, api_key: str):
        self.api_key = api_key

    def post_request(
            self,
            path: str,
            body: Any,
            json_encoder: Optional[Type[json.JSONEncoder]] = None) -> Any:
        """Post request."""
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key,
        }
        req = urllib.request.Request(
            API_ENDPOINT + path,
            json.dumps(body, cls=json_encoder).encode(), headers)
        with urllib.request.urlopen(req) as res:
            body = res.read()
        return json.loads(body)

    def save_api(self) -> None:
        """Save API to file."""
        d = os.path.join(os.environ["HOME"], ".bqcloud")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "api_key"), "w") as f:
            f.write(self.api_key)

    def credit(self) -> str:
        """Get credit."""
        path = "v1/credit/get"
        return self.post_request(path, {})["amount"]

    def post_executiondata(self, execdata: ExecutionRequest) -> Task:
        """Create new task"""
        path = "v2/quantum-tasks/create"
        res = self.post_request(path, execdata, json_encoder=ExecutionRequestEncoder)
        return res

    def annealing(self, qubo: list[list[float]], chain_strength: int,
                  num_reads: int) -> AnnealingResult:
        """Create annealing task"""
        path = "v1/quantum-tasks/create"
        res = self.post_request(path, {
            "qubo": qubo,
            "chain_strength": chain_strength,
            "num_reads": num_reads
        })
        return AnnealingResult(**res)

    def execute(self,
                c: 'Circuit',
                device: Device,
                shots: int,
                group: Optional[str] = None,
                send_email: bool = False) -> Task:
        """Create new task and execute the task."""
        execdata = make_executiondata(c, device, shots, group, send_email)
        return self.post_executiondata(execdata)

    def annealing_tasks(self, index: int = 0) -> List[AnnealingTask]:
        """Get tasks."""
        path = "v1/quantum-tasks/list"
        body = {
            "index": index,
        }
        tasks = self.post_request(path, body)
        assert isinstance(tasks, list)
        return [AnnealingTask(self, **task) for task in tasks]

    def tasks(self, index: int = 0, per: Optional[int] = None) -> TaskList:
        """Get tasks."""
        path = "v2/quantum-tasks/list"
        body = {
            "index": index,
        }
        if per is not None and per > 0:
            body["per"] = per
        tasks = self.post_request(path, body)
        return TaskList(self, TaskListData(**tasks), index, per)

    def iter_tasks(self) -> TaskIter:
        """Get paginator of tasks"""
        return TaskIter(self)


def load_api() -> Api:
    """Load API from file."""
    with open(os.path.join(os.environ["HOME"], ".bqcloud/api_key")) as f:
        return Api(f.read().strip())


def register_api(api_key: str) -> Api:
    """Save and return API."""
    api = Api(api_key)
    api.save_api()
    return api
