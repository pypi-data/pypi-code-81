from .progress_interface import ProgressInterface
from .terminator_interface import TerminatorInterface


class RunTerminator(TerminatorInterface):
    def __init__(self, number_of_runs: int):
        self.__number_of_runs = number_of_runs

    def should_terminate(self, progress: ProgressInterface) -> bool:
        if self.__number_of_runs <= progress.get_nr_of_evaluations():
            return True

        return False
