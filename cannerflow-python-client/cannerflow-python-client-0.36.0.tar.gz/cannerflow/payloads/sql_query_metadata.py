from .operation_type import OperationType


class SqlQueryMetadataPayload(object):
    def __init__(self) -> None:
        self._name = OperationType.SQL_QUERY_METADATA.value
        self._query = """
            query sqlQueryMetadata($where: SqlQueryWhereUniqueInput!) {
                sqlQueryMetadata(where: $where) {
                    columns
                    rowCount
                }
            }
        """

    def build(self, sql_query_id: str) -> dict:
        return {
            "operationName": self._name,
            "query": self._query,
            "variables": {"where": {"id": sql_query_id}},
        }