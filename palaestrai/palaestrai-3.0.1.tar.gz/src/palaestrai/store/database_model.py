import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import relationship
from palaestrai.store.database_base import Base

"""The database schema provided as Model for SQLAlchemy"""


class ExperimentStudy(Base):
    __tablename__ = "experiment_studies"
    id = sa.Column(sa.INTEGER, primary_key=True, unique=True, index=True)
    name = sa.Column(sa.String, nullable=True)
    study = sa.Column(sa.TEXT)
    experiments = relationship(
        "Experiment", back_populates="experiment_relation"
    )


class Experiment(Base):
    __tablename__ = "experiments"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    name = sa.Column(sa.VARCHAR(255), unique=True, index=True)
    experiment_study_id = sa.Column(
        sa.Integer, sa.ForeignKey(ExperimentStudy.id), index=True
    )
    experiment = sa.Column(sa.TEXT)
    experiment_relation = relationship(
        "ExperimentStudy", back_populates="experiments"
    )
    experiment_runs = relationship(
        "ExperimentRun", back_populates="experiment_run_relation"
    )


class ExperimentRun(Base):
    __tablename__ = "experiment_runs"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    uuid = sa.Column(sa.VARCHAR(255), unique=True, index=True)
    experiment_id = sa.Column(
        sa.Integer, sa.ForeignKey(Experiment.id), index=True
    )
    experiment_run_relation = relationship(
        "Experiment", back_populates="experiment_runs"
    )
    agent_conductors = relationship(
        "AgentConductor", back_populates="agent_conductor_relation"
    )
    simulation_instances = relationship(
        "SimulationInstance", back_populates="simulation_instance_relation"
    )


class SimulationInstance(Base):
    __tablename__ = "simulation_instances"
    id = sa.Column(sa.INTEGER, primary_key=True, unique=True, index=True)
    uuid = sa.Column(sa.VARCHAR(255), unique=True, index=True)
    experiment_run_id = sa.Column(
        sa.Integer, sa.ForeignKey(ExperimentRun.id), index=True
    )
    simulation_instance_relation = relationship(
        "ExperimentRun", back_populates="simulation_instances"
    )
    environment_conductors = relationship(
        "EnvironmentConductor", back_populates="simulation_instance"
    )
    muscles = relationship("Muscle", back_populates="simulation_instance")


class EnvironmentConductor(Base):
    __tablename__ = "environment_conductors"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    uuid = sa.Column(sa.VARCHAR(255), nullable=False, unique=True, index=True)
    type = sa.Column(sa.VARCHAR(255), nullable=True)
    parameters = sa.Column(sa.Text, nullable=True)
    simulation_instance_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(SimulationInstance.id),
        index=True,
    )
    simulation_instance = relationship(
        "SimulationInstance", back_populates="environment_conductors"
    )
    world_states = relationship(
        "WorldState", back_populates="environment_conductor"
    )


class WorldState(Base):
    __tablename__ = "world_states"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    simtime = sa.Column(sa.Integer)
    state_dump = sa.Column(sa.Text)
    is_terminal = sa.Column(
        sa.Boolean,
        unique=False,
        nullable=False,
        default=bool(False),
    )
    environment_conductor_id = sa.Column(
        sa.Integer, sa.ForeignKey(EnvironmentConductor.id), index=True
    )
    environment_conductor = relationship(
        "EnvironmentConductor", back_populates="world_states"
    )


class AgentConductor(Base):
    __tablename__ = "agent_conductors"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    uuid = sa.Column(sa.VARCHAR(255), nullable=False, unique=True, index=True)
    name = sa.Column(sa.VARCHAR(255), nullable=True)
    configuration = sa.Column(sa.LargeBinary, nullable=True)
    experiment_run_id = sa.Column(sa.Integer, sa.ForeignKey(ExperimentRun.id))
    agent_conductor_relation = relationship(
        "ExperimentRun", back_populates="agent_conductors"
    )
    muscles = relationship("Muscle", back_populates="agent_conductor")
    brain = relationship("Brain", back_populates="agent_conductor")


class Brain(Base):
    __tablename__ = "brains"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    parameters = sa.Column(sa.LargeBinary, nullable=True)
    agent_conductor_id = sa.Column(
        sa.Integer, sa.ForeignKey(AgentConductor.id), index=True
    )
    agent_conductor = relationship("AgentConductor", back_populates="brain")
    brain_configs = relationship(
        "BrainConfiguration", back_populates="brain_config_relation"
    )


class BrainConfiguration(Base):
    __tablename__ = "brain_configurations"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    brain_id = sa.Column(sa.Integer, sa.ForeignKey(Brain.id), index=True)
    agent_id = sa.Column(sa.Integer, index=True)
    simtime = sa.Column(sa.Integer)
    parameters = sa.Column(sa.LargeBinary, nullable=True)
    brain_config_relation = relationship(
        "Brain", back_populates="brain_configs"
    )


class Muscle(Base):
    __tablename__ = "muscles"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    agent_conductor_id = sa.Column(
        sa.Integer, sa.ForeignKey(AgentConductor.id), index=True
    )
    simulation_instance_id = sa.Column(
        sa.Integer, sa.ForeignKey(SimulationInstance.id), index=True
    )
    uuid = sa.Column(sa.VARCHAR(255), nullable=False, unique=True, index=True)
    agent_conductor = relationship("AgentConductor", back_populates="muscles")
    simulation_instance = relationship(
        "SimulationInstance", back_populates="muscles"
    )
    muscle_states = relationship(
        "MuscleState", back_populates="muscle_state_relation"
    )
    muscle_actions = relationship("MuscleAction", back_populates="muscle")
    muscle_sensor_readings = relationship(
        "MuscleSensorReading", back_populates="muscle_sensor_reads_relation"
    )


class MuscleState(Base):
    __tablename__ = "muscle_states"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    muscle_id = sa.Column(sa.Integer, sa.ForeignKey(Muscle.id), index=True)
    parameters = sa.Column(sa.LargeBinary, nullable=True)
    muscle_state_relation = relationship(
        "Muscle", back_populates="muscle_states"
    )


class MuscleAction(Base):
    __tablename__ = "muscle_actions"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    simtime = sa.Column(sa.BIGINT)  # TODO: REPLACE, JUST A WORKAROUND
    sensor_readings = sa.Column(sa.Text)
    actuator_information = sa.Column(sa.Text)
    reward = sa.Column(sa.FLOAT)
    muscle_id = sa.Column(sa.Integer, sa.ForeignKey(Muscle.id), index=True)
    muscle = relationship("Muscle", back_populates="muscle_actions")


class MuscleSensorReading(Base):
    __tablename__ = "muscle_sensor_readings"
    id = sa.Column(sa.Integer, primary_key=True, unique=True, index=True)
    active_agent_id = sa.Column(sa.Integer)
    sensor_id = sa.Column(sa.Integer)
    simtime = sa.Column(sa.Integer)
    value = sa.Column(sa.LargeBinary)
    muscle_id = sa.Column(sa.Integer, sa.ForeignKey(Muscle.id), index=True)
    muscle_sensor_reads_relation = relationship(
        "Muscle", back_populates="muscle_sensor_readings"
    )


Model = Base
