from ..interface.progress_interface import ProgressInterface


class Progress(ProgressInterface):
    """
    Mapping to API object for progress
    """

    def __init__(self, nr_of_evaluations: int, nr_of_pareto_points: int):
        self.__nr_of_evaluations = nr_of_evaluations
        self.__nr_of_pareto_points = nr_of_pareto_points

    def get_nr_of_evaluations(self) -> int:
        return self.__nr_of_evaluations

    def get_nr_of_pareto_points(self) -> int:
        return self.__nr_of_pareto_points
