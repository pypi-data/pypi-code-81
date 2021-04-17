
import boto3

class Athena:
    def __init__(self, region_name, access_key_id, secret_access_key):
        self.region_name = region_name
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session = boto3.session.Session()
        self._client = self.session.client('athena', region_name=region_name,
                            aws_access_key_id=self.access_key_id,
                            aws_secret_access_key=self.secret_access_key)

    def send_query(self, query, *args):
        response = self._client.start_query_execution(QueryString = query, *args)
        return response

    def query_status(self, query_id):
        response = self._client.get_query_execution(QueryExecutionId=query_id)
        return response['QueryExecution']['Status']['State']

    
