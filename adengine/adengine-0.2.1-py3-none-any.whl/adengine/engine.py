import dataclasses
import multiprocessing as mp
import datetime
import uuid
import tempfile
import logging
import threading
import queue
import asyncio
import functools
import abc
import traceback

from typing import *

from .pt import *

logger = logging.getLogger('adengine.engine')

__all__ = [
    'ActivityData',

    'ADEngine',

    'ADEngineError',
    'TaskIdNotFound',
    'TaskNotCompleted',
    'QueueIsFull',
]


@dataclasses.dataclass(frozen=True)
class Task:
    """This class represents the task for Scheduler."""
    id: str = dataclasses.field(init=False, default_factory=lambda: str(uuid.uuid4()))
    activity: bytes
    password: str
    net_stabilization_delay: int


@dataclasses.dataclass(frozen=True)
class ActivityData:
    """This class represents the result of extracting data."""
    error: ExtractorError
    data: dict


class Startable(abc.ABC):
    """Base class for classes with "stated" method."""

    @abc.abstractmethod
    def started(self) -> bool:
        pass


def check_started(exception_class):
    """Decorator for methods of objects of the classes derived from Startable.
    Runs decorated method only if "started" method returns True, otherwise raises specified exception.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self: Startable, *args, **kwargs):
            if not isinstance(self, Startable):
                raise TypeError(f'Object must be an instance of the class derived from {Startable.__name__}')
            if not self.started():
                raise exception_class()
            else:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator


class SessionWrapper:
    """Wrapper for session in SessionPool."""
    def __init__(self, session_pool: 'SessionPool', session: PacketTracerSession):
        self._session_pool = session_pool
        self._session = session

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session_pool._put(self._session)


class SessionPoolError(Exception):
    """Base SessionPool exception."""
    pass


class SessionPoolNotStarted(SessionPoolError):
    """Exception is raised when SessionPool not started."""
    pass


class SessionPoolEmpty(SessionPoolError):
    """Exception is raised when trying to get session from empty SessionPool."""
    pass


class Executor(threading.Thread):
    """Class for executing functions in separate thread."""

    def __init__(self, event: threading.Event):
        super().__init__(name='TaskExecutor',
                         daemon=True)
        self._task_queue = queue.Queue()
        self._event = event

    def run(self) -> None:
        while not self._event.is_set():
            try:
                task = self._task_queue.get(block=True, timeout=1.0)
            except queue.Empty:
                continue
            else:
                name, func, args, kwargs = task
                try:
                    func(*args, **kwargs)
                except Exception:
                    logger.warning(
                        f'Task {name} raised unexpected error in {self.__class__.__name__}:\n'
                        f'{traceback.format_exc()}')
                else:
                    logger.debug(f'Task {name} finished successfully!')

    def put(self, name: str, func: Callable, args: Iterable = None, kwargs: Mapping = None):
        self._task_queue.put((name, func, args or (), kwargs or dict()))


class SessionPool(Startable):
    """Pool with PacketTracer sessions."""

    def __init__(self, use_virtual_display: bool, tasks_before_session_restart: int):
        self._use_virtual_display = use_virtual_display
        self._tasks_before_session_restart = tasks_before_session_restart

        self._min_size = 1
        self._max_size = mp.cpu_count()

        self._pool = queue.Queue()
        self._sessions = []
        self._event = threading.Event()
        self._executor = Executor(self._event)
        self._tasks_counter = 0

        self._started = False

    def start(self):
        # create first session
        session = PacketTracerSession(use_virtual_display=self._use_virtual_display)
        session.start()
        self._sessions.append(session)
        self._pool.put(session)

        # start executor
        self._event.clear()
        self._executor.start()

        # pool started
        self._started = True

    @check_started(SessionPoolNotStarted)
    def stop(self):
        # pool stopped
        self._started = False

        # stop executor
        self._event.set()
        self._executor.join()

        # stop all sessions
        for session in self._sessions:
            session.stop()

    @check_started(SessionPoolNotStarted)
    def get(self):
        try:
            session = self._pool.get_nowait()
        except queue.Empty:
            raise SessionPoolEmpty()
        else:
            return SessionWrapper(self, session)

    @check_started(SessionPoolNotStarted)
    def _put(self, session: PacketTracerSession):
        def restart_session(_session_pool: SessionPool, _session: PacketTracerSession):
            _session_pool._sessions.remove(session)
            _session.stop()
            _session = PacketTracerSession(use_virtual_display=_session_pool._use_virtual_display)
            _session.start()
            _session_pool._sessions.append(session)
            _session_pool._pool.put(session)

        if self._tasks_counter == self._tasks_before_session_restart:
            self._executor.put('RestartSession', restart_session, (self, session))
            self._tasks_counter = 0
        else:
            self._pool.put(session)

    @check_started(SessionPoolNotStarted)
    def increase_pool(self):
        def _increase_pool(_session_pool: SessionPool):
            if _session_pool.size < self.max_size:
                session = PacketTracerSession(use_virtual_display=_session_pool._use_virtual_display)
                session.start()
                _session_pool._sessions.append(session)
                _session_pool._pool.put(session)

        self._executor.put('IncreasePool', _increase_pool, (self,))

    @check_started(SessionPoolNotStarted)
    def decrease_pool(self):
        def _decrease_pool(_session_pool: SessionPool):
            delay = 1.0
            try:
                session = _session_pool._pool.get(True, delay)
            except queue.Empty:
                logger.debug(f'No sessions reserved in {delay} seconds, abort pool decreasing')
            else:
                if _session_pool.size > _session_pool._min_size:
                    session.stop()
                    self._sessions.remove(session)
                    self._pool.task_done()
                else:
                    logger.debug('Not enough sessions, abort pool decreasing')
                    self._pool.put(session)

        self._executor.put('DecreasePool', _decrease_pool, (self,))

    @property
    def size(self) -> int:
        return len(self._sessions)

    @property
    def max_size(self) -> int:
        return self._max_size

    @property
    def min_size(self):
        return self._min_size

    def started(self) -> bool:
        return self._started


class WorkerPoolError(Exception):
    """Base class for WorkerPool exceptions."""
    pass


class WorkerPoolNotStarted(WorkerPoolError):
    """Exception is raised when trying to call public method when WorkerPool not started,
    but method requires WorkerPool to start."""
    pass


class WorkerPool(threading.Thread, Startable):
    """This class represents pool with workers extracting data from activities."""

    def __init__(self,
                 task_queue: queue.Queue,
                 result_pool: dict,
                 session_pool: SessionPool,
                 read_file_timeout: int,
                 event: threading.Event):
        super().__init__(name=f'WorkerPool-{str(uuid.uuid4())}', daemon=True)
        self._task_queue = task_queue
        self._result_pool = result_pool
        self._session_pool = session_pool
        self._read_file_timeout = read_file_timeout
        self._event = event

    def run(self) -> None:
        # set event loop for current thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # run workers
        asyncio.run(self._run_workers(), debug=True)

    async def _run_workers(self):
        tasks = [asyncio.create_task(self._run_worker(f'Worker-{i}')) for i in range(self._session_pool.max_size)]
        for task in tasks:
            await task

    async def _run_worker(self, worker_name: str):
        while not self._event.is_set():
            # reserve task
            try:
                task = self._task_queue.get_nowait()
            except queue.Empty:
                logger.debug('No tasks in queue')
                await asyncio.sleep(0.1)
                continue

            logger.debug(f'Worker {worker_name} reserved task {task.id}')

            while not self._event.is_set():
                try:
                    with self._session_pool.get() as session:
                        # extract data
                        with tempfile.NamedTemporaryFile('wb') as temp_file:
                            temp_file.write(task.activity)
                            temp_file.flush()

                            try:
                                data = await extract_data(session,
                                                          temp_file.name,
                                                          task.password,
                                                          self._read_file_timeout,
                                                          task.net_stabilization_delay)
                            except ExtractorError as e:
                                error = e
                                data = None
                            else:
                                error = None
                            finish_time = datetime.datetime.now()

                        self._result_pool[task.id] = ActivityData(error, data), finish_time
                        self._task_queue.task_done()

                        logger.debug(f'Task {task.id} completed.')
                except SessionPoolEmpty:
                    await asyncio.sleep(0.1)
                    logger.debug('No available sessions')
                except SessionPoolNotStarted:
                    logger.warning(f'Task {task.id} not completed because session pool stopped')
                    break
                except PacketTracerSessionNotStarted:
                    logger.error(f'Task {task.id} not completed because session stopped')
                    break
                else:
                    break

    def started(self) -> bool:
        return self.is_alive()


class ADEngineError(Exception):
    """Base Scheduler exception."""
    pass


class TaskIdNotFound(ADEngineError):
    """This exception is thrown when task id not found in result pool or in not completed tasks."""
    pass


class TaskNotCompleted(ADEngineError):
    """This exception is thrown when task with requested task id not completed."""
    pass


class QueueIsFull(ADEngineError):
    """This exception is thrown when user it trying to put new task to Scheduler with full queue."""
    pass


class ADEngineNotStarted(ADEngineError):
    """Exception is raised when trying to call public method when ADEngine not started,
    but method requires ADEngine to start."""
    pass


class ADEngine(Startable):
    """Class to control extracting process."""

    def __init__(self,
                 queue_size: int,
                 read_file_timeout: int,
                 use_virtual_display=False,
                 result_ttl=datetime.timedelta(minutes=5),
                 tasks_before_session_restart=100):
        self._task_queue = queue.Queue(maxsize=queue_size)
        self._result_pool = dict()
        self._session_pool = SessionPool(use_virtual_display,
                                         tasks_before_session_restart)
        self._event = threading.Event()
        self._worker_pool = WorkerPool(self._task_queue,
                                       self._result_pool,
                                       self._session_pool,
                                       read_file_timeout,
                                       self._event)
        self._not_completed_tasks = set()
        self._result_ttl = result_ttl
        self._get_lock = threading.Lock()
        self._put_lock = threading.Lock()
        self._result_cleaner = threading.Thread(target=self._clean_result_pool,
                                                name='ResultPoolCleaner',
                                                daemon=True)
        self._session_pool_controller = threading.Thread(target=self._control_session_pool,
                                                         name='SessionPoolController',
                                                         daemon=True)
        self._is_alive = False

    def started(self) -> bool:
        return self._is_alive

    def start(self):
        logger.debug('Starting ADEngine...')
        self._session_pool.start()
        self._worker_pool.start()
        self._result_cleaner.start()
        self._session_pool_controller.start()
        self._is_alive = True
        logger.debug('ADEngine started')

    @check_started(ADEngineNotStarted)
    def stop(self):
        logger.debug('Stopping ADEngine...')
        self._event.set()
        self._worker_pool.join()
        self._session_pool.stop()
        self._result_cleaner.join()
        self._session_pool_controller.join()
        self._is_alive = False
        logger.debug('ADEngine stopped')

    @check_started(ADEngineNotStarted)
    def put(self, activity: bytes, password: str, net_stabilization_delay=0) -> str:
        """Puts task in queue.

        Puts task instance in queue. If the queue is full, raises QueueIsFull exception.

        Args:
            activity: Binary representation of activity file.
            password: Password for activity.
            net_stabilization_delay: Delay for network stabilization.

        Returns:
            If the task is created correctly, returns task id.

        Raises:
            QueueIsFull: when try to put task in full queue.
        """
        with self._put_lock:
            if self._task_queue.full():
                logger.debug(f'Queue of ADEngine is full')
                raise QueueIsFull()

            task = Task(activity, password, net_stabilization_delay)
            self._task_queue.put(task)  # blocking safe process operation
            self._not_completed_tasks.add(task.id)
            logger.debug(f'Created task {task.id}')
            return task.id

    @check_started(ADEngineNotStarted)
    def get(self, task_id: str) -> ActivityData:
        """Gets extraction result from result pool.

        Tries to get a task with provided task id from result poll.\n
        If the task is in work, raises TaskInProgress exception.\n
        If the task is not found in result pool and not on progress, it is considered as unknown task and Scheduler raises
        TaskIdNotFound exception.

        Args:
            task_id: Task ID to get.

        Returns:
            An instance of ActivityData for requested task id.

        Raises:
            TaskNotFoundError: when task id not found.
            TaskNotCompleted: when task is not completed yet.
        """
        with self._get_lock:
            if task_id not in self._not_completed_tasks:
                logger.debug(f'Task {task_id} not found')
                raise TaskIdNotFound()
            elif task_id not in self._result_pool:
                logger.debug(f'Task {task_id} not completed')
                raise TaskNotCompleted()
            else:
                self._not_completed_tasks.remove(task_id)
                logger.debug(f'Return task {task_id}')
                return self._result_pool.pop(task_id)[0]

    def _clean_result_pool(self):
        while not self._event.wait(self._result_ttl.total_seconds()):
            logger.debug('Start cleaning...')

            with self._get_lock:
                results = tuple(self._result_pool.items())

            curr_time = datetime.datetime.now()
            for task_id, (_, finish_time) in results:
                if curr_time - finish_time > self._result_ttl:
                    logger.debug(f'Task {task_id} reached ttl')
                    try:
                        self.get(task_id)
                    except TaskIdNotFound:
                        pass

    def _control_session_pool(self):
        check_loading_delay = 2
        max_tasks_per_session = 5
        while not self._event.wait(check_loading_delay):
            not_completed_tasks = len(self._not_completed_tasks)
            session_pool_size = self._session_pool.size
            tasks_per_session = not_completed_tasks // session_pool_size

            if tasks_per_session > max_tasks_per_session:
                logger.debug(f'{tasks_per_session} tasks per session, try to increase pool')
                self._session_pool.increase_pool()

            elif session_pool_size > 1 and not_completed_tasks // (session_pool_size - 1) <= max_tasks_per_session:
                logger.debug(f'{tasks_per_session} tasks per session, try to decrease pool')
                self._session_pool.decrease_pool()

            else:
                logger.debug(f'{tasks_per_session} tasks per session, load is normal')

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
