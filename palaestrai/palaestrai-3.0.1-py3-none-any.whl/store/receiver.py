import json
import logging
import os
import queue
import threading
import time
import uuid
import zlib
from io import StringIO

import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy
import ruamel.yaml as yml
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.exc
import sqlalchemy.orm

import palaestrai.core.MDP as MDP
import palaestrai.core.protocol as proto
from palaestrai.core import RuntimeConfig
from palaestrai.core.serialisation import deserialize
from . import LOG
from . import database_model as dbm


class StoreReceiver(threading.Thread):
    """The message receiver of the palaestrAI store.

    The store hooks into the global communication, reading every message that
    is being exchanged between :class:`Executor`, :class:`RunGovernor`,
    :class:`AgentConductor`, :class:`Environment`, :class:`Brain`, and
    :class:`Muscle` instances. From these messages, it reads all relevant
    status informtion in order to relay them to the store database for later
    analysis of experiments.
    """

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = queue
        self._running = True
        self._uid = uuid.uuid4()
        self._db_engine = None
        self._db_session_maker = None
        self._db_session = None
        self._log_store_fh = None
        self._worlds_state_sensors = []  # Which sensors carry the world state
        # we know from the experiment object.
        self._message_dispatch = {
            proto.ExperimentStartRequest: self._write_experiment,
            proto.SimulationStartRequest: self._write_simulation_instance,
            proto.EnvironmentSetupRequest: None,
            proto.EnvironmentSetupResponse: self._write_environment,
            proto.EnvironmentStartRequest: None,
            proto.ExperimentStartResponse: None,
            proto.EnvironmentUpdateResponse: self._write_world_state,
            proto.AgentSetupRequest: self._write_agent,
            proto.AgentSetupResponse: None,
            proto.AgentUpdateRequest: None,
            proto.AgentUpdateResponse: self._write_agent_update,
            proto.MuscleUpdateRequest: None,
            proto.MuscleUpdateResponse: None,  # We need to dump brain data
        }
        LOG.debug("New store Receiver instance %s ready", self._uid)
        try:
            self._store_uri = RuntimeConfig().store_uri
            if not self._store_uri:
                raise KeyError
        except KeyError:
            LOG.error(
                "StoreReceiver(id=%0xd, uid=%s) "
                "has no store_uri configured; the store will be next to "
                "useless :-(",
                id(self),
                self._uid,
            )
            for k in self._message_dispatch.keys():  # Disable all handlers.
                self._message_dispatch[k] = None
        jsonpickle_numpy.register_handlers()

    def __del__(self):
        if self._db_session:
            self._db_session.flush()
            self._db_session.close()
        if self._log_store_fh:
            self._log_store_fh.flush()
            self._log_store_fh.close()

    @property
    def _log_store(self):
        if not self._log_store_fh:
            log_store_dir = os.path.join(os.getcwd(), "store.log")
            os.makedirs(log_store_dir, exist_ok=True)
            log_store_fp = os.path.join(
                log_store_dir, "%s-%s.log" % (int(time.time()), self._uid)
            )
            self._log_store_fh = open(log_store_fp, "w")
            LOG.debug(
                "StoreReceiver(id=%0xd, uid=%s) writing message log to: %s",
                id(self),
                self._uid,
                log_store_fp,
            )
        return self._log_store_fh

    @property
    def uid(self):
        return self._uid

    @property
    def _dbh(self) -> sqlalchemy.orm.session:
        if self._db_session is None:
            self._db_engine = sqlalchemy.create_engine(
                RuntimeConfig().store_uri
            )
            self._db_session_maker = sqlalchemy.orm.sessionmaker()
            self._db_session_maker.configure(bind=self._db_engine)
            try:
                self._db_session = self._db_session_maker()
            except sqlalchemy.exc.OperationalError as e:
                LOG.error("Store could not connect: %s", e)
                for (
                    k
                ) in self._message_dispatch.keys():  # Disable all handlers.
                    self._message_dispatch[k] = None
            except sqlalchemy.exc.ArgumentError as e:
                LOG.error("Store could not connect: %s", e)
                for (
                    k
                ) in self._message_dispatch.keys():  # Disable all handlers.
                    self._message_dispatch[k] = None
        return self._db_session

    def run(self):
        """Run the store."""
        LOG.debug(
            "Starting StoreReceiver(id=0x%x, uid=%s)", id(self), self._uid
        )
        while self._running or not self._queue.empty():
            try:
                msg = self._queue.get(timeout=1)
            except queue.Empty:
                time.sleep(1)
                continue
            msg_type, msg_uid, msg_obj = self.read(msg)
            LOG.debug(
                "StoreReceiver(id=0x%x, uid=%s) received message: "
                "type=%s, uid=%s, payload=%s",
                id(self),
                self._uid,
                msg_type,
                msg_uid,
                msg_obj,
            )
            if msg_type in ("ignore", "error"):
                continue
            self.write(msg_obj)
        LOG.debug("StoreReceiver(id=0x%x, uid=%s) closed", id(self), self._uid)

    def shutdown(self):
        LOG.debug(
            "StoreReceiver(id=0x%x, uid=%s) preparing shutdown",
            id(self),
            self._uid,
        )
        self._running = False

    def write(self, message):
        if LOG.level == logging.DEBUG:
            self._log_store.write(
                "%s StoreReceiver(id=0x%x, uid=%s)[%d] %s %s"
                % (
                    time.time(),
                    id(self),
                    self._uid,
                    os.getpid(),
                    message,
                    message.__dict__
                    if hasattr(message, "__dict__")
                    else str(message),
                )
            )
            self._log_store.flush()
        if message.__class__ not in self._message_dispatch:
            StoreReceiver._handle_unknown_message(message)
            return
        if self._message_dispatch[message.__class__] is not None:
            try:
                LOG.debug(
                    "StoreReceiver(id=0x%x, uid=%s) " "dispatching message %s",
                    id(self),
                    self.uid,
                    message,
                )
                self._message_dispatch[message.__class__](message)
            except (
                sqlalchemy.exc.NoForeignKeysError,
                sqlalchemy.exc.ProgrammingError,
            ) as e:
                LOG.critical(
                    "StoreReceiver(id=0x%x, uid=%s) "
                    "notes that the developers are too stupid to get the "
                    "schema right: %s",
                    id(self),
                    self.uid,
                    e,
                )
            except sqlalchemy.exc.InvalidRequestError as e:
                LOG.critical(
                    "StoreReceiver(id=0x%x, uid=%s) "
                    "failed to write to the database: %s",
                    id(self),
                    self.uid,
                    e,
                )

    @staticmethod
    def _handle_unknown_message(message):
        LOG.warning(
            "Store received message %s, but cannot handle it - ignoring",
            message,
        )

    def _write_experiment(self, msg: proto.ExperimentStartRequest):
        from palaestrai.experiment.experiment import Experiment

        study_hack = dbm.ExperimentStudy()  # TODO Hack, hack!!
        study_hack.name = (
            "I'm a Dummy Hacky Study :^), "
            "please replace me at %s" % __file__
        )
        self._dbh.add(study_hack)

        eq = self._dbh.query(dbm.Experiment).filter_by(name=msg.experiment.id)
        experiment_record = eq.first()
        if not experiment_record:
            sio = StringIO()
            yaml = yml.YAML(typ="safe")
            yaml.register_class(Experiment)
            yaml.dump(msg.experiment, sio)
            experiment_record = dbm.Experiment(
                experiment_study_id=study_hack.id,
                experiment=sio.getvalue(),
                name=msg.experiment.id,
            )
            self._dbh.add(experiment_record)
            self._dbh.commit()

        experiment_run_record = (
            self._dbh.query(dbm.ExperimentRun)
            .filter_by(uuid=msg.experiment_run_id)
            .first()
        )
        if not experiment_run_record:
            experiment_run_record = dbm.ExperimentRun(
                uuid=msg.experiment_run_id, experiment_id=experiment_record.id
            )
            self._dbh.add(experiment_run_record)
            self._dbh.commit()
        else:
            LOG.warn(
                "Duplicate ExperimentRun record with uuid=%s",
                experiment_run_record.uuid,
            )
        self._worlds_state_sensors = [
            s
            for l in msg.experiment.env_configs
            if "world_state_sensors" in l["env_params"]
            for s in l["env_params"]["world_state_sensors"]
        ]

    def _write_simulation_instance(
        self, message: proto.SimulationStartRequest
    ):
        q = self._dbh.query(dbm.ExperimentRun).filter_by(
            uuid=message.experiment_run_id
        )
        experiment_run_record = q.first()
        if not experiment_run_record:
            LOG.error(
                "Store received SimulationStartRequest, but could not find "
                "run for run_id=%s",
                message.experiment_run_id,
            )
            return
        q = self._dbh.query(dbm.SimulationInstance).filter_by(
            uuid=message.simulation_controller_id
        )
        if (
            q.count() > 0
            and q.one().experiment_run_id == experiment_run_record.id
        ):
            return  # OK, we received a duplicate
        elif (
            q.count() > 0
            and q.one().experiment_run_id != experiment_run_record.id
        ):
            LOG.error(
                "StoreReceiver(id=0x%x, uid=%s) "
                "received SimulationStartRequest(simulation_controller_id=%s);"
                " the SimulationController.uid already exists, but with "
                "different experiment runs (in DB: %s, received: %s); "
                "ignoring - expect more errors",
                id(self),
                self.uid,
                message.simulation_controller_id,
                q.one().uuid,
                message.simulation_controller_id,
            )
            return  # Nothing we can do here except complaining
        LOG.debug(
            "Writing new SimulationInstance for experiment_run_id=%s",
            experiment_run_record.uuid,
        )
        self._dbh.add(
            dbm.SimulationInstance(
                uuid=message.simulation_controller_id,
                experiment_run_id=experiment_run_record.id,
            )
        )
        self._dbh.commit()

    def _write_environment(self, message: proto.EnvironmentSetupResponse):
        q = self._dbh.query(dbm.SimulationInstance).filter_by(
            uuid=message.receiver_simulation_controller
        )
        simulation_instance_record = q.first()
        self._dbh.add(
            dbm.EnvironmentConductor(
                uuid=message.sender_environment_conductor,
                type=message.environment_type,
                parameters=json.dumps(message.environment_parameters),
                simulation_instance_id=simulation_instance_record.id,
            )
        )
        self._dbh.commit()

    def _write_world_state(self, message: proto.EnvironmentUpdateResponse):

        q = self._dbh.query(dbm.EnvironmentConductor).filter_by(
            uuid=message.environment_conductor_id
        )
        environment_conductor_record = q.one()

        self._dbh.add(
            dbm.WorldState(
                environment_conductor_id=environment_conductor_record.id,
                is_terminal=message.is_terminal,
                state_dump=jsonpickle.encode(message.sensors),
            )
        )
        self._dbh.commit()

    def _write_agent(self, message: proto.AgentSetupRequest):
        q = self._dbh.query(dbm.ExperimentRun).filter_by(
            uuid=message.experiment_run_id
        )
        experiment_run_record = q.one()
        q = self._dbh.query(dbm.AgentConductor).filter_by(
            uuid=message.receiver_agent_conductor,
        )
        if q.count() == 0:
            agent_conductor_record = dbm.AgentConductor(
                experiment_run_id=experiment_run_record.id,
                uuid=message.receiver_agent_conductor,
                name=message.agent_name,
            )
            self._dbh.add(agent_conductor_record)
        else:
            agent_conductor_record = q.one()
        q = self._dbh.query(dbm.SimulationInstance).filter_by(
            uuid=message.sender_simulation_controller
        )
        simulation_instance_record = q.one()
        self._dbh.add(
            dbm.Muscle(
                agent_conductor_id=agent_conductor_record.id,
                simulation_instance_id=simulation_instance_record.id,
                uuid=message.agent_id,
            )
        )
        self._dbh.commit()

    def _write_agent_update(self, message: proto.AgentUpdateResponse):

        q = self._dbh.query(dbm.Muscle).filter_by(
            uuid=message.sender_agent_id,
        )
        muscle_record = q.one()
        muscle_action_record = dbm.MuscleAction(
            muscle_id=muscle_record.id,
            reward=message.rewards[0],
            sensor_readings=jsonpickle.encode(message.sensor_information),
            actuator_information=jsonpickle.encode(
                message.actuator_information
            ),
        )
        self._dbh.add(muscle_action_record)
        self._dbh.commit()

    def read(self, msg):
        """Dummy store in a text file.

        Replace by sending to the database.

        """
        # print("Len Message", len(msg))
        # if len(msg) >= 3:

        sender = msg.pop(0)
        empty = msg.pop(0)
        assert empty == b""
        header = msg.pop(0)
        # if len(msg) >= 1:
        #     serv_comm = msg.pop(0)
        if len(msg) > 3:
            sender = msg.pop(0)
            empty = msg.pop(0)
            header = msg.pop(0)
            LOG.debug(
                "Ignored message parts: %s, %s, %s", sender, empty, header
            )

        if msg[0] == MDP.W_HEARTBEAT:
            # We ignore heartbeats
            return "ignore", None, None
        if msg[0] == MDP.W_READY:
            return "ignore", None, None

        if len(msg) == 1:
            # it is a response
            uid = ""
            msg_obj = self._deserialize(msg.pop(0))
            msg_type = "response"

        elif len(msg) == 2:
            uid = self._deserialize(msg.pop(0))
            msg_obj = self._deserialize(msg.pop(0))
            msg_type = "request"
        else:
            print(msg)
            uid = ""
            msg_obj = "None"
            msg_type = "error"

        return msg_type, uid, msg_obj

    def _deserialize(self, msg):
        try:
            msg = deserialize([msg])
            return msg
        except zlib.error:
            LOG.debug("Message %s could not be deserialized.", msg)
        try:
            msg = str(msg.decode())
            return msg
        except AttributeError:
            LOG.debug("Message %s could not be decoded.", msg)

        return msg
