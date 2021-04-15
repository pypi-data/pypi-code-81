"""Module for task."""
import typing
from typing import Optional, SupportsIndex

from .data import TaskData, TaskListData
if typing.TYPE_CHECKING:
    from .api import Api


class Task:
    """Task."""
    def __init__(self, api: 'Api', taskdata: TaskData) -> None:
        self._api = api
        self.data = taskdata


class TaskList:
    """Task list."""
    def __init__(self, api: 'Api', tasklist: TaskListData, index: int, per: Optional[int]) -> None:
        self._api = api
        self.tasklist = tasklist
        self.index = index
        self.per = per

    @property
    def count(self) -> int:
        """Returns count of tasklist. It may larger than length of TaskList."""
        return self.tasklist.count

    def __getitem__(self, idx: SupportsIndex) -> Task:
        return Task(self._api, self.tasklist.tasks[idx])

    def __len__(self) -> int:
        return len(self.tasklist.tasks)

    def nextpage(self) -> 'TaskList':
        """Get next page of task list."""
        return self._api.tasks(self.index + 1, self.per)


class TaskIter:
    """Paginator of tasks."""
    def __init__(self, api: 'Api') -> None:
        self.tasklist = api.tasks()
        self.next_i = 0

    def __iter__(self) -> 'TaskIter':
        return self

    def __next__(self) -> Task:
        try:
            task = self.tasklist[self.next_i]
        except IndexError:
            self.tasklist = self.tasklist.nextpage()
            self.next_i = 0
            if len(self.tasklist) > 0:
                task = self.tasklist[self.next_i]
            else:
                raise StopIteration
        self.next_i += 1
        return task
