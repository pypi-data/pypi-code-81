import pandas as pd
from typing import Dict, List, Optional

from .connection import Connection
from .error import APIError
from .get import Get
from .create import Create
from .match import Match
from .update import Update
from pyrasgo.primitives.collection import Collection
from pyrasgo.primitives.feature import Feature, FeatureList
from pyrasgo.primitives.feature_set import FeatureSet
from pyrasgo.primitives.source import DataSource
from pyrasgo.storage import DataWarehouse, SnowflakeDataWarehouse
from pyrasgo.utils import ingestion
from pyrasgo.utils.monitoring import track_usage
from pyrasgo import schemas as api


class Save(Connection):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_warehouse: SnowflakeDataWarehouse = DataWarehouse.connect()
        self.get = Get(api_key=self._api_key)
        self.match = Match(api_key=self._api_key)
        self.create = Create(api_key=self._api_key)
        self.update = Update(api_key=self._api_key)

    def data_source(self, 
                    name: str, 
                    table: str, 
                    database: Optional[str] = None, 
                    schema: Optional[str] = None, 
                    domain: Optional[str] = None, 
                    source_type: Optional[str] = None, 
                    parent_source_id: Optional[int] = None, 
                    if_exists: str = 'return') -> DataSource:
        """
        Creates or returns a DataSource depending on of the defined parameters
        
        if_exists:  return - returns the source without operating on it
                    edit - edits the existing source
                    new - creates a new source
        """
        ds = self.match.data_source(table=table)
        if ds and if_exists == 'return':
            return ds
        if ds and if_exists == 'edit':
            return self.update.data_source(id=ds.id, name=name, table=table, database=database, schema=schema, domain=domain, source_type=source_type, parent_source_id=parent_source_id)
        return self.create.data_source(name=name, table=table, database=database, schema=schema, domain=domain, source_type=source_type, parent_source_id=parent_source_id)

    def dimension(self, 
                  organization_id: int, 
                  feature_set_id: int, 
                  name: str, 
                  data_type: str, 
                  display_name: Optional[str] = None,
                  dimension_type: Optional[str] = None, 
                  granularity: Optional[str] = None, 
                  if_exists: str = 'return') ->api.Column:
        """
        Creates or updates a dimension depending on existence of the defined parameters
        
        if_exists:  return - returns the source without operating on it
                    edit - edits the existing source
                    new - creates a new source
        """
        dimensionality = self.dimensionality(organization_id=organization_id, dimension_type=dimension_type, granularity=granularity)
        dim = self.match.column(name=name, feature_set_id=feature_set_id)
        if dim and if_exists == 'return':
            return dim
        if dim and if_exists == 'edit':
            return self.update.column(id=dim.id, name=name, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimensionality.id)
        return self.create.column(name=name, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimensionality.id)

    def dimensionality(self, 
                       organization_id: int, 
                       dimension_type: Optional[str] = None,
                       granularity: Optional[str] = None, 
                       if_exists: str = 'return') -> api.Dimensionality:
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

        dimensionality = self.match.dimensionality(granularity)
        # No edit path for dimensionality for now...
        if dimensionality and if_exists in ['return', 'edit']:
            return dimensionality
        return self.create.dimensionality(organization_id=organization_id, name=dimensionality_name, dimension_type=dimension_type, granularity=granularity)

    def feature(self, 
                organization_id: int, 
                feature_set_id: int, 
                name: str, 
                data_type: str, 
                code: Optional[str] = None,
                description: Optional[str] = None, 
                granularity: Optional[str] = None,
                status: Optional[str] = None, 
                tags: Optional[List[str]] = None, 
                git_repo: Optional[str] = None, 
                if_exists: str = 'return') -> Feature:
        """
        Creates or updates a feature depending on existence of the defined parameters

        if_exists:  return - returns the source without operating on it
                    edit - edits the existing source
                    new - creates a new source
        """
        code = code or name
        description = description or f"Feature that contains {name} data"
        status = status or "Sandboxed"
        dimension_id = None if granularity is None else self.dimensionality(organization_id=organization_id, dimension_type=None, granularity=granularity).id

        ft = self.match.feature(code, feature_set_id)
        if ft and if_exists == 'return':
            return ft
        if ft and if_exists == 'edit':
            self.update.column(id=ft.columnId, name=code, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimension_id)
            return self.update.feature(id=ft.id, name=name, code=code, description=description, status=status, tags=tags or [], git_repo=git_repo)
        column = self.create.column(name=code, data_type=data_type, feature_set_id=feature_set_id, dimension_id=dimension_id)
        return self.create.feature(organization_id=organization_id, feature_set_id=feature_set_id, name=name, code=code, description=description, column_id=column.id, status=status, git_repo=git_repo, tags=tags or [])

    def feature_set(self, 
                    name: str, 
                    data_source_id: int, 
                    table_name: str, 
                    organization_id: int, 
                    granularity: Optional[str] = None, 
                    file_path: Optional[str] = None, 
                    if_exists: str = 'return') -> FeatureSet:
        """
        Creates or updates a featureset depending on existence of the defined parameters

        if_exists:  return - returns the source without operating on it
                    edit - edits the existing source
                    new - creates a new source
        """
        fs = self.match.feature_set(table_name=table_name, fs_name=name)
        if fs and if_exists == 'return':
            return fs
        if fs and if_exists == 'edit':
            return self.update.feature_set(id=fs.id, name=name, data_source_id=data_source_id, table_name=table_name, granularity=granularity, file_path=file_path)
        return self.create.feature_set(name=name, data_source_id=data_source_id, table_name=table_name, organization_id=organization_id, granularity=granularity, file_path=file_path)

    def feature_set_dict(self, 
                         feature_set_dict: dict) -> FeatureSet:
        """
        Creates or updates a featureset based on values in a dict
        """
        if not ingestion._confirm_valid_dict(dict_in=feature_set_dict):
            raise APIError("Not a valid dict")
        org_id = self._profile.get('organizationId', None)
        source_table = feature_set_dict.get("sourceTable")
        ds = feature_set_dict.get("datasource")
        ds_name = ds.get("name", source_table) if ds else source_table
        data_source = self.data_source(name=ds_name, table=source_table, source_type="Table")
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
        featureset = self.feature_set(name=featureset_name, data_source_id=data_source.id, table_name=source_table, organization_id=org_id, if_exists='edit')
            
        # publish dimensions
        for dim in feature_set_dict["dimensions"]:
            name = dim.get("columnName")
            display_name = dim.get("displayName")
            data_type = dim.get("dataType")
            # if we get an enum, convert it to str so pydantic doesn't get mad
            if isinstance(data_type, api.v1.DataType):
                data_type = data_type.value
            dim_granularity = dim.get("granularity")
            self.dimension(organization_id=org_id, feature_set_id=featureset.id, name=name, display_name=display_name, data_type=data_type, granularity=dim_granularity, if_exists='edit')

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
            f = self.feature(organization_id=org_id, feature_set_id=featureset.id, name=name, data_type=data_type, code=code, description=description, status=status, tags=feature_tags, if_exists='edit')
            self.update.feature_attributes(f.id, feature_attributes)

        # Post stats for features
        self.create.feature_set_stats(featureset.id)
        return self.get.feature_set(featureset.id)