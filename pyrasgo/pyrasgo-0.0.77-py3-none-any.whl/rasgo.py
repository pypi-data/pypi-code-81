from datetime import datetime
import hashlib
from more_itertools import lstrip
import pandas as pd
from pathlib import Path
from requests.exceptions import HTTPError
from types import FunctionType
from typing import Any, Dict, List, Optional, Union
import uuid
import webbrowser
import yaml

from pyrasgo.connection import Connection
from pyrasgo.primitives.enums import Granularity, ModelType
from pyrasgo.primitives.collection import Collection
from pyrasgo.primitives.feature import Feature, FeatureList
from pyrasgo.primitives.feature_set import FeatureSet
from pyrasgo.primitives.source import DataSource
from pyrasgo.monitoring import track_usage
from pyrasgo.storage import DataWarehouse, SnowflakeDataWarehouse
from pyrasgo.utils import dataframe, ingestion
from pyrasgo import schemas as api

class APIError(Exception):
    pass

class ParameterValueError(Exception):
    def __init__(self, param: str, values: List[str]):
        self.param = param
        self.values = values

    def __str__(self):
        return f"Please pass a valid value for {self.param}. Values are {self.values}" 

class Rasgo(Connection):
    """
    Base connection object to handle interactions with the Rasgo API.
    """
    from pyrasgo.version import __version__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_warehouse: SnowflakeDataWarehouse = DataWarehouse.connect()

    def open_docs(self):
        webbrowser.open("https://docs.rasgoml.com/rasgo-docs/pyrasgo/pyrasgo-getting-started")

    def pronounce_rasgo(self):
        webbrowser.open("https://www.spanishdict.com/pronunciation/rasgo?langFrom=es")

# ---------
# Get Calls
# ---------
    # Alias
    @track_usage
    def get_collection(self, collection_id: int) -> Collection:
        """
        Returns a Rasgo Collection (set of joined Features) matching the specified id
        """
        return self.get_model(model_id=collection_id)

    @track_usage
    def get_collection_attributes(self, collection_id: int) -> api.CollectionAttributes:
        """
        Returns a dict of attributes for a collection
        """
        try:
            response = self._get(f"/models/{collection_id}/attributes", api_version=1).json()
            dict_out = {}
            for kv in response:
                dict_out[kv['key']] = kv['value']
            return api.CollectionAttributes(collectionId=collection_id, attributes=dict_out)
        except:
            raise ValueError(f"Collection {collection_id} does not exist or this API key does not have access.")

    # Alias
    @track_usage
    def get_collections(self, include_shared: bool=False) -> List[Collection]:
        """
        Returns all Rasgo Collections (set of joined Features) that I have author access to. Add an include_shared 
        parameter to return all Rasgo Collections that I have any access to (author or shared access)
        :param include_shared: Boolean value indicating if the return should include all accessible collections
        """
        return self.get_models(include_shared=include_shared)

    @track_usage
    def get_collections_by_attribute(self, key: str, value: str = None) -> List[Collection]:
        """
        Returns a list of Rasgo Collections that match an attribute
        """
        try:
            params = {"key": key}
            if value:
                params.update({"value": value})
            return self._get(f"/models/attributes/models", params=params, api_version=1).json()
        except:
            raise ValueError(f"Key {key}: {value or 'Any'} does not exist or this API key does not have access.")

    @track_usage
    def get_column(self, column_id: int) -> api.Column:
        """
        Returns a Column with the specified id
        """
        try:
            response = self._get(f"/columns/{column_id}", api_version=1).json()
            return api.Column(**response)
        except:
            raise ValueError(f"Column {column_id} does not exist or this API key does not have access.")

    @track_usage
    def get_columns_by_featureset(self, feature_set_id: int) -> List[api.Column]:
        """
        Returns all Columns in the specified FeatureSet
        """
        try:
            response = self._get(f"/columns/by-featureset/{feature_set_id}", api_version=1).json()
            return [api.Column(**entry) for entry in response]
        except:
            raise ValueError(f"FeatureSet {feature_set_id} does not exist or this API key does not have access.")

    @track_usage
    def get_data_sources(self) -> List[DataSource]:
        """
        Returns all DataSources available in your organization or Rasgo Community
        """
        try:
            response = self._get("/data-source", api_version=1).json()
            return [DataSource(api_object=entry) for entry in response]
        except:
            raise ValueError("Data Sources do not exist or this API key does not have access.")

    @track_usage
    def get_data_source(self, data_source_id: int) -> DataSource:
        """
        Returns the DataSource with the specified id
        """
        try:
            response = self._get(f"/data-source/{data_source_id}", api_version=1).json()
            return DataSource(api_object=response)
        except:
            raise ValueError(f"Data Source {data_source_id} does not exist or this API key does not have access.")

    @track_usage
    def get_data_source_columns(self, data_source_id: int) -> List[api.DataSourceColumn]:
        """
        Returns columns in the DataSource with the specified id
        """
        try:
            response = self._get(f"/data-source/columns/{data_source_id}", api_version=1).json()
            return [api.DataSourceColumn(**column) for column in response['columns']]
        except:
            raise ValueError(f"Data Source {data_source_id} does not exist or this API key does not have access.")

    @track_usage
    def get_data_source_stats(self, data_source_id: int):
        """
        Returns the stats profile of the specificed data source
        """
        try:
            return self._get(f"/data-source/profile/{data_source_id}", api_version=1).json()
        except:
            raise ValueError(f"Stats do not exist for DataSource {data_source_id}")

    @track_usage
    def get_dimensionalities(self) -> List[api.Dimensionality]:
        """
        Returns all Dimensionalities available in your organization or Rasgo Community
        """
        try:
            response = self._get("/dimensionalities", api_version=1).json()
            return [api.Dimensionality(**entry) for entry in response]
        except:
            raise ValueError("Dimensionalities do not exist or this API key does not have access.")
    
    @track_usage
    def get_feature(self, feature_id: int) -> Feature:
        """
        Returns the Feature with the specified id
        """
        try:
            return Feature(api_object=self._get(f"/features/{feature_id}", api_version=1).json())
        except:
            raise ValueError(f"Feature {feature_id} does not exist or this API key does not have access.")
    
    @track_usage
    def get_feature_attributes(self, feature_id: int) -> api.FeatureAttributes:
        """
        Returns a dict of attributes for a feature
        """
        try:
            response = self._get(f"/features/{feature_id}/attributes", api_version=1).json()
            dict_out = {}
            for kv in response:
                dict_out[kv['key']] = kv['value']
            return api.FeatureAttributes(featureId=feature_id, attributes=dict_out)
        except:
            raise ValueError(f"Feature {feature_id} does not exist or this API key does not have access.")

    @track_usage
    def get_feature_attributes_log(self, feature_id: int) -> tuple:
        """
        Returns a list of all attributes values logged to a feature over time
        """
        try:
            response = self._get(f"/features/{feature_id}/attributes/log", api_version=1).json()
            lst_out = []
            for kv in response:
                dict_item={}
                dict_item[kv['key']] = kv.get('value', None)
                dict_item['updatedBy'] = kv.get('recordAuthorId', None)
                dict_item['updated'] = kv.get('recordTimestamp', None)
                lst_out.append(dict_item)
            return api.FeatureAttributesLog(featureId=feature_id, attributes=lst_out)
        except:
            raise ValueError(f"Feature {feature_id} does not exist or this API key does not have access.")

    @track_usage
    def get_feature_set(self, feature_set_id: int) -> FeatureSet:
        """
        Returns the FeatureSet (set of Fetures) with the specified id
        """
        try:
            response = self._get(f"/feature-sets/{feature_set_id}", api_version=1).json()
            return FeatureSet(api_object=response)
        except:
            raise ValueError(f"FeatureSet {feature_set_id} does not exist or this API key does not have access.")

    @track_usage
    def get_feature_sets(self) -> List[FeatureSet]:
        """
        Returns a list of FeatureSets (set of Features) available in your organization or Rasgo Community
        """
        try:
            response = self._get("/feature-sets", api_version=1).json()
            return [FeatureSet(api_object=entry) for entry in response]
        except:
            raise ValueError("FeatureSets do not exist or this API key does not have access.")

    @track_usage
    def get_feature_stats(self, feature_id: int) -> Optional[api.FeatureStats]:
        """
        Returns the stats profile for the specified Feature
        """
        try:
            stats_json = self._get(f"/features/{feature_id}/stats", api_version=1).json()
            return api.FeatureStats(**stats_json["featureStats"])
        except:
            raise ValueError(f"Stats do not exist yet for feature {feature_id}.")
    
    @track_usage
    def get_features(self) -> FeatureList:
        """
        Returns a list of Features available in your organization or Rasgo Community
        """
        try:
            return FeatureList(api_object=self._get("/features", api_version=1).json())
        except:
            raise ValueError("Features do not exist or this API key does not have access.")

    @track_usage
    def get_features_by_attribute(self, key: str, value: str = None) -> List[Feature]:
        """
        Returns a list of features that match an attribute
        """
        try:
            params = {"key": key}
            if value:
                params.update({"value": value})
            return FeatureList(api_object=self._get(f"/features/attributes/features", params=params, api_version=1).json())
        except:
            raise ValueError(f"Key {key}: {value or 'Any'} does not exist or this API key does not have access.")

    @track_usage
    def get_features_by_featureset(self, feature_set_id) -> FeatureList:
        """
        Returns a list of Features in the specific FeatureSet
        """
        try:
            response = self._get(f"/features/by-featureset/{feature_set_id}", api_version=1)
            return FeatureList(api_object=response.json())
        except:
            raise ValueError(f"FeatureSet {feature_set_id} does not exist or this API key does not have access.")

    @track_usage
    def get_model(self, model_id) -> Collection:
        """
        Returns a Rasgo Model (set of joined Features) matching the specified id
        """
        try:
            return Collection(api_object=self._get(f"/models/{model_id}", api_version=1).json())
        except:
            raise ValueError(f"Model {model_id} does not exist or this API key does not have access.")

    @track_usage
    def get_models(self, include_shared: bool=False) -> List[Collection]:
        """
        Returns all Rasgo Collections (set of joined Features) that I have author access to. Add an include_shared 
        parameter to return all Rasgo Collections that I have any access to (author or shared access)
        :param include_shared: Boolean value indicating if the return should include all accessible collections
        """
        try:
            return [Collection(api_object=entry) for entry in self._get(f"/models", {"include_shared": include_shared}, api_version=1).json()]
        except:
            raise ValueError("Models do not exist or this API key does not have access.")

    # Alias
    @track_usage
    def get_shared_collections(self) -> List[Collection]:
        """
        Returns all Rasgo Collections (set of joined Features) shared in my organization or in Rasgo community
        """
        return self.get_shared_models()

    @track_usage
    def get_shared_models(self) -> List[Collection]:
        """
        Returns all Rasgo Models (set of joined Features) shared in my organization or in Rasgo community
        """
        try:
            return [Collection(api_object=entry) for entry in self._get(f"/models/shared", api_version=1).json()]
        except:
            raise ValueError("Shared Models do not exist or this API key does not have access.")

    @track_usage
    def get_source_columns(self, table: Optional[str] = None, database: Optional[str] = None, schema: Optional[str] = None, data_type: Optional[str] = None) -> pd.DataFrame:
        """
        Returns a DataFrame of columns in Snowflake tables and views that are queryable as feature sources
        """
        return self.data_warehouse.get_source_columns(table=table, database=database, schema=schema, data_type=data_type)

    @track_usage
    def get_source_table(self, table_name: str, record_limit: int, database: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
        """
        Returns a DataFrame of top n records in a Snowflake source table
        """
        return self.data_warehouse.get_source_table(table_name=table_name, record_limit=record_limit, database=database, schema=schema)

    @track_usage
    def get_source_tables(self, database: Optional[str] = None, schema: Optional[str] = None) -> pd.DataFrame:
        """
        Return a DataFrame of Snowflake tables and views that are queryable as feature sources
        """
        return self.data_warehouse.get_source_tables(database=database, schema=schema)

    @track_usage
    def match_data_source(self, table: str) -> DataSource:
        """
        Returns the first Data Source that matches the specified name
        """
        try:
            response = self._get(f"/data-source", {"table": table}, api_version=1).json()
            return DataSource(api_object=response[0])
        except:
            return None

    @track_usage
    def match_dimensionality(self, granularity: str) -> api.Dimensionality:
        """
        Returns the first community or private Dimensionality that matches the specified granularity 
        """
        try:
            response = self._get(f"/dimensionalities/granularity/{granularity}", api_version=1).json()
            return api.Dimensionality(**response)
        except:
            return None

    @track_usage
    def match_column(self, name: str, feature_set_id: int) -> Optional[api.Column]:
        """
        Returns the first Column matching the specidied name in the specified featureset
        """
        try:
            cols = self._get(f"/columns/by-featureset/{feature_set_id}", api_version=1).json()
            for c in cols:
                if name == c["name"]:
                    return api.Column(**c)
            return None
        except:
            return None

    @track_usage
    def match_feature(self, code: str, feature_set_id: int) -> Optional[Feature]:
        """
        Returns the first Feature matching the specified name in the specified featureset
        """
        try:
            features = self._get(f"/features/by-featureset/{feature_set_id}", api_version=1).json()
            for f in features: 
                if code == f["code"]:
                    return Feature(api_object=f)
            return None
        except:
            return None

    @track_usage
    def match_feature_set(self, table_name: str, fs_name: Optional[str] = None) -> Optional[FeatureSet]:
        """
        Returns the first FeatureSet matching the specified table name
        """
        try:
            fs = self._get(f"/feature-sets/", {"source_table": table_name}, api_version=1).json()
            # NOTE: This assumes there will be only 1 featureset in an Organization per table
            # At the point this no longer holds true, we will want to update this logic
            if fs_name and len(fs) > 1:
                for f in fs:
                    if f.name == fs_name:
                        print("f", f)
                        return FeatureSet(api_object=f)
                return None
            else:
                return FeatureSet(api_object=fs[0])
        except:
            return None


# -------------------
# Post / Create Calls
# -------------------
    # Alias
    @track_usage
    def create_collection(self, name: str,
                          type: Union[str, ModelType],
                          granularity: Union[str, Granularity],
                          description: Optional[str] = None,
                          is_shared: Optional[bool] = False) -> Collection:
        return self.create_model(name, type, granularity, description, is_shared)

    @track_usage
    def create_column(self, name: str, data_type: str, feature_set_id: int, dimension_id: int) -> api.Column:
        column = api.ColumnCreate(name=name, dataType=data_type,
                                  featureSetId=feature_set_id,
                                  dimensionId=dimension_id)
        response = self._post("/columns/", column.dict(exclude_unset=True), api_version=1).json()
        return api.Column(**response)

    @track_usage
    def create_data_source(self, name: str, source_type: str, table: str, database: Optional[str] = None, schema: Optional[str] = None, domain: Optional[str] = None, parent_source_id: Optional[int] = None) -> DataSource:
        data_source = api.DataSourceCreate(name=name,
                                           table=table,
                                           tableDatabase=database,
                                           tableSchema=schema,
                                           domain=domain,
                                           sourceType=source_type,
                                           parentId=parent_source_id)
        response = self._post("/data-source", data_source.dict(exclude_unset=True), api_version=1).json()
        return DataSource(api_object=response)

    @track_usage
    def create_dimensionality(self, organization_id: int, name: str, dimension_type: str, granularity: str) -> api.Dimensionality:
        """
        Creates a dimensionality record in a user's organization with format: DimensionType - Granularity
        """
        dimensionality = api.DimensionalityCreate(name=name,
                                                  dimensionType=dimension_type,
                                                  granularity=granularity,
                                                  organizationId=organization_id)
        response = self._post("/dimensionalities", dimensionality.dict(exclude_unset=True), api_version=1).json()
        return api.Dimensionality(**response)

    @track_usage
    def create_feature(self, organization_id: int, feature_set_id: int, name: str, code: str, description: str, column_id: int,
                       status: str, git_repo: str, tags: Optional[List[str]] = None) -> Feature:
        feature = api.FeatureCreate(name=name,
                                    code=code,
                                    description=description,
                                    featureSetId=feature_set_id,
                                    columnId=column_id,
                                    organizationId=organization_id,
                                    orchestrationStatus=status,
                                    tags=tags or [],
                                    gitRepo=git_repo)
        try:
            response = self._post("/features/", feature.dict(exclude_unset=True), api_version=1).json()
        except HTTPError as e:
            error_message = f"Failed to create Feature {name}."
            if e.response.status_code == 409:
                error_message += f" This name is already in use in your organization. Feature names must be unique."
            raise APIError(error_message)
        return Feature(api_object=response)

    @track_usage
    def create_feature_set(self, name: str, data_source_id: int, table_name: str, organization_id: int, 
                           granularity: Optional[str] = None, file_path: Optional[str] = None) -> FeatureSet:
        feature_set = api.v0.FeatureSetCreate(name=name,
                                              snowflakeTable=table_name,
                                              dataSourceId=data_source_id,
                                              granularity=granularity,
                                              rawFilePath=file_path)
        response = self._post("/feature-sets/", feature_set.dict(), api_version=0).json()
        return FeatureSet(api_object=response)

    @track_usage
    def create_model(self, name: str,
                     type: Union[str, ModelType],
                     granularity: Union[str, Granularity],
                     description: Optional[str] = None,
                     is_shared: Optional[bool] = False) -> Collection:
        """
        Creates model within Rasgo within the account specified by the API key.
        :param name: Model name
        :param model_type: Type of model specified
        :param granularity: Granularity of the data.
        :param is_shared: True = make model shared , False = make model private
        :return: Model object.
        """
        try:
            # If not enum, convert to enum first.
            model_type = type.name
        except AttributeError:
            model_type = ModelType(type)

        try:
            # If not enum, convert to enum first.
            granularity = granularity.name
        except AttributeError:
            granularity = Granularity(granularity)

        content = {"name": name,
                   "type": model_type.value,
                   "granularities": [{"name": granularity.value}],
                   "isShared": is_shared
                   }
        if description:
            content["description"] = description
        response = self._post("/models", _json=content, api_version=1)
        return Collection(api_object=response.json())

    @track_usage
    def put_collection_attributes(self, collection_id: int, attributes: List[dict]):
        """
        Create or update attributes on a Rasgo Collection

        param attributes: dict [{"key": "value"}, {"key": "value"}]
        """
        msg = 'attributes parameter must be passed in as a list of k:v pairs. Example: [{"key": "value"}, {"key": "value"}]'
        if not isinstance(attributes, list):
            raise APIError(msg)
        attr = []
        for kv in attributes:
            if not isinstance(kv, dict):
                raise APIError(msg)
            for k, v in kv.items():
                attr.append(api.Attribute(key=k, value=v))
        attr_in = api.CollectionAttributeBulkCreate(collectionId = collection_id, attributes=attr)
        return self._put(f"/models/{collection_id}/attributes", attr_in.dict(exclude_unset=True), api_version=1).json()

    @track_usage
    def put_feature_attributes(self, feature_id: int, attributes: List[dict]):
        """
        Create or update attributes on a feature

        param attributes: dict [{"key": "value"}, {"key": "value"}]
        """
        msg = 'attributes parameter must be passed in as a list of k:v pairs. Example: [{"key": "value"}, {"key": "value"}]'
        if not isinstance(attributes, list):
            raise APIError(msg)
        attr = []
        for kv in attributes:
            if not isinstance(kv, dict):
                raise APIError(msg)
            for k, v in kv.items():
                attr.append(api.Attribute(key=k, value=v))
        attr_in = api.FeatureAttributeBulkCreate(featureId = feature_id,
                                             attributes=attr)
        return self._put(f"/features/{feature_id}/attributes", attr_in.dict(exclude_unset=True), api_version=1).json()

    @track_usage
    def post_feature_stats(self, feature_id: int):
        """
        Sends an api request to build feature stats for a specified feature.
        """
        return self._post(f"/features/{feature_id}/stats", api_version=1).json()

    @track_usage
    def post_feature_set_stats(self, feature_set_id: int):
        """
        Sends an api request to build feature stats for a specified feature.
        """
        return self._post(f"/feature-sets/{feature_set_id}/stats", api_version=1).json()

    @track_usage
    def post_data_source_stats(self, data_source_id: int):
        """
        Sends an api request to build stats for a specified data source.
        """
        return self._post(f"/data-source/profile/{data_source_id}", api_version=1).json()


# --------------------
# Patch / Update Calls
# --------------------
    @track_usage
    def update_column(self, column_id: int, name: Optional[str] = None, data_type: Optional[str] = None, 
                      feature_set_id: Optional[int] = None, dimension_id: Optional[int] = None
                      ) -> api.Column:
        column = api.ColumnUpdate(id=column_id,
                                  name=name, dataType=data_type,
                                  featureSetId=feature_set_id,
                                  dimensionId=dimension_id)
        response = self._patch(f"/columns/{column_id}", column.dict(exclude_unset=True, exclude_none=True), api_version=1).json()
        return api.Column(**response)

    @track_usage
    def update_data_source(self, data_source_id: int, name: Optional[str] = None, domain: Optional[str] = None, source_type: Optional[str] = None, table: Optional[str] = None, database: Optional[str] = None, schema: Optional[str] = None, table_status: Optional[str] = None, parent_source_id: Optional[int] = None):
        data_source = api.DataSourceUpdate(id=data_source_id,
                                           name=name,
                                           domain=domain,
                                           table=table,
                                           tableDatabase=database,
                                           tableSchema=schema,
                                           tableStatus=table_status,
                                           sourceType=source_type,
                                           parentId=parent_source_id)
        response = self._patch(f"/data-source/{data_source_id}", data_source.dict(exclude_unset=True, exclude_none=True), api_version=1).json()
        return DataSource(api_object=response)

    @track_usage
    def update_feature(self, feature_id: int, organization_id: Optional[int] = None, feature_set_id: Optional[int] = None, 
                       name: Optional[str] = None, code: Optional[str] = None, description: Optional[str] = None,
                       column_id: Optional[int] = None, status: Optional[str] = None, tags: Optional[List[str]] = None, 
                       git_repo: Optional[str] = None
                       ) -> Feature:
        feature = api.FeatureUpdate(id=feature_id,
                                    name=name,
                                    code=code,
                                    description=description,
                                    orchestrationStatus=status,
                                    tags=tags,
                                    gitRepo=git_repo)
        response = self._patch(f"/features/{feature_id}", feature.dict(exclude_unset=True, exclude_none=True), api_version=1).json()
        return Feature(api_object=response)

    @track_usage
    def update_feature_set(self, feature_set_id: int, name: Optional[str] = None, data_source_id: Optional[int] = None, 
                           table_name: Optional[str] = None, granularity: Optional[str] = None, file_path: Optional[str] = None
                           ) -> FeatureSet:
        feature_set = api.v0.FeatureSetUpdate(id=feature_set_id,
                                              name=name,
                                              snowflakeTable=table_name,
                                              dataSourceId=data_source_id,
                                              granularity=granularity,
                                              rawFilePath=file_path)
        response = self._patch(f"/feature-sets/{feature_set_id}", feature_set.dict(exclude_unset=True, exclude_none=True), api_version=0).json()
        return FeatureSet(api_object=response)


# ------------
# Delete Calls
# ------------
    def delete_collection(self):
        raise NotImplementedError('Not avaliable yet.')

    def delete_dimension(self):
        raise NotImplementedError('Not available yet.')

    def delete_feature(self):
        raise NotImplementedError('Not available yet.')

    def delete_feature_set(self):
        raise NotImplementedError('Not available yet.')


# ------------------
# Workflow Functions
# ------------------    
    @track_usage
    def prepare_feature_set_dict(self, feature_set_id: int = None):
        """
        Returns a dict of metadata values for the specificed Rasgo FeatureSet
        
        params
        ------
        feature_set_id: int: ID of a Rasgo FeatureSet
        
        Alternate Usage
        ---------------
        Pass in no params to return a blank featureset dict template
        """
        if feature_set_id:
            fs = self.get_feature_set(feature_set_id)
            return ingestion.save_feature_set_to_dict(fs)
        return ingestion.RASGO_DICT

    @track_usage
    def prepare_feature_set_yml(self, feature_set_id: int, file_name: str, directory: str = None):
        """
        Saves a yml file of metadata values for the specificed Rasgo FeatureSet to a directory location
        
        params
        ------
        feature_set_id: int: ID of a Rasgo FeatureSet
        file_name: str: name for the output file 
        directory: str: full dir location for the output file (minus file_name)
        """
        response = self._get(f"/feature-sets/{feature_set_id}", api_version=1).json()
        fs = api.v1.FeatureSetYML(**response)
        return ingestion.save_feature_set_to_yaml(fs, file_name=file_name, directory=directory)

    @track_usage
    def publish_features(self, features_dict: dict) -> FeatureSet:
        f"""
        Creates or updates Features based on metadata provided in the dict

        params:
            features_dict: Valid Rasgo dict (see below)

        return:
            Rasgo FeatureSet

        Valid Rasgo dict format:
        -----------------------
        {ingestion.RASGO_DICT}
        """
        # TODO need to publish docs on granularity and data types
        return self._save_feature_set_dict(features_dict)

    @track_usage
    def publish_features_from_df(self, df: pd.DataFrame, dimensions: List[str], features: List[str],
                                 granularity: List[str] = [], tags: List[str] = [], 
                                 sandbox: bool = True) -> FeatureSet:
        """
        Creates a Feature Set from a pandas dataframe

        :dataframe: Pandas DataFrame containing all columns that will be registered with Rasgo
        :param dimensions: List of columns in df that should be used for joins to other featursets
        :param features: List of columns in df that should be registered as features in Rasgo
        :param granularity: List of grains that describe the form of the data. Common values are: 'day', 'week', 'month', 'second'
        :param tags: List of tags to be added to all features in the df
        :return: description of the featureset created
        """
        # Type checking
        if not isinstance(dimensions, list) and all([isinstance(dimension, str) for dimension in dimensions]):
            raise TypeError('Dimensions must be provided as a list of strings, naming the columns within the dataframe')
        if not isinstance(features, list) and all([isinstance(feature, str) for feature in features]):
            raise TypeError('Features must be provided as a list of strings, naming the columns within the dataframe')
        if not isinstance(granularity, list):
            if isinstance(granularity, str):
                granularity = [granularity]
            else:
                raise TypeError("granularity must be provided as a list of strings")
        if not isinstance(tags, list):
            if isinstance(tags, str):
                tags = [tags]
            else:
                raise TypeError("tags must be provided as a list of strings")
        if len(granularity) > len(dimensions):
            raise APIError("Number of granularities cannot exceed number of dimensions." 
                           "Dimensions are the index fields your data should join on and group by."
                           "Granularity is an attribute that describes precision of your dimensions."
                           "Consider passing more dimensions or fewer granularities.")

        org_id = self._profile.get('organizationId', None)
        timestamp = self._make_timestamp()
        featureset_name = f"pandas_by_{'_'.join(dimensions)}_{timestamp}"
        data_source = self._save_data_source(name="PANDAS", table=featureset_name, domain="PANDAS", source_type="DataFrame")

        # Convert all strings to work with Snowflake
        # Confirm each named dimension and feature exists in the dataframe.
        self._confirm_df_columns(df, dimensions, features)

        # Create a table in the data warehouse with the subset of columns we want, name table after featureset.
        all_columns = dimensions + features
        exportable_df = df[all_columns].copy()
        self.data_warehouse.write_dataframe_to_table(exportable_df, table_name=featureset_name)
        self.data_warehouse.grant_table_ownership(table=featureset_name, role=self.data_warehouse.publisher_role)
        self.data_warehouse.grant_table_access(table=featureset_name, role=self.data_warehouse.reader_role)

        # Add a reference to the FeatureSet
        featureset = self.create_feature_set(name=featureset_name, data_source_id=data_source.id,
                                             table_name=featureset_name, organization_id=org_id, granularity=', '.join(granularity),
                                             file_path=None)
        schema = dataframe.build_schema(df)

        # Add references to all the dimensions
        for d in dimensions:
            column = schema[d]
            data_type = column["type"]
            dimension_name = column["name"]
            dim_granularity = granularity.pop(0) if len(granularity) > 1 else granularity[0]
            self._save_dimension(organization_id=org_id, feature_set_id=featureset.id, name=dimension_name, data_type=data_type, dimension_type=None, granularity=dim_granularity)

        # Add references to all the features
        tags.append("Pandas")
        for f in features:
            column = schema[f]
            data_type = column["type"]
            code = column["name"]
            feature_name = f"PANDAS_{code}_{timestamp}"
            status = "Sandboxed" if sandbox else "Productionized"
            self._save_feature(organization_id=org_id, feature_set_id=featureset.id, name=feature_name, data_type=data_type, code=code, description=None, granularity=granularity[0], status=status, tags=tags, git_repo=None)
        
        self.post_feature_set_stats(featureset.id)
        return self.get_feature_set(featureset.id)

    @track_usage
    def publish_features_from_source(self, data_source_id: int,
                                     features: List[str], dimensions: List[str], 
                                     granularity: List[str] = [], tags: List[str] = [],
                                     feature_set_name: str = None,
                                     sandbox: bool = True, 
                                     if_exists: str = 'fail') -> FeatureSet:
        """
        Publishes a FeatureSet from an existing DataSource table

        params:
            data_source_id: ID to a Rasgo DataSource
            features: List of column names that will be features
            dimensions: List of column names that will be dimensions
            granularity: List of grains that describe the form of the data. Common values are: 'day', 'week', 'month', 'second'
            tags: List of tags to be added to all features
            feature_set_name: Optional name for the FeatureSet (if not passed a random string will be assigned)

            if_exists:  fail - returns an error message if a featureset already exists against this table
                        return - returns the featureset without operating on it
                        edit - edits the existing featureset
                        new - creates a new featureset

        return:
            Rasgo FeatureSet
        """
        # V1 Trade-offs / Possible Future Enhancements
        # --------------
        # Constucting a featureset using v0 method - cut over to v1
        # We aren't adding display names, descriptions to features
        # Do we allow running a script agasint the data_source table in this step?

        # Check for valid DataSource
        data_source = self.get_data_source(data_source_id)
        if not data_source.table:
            raise ValueError(f"DataSource {data_source_id} is not usable. Please make sure it exists and has a valid table registered.")
        if not isinstance(dimensions, list) and all([isinstance(dimension, str) for dimension in dimensions]):
            raise TypeError('Dimensions must be provided as a list of strings.')
        if not isinstance(features, list) and all([isinstance(feature, str) for feature in features]):
            raise TypeError('Features must be provided as a list of strings.')
        if not isinstance(granularity, list):
            if isinstance(granularity, str):
                granularity = [granularity]
            else:
                raise TypeError("granularity must be provided as a list of strings")
        if not isinstance(tags, list):
            if isinstance(tags, str):
                tags = [tags]
            else:
                raise TypeError("tags must be provided as a list of strings")
        if len(granularity) > len(dimensions):
            raise APIError("Number of granularities cannot exceed number of dimensions." 
                           "Dimensions are the index fields your data should join on and group by."
                           "Granularity is an attribute that describes precision of your dimensions."
                           "Consider passing more dimensions or fewer granularities.")

        db = data_source.tableDatabase.upper() if data_source.tableDatabase else None 
        schema = data_source.tableSchema.upper() if data_source.tableSchema else None
        table = data_source.table.split(".")[-1] if data_source.table.count(".") > 0 else data_source.table
        
        # Handle if FeatureSet already exists
        feature_set = self.match_feature_set(table_name=table)
        if feature_set and if_exists == 'fail':
            raise APIError(f"A featureset ({feature_set.id} - {feature_set.name}) is already built against this table. "
                            "Pass parameter if_exists = 'edit', 'new', or 'return' to continue.")
        
        columns = self.data_warehouse.get_source_columns(table=table, database=db, schema=schema)
        if columns.empty:
            raise APIError("The table associated with this DataSource is not accessible.")
        self._confirm_list_columns(columns["COLUMN_NAME"].values.tolist(), dimensions, features)

        # Publish Featureset V0
        timestamp = self._make_timestamp()
        org_id = self._profile.get("organizationId") 
        feature_set = self._save_feature_set(name=feature_set_name or data_source.name+"_"+timestamp,
                                                      data_source_id=data_source.id,
                                                      table_name=data_source.table,
                                                      granularity=', '.join(granularity),
                                                      organization_id=org_id,
                                                      if_exists=if_exists)

        for _i, row in columns.iterrows():
            if row["COLUMN_NAME"] in dimensions:
                dim_granularity = granularity.pop(0) if len(granularity) > 1 else granularity[0]
                self._save_dimension(organization_id=org_id,
                                              feature_set_id=feature_set.id,
                                              name=row["COLUMN_NAME"],
                                              data_type=self.data_warehouse._snowflakify_data_type(row["DATA_TYPE"]),
                                              granularity=dim_granularity,
                                              if_exists=if_exists)
            
            if row["COLUMN_NAME"] in features:
                self._save_feature(organization_id=org_id,
                                            feature_set_id=feature_set.id,
                                            name=row["COLUMN_NAME"],
                                            data_type=self.data_warehouse._snowflakify_data_type(row["DATA_TYPE"]),
                                            description=f"Feature {row['COLUMN_NAME']} created from DataSource {data_source.table}",
                                            code=row["COLUMN_NAME"],
                                            granularity=granularity[0],
                                            tags=tags,
                                            status="Sandboxed" if sandbox else "Productionized",
                                            if_exists=if_exists)

        self.post_feature_set_stats(feature_set.id)
        return self.get_feature_set(feature_set.id)

    @track_usage
    def publish_features_from_yml(self, yml_file: str, sandbox: Optional[bool] = True, 
                                  git_repo: Optional[str] = None) -> FeatureSet:
        """
        Publishes metadata about a FeatureSet to Pyrasgo

        :param yml_file: Rasgo compliant yml file that describes the featureset(s) being created
        :param sandbox: Status of the features (True = 'Sandboxed' | False = 'Productionized')
        :param git_repo: Filepath string to these feature recipes in git
        :return: description of the featureset created
        """
        with open(yml_file) as fobj:
            contents = yaml.load(fobj, Loader=yaml.SafeLoader)
        if isinstance(contents, list):
            raise APIError("More than one feature set found, please pass in only one feature set per yml")
        else:
            feature_set = self._save_feature_set_dict(contents)
        return feature_set

    @track_usage
    def publish_source_data(self, source_type: str, 
                            file_path: Optional[Path] = None, 
                            df: Optional[pd.DataFrame] = None, 
                            table: Optional[str] = None, table_database:Optional[str] = None, table_schema: Optional[str] = None,
                            data_source_name: Optional[str] = None, data_source_domain: Optional[str] = None, 
                            data_source_table_name: Optional[str] = None, parent_data_source_id: Optional[int] = None, 
                            if_exists: Optional[str] = 'fail'
                            ) -> DataSource:
        """
        Push a csv, Dataframe, or table to a Snowflake table and register it as a Rasgo DataSource (TM)

        NOTES: csv files will import all columns as strings

        params:
            source_type: Values: ['csv', 'dataframe', 'table']
            df: pandas DataFrame (only use when passing source_type = 'dataframe')
            file_path: full path to a file on your local machine (only use when passing source_type = 'csv')
            table: name of a valid Snowflake table in your Rasgo account (only use when passing source_type = 'table')
            table_database: Optional: name of the database of the table passed in 'table' param (only use when passing source_type = 'table')
            table_schema: Optional: name of the schema of the table passed in 'table' param (only use when passing source_type = 'table')
            
            data_source_name: Optional name for the DataSource (if not provided a random string will be used)
            data_source_table_name: Optional name for the DataSource table in Snowflake (if not provided a random string will be used)
            data_source_domain: Optional domain for the DataSource (default is NULL)
            parent_data_source_id: Optional ID of a valid Rasgo DataSource that is a parent to this DataSource (default is NULL)

            if_exists: Values: ['fail', 'append', 'replace'] directs the function what to do if a DataSource already exists with this table name  (defaults to fail)

        return:
            Rasgo DataSource
        """
        # V1 Trade-offs / Possible Future Enhancements
        # --------------
        # csv's upload with all columns as string data type
        # uploading csv locally vs. calling the post/data-source/csv endpoint

        # Validate inputs
        vals = ["csv", "dataframe", "table"]
        if source_type.lower() not in vals:
            raise ParameterValueError("sourceType", vals)
        if source_type.lower() == "csv" and not Path(file_path).exists():
            raise FileNotFoundError("Please pass in a valid file path using the file_path parameter")
        if source_type.lower() == "dataframe" and df.empty:
            raise ImportError("Please pass in a valid DataFrame using the df parameter")
        if source_type.lower() == "table":
            if not table:
                raise ValueError("Please pass in a valid table using the table parameter")
            try:
                src_table = self.data_warehouse.get_source_table(table_name=table, database=table_database, schema=table_schema, record_limit=10)
                if src_table.empty:
                    raise APIError(f"Source table {table} is empty or this role does not have access to it.")
            except:
                raise APIError(f"Source table {table} does not exist or this role does not have access to it.")
        if data_source_table_name == "":
            raise ParameterValueError("data_source_table_name", "a valid SQL table name")

        # Determine the source table based on user inputs
        if source_type in ["csv", "dataframe"]:
            table_name = data_source_table_name or self._random_table_name()
        else: #source_type == "table":
            table_name = table
        table_name = table_name.upper()
        table_database = table_database if table == table_name else None
        table_schema = table_schema if table == table_name else None
       
        # Check if a DataSource already exists
        data_source = self.match_data_source(table=table_name)
        if data_source:
            # If it does, override to the existing table
            table_name = data_source.table
            table_database = data_source.tableDatabase
            table_schema = data_source.tableSchema
            
            # Then handle input directives
            vals = ["append", "fail", "replace"]
            msg = f"DataSource {data_source.id} already exists. "
            if data_source.organizationId != self._profile.get('organizationId'):
                raise APIError(msg+"This API key does not have permission to replace it.")
            if data_source.sourceType != source_type:
                raise APIError(msg+"Your input parameters would edit the source_type. To change DataSource attributes, use the update_data_source method. To update this source table, ensure your input parameters match the DataSource definition.")
            if if_exists not in vals:
                raise ParameterValueError("if_exists", vals)
            if if_exists == 'fail':
                raise APIError(msg+"Pass if_exists='replace' or 'append' to proceed.")

        # Determine operation to perform: [create, append, replace, register, no op]
        table_fqtn = f"{table_database}.{table_schema}.{table_name}"
        _operation = self._source_table_operation(source_type, if_exists, table_fqtn)
        print(f"Proceeding with operation {_operation}")
        # we'll want this function for future when we support more complex table operations
        # for now, its sole purpose is to check table existence, raise directive errors

        # Upload to Snowflake
        # Path: csv & dataframe
        if source_type.lower() in ["csv", "dataframe"]:
            if source_type.lower() == "csv":
                df = pd.read_csv(file_path, prefix="COL")
            print("Uploading to table:", table_name)
            self.data_warehouse._snowflakify_dataframe(df)
            self.data_warehouse.write_dataframe_to_table(df, table_name=table_name, append=True if if_exists=="append" else False)
            self.data_warehouse.grant_table_ownership(table=table_name, role=self.data_warehouse.publisher_role)
            self.data_warehouse.grant_table_access(table=table_name, role=self.data_warehouse.reader_role)

        # Path: table            
        if source_type.lower() == "table":
            print(f"Granting read access on table {table_name} to {self.data_warehouse.reader_role.upper()}")
            # NOTE: grant_table_acess is intentional here
            # In other methods, we create a table with the rasgo user role and want to hand if off to the reader role
            # In this case, the table is likely part of a pre-existing rbac model and we just want to grant rasgo access
            self.data_warehouse.grant_table_access(table=table_name, role=self.data_warehouse.reader_role, database=table_database, schema=table_schema)

        # Publish DataSource
        data_source = self._save_data_source(name=data_source_name or table_name,
                                                      table=table_name,
                                                      domain=data_source_domain,
                                                      source_type=source_type,
                                                      parent_source_id=parent_data_source_id,
                                                      if_exists='edit')
        if data_source:
            self.post_data_source_stats(data_source.id)
            return data_source
        else:
            raise APIError("DataSource failed to upload")

    @track_usage
    def read_collection_data(self, collection_id: int,
                             filters: Optional[Dict[str, str]] = None,
                             limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs a pandas DataFrame from the specified Rasgo Collection

        :param collection_id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        collection = self.get_collection(collection_id)
        if collection:
            try:
                table_metadata = collection._make_table_metadata()
                query, values = self.data_warehouse._make_select_statement(table_metadata, filters, limit)
                return self.data_warehouse.query_into_dataframe(query, values)
            except:
                raise APIError("Collection table is not reachable")
        raise APIError("Collection does not exist")

    @track_usage
    def read_feature_data(self, feature_id: int,
                          filters: Optional[Dict[str, str]] = None,
                          limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs a pandas DataFrame from the specified Rasgo Feature data

        :param feature_id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        feature = self.get_feature(feature_id)
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
    def read_source_data(self, source_id: int,
                         filters: Optional[Dict[str, str]] = None,
                         limit: Optional[int] = None) -> pd.DataFrame:
        """
        Constructs a pandas DataFrame from the specified Rasgo DataSource

        :param source_id: int
        :param filters: dictionary providing columns as keys and the filtering values as values.
        :param limit: integer limit for number of rows returned
        :return: Dataframe containing feature data
        """
        data_source = self.get_data_source(data_source_id=source_id)
        if data_source:
            try:
                table_metadata = data_source._make_table_metadata()
                query, values = self.data_warehouse._make_select_statement(table_metadata, filters, limit)
                return self.data_warehouse.query_into_dataframe(query, values)
            except:
                raise APIError("DataSource table is not reachable")
        raise APIError("DataSource does not exist")


# ---------------------
# Awkward Model Methods
# ---------------------
    # Alias
    @track_usage
    def get_feature_data(self, model_id: int,
                         filters: Optional[Dict[str, str]] = None,
                         limit: Optional[int] = None) -> pd.DataFrame:
        return self.read_collection_data(collection_id=model_id, filters=filters, limit=limit)


# -------------------------------
# Undocumented / Helper Functions
# -------------------------------

    def _confirm_df_columns(self, dataframe: pd.DataFrame, dimensions: List[str], features: List[str]):
        self._confirm_list_columns(list(dataframe.columns), dimensions, features)

    def _confirm_list_columns(self, columns: list, dimensions: List[str], features: List[str]):
        missing_dims = []
        missing_features = []
        consider = []
        for dim in dimensions:
            if dim not in columns:
                missing_dims.append(dim)
                if self.data_warehouse._snowflakify_name(dim) in columns:
                    consider.append(self.data_warehouse._snowflakify_name(dim))
        for ft in features:
            if ft not in columns:
                missing_features.append(ft)
                if self.data_warehouse._snowflakify_name(ft) in columns:
                    consider.append(self.data_warehouse._snowflakify_name(ft))
        if missing_dims or missing_features:
            raise APIError(f"Specified columns do not exist in dataframe: "
                           f"Dimensions({missing_dims}) Features({missing_features}) "
                           f"Consider these: ({consider})?")

    def _get_user(self):
        return self._get("/users/me", api_version=1).json()

    def _make_timestamp(self):
        now = datetime.now()
        return now.strftime("%Y_%m_%d_%H_%M")

    def _save_data_source(self, name: str, table: str, database: Optional[str] = None, schema: Optional[str] = None, domain: Optional[str] = None, source_type: Optional[str] = None, parent_source_id: Optional[int] = None, if_exists: str = 'return') -> DataSource:
        """
        Creates or returns a DataSource depending on of the defined parameters
        
        if_exists:  return - returns the source without operating on it
                    edit - edits the existing source
                    new - creates a new source
        """
        ds = self.match_data_source(table=table)
        if ds and if_exists == 'return':
            return ds
        if ds and if_exists == 'edit':
            return self.update_data_source(data_source_id=ds.id, name=name, table=table, database=database, schema=schema, domain=domain, source_type=source_type, parent_source_id=parent_source_id)
        return self.create_data_source(name=name, table=table, database=database, schema=schema, domain=domain, source_type=source_type, parent_source_id=parent_source_id)

    def _save_dimension(self, organization_id: int, feature_set_id: int, name: str, data_type: str, display_name: Optional[str] = None,
                          dimension_type: Optional[str] = None, granularity: Optional[str] = None, if_exists: str = 'return') ->api.Column:
        """
        Creates or updates a dimension depending on existence of the defined parameters
        
        if_exists:  return - returns the source without operating on it
                    edit - edits the existing source
                    new - creates a new source
        """
        dimensionality = self._save_dimensionality(organization_id=organization_id, dimension_type=dimension_type, granularity=granularity)
        dim = self.match_column(name=name, feature_set_id=feature_set_id)
        if dim and if_exists == 'return':
            return dim
        if dim and if_exists == 'edit':
            return self.update_column(column_id=dim.id, name=name, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimensionality.id)
        return self.create_column(name=name, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimensionality.id)

    def _save_dimensionality(self, organization_id: int, dimension_type: Optional[str] = None,
                               granularity: Optional[str] = None, if_exists: str = 'return') -> api.Dimensionality:
        """
        Creates or returns a dimensionality depending on existence of the defined parameters

        Dimensionality is a named pairing of a datatype and a granularity. Note in some cases the
        granularity is actually a data type.
        """
        # TODO: We should move this mapping to the Granularity enum class or behind an API
        if dimension_type is None:
            if granularity.lower() in ["second", "minute", "hour", "day", "week", "month", "quarter", "year"]:
                dimension_type = "DateTime"
            elif granularity.lower() in ["latlong", "zipcode", "fips", "dma", "city", "cbg", "county", "state",
                                         "country"]:
                dimension_type = "Geolocation"
            else:
                dimension_type = "Custom"
        elif dimension_type.lower() == "datetime":
            dimension_type = "DateTime"
        elif dimension_type.lower() in ["geo", "geoloc", "geolocation"]:
            dimension_type = "Geolocation"
        else:
            dimension_type = dimension_type.title()
        dimensionality_name = "{} - {}".format(dimension_type, str(granularity).title())

        dimensionality = self.match_dimensionality(granularity)
        # No edit path for dimensionality for now...
        if dimensionality and if_exists in ['return', 'edit']:
            return dimensionality
        return self.create_dimensionality(organization_id=organization_id, name=dimensionality_name, dimension_type=dimension_type, granularity=granularity)

    def _save_feature(self, organization_id: int, feature_set_id: int, name: str, data_type: str, code: Optional[str] = None,
                        description: Optional[str] = None, granularity: Optional[str] = None,
                        status: Optional[str] = None, tags: Optional[List[str]] = None, git_repo: Optional[str] = None, if_exists: str = 'return') -> Feature:
        """
        Creates or updates a feature depending on existence of the defined parameters

        if_exists:  return - returns the source without operating on it
                    edit - edits the existing source
                    new - creates a new source
        """
        code = code or name
        description = description or f"Feature that contains {name} data"
        status = status or "Sandboxed"
        dimension_id = None if granularity is None else self._save_dimensionality(organization_id=organization_id, dimension_type=None, granularity=granularity).id

        ft = self.match_feature(code, feature_set_id)
        if ft and if_exists == 'return':
            return ft
        if ft and if_exists == 'edit':
            self.update_column(column_id=ft.columnId, name=code, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimension_id)
            return self.update_feature(feature_id=ft.id, name=name, code=code, description=description, status=status, tags=tags or [], git_repo=git_repo)
        column = self.create_column(name=code, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimension_id)
        return self.create_feature(organization_id=organization_id, feature_set_id=feature_set_id, name=name, code=code, description=description, column_id=column.id, status=status, git_repo=git_repo, tags=tags or [])

    def _save_feature_set(self, name: str, data_source_id: int, table_name: str, organization_id: int, granularity: Optional[str] = None, file_path: Optional[str] = None, if_exists: str = 'return') -> FeatureSet:
        """
        Creates or updates a featureset depending on existence of the defined parameters

        if_exists:  return - returns the source without operating on it
                    edit - edits the existing source
                    new - creates a new source
        """
        fs = self.match_feature_set(table_name=table_name, fs_name=name)
        if fs and if_exists == 'return':
            return fs
        if fs and if_exists == 'edit':
            return self.update_feature_set(feature_set_id=fs.id, name=name, data_source_id=data_source_id, table_name=table_name, granularity=granularity, file_path=file_path)
        return self.create_feature_set(name=name, data_source_id=data_source_id, table_name=table_name, organization_id=organization_id, granularity=granularity, file_path=file_path)

    def _save_feature_set_dict(self, feature_set_dict: dict) -> FeatureSet:
        """
        Creates or updates a featureset based on values in a dict
        """
        if not ingestion._confirm_valid_dict(dict_in=feature_set_dict):
            raise APIError("Not a valid dict")
        org_id = self._profile.get('organizationId', None)
        source_table = feature_set_dict.get("sourceTable")
        ds = feature_set_dict.get("datasource")
        ds_name = ds.get("name", source_table) if ds else source_table
        data_source = self._save_data_source(name=ds_name, table=source_table, source_type="Table")
        featureset_name = feature_set_dict.get("name", source_table)
        tags = []
        if feature_set_dict.get("tags"):
            for t in feature_set_dict.get("tags"):
                tags.append(t)
        attributes = []
        if feature_set_dict.get("attributes"):
            for a in feature_set_dict.get("attributes"):
                for k, v in a.items():
                    attributes.append({k: v})
        featureset = self._save_feature_set(name=featureset_name, data_source_id=data_source.id, table_name=source_table, organization_id=org_id, if_exists='edit')
            
        # publish dimensions
        for dim in feature_set_dict["dimensions"]:
            name = dim.get("columnName")
            display_name = dim.get("displayName")
            data_type = dim.get("dataType")
            # if we get an enum, convert it to str so pydantic doesn't get mad
            if isinstance(data_type, api.v1.DataType):
                data_type = data_type.value
            dim_granularity = dim.get("granularity")
            self._save_dimension(organization_id=org_id, feature_set_id=featureset.id, name=name, display_name=display_name, data_type=data_type, granularity=dim_granularity, if_exists='edit')

        # publish features
        for feature in feature_set_dict["features"]:
            name = feature.get("displayName")
            code = feature.get("columnName")
            data_type = feature.get("dataType")
            # if we get an enum, convert it to str so pydantic doesn't get mad
            if isinstance(data_type, api.v1.DataType):
                data_type = data_type.value
            description = feature.get("description", f"Feature that contains {name} data")
            # apply featureset tags to all features...
            feature_tags = tags
            # ...and add feature-specific tags
            if feature.get("tags"):
                for t in feature.get("tags"):
                    feature_tags.append(t)
            feature_attributes = attributes
            if feature.get("attributes"):
                for a in feature.get("attributes"):
                    for k, v in a.items():
                        feature_attributes.append({k: v})
            status = "Sandboxed" if feature_set_dict.get("status") == "Sandboxed" else "Productionized"
            f = self._save_feature(organization_id=org_id, feature_set_id=featureset.id, name=name, data_type=data_type, code=code, description=description, status=status, tags=feature_tags, if_exists='edit')
            self.put_feature_attributes(f.id, feature_attributes)

        # Post stats for features
        self.post_feature_set_stats(featureset.id)
        return self.get_feature_set(featureset.id)

    def _random_table_name(self):
        identifier = str(uuid.uuid4())
        table_name = ''.join(list(lstrip(hashlib.md5(identifier.encode('utf-8')).hexdigest(),
                                lambda x: x.isnumeric()))).upper()
        return table_name

    def _source_table_operation(self, source_type: str, if_exists: str, to_fqtn: str, from_fqtn: Optional[str] = None):
        """
        Called by publish_source_data: 
            Given a source_type and tables, return the operation that should be performed to publish this table
        """
        to_database = to_fqtn.split(".")[0]
        to_schema = to_fqtn.split(".")[1]
        to_table = to_fqtn.split(".")[-1]
        data_source_exists = True if self.match_data_source(table=to_table) is not None else False

        try: 
            dest_table = self.data_warehouse.get_source_table(table_name=to_table, database=to_database, schema=to_schema, record_limit=10)
            is_dest_table_empty = dest_table.empty
        except:
            is_dest_table_empty = True

        if source_type in ["csv", "dataframe"]:
            if not data_source_exists:
                if is_dest_table_empty:
                    return "create"
                else: #not is_dest_table_empty
                    raise APIError(f"A table named {to_fqtn} already exists, but is not registered as a Rasgo DataSource. " 
                                   f"Try running this function with params: source_type='table', table='{to_table}'. "
                                    "If this wasn't an intentional match, run this function again to generate a new table name.")
            elif data_source_exists:
                if is_dest_table_empty:
                    return "create"
                else: #not is_dest_table_empty
                    return if_exists
            else:
                raise APIError("Could not determine what operation to perform.")
        elif source_type == "table":
            if not data_source_exists:
                return "register"
            elif not is_dest_table_empty and if_exists in ["append", "replace"]:
                print(f"pyRasgo does not support {if_exists} operations on tables yet.")
            return "no op"
        else:
            raise APIError("Could not determine what operation to perform.")