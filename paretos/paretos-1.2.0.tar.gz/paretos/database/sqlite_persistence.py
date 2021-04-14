from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from .. import optimization
from . import data_model
from .enums import ProjectStatusEnum
from .exceptions import ProjectAlreadyExists
from .sqlite_database import SQLiteDatabase
from .sqlite_persistence_project_loader import SQLitePersistenceProjectLoader


class SQLitePersistence:
    def __init__(self, database: SQLiteDatabase):
        self.__database = database
        self.__project_loader = SQLitePersistenceProjectLoader(database=database)

    def __project_exists(self, session: Session, project_name: str):
        count = (
            session.query(data_model.Project)
            .filter(data_model.Project.name == project_name)
            .count()
        )

        return count > 0

    def save_project(self, project: optimization.Project):
        session = self.__database.begin()
        project_name = project.get_name()
        project_id = project.get_id()

        if self.__project_exists(session=session, project_name=project_name):
            raise ProjectAlreadyExists()

        self.__database.add_project(
            session=session, project_name=project_name, project_id=project_id
        )

        problem = project.get_optimization_problem()

        self.__database.add_project_meta(
            session=session, project_id=project_id, problem=problem
        )

        session.commit()
        session.close()

    def save_planned_evaluations(
        self, evaluations: List[optimization.Evaluation], project: optimization.Project
    ):
        session = self.__database.begin()

        for evaluation in evaluations:
            project_id = project.get_id()
            simulation_id = evaluation.get_id()
            design = evaluation.get_design()
            kpis = evaluation.get_kpis()

            self.__database.add_simulation_design(
                session=session,
                project_id=project_id,
                simulation_id=simulation_id,
                design_values=design,
            )

            if kpis is not None:
                self.__database.add_simulation_kpis(
                    session=session, simulation_id=simulation_id, kpi_values=kpis
                )

        session.commit()
        session.close()

    def update_project_status(self, project):
        session = self.__database.begin()
        project_id = project.get_id()

        if isinstance(project.get_status(), optimization.project_status.Done):
            status = ProjectStatusEnum.set.value
        else:
            raise RuntimeError("Unexpected new Project status.")

        self.__database.update_project_status(
            session, project_id=project_id, status=status
        )

        session.commit()
        session.close()

    def update_evaluation_add_kpis(self, evaluation):
        session = self.__database.begin()
        simulation_id = evaluation.get_id()
        kpi_values = evaluation.get_kpis()

        if kpi_values is None:
            raise RuntimeError("No KPIs to update.")

        self.__database.add_simulation_kpis(
            session=session, simulation_id=simulation_id, kpi_values=kpi_values
        )

        session.commit()
        session.close()

    def update_evaluation_pareto_states(self, evaluations: optimization.Evaluations):
        session = self.__database.begin()

        for evaluation in evaluations.get_evaluations():
            db_evaluation = self.__database.get_simulation(session, evaluation.get_id())
            db_evaluation.is_pareto = evaluation.is_pareto_optimal()

        session.commit()
        session.close()

    def load_project_data_by_name(
        self, project_name: str
    ) -> Tuple[Optional[optimization.Project], optimization.Evaluations]:
        return self.__project_loader.load_project_data_by_name(
            project_name=project_name
        )
