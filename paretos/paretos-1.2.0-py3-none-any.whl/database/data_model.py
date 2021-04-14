import uuid

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Table, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import CHAR

DB_VERSION = "db_version_3"

Base = declarative_base()


class TimedTable:
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


def create_uuid() -> str:
    return str(uuid.uuid4())


project_parameters = Table(
    "project_parameters",
    Base.metadata,
    Column("project_id", CHAR(36), ForeignKey("project.id")),
    Column("parameter_id", CHAR(36), ForeignKey("parameter.id")),
)

simulation_values = Table(
    "simulation_values",
    Base.metadata,
    Column("simulation_id", CHAR(36), ForeignKey("simulation.id")),
    Column("parameter_value_id", CHAR(36), ForeignKey("parameter_value.id")),
)


class Project(TimedTable, Base):
    __tablename__ = "project"

    id = Column(
        CHAR(36),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    statusCodeId = Column(CHAR(36), ForeignKey("project_status.id"))

    name = Column(String)

    simulation = relationship("Simulation")

    parameter = relationship(
        "Parameter",
        secondary=project_parameters,
    )


class Simulation(TimedTable, Base):
    __tablename__ = "simulation"

    id = Column(
        CHAR(36),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    status_code_id = Column(CHAR(36), ForeignKey("simulation_status.id"))

    project_id = Column(CHAR(36), ForeignKey("project.id"))

    is_pareto = Column(Boolean)

    values = relationship(
        "ParameterValue",
        secondary=simulation_values,
    )


class SimulationStatus(TimedTable, Base):
    __tablename__ = "simulation_status"

    id = Column(
        CHAR(36), primary_key=True, nullable=False, unique=True, default=create_uuid
    )

    name = Column(String)

    simulation = relationship("Simulation")


class Parameter(TimedTable, Base):
    __tablename__ = "parameter"

    id = Column(
        CHAR(36),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    parameter_type_id = Column(CHAR(36), ForeignKey("parameter_type.id"))

    name = Column(String)

    unit = Column(String)

    options = relationship("ParameterOption", back_populates="parameter")

    type = relationship("ParameterType", back_populates="parameter")

    value = relationship("ParameterValue", back_populates="parameter")


class ParameterType(TimedTable, Base):
    __tablename__ = "parameter_type"

    id = Column(
        CHAR(36), primary_key=True, nullable=False, unique=True, default=create_uuid
    )

    name = Column(String)

    parameter = relationship("Parameter", back_populates="type")


class ParameterValue(TimedTable, Base):
    __tablename__ = "parameter_value"

    id = Column(
        CHAR(36),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    parameter_id = Column(CHAR(36), ForeignKey("parameter.id"))

    number_value = Column(Float)

    parameter = relationship("Parameter", back_populates="value")


class ProjectStatus(TimedTable, Base):
    __tablename__ = "project_status"

    id = Column(
        CHAR(36),
        primary_key=True,
        nullable=False,
        unique=True,
        default=create_uuid,
    )

    name = Column(String)

    project = relationship("Project")


class ParameterOption(TimedTable, Base):
    __tablename__ = "parameter_option"

    id = Column(
        CHAR(36),
        primary_key=True,
        nullable=False,
        unique=True,
    )

    parameter_option_type_id = Column(CHAR(36), ForeignKey("parameter_option_type.id"))

    parameter_id = Column(CHAR(36), ForeignKey("parameter.id"))

    number_value = Column(Float)
    string_value = Column(String)

    type = relationship("ParameterOptionType", back_populates="option")

    parameter = relationship("Parameter", back_populates="options")


class ParameterOptionType(TimedTable, Base):
    __tablename__ = "parameter_option_type"

    id = Column(
        CHAR(36), primary_key=True, nullable=False, unique=True, default=create_uuid
    )

    name = Column(String, unique=True)

    option = relationship("ParameterOption", back_populates="type")


class Version(TimedTable, Base):
    __tablename__ = "version"

    id = Column(
        CHAR(36), primary_key=True, nullable=False, unique=True, default=create_uuid
    )

    name = Column(String, unique=True)
