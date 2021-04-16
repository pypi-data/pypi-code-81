from typing import Union, List

import time
from tqdm import tqdm

from pyrasgo.connection import Connection
from pyrasgo.monitoring import track_usage
from pyrasgo.namespace import Namespace
from pyrasgo.schemas import data_source as api


class DataSource(Connection):
    """
    Stores a Rasgo DataSource
    """

    def __init__(self, api_object, **kwargs):
        super().__init__(**kwargs)
        self._fields = api.DataSource(**api_object)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Source(id={self.id}, name={self.name}, sourceType={self.sourceType}, table={self.table})"

    def __getattr__(self, item):
        try:
            return self._fields.__getattribute__(item)
        except KeyError:
            self.get()
        try:
            return self._fields.__getattribute__(item)
        except KeyError:
            raise AttributeError(f"No attribute named {item}")

    @track_usage
    def get(self):
        """
        Updates the Soure's attributes from the API
        """
        self._fields = api.DataSource(**self._get(f"/data-source/{self.id}", api_version=1).json())

    @track_usage
    def rename(self, new_name: str):
        """
        Updates a DataSource's display name
        """
        print(f"Renaming DataSource {self.id} from {self.name} to {new_name}")
        source = api.DataSourceUpdate(id=self.id, name=new_name)
        self._fields = api.DataSource(**self._patch(f"/data-source/{self.id}", 
                                                    api_version=1, _json=source.dict(exclude_unset=True, exclude_none=True)).json())

    @property
    @track_usage
    def columns(self) -> List[api.DataSourceColumn]:
        """
        Returns columns in the DataSource table
        """
        response = self._get(f"/data-source/columns/{self.id}", api_version=1).json()
        return [api.DataSourceColumn(**column) for column in response['columns']]
    
    def _make_table_metadata(self):
        organization = self._get_profile().get("organization")
        metadata = {
            "database": self._fields.tableDatabase or organization.get("database"),
            "schema": self._fields.tableSchema or organization.get("schema"),
            "table": self._fields.table,
        }
        return metadata