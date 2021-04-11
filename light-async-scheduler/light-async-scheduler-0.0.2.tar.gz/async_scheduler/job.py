from datetime import datetime as dt
from datetime import timedelta as td
from typing import Any, Dict, List
from uuid import UUID, uuid1

class BaseJob:
    """Job class.
    A basic job which will run and will pass ```job_type``` as a parameter to the scheduler function.
    Runs every ```interval```. This is a base class and so can (and should) be extended.

    Args:
        interval (timedelta):
            The interval at which this job should run
        (opt) name (str):
            The name given to the job
        (opt) id (UUID):
            A unique job identifier. One will be created automatically if this is none.
        (opt) job_type (str):
            The type of job being run. This is passed to the scheduler.

    Props:
        is_due (bool):
            True if the task is currently due or overdue
        overdue_amount (datetime.timedelta):
            The difference between current time and the due time
        next_run (datetime):
            The next time this job is due to be run
    """
    KEYS = [
        "id",
        "job_type",
        "interval",
        "last_run",
        "next_run",
    ]

    def __init__(
            self,
            interval: td,
            name: str = None,
            id: UUID = None,
            job_type = None):
        """
        Interval will eventually be defined as fastapischeduler.Interval class
        Type will eventually be defined as fastapischeduler.Type class
        """
        self.id: UUID = id or uuid1()
        self.job_type = job_type
        self.name = name

        self._interval: td = interval
        self._last_run: dt = dt.now()
        self._calculate_next_run()

    def __str__(self):
        return f"<Job: {self.name} interval: {self.interval} next due at: {self._next_run}{ ' (overdue by: ' + str(self.overdue_amount) + ')' if self.is_due else ''}>"

    def __getitem__(self, key: str) -> Dict[str, Any]:
        values = [
            self.id,
            self.job_type,
            self._interval,
            self._last_run,
            self._next_run,
        ]
        all_attrs = zip(self.KEYS, values)
        return dict(all_attrs)[key]

    def _calculate_next_run(self) -> dt:
        self._next_run = self._last_run + self.interval
        return self._next_run

    def keys(self) -> List[str]:
        return self.KEYS

    def run(self) -> None:
        """Called by a scheduler to mark the job as run and update the next due time"""
        self._last_run = dt.now()
        self._calculate_next_run()
        return None

    @property
    def is_due(self) -> bool:
        """Returns True if the job is due or overdue"""
        return self._next_run < dt.now()

    @property
    def overdue_amount(self) -> td:
        """Returns timedelta object of ```now - time of next run```"""
        return dt.now() - self._next_run

    @property
    def next_run(self) -> dt:
        """The time when the job next needs to be run"""
        if not self._next_run:
            self._calculate_next_run()
        return self._next_run

    @next_run.setter
    def next_run_setter(self, proposed_next_run: dt) -> None:
        current_time = dt.now()
        if proposed_next_run < current_time:
            raise ValueError(f"Cannot set a next run time in the past.")
        else:
            self._next_run = proposed_next_run
        return None

    @property
    def interval(self) -> td:
        """The interval at which this job should be run"""
        return self._interval

    @interval.setter
    def interval_setter(self, proposed_interval: td):
        self._interval = proposed_interval

    """There is potential to add these methods in for the future.
    @property
    def last_result(self) -> Any:
        return self._last_result

    @last_result.setter
    def set_last_result(self, result):
        self._last_result = result"""

class UserJob(BaseJob):
    """Job class.
    A job class which will pass ```job_type``` and ```user_id``` as paramteres to the scheduler.
    Runs every ```interval```.
    Args:
        user_id (UUID):
            The id of the user this job belongs to
        interval (timedelta):
            The interval at which this job should run
        (opt) name (str):
            The name given to the job
        (opt) id (UUID):
            A unique job identifier. One will be created automatically if this is none.
        (opt) job_type (str):
            The type of job being run. This is passed to the scheduler.

    Props:
        is_due (bool):
            True if the task is currently due or overdue
        overdue_amount (datetime.timedelta):
            The difference between current time and the due time
        next_run (datetime):
            The next time this job is due to be run
    """
    KEYS = [
        "id",
        "user_id",
        "job_type",
        "interval",
        "last_run",
        "next_run",
    ]

    def __init__(self,
            interval: td,
            user_id, 
            name: str = None, 
            id: UUID = None,
            job_type=None):

        super().__init__(interval, name=name, id=id, job_type=job_type)
        self.user_id: UUID = user_id

    def __getitem__(self, key: str) -> Dict[str, Any]:
        values = [
            self.id,
            self.user_id,
            self.job_type,
            self._interval,
            self._last_run,
            self._next_run,
        ]
        all_attrs = zip(self.KEYS, values)
        return dict(all_attrs)[key]

