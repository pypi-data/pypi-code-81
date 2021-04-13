import io
import uuid
import unittest
import numpy as np
from unittest import TestCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import palaestrai.store.database_model as model


class TestDatabaseModel(TestCase):
    _URI = "sqlite://"

    def setUp(self):
        self._engine = create_engine(TestDatabaseModel._URI)
        model.Base.metadata.bind = self._engine
        self._Session = sessionmaker(bind=self._engine)
        self._session = self._Session()

    def tearDown(self) -> None:
        self.store.close()

    @property
    def store(self):
        return self._session

    def test_create(self):
        try:
            model.Base.metadata.create_all()
        except Exception as e:
            self.fail(
                "model.Base.metadata.create_all() must not raise: %s" % e
            )

    def test_add(self):
        """
        Tests addition with all relevant relationships, confirming
        the schema
        """
        model.Base.metadata.create_all()

        experiment_study_entity = model.ExperimentStudy(
            name="Test", study="many things"
        )
        experiment_1 = model.Experiment(experiment="many more things")
        experiment_2 = model.Experiment(experiment="many more things again")

        experiment_study_entity.experiments.append(experiment_1)
        experiment_study_entity.experiments.append(experiment_2)

        experiment_run_entity = model.ExperimentRun(uuid=str(uuid.uuid4()))
        experiment_1.experiment_runs.append(experiment_run_entity)

        agent_conductor_entity = model.AgentConductor(
            uuid="Momzobo", name="the greatest conductor"
        )
        experiment_run_entity.agent_conductors.append(agent_conductor_entity)

        brain_entity = model.Brain(parameters=np.random.rand(3, 7))
        agent_conductor_entity.brain.append(brain_entity)

        brain_config_entity = model.BrainConfiguration(
            agent_id="0815", simtime=1387, parameters=np.random.rand(2, 4)
        )
        brain_entity.brain_configs.append(brain_config_entity)

        simulation_instance_entity = model.SimulationInstance(
            uuid=str(uuid.uuid4())
        )
        experiment_run_entity.simulation_instances.append(
            simulation_instance_entity
        )

        environment_conductor_entity = model.EnvironmentConductor(
            uuid="Test Environment Conductor"
        )
        simulation_instance_entity.environment_conductors.append(
            environment_conductor_entity
        )

        muscle_entity = model.Muscle(uuid="MuscleRoaar")
        agent_conductor_entity.muscles.append(muscle_entity)
        simulation_instance_entity.muscles.append(muscle_entity)

        muscle_states_entity = model.MuscleState(
            parameters=np.random.rand(3, 2)
        )
        muscle_entity.muscle_states.append(muscle_states_entity)

        muscle_actions_entity = model.MuscleAction(
            simtime=19786,
            actuator_information=np.zeros((2, 7)),
        )
        muscle_entity.muscle_actions.append(muscle_actions_entity)

        muscle_sensor_readings_entity = model.MuscleSensorReading(
            active_agent_id=42,
            sensor_id=13,
            simtime=19786,
            value=np.random.rand(7),
        )
        muscle_entity.muscle_sensor_readings.append(
            muscle_sensor_readings_entity
        )

        world_states_entity = model.WorldState(
            simtime=19786,
            state_dump=np.random.rand(5, 7),
        )
        environment_conductor_entity.world_states.append(world_states_entity)
        self.store.add(world_states_entity)
        self.store.commit()
        try:
            run_e = self.store.query(model.ExperimentRun).one()
        except Exception as e:
            self.fail("Query.one must succeed, but raised: %s" % e)

    def test_query_by_experiment_run_id(self):
        self.test_add()
        try:
            run_e: model.ExperimentRun = self.store.query(
                model.ExperimentRun
            ).one()
        except Exception as e:
            self.fail("Query.one must succeed, but raised: %s" % e)
        ety = (
            self.store.query(
                model.ExperimentRun,
                model.SimulationInstance,
                model.MuscleState,
            )
            .join(model.SimulationInstance)
            .join(model.Muscle)
            .join(model.MuscleState)
        )
        try:
            param = ety.one()[2].parameters
        except Exception as e:
            self.fail("Query.join.one must succeed, but raised: %s" % e)
        self.assertEqual(np.frombuffer(param).shape, (6,))


if __name__ == "__main__":
    unittest.main()
