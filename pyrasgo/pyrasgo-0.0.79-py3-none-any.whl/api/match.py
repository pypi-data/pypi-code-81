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


class Match(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @track_usage
    def data_source(self, table: str) -> DataSource:
        """
        Returns the first Data Source that matches the specified name
        """
        try:
            response = self._get(f"/data-source", {"table": table}, api_version=1).json()
            return DataSource(api_object=response[0])
        except:
            return None

    @track_usage
    def dimensionality(self, granularity: str) -> api.Dimensionality:
        """
        Returns the first community or private Dimensionality that matches the specified granularity 
        """
        try:
            response = self._get(f"/dimensionalities/granularity/{granularity}", api_version=1).json()
            return api.Dimensionality(**response)
        except:
            return None

    @track_usage
    def column(self, name: str, feature_set_id: int) -> Optional[api.Column]:
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
    def feature(self, code: str, feature_set_id: int) -> Optional[Feature]:
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
    def feature_set(self, table_name: str, fs_name: Optional[str] = None) -> Optional[FeatureSet]:
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