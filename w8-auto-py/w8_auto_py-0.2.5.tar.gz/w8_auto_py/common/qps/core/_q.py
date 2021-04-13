# @Time     : 2021/3/26
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import enum

from w8_auto_py.typings import NumberTypes
from w8_auto_py.global_vars import TimeUnit
from w8_auto_py.common.qps import AbstractQueryPerSecond, QpsCounter, QpsTimer


class RunStates(enum.Enum):
    """
    运行状态
    """
    STOP, START, PAUSE = range(3)  # 0 stop, 1 start 2 pause


class QueryPreSecond(AbstractQueryPerSecond):

    def __init__(self, timeout: NumberTypes, date_unit: TimeUnit = TimeUnit.MS):
        """

        Args:
            timeout:        超时时间
            date_unit:      时间单位
        """

        self.__st: NumberTypes = 0  # 开始时间
        self.__states: RunStates = RunStates.STOP  # 运行状态
        self.__timeout = timeout  # 超时时间
        self._counter = QpsCounter(0)  # 计数器
        self._timer = QpsTimer(date_unit)  # 计时器

    @property
    def counter(self):
        return self._counter

    @property
    def timer(self):
        return self._timer

    @property
    def is_start(self) -> bool:
        """
        是否开始
        Returns:

        """
        return self.__states == RunStates.START

    def auto_increment(self) -> None:
        """
        自增
        Returns:

        """
        if not self.is_start:
            return
        self.counter.increment(1)

    def clear(self) -> None:
        """
        清零
        Returns:

        """
        # 清除超时、计数
        self.timer.clear()
        self.counter.clear()

    def start(self) -> None:
        if not self.is_start:
            self.__states = RunStates.START
            # 获取开始时间
            self._set_st(self.timer.get_current())

    def restart(self) -> None:
        """
        重新开始
        Returns:

        """
        self.clear()
        self._set_st(self.timer.get_current())

    def stop(self) -> None:
        self.__states = RunStates.STOP

    def _output_log(self) -> None:
        logger.warning(f"current qps: {self.counter.count}/s")

    def _set_st(self, current: NumberTypes) -> None:
        """
        更新开始时间
        Args:
            current:

        Returns:

        """
        if not isinstance(current, (int, float)):
            return
        self.__st = current

    def _set_timeout(self) -> None:
        """
        设置超时
        Returns:

        """
        if self.timer.get_current() - self.__st >= self.__timeout:
            self.timer.set_timeout()

    def __call__(self, *args, **kwargs) -> None:
        self.run()

    def run(self):
        self.start()
        self.auto_increment()
        self._set_timeout()

        if self.timer.is_timeout:
            self._output_log()
            self.restart()
