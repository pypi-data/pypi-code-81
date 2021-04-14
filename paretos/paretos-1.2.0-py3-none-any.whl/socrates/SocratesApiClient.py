from typing import List

from .. import OptimizationProblem, optimization
from ..interface import ProgressInterface
from .SocratesApiHttpSession import SocratesApiHttpSession
from .SocratesRequestMapper import SocratesRequestMapper
from .SocratesResponseMapper import SocratesResponseMapper


class SocratesApiClient(object):
    def __init__(
        self,
        session: SocratesApiHttpSession,
        request_mapper: SocratesRequestMapper,
        response_mapper: SocratesResponseMapper,
    ):
        self.__session = session
        self.__request_mapper = request_mapper
        self.__response_mapper = response_mapper

    def __problem_request(
        self,
        path: str,
        version: str,
        problem: OptimizationProblem,
        evaluations: optimization.Evaluations,
        additional_data: dict = None,
    ):
        if additional_data is None:
            additional_data = {}

        request_evaluations = self.__request_mapper.evaluations_to_request(evaluations)
        request_problem = self.__request_mapper.problem_to_request(problem)

        problem_data = {
            "problem": request_problem,
            "evaluations": request_evaluations,
        }

        data = {**problem_data, **additional_data}

        return self.__session.authenticated_request(
            path=path, version=version, contains_sensitive_data=False, data=data
        )

    # API methods
    def predict_design(
        self,
        problem: OptimizationProblem,
        evaluations: optimization.Evaluations,
        quantity: int,
        version: str = "v1",
    ) -> optimization.design.Designs:
        response = self.__problem_request(
            "design/predict", version, problem, evaluations, {"quantity": quantity}
        )

        designs = self.__response_mapper.predict_response_to_designs(
            problem=problem, response_data=response
        )

        return designs

    def track_progress(
        self,
        problem: OptimizationProblem,
        evaluations: optimization.Evaluations,
        version: str = "v1",
    ) -> ProgressInterface:
        response = self.__problem_request(
            "progress/track", version, problem, evaluations
        )

        progress = self.__response_mapper.track_response_to_progress(
            response_data=response
        )

        return progress

    def get_pareto_optimal_evaluation_ids(
        self,
        problem: OptimizationProblem,
        evaluations: optimization.Evaluations,
        version: str = "v1",
    ) -> List[str]:
        response = self.__problem_request(
            "result/analyze", version, problem, evaluations
        )

        optimal_ids = []

        for evaluation_data in response["evaluations"]:
            evaluation_id = evaluation_data["evaluationId"]
            is_optimal = evaluation_data["isParetoOptimal"]

            if is_optimal:
                optimal_ids.append(evaluation_id)

        return optimal_ids
