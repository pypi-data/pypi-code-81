from uuid import uuid4

import sqlalchemy_utils
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import Session, sessionmaker

from paretos.database.enums import (
    ContinuityOptions,
    ParameterOptions,
    ParameterTypes,
    ProjectStatusEnum,
    SimulationStatusEnum,
)

# import package models namespaced to avoid conflicts
from .. import optimization as o
from ..exceptions import InitializationError
from .data_model import (
    DB_VERSION,
    Base,
    Parameter,
    ParameterOption,
    ParameterOptionType,
    ParameterType,
    ParameterValue,
    Project,
    ProjectStatus,
    Simulation,
    SimulationStatus,
    Version,
)


class SQLiteDatabase(object):
    """
    Class to connect database and get / post values
    """

    def __init__(self, data_source_name: str):
        create_database = not sqlalchemy_utils.database_exists(data_source_name)

        self.__engine = create_engine(data_source_name)

        if create_database:
            Base.metadata.create_all(self.__engine)

        self.__session_maker = sessionmaker(bind=self.__engine)

        if not create_database and not self.__is_current_version():
            raise InitializationError(
                "Current DB version incompatible. Change DB path."
            )

        if create_database:
            self.__set_init_db_data()

    def begin(self) -> Session:
        return self.__session_maker()

    def __set_init_db_data(self):
        session = self.begin()

        version = Version(name=DB_VERSION)

        session.add(version)

        for project_status in ProjectStatusEnum:
            ps = ProjectStatus(name=project_status.value)

            session.add(ps)

        for parameter_option in ParameterOptions:
            ct = ParameterOptionType(name=parameter_option.value)

            session.add(ct)

        for simulation_status in SimulationStatusEnum:
            ss = SimulationStatus(name=simulation_status.value)

            session.add(ss)

        for parameter_type in ParameterTypes:
            pt = ParameterType(name=parameter_type.value)

            session.add(pt)

        session.commit()
        session.close()

    def __is_current_version(self):
        session = self.begin()

        most_current_version = (
            session.query(Version).order_by(desc(Version.time_created)).first()
        )

        session.close()

        return most_current_version.name == DB_VERSION

    def add_project(
        self,
        session: Session,
        project_id: str,
        project_name: str,
    ):
        project = Project(
            id=project_id,
            # USE Enum here as well
            statusCodeId=session.query(ProjectStatus)
            .filter(ProjectStatus.name == ProjectStatusEnum.initialized.name)
            .first()
            .id,
            name=project_name,
        )

        session.add(project)

    def __build_db_parameter(self, session: Session, parameter: o.parameter.Parameter):
        if isinstance(parameter, o.design.DesignParameter):
            parameter_type = ParameterTypes.design.value
        elif isinstance(parameter, o.kpi.KpiParameter):
            parameter_type = ParameterTypes.kpi.value
        else:
            raise RuntimeError("Unexpected Parameter type.")

        return Parameter(
            id=parameter.get_id(),
            parameter_type_id=session.query(ParameterType)
            .filter(ParameterType.name == parameter_type)
            .first()
            .id,
            name=parameter.get_name(),
        )

    def __add_db_parameter_value(
        self, session: Session, parameter_value: o.parameter.ParameterValue
    ) -> ParameterValue:
        parameter_id = parameter_value.get_parameter().get_id()
        value = parameter_value.get_value()
        parameter_value_id = str(uuid4())

        parameter_value = ParameterValue(
            id=parameter_value_id,
            parameter_id=parameter_id,
            number_value=value,
        )

        session.add(parameter_value)

        return parameter_value

    def add_project_meta(
        self, session: Session, project_id: str, problem: o.OptimizationProblem
    ):
        project = session.query(Project).filter(Project.id == project_id).first()

        for design_param in problem.get_design_space():
            design_db_param = self.__build_db_parameter(
                session=session, parameter=design_param
            )

            minimum = design_param.get_minimum()
            maximum = design_param.get_maximum()
            minimum_option = ParameterOption(
                id=str(uuid4()),
                parameter_option_type_id=session.query(ParameterOptionType)
                .filter(ParameterOptionType.name == ParameterOptions.minimum.name)
                .first()
                .id,
                number_value=minimum,
            )

            design_db_param.options.append(minimum_option)

            maximum_option = ParameterOption(
                id=str(uuid4()),
                parameter_option_type_id=session.query(ParameterOptionType)
                .filter(ParameterOptionType.name == ParameterOptions.maximum.name)
                .first()
                .id,
                number_value=maximum,
            )

            design_db_param.options.append(maximum_option)

            continuity_type = type(design_param.get_continuity())

            if continuity_type is o.design.continuity.Continuous:
                db_continuity = ContinuityOptions.continuous.value
            elif continuity_type is o.design.continuity.Discrete:
                db_continuity = ContinuityOptions.discrete.value
            else:
                raise RuntimeError("Unexpected continuity type.")

            continuity_option = ParameterOption(
                id=str(uuid4()),
                parameter_option_type_id=session.query(ParameterOptionType)
                .filter(ParameterOptionType.name == ParameterOptions.continuity.value)
                .first()
                .id,
                string_value=db_continuity,
            )

            design_db_param.options.append(continuity_option)

            project.parameter.append(design_db_param)

        for kpi_param in problem.get_kpi_space():
            kpi_db_param = self.__build_db_parameter(
                session=session, parameter=kpi_param
            )

            goal = kpi_param.get_goal()

            if isinstance(goal, o.goals.Minimum):
                goal_name = ParameterOptions.goal.minimum.value
            elif isinstance(goal, o.goals.Maximum):
                goal_name = ParameterOptions.goal.maximum.value
            else:
                raise RuntimeError("Unexpected goal type.")

            goal_option = ParameterOption(
                id=str(uuid4()),
                parameter_option_type_id=session.query(ParameterOptionType)
                .filter(ParameterOptionType.name == ParameterOptions.goal.value)
                .first()
                .id,
                string_value=goal_name,
            )

            kpi_db_param.options.append(goal_option)

            project.parameter.append(kpi_db_param)

    def add_simulation(self, session: Session, simulation_id: str, project_id: str):
        simulation = Simulation(
            id=simulation_id,
            status_code_id=session.query(SimulationStatus)
            .filter(SimulationStatus.name == SimulationStatusEnum.predicted.name)
            .first()
            .id,
            project_id=project_id,
            is_pareto=False,
        )

        session.add(simulation)

    def add_simulation_design(
        self,
        session: Session,
        project_id,
        simulation_id: str,
        design_values: o.design.DesignValues,
    ) -> str:
        simulation = Simulation(
            id=simulation_id,
            status_code_id=session.query(SimulationStatus)
            .filter(SimulationStatus.name == SimulationStatusEnum.predicted.name)
            .first()
            .id,
            project_id=project_id,
            is_pareto=False,
        )

        for design_value in design_values:
            parameter_value = self.__add_db_parameter_value(
                session=session, parameter_value=design_value
            )

            simulation.values.append(parameter_value)

        session.add(simulation)

        return simulation.id

    def get_simulation(self, session: Session, simulation_id: str):
        return session.query(Simulation).filter(Simulation.id == simulation_id).first()

    def add_simulation_kpis(
        self, session: Session, simulation_id: str, kpi_values: o.kpi.KpiValues
    ):
        simulation = self.get_simulation(session=session, simulation_id=simulation_id)

        for kpi_value in kpi_values:
            parameter_value = self.__add_db_parameter_value(
                session=session, parameter_value=kpi_value
            )

            simulation.values.append(parameter_value)

        status = (
            session.query(SimulationStatus)
            .filter_by(name=SimulationStatusEnum.completed.value)
            .one_or_none()
        )

        if status is None:
            raise ValueError("Unable to update project status.")

        simulation.status_code_id = status.id

    def get_all_simulation_data(self, project_id: str):
        raise NotImplementedError

    def update_project_status(self, session: Session, project_id: str, status: str):
        project = session.query(Project).filter(Project.id == project_id).first()

        status_id = (
            session.query(ProjectStatus).filter(ProjectStatus.name == status).first().id
        )

        project.statusCodeId = status_id
