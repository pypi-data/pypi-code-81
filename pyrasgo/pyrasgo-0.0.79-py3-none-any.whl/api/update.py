from typing import List, Optional

from .connection import Connection
from .error import APIError
from pyrasgo.primitives.enums import Granularity, ModelType
from pyrasgo.primitives.collection import Collection
from pyrasgo.primitives.feature import Feature, FeatureList
from pyrasgo.primitives.feature_set import FeatureSet
from pyrasgo.primitives.source import DataSource
from pyrasgo.utils.monitoring import track_usage
from pyrasgo import schemas as api


class Update(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @track_usage
    def collection_attributes(self, 
                              id: int, 
                              attributes: List[dict]):
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
        attr_in = api.CollectionAttributeBulkCreate(collectionId = id, attributes=attr)
        return self._put(f"/models/{id}/attributes", attr_in.dict(exclude_unset=True), api_version=1).json()

    @track_usage
    def column(self, 
               id: int, 
               name: Optional[str] = None, 
               data_type: Optional[str] = None, 
               feature_set_id: Optional[int] = None, 
               dimension_id: Optional[int] = None) -> api.Column:
        column = api.ColumnUpdate(id=id,
                                  name=name, dataType=data_type,
                                  featureSetId=feature_set_id,
                                  dimensionId=dimension_id)
        response = self._patch(f"/columns/{id}", column.dict(exclude_unset=True, exclude_none=True), api_version=1).json()
        return api.Column(**response)

    @track_usage
    def data_source(self, 
                    id: int, 
                    name: Optional[str] = None, 
                    domain: Optional[str] = None, 
                    source_type: Optional[str] = None, 
                    table: Optional[str] = None, 
                    database: Optional[str] = None, 
                    schema: Optional[str] = None, 
                    table_status: Optional[str] = None, 
                    parent_source_id: Optional[int] = None):
        data_source = api.DataSourceUpdate(id=id,
                                           name=name,
                                           domain=domain,
                                           table=table,
                                           tableDatabase=database,
                                           tableSchema=schema,
                                           tableStatus=table_status,
                                           sourceType=source_type,
                                           parentId=parent_source_id)
        response = self._patch(f"/data-source/{id}", data_source.dict(exclude_unset=True, exclude_none=True), api_version=1).json()
        return DataSource(api_object=response)

    @track_usage
    def feature(self, 
                id: int, 
                organization_id: Optional[int] = None, 
                feature_set_id: Optional[int] = None, 
                name: Optional[str] = None, 
                code: Optional[str] = None, 
                description: Optional[str] = None,
                column_id: Optional[int] = None, 
                status: Optional[str] = None, 
                tags: Optional[List[str]] = None, 
                git_repo: Optional[str] = None) -> Feature:
        feature = api.FeatureUpdate(id=id,
                                    name=name,
                                    code=code,
                                    description=description,
                                    orchestrationStatus=status,
                                    tags=tags,
                                    gitRepo=git_repo)
        response = self._patch(f"/features/{id}", feature.dict(exclude_unset=True, exclude_none=True), api_version=1).json()
        return Feature(api_object=response)

    @track_usage
    def feature_attributes(self, 
                           id: int, 
                           attributes: List[dict]):
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
        attr_in = api.FeatureAttributeBulkCreate(featureId = id,
                                             attributes=attr)
        return self._put(f"/features/{id}/attributes", attr_in.dict(exclude_unset=True), api_version=1).json()

    @track_usage
    def feature_set(self, 
                    id: int, 
                    name: Optional[str] = None, 
                    data_source_id: Optional[int] = None, 
                    table_name: Optional[str] = None, 
                    granularity: Optional[str] = None, 
                    file_path: Optional[str] = None) -> FeatureSet:
        feature_set = api.v0.FeatureSetUpdate(id=id,
                                              name=name,
                                              snowflakeTable=table_name,
                                              dataSourceId=data_source_id,
                                              granularity=granularity,
                                              rawFilePath=file_path)
        response = self._patch(f"/feature-sets/{id}", feature_set.dict(exclude_unset=True, exclude_none=True), api_version=0).json()
        return FeatureSet(api_object=response)