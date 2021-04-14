from typing import Dict, List, Optional

from . import (
    CONTINUITY_DISCRETE,
    EnvironmentInterface,
    KpiGoalMaximum,
    KpiGoalMinimum,
    OptimizationProblem,
    OptimizationResultInterface,
    TerminatorInterface,
    optimization,
)
from .app.run import run as show_dashboard
from .config import Config
from .database.exceptions import ProjectAlreadyExists
from .database.sqlite_database import SQLiteDatabase
from .database.sqlite_persistence import SQLitePersistence
from .exceptions import KpiNotFoundInEvaluationResult, ProjectNotFoundError
from .export import OptimizationResult
from .exporter import export
from .socrates.SocratesApiClient import SocratesApiClient
from .socrates.SocratesApiHttpSession import SocratesApiHttpSession
from .socrates.SocratesRequestMapper import SocratesRequestMapper
from .socrates.SocratesResponseMapper import SocratesResponseMapper


class Paretos:
    def __init__(self, config: Config):
        self.__logger = config.get_logger()
        self.__data_source_name = config.get_data_source_name()

        self.__persistence = self.__connect_persistence(
            data_source_name=self.__data_source_name
        )

        self.__config = config

        api_session = SocratesApiHttpSession(
            api_url=config.get_api_url(),
            customer_token=config.get_customer_token(),
            logger=self.__logger,
        )

        request_mapper = SocratesRequestMapper()
        response_mapper = SocratesResponseMapper()

        self.__api_client = SocratesApiClient(
            session=api_session,
            request_mapper=request_mapper,
            response_mapper=response_mapper,
        )

    def optimize(
        self,
        name: str,
        optimization_problem: OptimizationProblem,
        environment: EnvironmentInterface,
        terminators: Optional[List[TerminatorInterface]] = None,
        n_parallel: int = 1,
        max_number_of_runs: int = 10000,
        resume: bool = False,
    ) -> None:
        """
        Main function the user calls when optimizing with socrates
        :param name: project name which will be added to database then!
        :param optimization_problem: hyper space definition of the problem
        :param environment: simulation environment to use for the execution
            :param terminators: list of all terminator functions which can lead to stop
        :param n_parallel: Number of parallel simulations that can be run on customer side
        :param max_number_of_runs: Absolute maximum to have hard stopping criteria
        :param resume: Set to true to resume the optimization if it already exists.
        """

        project = None
        done_evaluations = optimization.Evaluations()
        planned_evaluations = []

        if resume:
            (
                project,
                previous_evaluations,
            ) = self.__persistence.load_project_data_by_name(project_name=name)

            for previous_evaluation in previous_evaluations.get_evaluations():
                # TODO: simulation status instead of empty kpis
                if previous_evaluation.get_kpis() is None:
                    planned_evaluations.append(previous_evaluation)
                else:
                    done_evaluations.add_evaluation(evaluation=previous_evaluation)

        if project is None:
            problem = self.__create_problem_definition(optimization_problem)
            project = optimization.Project(name=name, problem=problem)

            try:
                self.__persistence.save_project(project)
            except ProjectAlreadyExists as already_exists_error:
                self.__logger.error(
                    msg="Project already exists. Set the resume parameter to continue "
                    "an already started project or use a different project name.",
                    extra={"project_name": project.get_name()},
                )

                raise already_exists_error

            self.__logger.info(
                "Started optimization project.",
                extra={
                    "projectId": project.get_id(),
                    "projectName": project.get_name(),
                },
            )
        else:
            self.__logger.info(
                "Resuming project.", extra={"projectName": project.get_name()}
            )

        if terminators is None:
            terminators = [optimization.DefaultTerminator()]

        self.__optimize(
            project=project,
            done_evaluations=done_evaluations,
            planned_evaluations=planned_evaluations,
            terminators=terminators,
            max_number_of_runs=max_number_of_runs,
            n_parallel=n_parallel,
            environment=environment,
        )

    def obtain(self, name: str) -> OptimizationResultInterface:
        done_evaluations = optimization.Evaluations()

        project, previous_evaluations = self.__persistence.load_project_data_by_name(
            project_name=name
        )

        if project is None:
            self.__logger.error("Project not found.", extra={"projectName": name})

            raise ProjectNotFoundError()

        if not isinstance(project.get_status(), optimization.project_status.Done):
            self.__logger.warning(
                "Optimization was not finished correctly, data might be incomplete."
            )

        for previous_evaluation in previous_evaluations.get_evaluations():
            if previous_evaluation.get_kpis() is not None:
                done_evaluations.add_evaluation(evaluation=previous_evaluation)

        return OptimizationResult(done_evaluations)

    def export(self, name: str) -> List[Dict]:
        return export(data_source_name=self.__data_source_name, project_name=name)

    def __create_problem_definition(
        self, definition: OptimizationProblem
    ) -> optimization.OptimizationProblem:

        design_parameters = []
        kpi_parameters = []

        for definition_kpi_parameter in definition.get_kpi_parameters():
            name = definition_kpi_parameter.get_name()
            goal_string = definition_kpi_parameter.get_goal()

            if goal_string == KpiGoalMinimum:
                parameter_goal = optimization.goals.Minimum()
            elif goal_string == KpiGoalMaximum:
                parameter_goal = optimization.goals.Maximum()
            else:
                raise RuntimeError("Unexpected KPI parameter goal.")

            kpi_parameter = optimization.kpi.KpiParameter(
                name=name, goal=parameter_goal
            )

            kpi_parameters.append(kpi_parameter)

        for definition_design_parameter in definition.get_design_parameters():
            interface_continuity = definition_design_parameter.get_continuity()
            continuity = optimization.design.continuity.Continuous()

            if interface_continuity == CONTINUITY_DISCRETE:
                continuity = optimization.design.continuity.Discrete()

            design_parameter = optimization.design.DesignParameter(
                name=definition_design_parameter.get_name(),
                minimum=definition_design_parameter.get_minimum(),
                maximum=definition_design_parameter.get_maximum(),
                continuity=continuity,
            )

            design_parameters.append(design_parameter)

        design_space = optimization.design.DesignSpace(design_parameters)
        kpi_space = optimization.kpi.KpiSpace(kpi_parameters)

        return optimization.OptimizationProblem(
            design_space=design_space, kpi_space=kpi_space
        )

    @staticmethod
    def __connect_persistence(data_source_name: str):
        database = SQLiteDatabase(data_source_name=data_source_name)
        # TODO: version check here
        return SQLitePersistence(database=database)

    def __clean_kpis(
        self,
        dirty_kpis: Dict[str, float],
        kpi_space: optimization.kpi.KpiSpace,
        evaluation_uuid: str,
    ) -> optimization.kpi.KpiValues:
        clean_kpis = []

        for kpi in kpi_space:
            name = kpi.get_name()

            if name not in dirty_kpis:
                self.__logger.error(
                    msg="KPI missing in evaluation result.",
                    extra={"kpi_name": name, "evaluation_uuid": evaluation_uuid},
                )

                raise KpiNotFoundInEvaluationResult(
                    f"KPI {name} missing in evaluation result."
                )

            value = dirty_kpis[name]

            if not isinstance(value, float):
                self.__logger.error(
                    msg="Evaluation result contains invalid types.",
                    extra={
                        "kpi_name": name,
                        "type": str(type(value)),
                        "evaluation_uuid": evaluation_uuid,
                    },
                )

                raise TypeError(
                    "Evaluation result contains invalid type. "
                    "Results have to be an instance of float."
                )

            clean_kpi = optimization.parameter.ParameterValue(kpi, value)

            clean_kpis.append(clean_kpi)

        return optimization.kpi.KpiValues(clean_kpis)

    def __optimize(
        self,
        project: optimization.Project,
        done_evaluations: optimization.Evaluations,
        planned_evaluations: List[optimization.Evaluation],
        terminators: List[TerminatorInterface],
        max_number_of_runs: int,
        n_parallel: int,
        environment: EnvironmentInterface,
    ):
        problem = project.get_optimization_problem()

        try:
            progress = self.__api_client.track_progress(problem, done_evaluations)
        except Exception as api_tracking_error:
            self.__logger.error("Unable to update optimization progress.")
            raise api_tracking_error

        nr_of_runs = 0

        while (
            not any(
                [terminator.should_terminate(progress) for terminator in terminators]
            )
            and nr_of_runs < max_number_of_runs
        ):
            nr_of_runs += 1

            if len(planned_evaluations) == 0:
                designs = self.__api_client.predict_design(
                    problem=problem, evaluations=done_evaluations, quantity=n_parallel
                )

                self.__logger.info(
                    "Fetched new designs from Socrates API.",
                    extra={"count": len(designs.get_designs())},
                )

                for design in designs:
                    evaluation = optimization.Evaluation(design=design)

                    planned_evaluations.append(evaluation)

                self.__persistence.save_planned_evaluations(
                    planned_evaluations, project
                )

            for evaluation in planned_evaluations:
                design_values = evaluation.get_design().to_dict()

                self.__logger.info(
                    "Starting evaluation.",
                    extra={
                        "evaluationId": evaluation.get_id(),
                        "design": design_values,
                    },
                )

                try:
                    dirty_kpis = environment.evaluate(design_values=design_values)
                except Exception as simulation_exception:
                    self.__logger.error(
                        "Evaluation failed.",
                        extra={"evaluationId": evaluation.get_id()},
                    )

                    raise simulation_exception

                try:
                    self.__logger.info(
                        "Evaluation successful.",
                        extra={"evaluationId": evaluation.get_id(), "kpis": dirty_kpis},
                    )
                except TypeError:
                    # something unserializable in dirty_kpis, ignore
                    pass

                kpis = self.__clean_kpis(
                    dirty_kpis=dirty_kpis,
                    kpi_space=problem.get_kpi_space(),
                    evaluation_uuid=evaluation.get_id(),
                )

                evaluation.add_result(kpis)

                done_evaluations.add_evaluation(evaluation)

                try:
                    self.__persistence.update_evaluation_add_kpis(evaluation=evaluation)
                except Exception as database_error:
                    self.__logger.error("Saving evaluation result failed.")
                    raise database_error

            self.__logger.info("Batch of designs done.")

            planned_evaluations = []

            try:
                progress = self.__api_client.track_progress(problem, done_evaluations)
            except Exception as api_tracking_error:
                self.__logger.error("Unable to update optimization progress.")
                raise api_tracking_error

            self.__logger.info(
                "Analyzed current progress.",
                extra={
                    "evaluations": len(done_evaluations.get_evaluations()),
                    "paretoPoints": progress.get_nr_of_pareto_points(),
                },
            )

        self.__logger.info("Optimization finished.")

        project.finish()

        try:
            self.__persistence.update_project_status(project)
        except Exception as project_status_update_failed:
            self.__logger.error("Unable to set project to finished.")
            raise project_status_update_failed

        self.__logger.info("Analyzing result.")

        pareto_optimal_ids = self.__api_client.get_pareto_optimal_evaluation_ids(
            problem, done_evaluations
        )

        for evaluation in done_evaluations.get_evaluations():
            is_pareto_optimal = evaluation.get_id() in pareto_optimal_ids
            evaluation.update_pareto_optimality(is_pareto_optimal)

        self.__persistence.update_evaluation_pareto_states(done_evaluations)

        self.__logger.info(
            "Result analyzed.",
            extra={
                "evaluations": len(done_evaluations.get_evaluations()),
                "paretoPoints": len(done_evaluations.get_pareto_optimal_evaluations()),
            },
        )

    def show(self):
        show_dashboard(self.__config)
