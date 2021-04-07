from enum import Enum


class OperationType(Enum):
    CREATE_SQL_QUERY = "createSqlQuery"
    SQL_QUERY = "sqlQuery"
    SQL_QUERY_METADATA = "sqlQueryMetadata"
    SQL_RESULT_PAGINATION = "sqlResultPagination"
    DELETE_STATEMENT = "deleteStatement"
