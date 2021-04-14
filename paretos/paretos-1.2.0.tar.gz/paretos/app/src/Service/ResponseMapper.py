from typing import Dict, List

from ....optimization import Evaluations, OptimizationProblem
from ....optimization.design.continuity import Discrete
from ....optimization.goals import Maximum, Minimum


class DataApiResponseMapper:
    @staticmethod
    def evaluations_to_request(evaluations: Evaluations) -> List[Dict]:
        request_evaluations = []

        for evaluation in evaluations.get_evaluations():
            design = evaluation.get_design()

            request_designs = []
            request_kpis = []

            for design_value in design.get_values():
                request_design_value = {
                    "id": design_value.get_parameter().get_id(),
                    "value": design_value.get_value(),
                }

                request_designs.append(request_design_value)

            for kpi in evaluation.get_kpis():
                request_kpi = {
                    "id": kpi.get_parameter().get_id(),
                    "value": kpi.get_value(),
                }

                request_kpis.append(request_kpi)

            request_evaluation = {
                "id": evaluation.get_id(),
                "design": request_designs,
                "kpis": request_kpis,
            }

            request_evaluations.append(request_evaluation)

        return request_evaluations

    @staticmethod
    def problem_to_request(problem: OptimizationProblem) -> Dict:
        design_space = problem.get_design_space()
        kpi_space = problem.get_kpi_space()

        request_design = []
        request_kpis = []

        for design_parameter in design_space:
            continuity = "continuous"

            if type(design_parameter.get_continuity()) is Discrete:
                continuity = "discrete"

            request_design_parameter = {
                "id": design_parameter.get_id(),
                "name": design_parameter.get_name(),
                "minimum": design_parameter.get_minimum(),
                "maximum": design_parameter.get_maximum(),
                "continuity": continuity,
            }

            request_design.append(request_design_parameter)

        for kpi in kpi_space:
            goal = kpi.get_goal()

            if isinstance(goal, Minimum):
                request_goal = "minimize"
            elif isinstance(goal, Maximum):
                request_goal = "maximize"
            else:
                raise RuntimeError("Unexpected Goal type.")

            request_kpi = {
                "id": kpi.get_id(),
                "name": kpi.get_name(),
                "goal": request_goal,
            }

            request_kpis.append(request_kpi)

        return {"design": request_design, "kpis": request_kpis}
