from typing import Optional

from pyrasgo.api.connection import Connection
from pyrasgo.rasgo import Rasgo
from pyrasgo.utils.monitoring import track_usage

class RasgoOrchestration():

    def __init__(self, api_key: str):
        self.rasgo = Rasgo(api_key=api_key)

    @track_usage
    def get_featureset_id(self, snowflakeTable: str, fs_name: Optional[str] = None) -> Optional[int]:
            fs = self.rasgo.match.feature_set(table_name=snowflakeTable, fs_name=fs_name)
            return fs.id if fs else None

    @track_usage
    def publish_features_from_yml(self, yml_file: str, sandbox: Optional[bool] = True, git_repo: Optional[str] = None):
        return self.rasgo.publish_features_from_yml(yml_file=yml_file, sandbox=sandbox, git_repo=git_repo)

    @track_usage
    def run_stats_for_feature(self, feature_id: int):
        return self.rasgo.create.feature_stats(feature_id)

    @track_usage
    def run_stats_for_featureset(self, featureset_id: int):
        return self.rasgo.create.feature_set_stats(featureset_id)
    
    @track_usage
    def simulate_orchestration(self, source_table: str, func):
        """
        Run a python function against a source table
        
        param source_table: Snowflake table holding raw data
        param func: function containing feature transformation code (should be named generate_feature)

        return: Success or Failure message
        """
        df = self.rasgo.get.source_table(table_name=source_table, record_limit=-1)
        dx = func(df)
        return f"Code successfully created dataframe with shape {dx.shape}"