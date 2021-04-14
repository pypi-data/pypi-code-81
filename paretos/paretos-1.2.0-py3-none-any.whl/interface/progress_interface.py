class ProgressInterface:
    def get_nr_of_evaluations(self) -> int:
        raise NotImplementedError()

    def get_nr_of_pareto_points(self) -> int:
        raise NotImplementedError()
