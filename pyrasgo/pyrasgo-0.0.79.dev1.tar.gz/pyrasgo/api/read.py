import pandas as pd
from typing import Dict, List, Optional

from .connection import Connection
from .error import APIError
from .get import Get
from pyrasgo.primitives.collection import Collection
from pyrasgo.primitives.feature import Feature, FeatureList
from pyrasgo.primitives.source import DataSource
from pyrasgo.storage import DataWarehouse, SnowflakeDataWarehouse
from pyrasgo.utils.monitoring import track_usage
from pyrasgo import schemas as api


class Read(Connection):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_warehouse: SnowflakeDataWarehouse = DataWarehouse.connect()
        self.get = Get(api_key=self._api_key)

    @track_usage
    def collection_data(self, 
                        id: int,
                        filters: Optional[Dict[str, str]] = None,
                        limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs a pandas DataFrame from the specified Rasgo Collection

        :param id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        collection = self.get.collection(id)
        if collection:
            try:
                table_metadata = collection._make_table_metadata()
                query, values = self.data_warehouse._make_select_statement(table_metadata, filters, limit)
                return self.data_warehouse.query_into_dataframe(query, values)
            except:
                raise APIError("Collection table is not reachable")
        raise APIError("Collection does not exist")

    @track_usage
    def feature_data(self, 
                     id: int,
                     filters: Optional[Dict[str, str]] = None,
                     limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs a pandas DataFrame from the specified Rasgo Feature data

        :param id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        feature = self.get.feature(id)
        if feature.sourceTable:
            try:
                table_metadata = feature._make_table_metadata()
                #TODO: if we ever support multiple features, add them to this line -
                features = feature.columnName
                indices = ','.join(feature.indexFields)
                columns = indices +', '+features
                query, values = self.data_warehouse._make_select_statement(table_metadata, filters, limit, columns)
                return self.data_warehouse.query_into_dataframe(query, values)
            except:
                raise APIError("Feature table is not reachable")
        raise APIError("Feature table does not exist")

    @track_usage
    def source_data(self, 
                    id: int,
                    filters: Optional[Dict[str, str]] = None,
                    limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs a pandas DataFrame from the specified Rasgo DataSource

        :param id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        data_source = self.get.data_source(id)
        if data_source:
            try:
                table_metadata = data_source._make_table_metadata()
                query, values = self.data_warehouse._make_select_statement(table_metadata, filters, limit)
                return self.data_warehouse.query_into_dataframe(query, values)
            except:
                raise APIError("DataSource table is not reachable")
        raise APIError("DataSource does not exist")