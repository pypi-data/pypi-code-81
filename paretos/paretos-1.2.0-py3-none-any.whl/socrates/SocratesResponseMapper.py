from .. import optimization


class SocratesResponseMapper:
    @staticmethod
    def analyze_response_to_evaluations(
        response_data: dict,
    ) -> optimization.results.AnalyzedEvaluations:
        analyzed_evaluations = []

        for evaluation_data in response_data["evaluations"]:
            id_ = evaluation_data["evaluationId"]
            is_pareto_optimal = evaluation_data["isParetoOptimal"]
            analyzed_evaluation = optimization.results.AnalyzedEvaluation(
                id=id_, is_pareto_optimal=is_pareto_optimal
            )
            analyzed_evaluations.append(analyzed_evaluation)

        return optimization.results.AnalyzedEvaluations(
            analyzed_evaluations=analyzed_evaluations
        )

    @staticmethod
    def predict_response_to_designs(
        problem: optimization.OptimizationProblem, response_data: dict
    ) -> optimization.design.Designs:
        design_values = []

        # TODO: validate response data structure
        for design_data in response_data["designs"]:
            parameter_values = []

            for design_value in design_data:
                id_ = design_value["id"]
                value = design_value["value"]

                # TODO: handle id mismatch
                parameter = problem.get_design_space().get_parameter_by_id(id_)

                parameter_value = optimization.parameter.ParameterValue(
                    parameter=parameter, value=value
                )
                parameter_values.append(parameter_value)

            design = optimization.design.DesignValues(values=parameter_values)

            design_values.append(design)

        return optimization.design.Designs(designs=design_values)

    @staticmethod
    def track_response_to_progress(response_data: dict) -> optimization.Progress:
        # TODO: type plucking from response object
        nr_of_evaluations = response_data["nrOfEvaluations"]
        nr_of_pareto_points = response_data["nrOfParetoPoints"]

        return optimization.Progress(
            nr_of_evaluations=nr_of_evaluations, nr_of_pareto_points=nr_of_pareto_points
        )
