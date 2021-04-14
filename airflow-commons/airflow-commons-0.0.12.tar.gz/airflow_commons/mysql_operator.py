from airflow_commons.utils.mysql.mysql_utils import upsert, get_db_engine
import airflow_commons.logger as logger
from airflow_commons.utils.file_utils import read_sql
from airflow_commons.utils.mysql.sql_utils import get_delete_sql


def write_to_mysql(
    username: str,
    password: str,
    host: str,
    db_name: str,
    values: dict,
    chunk_size: int,
    table_name: str,
):
    """

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param values: values to write into database
    :param chunk_size: data size to upload at a time
    :param table_name: database table name to write
    :return:
    """
    engine = get_db_engine(username, password, host, db_name)
    chunks = [values[i : i + chunk_size] for i in range(0, len(values), chunk_size)]
    logger.LOGGER("Chunk size is {}.".format(chunk_size))
    with engine.connect() as conn:
        i = 0
        for chunk in chunks:
            i += 1
            upsert(values=chunk, conn=conn, table_name=table_name)
            logger.LOGGER("Chunk {} uploaded".format(i))
    logger.LOGGER("Data uploaded to MySql.")


def delete(
    username: str,
    password: str,
    host: str,
    db_name: str,
    table_name: str,
    where_statement_file: str,
    where_statement_params: dict = None,
):
    """
    Runs a delete query on given table, and removes rows that conform where condition

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :param table_name: table name
    :param where_statement_file: relative location of where statement sql file
    :param where_statement_params: parameters of where statements
    """
    engine = get_db_engine(username, password, host, db_name)
    connection = engine.raw_connection()
    if where_statement_params is None:
        where_statement_params = dict()
    where_statement = read_sql(sql_file=where_statement_file, **where_statement_params)
    sql = get_delete_sql(
        table_name=table_name,
        where_statement=where_statement,
    )
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    logger.LOGGER("The below sql statement is executed " + sql)
