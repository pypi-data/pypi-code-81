from requests.exceptions import HTTPError
from typing import List, Optional, Union

from .connection import Connection
from .error import APIError
from pyrasgo.primitives.enums import Granularity, ModelType
from pyrasgo.primitives.collection import Collection
from pyrasgo.primitives.feature import Feature, FeatureList
from pyrasgo.primitives.feature_set import FeatureSet
from pyrasgo.primitives.source import DataSource
from pyrasgo.utils.monitoring import track_usage
from pyrasgo import schemas as api


class Create(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @track_usage
    def collection(self, 
                   name: str,
                   type: Union[str, ModelType],
                   granularity: Union[str, Granularity],
                   description: Optional[str] = None,
                   is_shared: Optional[bool] = False) -> Collection:
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
    def column(self, 
               name: str, 
               data_type: str, 
               feature_set_id: int, 
               dimension_id: int) -> api.Column:
        column = api.ColumnCreate(name=name, dataType=data_type,
                                  featureSetId=feature_set_id,
                                  dimensionId=dimension_id)
        response = self._post("/columns/", column.dict(exclude_unset=True), api_version=1).json()
        return api.Column(**response)

    @track_usage
    def data_source(self, 
                    name: str, 
                    source_type: str, 
                    table: str, 
                    database: Optional[str] = None, 
                    schema: Optional[str] = None, 
                    domain: Optional[str] = None, 
                    parent_source_id: Optional[int] = None) -> DataSource:
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
    def data_source_stats(self, data_source_id: int):
        """
        Sends an api request to build stats for a specified data source.
        """
        return self._post(f"/data-source/profile/{data_source_id}", api_version=1).json()

    @track_usage
    def dimensionality(self, 
                       organization_id: int, 
                       name: str, 
                       dimension_type: str, 
                       granularity: str) -> api.Dimensionality:
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
    def feature(self, 
                organization_id: int, 
                feature_set_id: int, 
                name: str, code: str, 
                description: str, 
                column_id: int,
                status: str, 
                git_repo: str, 
                tags: Optional[List[str]] = None) -> Feature:
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
    def feature_set(self, 
                    name: str, 
                    data_source_id: int, 
                    table_name: str, 
                    organization_id: int, 
                    granularity: Optional[str] = None, 
                    file_path: Optional[str] = None) -> FeatureSet:
        feature_set = api.v0.FeatureSetCreate(name=name,
                                              snowflakeTable=table_name,
                                              dataSourceId=data_source_id,
                                              granularity=granularity,
                                              rawFilePath=file_path)
        response = self._post("/feature-sets/", feature_set.dict(), api_version=0).json()
        return FeatureSet(api_object=response)
    
    @track_usage
    def feature_set_stats(self, feature_set_id: int):
        """
        Sends an api request to build feature stats for a specified feature.
        """
        return self._post(f"/feature-sets/{feature_set_id}/stats", api_version=1).json()
    
    @track_usage
    def feature_stats(self, feature_id: int):
        """
        Sends an api request to build feature stats for a specified feature.
        """
        return self._post(f"/features/{feature_id}/stats", api_version=1).json()