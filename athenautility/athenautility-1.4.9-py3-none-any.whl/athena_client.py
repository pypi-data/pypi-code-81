#!/usr/bin/env python
import json
import os
import logging
import requests
import pandas as pd
from IPython.display import display, HTML


logger = logging.getLogger(__name__)

STATUS = "status"
RESULT = "result"
ERROR = "error"
SUCCESS = "SUCCESS"
FAILED = "FAILED"

################################################################################
# Queries
################################################################################

QUERY_SHOW_DATABASES = """show databases;"""
QUERY_SHOW_TABLES = """show tables in {schema_name};"""
QUERY_TABLE_RECORDS_WITH_LIMIT = """select * from {schema_name}.{table_name} limit {limit};"""
QUERY_TABLE_RECORDS = """select * from {schema_name}.{table_name} limit 100;"""

# Athena services
API_VALIDATE_USER = "/ccf/services/v2.0/validate_user"
API_GET_ATHENA_DATABASES = "/ccf/services/v2.0/get_athena_databases"
API_GET_ATHENA_TABLES = "/ccf/services/v2.0/get_athena_tables"
API_QUERY_ATHENA_TABLE = "/ccf/services/v2.0/query_athena_table"
API_RUN_QUERY_ON_ATHENA = "/ccf/services/v2.0/run_query_on_athena"
API_SAVE_DATA_TO_S3 = "/ccf/services/v2.0/save_data_to_s3"

# Environment Variables
_USER_NAME: str = 'USER_NAME'
_ACCESS_TOKEN: str = 'ACCESS_TOKEN'
_USER_ROLE: str = 'USER_ROLE'
_CCF_SERVICES_HOST: str = 'CCF_SERVICES_HOST'
_USER_S3_BUCKET: str = 'USER_S3_BUCKET'

HEADERS = {
    'content-type': "application/json",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.90 Safari/537.36"
}

TABLE_STYLES = [dict(selector="caption", props=[("text-align", "inline"), ("font-size", "100%"), ("color", 'black')]),
                dict(selector="td", props=[('border', '1px solid black'), ("text-align", "left")]),
                dict(selector="th", props=[('border', '1px solid black'), ("text-align", "center")])]


################################################################################
# Athena Client
################################################################################
def connect():
    # TODO - Add user validation
    try:
        _user_name = os.getenv(_USER_NAME, None)
        _access_token = os.getenv(_ACCESS_TOKEN, None)
        _user_role = os.getenv(_USER_ROLE, None)
        _ccf_services_host = os.getenv(_CCF_SERVICES_HOST, None)
        _user_s3_bucket = os.getenv(_USER_S3_BUCKET, None)
        payload = json.dumps({"user_name": _user_name, "role_id": _user_role})
        r = requests.post(_ccf_services_host + API_VALIDATE_USER, data=payload, headers=HEADERS,
                          cookies=dict(sessionId=_access_token))
        response = r.json()
        if response[STATUS] == SUCCESS:
            athena_client = AthenaClient(user_name=_user_name, user_role=_user_role, access_token=_access_token,
                                         ccf_services_host=_ccf_services_host, user_s3_bucket=_user_s3_bucket)
            return athena_client
        else:
            print(response[ERROR])

    except requests.exceptions.HTTPError:
        print("Http error occurred")
    except requests.exceptions.ConnectionError:
        print("Connection error occurred")
    except requests.exceptions.Timeout:
        print("Request timed out...")
    except requests.exceptions.RequestException:
        print("RequestException occurred")


class AthenaClient:

    def __init__(self, user_name, access_token, user_role, ccf_services_host, user_s3_bucket):
        self._user_name = user_name
        self._access_token = access_token
        self._user_role = user_role
        self._ccf_services_host = ccf_services_host
        self._user_s3_bucket = user_s3_bucket
        print("Connection is successful...")

    def databases(self, result_as_df=True):
        """Returns all the schemas available in Athena"""
        try:
            payload = json.dumps({"user_name": self._user_name, "role_id": self._user_role})
            r = requests.post(self._ccf_services_host + API_GET_ATHENA_DATABASES, data=payload, headers=HEADERS,
                              cookies=dict(sessionId=self._access_token))
            response = r.json()
            if response[STATUS] == SUCCESS:
                if not result_as_df and isinstance(response[RESULT], (dict, list)):
                    response_as_df = pd.DataFrame.from_dict(response[RESULT]).style.set_caption(
                        "Databases").hide_index().set_table_styles(TABLE_STYLES)
                    return display(response_as_df)
                else:
                    response_as_df = pd.DataFrame.from_dict(response[RESULT])
                    return response_as_df
            else:
                return response[ERROR]

        except requests.exceptions.HTTPError:
            print("Http error occurred")
        except requests.exceptions.ConnectionError:
            print("Connection error occurred")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException:
            print("RequestException occurred")

    def tables(self, schema_name, result_as_df=True):
        """Returns all the tables present in a schema"""
        try:
            payload = json.dumps({"user_name": self._user_name, "role_id": self._user_role, "schema_name": schema_name})
            r = requests.post(self._ccf_services_host + API_GET_ATHENA_TABLES, data=payload, headers=HEADERS,
                              cookies=dict(sessionId=self._access_token))
            response = r.json()
            if response[STATUS] == SUCCESS:
                if not result_as_df and isinstance(response[RESULT], (dict, list)):
                    response_as_df = pd.DataFrame.from_dict(response[RESULT]).style.set_caption(
                        "Tables").hide_index().set_table_styles(TABLE_STYLES)
                    return display(response_as_df)
                else:
                    response_as_df = pd.DataFrame.from_dict(response[RESULT])
                    return response_as_df
            else:
                return response[ERROR]

        except requests.exceptions.HTTPError:
            print("Http error occurred")
        except requests.exceptions.ConnectionError:
            print("Connection error occurred")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException:
            print("RequestException occurred")

    def top(self, schema_name, table_name, limit=None, result_as_df=True):
        """Returns records from a table"""
        try:
            payload = json.dumps({"user_name": self._user_name, "role_id": self._user_role, "schema_name": schema_name,
                                  "table_name": table_name, "limit": limit})
            r = requests.post(self._ccf_services_host + API_QUERY_ATHENA_TABLE, data=payload, headers=HEADERS,
                              cookies=dict(sessionId=self._access_token))
            response = r.json()
            if response[STATUS] == SUCCESS:
                if not result_as_df and isinstance(response[RESULT], (dict, list)):
                    table_header = f'Top {limit} records of table {schema_name}.{table_name}' if limit else f'Top 100 records of table <i>{schema_name}.{table_name}</i>'
                    response_as_df = pd.DataFrame.from_dict(response[RESULT]).style.set_caption(
                        table_header).hide_index().set_table_styles(TABLE_STYLES)
                    return display(response_as_df)
                else:
                    response_as_df = pd.DataFrame.from_dict(response[RESULT])
                    return response_as_df
            else:
                return response[ERROR]

        except requests.exceptions.HTTPError:
            print("Http error occurred")
        except requests.exceptions.ConnectionError:
            print("Connection error occurred")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException:
            print("RequestException occurred")

    def run_query(self, query_string, result_as_df=True):
        """Run a specified query"""
        try:
            payload = json.dumps(
                {"user_name": self._user_name, "role_id": self._user_role, "query_string": query_string})
            r = requests.post(self._ccf_services_host + API_RUN_QUERY_ON_ATHENA, data=payload, headers=HEADERS,
                              cookies=dict(sessionId=self._access_token))
            response = r.json()
            queries = list(filter(None, query_string.split(';')))
            if response[STATUS] == SUCCESS:
                if not result_as_df and isinstance(response[RESULT], (dict, list)):
                    if len(queries) > 1:
                        results = [pd.DataFrame.from_dict(item).style.set_caption(
                            f"""Query results for <i>\"{queries[i]};\"</i>""").hide_index().set_table_styles(TABLE_STYLES) for i, item in
                                   enumerate(response[RESULT])]
                        return display(*results)
                    else:
                        result = pd.DataFrame.from_dict(response[RESULT]).style.set_caption(
                            f"""Query results for <i>\"{queries[0]};\"</i>""").hide_index().set_table_styles(
                            TABLE_STYLES)
                        return display(result)
                else:
                    if len(queries) > 1:
                        results = [pd.DataFrame.from_dict(item) for item in response[RESULT]]
                    else:
                        results = pd.DataFrame.from_dict(response[RESULT])
                    return results
            else:
                return response[ERROR]

        except requests.exceptions.HTTPError:
            print("Http error occurred")
        except requests.exceptions.ConnectionError:
            print("Connection error occurred")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException:
            print("RequestException occurred")

    def save_data(self, data, file_name):
        """Returns records from a table"""
        try:
            d = data.to_dict(orient='records')
            payload = json.dumps({"user_name": self._user_name, "role_id": self._user_role, "file_name": file_name,
                                  "s3_bucket": self._user_s3_bucket, "data": d})
            r = requests.post(self._ccf_services_host + API_SAVE_DATA_TO_S3, data=payload, headers=HEADERS,
                              cookies=dict(sessionId=self._access_token))
            response = r.json()
            if response[STATUS] == SUCCESS:
                return response[RESULT]
            else:
                return response[ERROR]

        except requests.exceptions.HTTPError:
            print("Http error occurred")
        except requests.exceptions.ConnectionError:
            print("Connection error occurred")
        except requests.exceptions.Timeout:
            print("Request timed out...")
        except requests.exceptions.RequestException:
            print("RequestException occurred")
