from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.sql.expression import text
from sqlalchemy_utils import database_exists, create_database

from . import LOG
from .database_model import Model


def setup_database(uri):
    """Creates the database from the current model in one go.

    :param uri: The complete database connection URI.
    """
    engine = create_engine(uri)
    if not database_exists(uri):
        create_database(uri)
    timescale_tables = {
        "world_states",
        "muscle_actions",
        "muscle_sensor_readings",
        "muscle_states",
    }

    with engine.begin() as conn:
        try:
            Model.metadata.create_all(engine)
        except ProgrammingError as e:
            LOG.error("Could not create database: %s" % e)
            raise e
        try:
            conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
        except ProgrammingError as e:
            LOG.critical("Could not create extension timescaledb: %s" % e)
            raise e
    with engine.begin() as conn:
        for tbl in timescale_tables:
            cmd = (
                "SELECT * FROM create_hypertable("
                "'%s', 'id', chunk_time_interval => 40960);" % tbl
            )
            try:
                res = conn.execute(text(cmd))
                LOG.debug(
                    'Result of executing "%s" during setup: %s',
                    cmd,
                    res.fetchall(),
                )
                res.close()
            except ProgrammingError as e:
                LOG.error("Could not create hypertable (%s): %s" % (cmd, e))
                raise e


def get_connection(uri):
    """This function creates a database if necessary and returns an engine
    object from SQLAlchemy. The database is automatically created, if not
    existent.

    Args:
        uri (String): <driver>://<user>:<password>@<uri>/<database name>
                e.g.: postgres://otto:vBismarck@8.8.8.8/rent

    Returns:
        engine: A SQLAlchemy object that provides a connection to the database,
        given in the url.
    """
    setup_database(uri)
    return create_engine(uri)
