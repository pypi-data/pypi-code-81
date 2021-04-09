#!/usr/bin/env python
from pyathena import connect
from pyathena.pandas.cursor import PandasCursor

QUERY_SHOW_DATABASES = """show databases;"""
QUERY_SHOW_TABLES = """show tables in {schema_name};"""
QUERY_TABLE_RECORDS_WITH_LIMIT = """select * from {schema_name}.{table_name} limit {limit};"""
QUERY_TABLE_RECORDS = """select * from {schema_name}.{table_name} limit 1000;"""


################################################################################
# Athena Utility
################################################################################

class AthenaLoader:

    def connect(self, s3_staging_dir, region_name, access_key_id=None,
                secret_access_key_id=None, botocore_session=None, aws_session_token=None):
        """Creates a connection to Athena"""
        try:
            conn = connect(
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key_id,
                s3_staging_dir=s3_staging_dir,
                region_name=region_name,
                botocore_session=botocore_session,
                aws_session_token=aws_session_token,
            )
            if hasattr(self, 'conn'):
                self._conn.close()
            self._conn = conn
        except Exception as X:
            return X

    def databases(self):
        """Returns all the schemas available in Athena"""
        dbs = self.run_query(QUERY_SHOW_DATABASES)
        return dbs

    def tables(self, schema_name):
        """Returns all the tables present in a schema"""
        tables = self.run_query(QUERY_SHOW_TABLES.format(schema_name=schema_name))
        return tables

    def top(self, schema_name, table_name, limit=None):
        """Returns records from a table"""
        if limit:
            records = self.run_query(QUERY_TABLE_RECORDS_WITH_LIMIT.format(schema_name=schema_name, table_name=table_name,limit=limit))
        else:
            records = self.run_query(QUERY_TABLE_RECORDS.format(schema_name=schema_name, table_name=table_name))
        return records

    def run_query(self, query_string, parameters=None, result_as_df=True):
        """Run SQL query using pyathena."""
        if result_as_df:
            result = self._pandas_cursor_execute(query_string, parameters)
        else:
            result = list(self._cursor_execute(query_string, parameters))
        return result

    def _cursor_execute(self, query_string, parameters):
        try:
            with self._conn.cursor() as athena_cursor:
                athena_cursor.execute(query_string, parameters)
                columns = [desc[0] for desc in athena_cursor.description]
                while True:
                    row = athena_cursor.fetchone()
                    if row is None:
                        break
                    yield dict(zip(columns, row))
        except Exception as X:
            return X

    def _pandas_cursor_execute(self, query_string, parameters):
        """Execute query using cursor and parameters, and return the results as a Dataframe"""
        try:
            with self._conn.cursor(PandasCursor) as athena_cursor:
                result = athena_cursor.execute(query_string, parameters)
                return result.as_pandas()
        except Exception as X:
            return X

    def __exit__(self):
        if self._conn:
            self._conn.close()

    def __del__(self):
        if self._conn:
            self._conn.close()
