from datetime import datetime
from dataclasses import asdict, dataclass, fields
from typing import Union
from . import exceptions as exc
from .endpoints import Endpoints
from .sync import SyncClient


@dataclass
class PeepObject:
    """Base class for all objects."""

    id: int = None

    @staticmethod
    def endpoint():
        """Object API endpoint."""
        raise Exception(f"Not yet implemented on this object.")

    def to_schema(self, drop_id=False, drop_empty=False):
        dict_ = asdict(self)
        if drop_id is True:
            del dict_["id"]
        if drop_empty is True:
            dict_ = {k: v for k, v in dict_.items() if v is not None}
        return dict_

    def to_fields(self):
        return list(asdict(self).keys())

    @classmethod
    def generate(cls, client=None, schema: dict = {}):
        """Generate object from a schema."""
        obj = cls(**schema)
        obj.client = client
        return obj

    def create(self, client=None):
        """Creates a new object on the API."""
        if self.id is not None:
            raise exc.CRUDError(
                f"This object already has an id.  Cannot create new.  Use update() instead."
            )
        if client:
            self.client = client
        r = self.client.post(f"{self.endpoint()}", data=self.to_schema(drop_empty=True))
        self.id = r["id"]
        self.refresh()
        return r

    @classmethod
    def read(cls, client, id: int):
        """Read object from API using id."""
        schema = client.get(f"{cls.endpoint()}{id}")
        return cls.generate(client=client, schema=schema)

    def update(self):
        """Update the object state on the API."""
        if self.id is None:
            raise exc.CRUDError(
                f"This object has no id.  Cannot update it. Use create() instead."
            )
        return self.client.put(
            f"{self.endpoint()}{self.id}",
            data=self.to_schema(drop_id=True, drop_empty=True),
        )

    def delete(self):
        """Delete the object on the API."""
        if self.id is None:
            raise exc.CRUDError(f"This object has no id.  Cannot delete it on the API.")
        r = self.client.delete(f"{self.endpoint()}{self.id}")
        self.id = None
        return r

    def refresh(self):
        """Refreshes the current object from the API."""
        if self.id is None:
            raise exc.CRUDError(
                f"This object has no id.  Cannot refresh it from the API."
            )
        schema = self.client.get(f"{self.endpoint()}{self.id}")
        for k, v in schema.items():
            setattr(self, k, v)


@dataclass
class User(PeepObject):
    """A User."""

    email: str = None
    full_name: str = None
    is_active: bool = None
    can_read: bool = None
    can_write: bool = None
    is_superuser: bool = None
    password: str = None

    @staticmethod
    def endpoint():
        return Endpoints.USERS


@dataclass
class Periodicity(PeepObject):
    """A Periodicity for candles."""

    name: str = None
    description: str = None

    @staticmethod
    def endpoint():
        return Endpoints.PERIODICITIES


@dataclass
class Asset(PeepObject):
    """An asset."""

    name: str = None
    source: str = None

    @staticmethod
    def endpoint():
        return Endpoints.ASSETS


@dataclass
class Candle(PeepObject):
    """A Candle."""

    datetime: datetime = None
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    volume: float = None
    note: str = None
    asset_id: int = None
    periodicity_id: int = None

    @staticmethod
    def endpoint():
        return Endpoints.CANDLES


@dataclass
class Pattern(PeepObject):
    """A TA Pattern."""

    name: str = None
    category: str = None
    url: str = None
    parameters: dict = None
    active: bool = None
    datatype: str = None

    @staticmethod
    def endpoint():
        return Endpoints.PATTERNS


@dataclass
class Indicator(PeepObject):
    """An Indicator."""

    value: Union[float, list, dict] = None
    data: dict = None
    candle_id: int = None
    pattern_id: int = None

    @staticmethod
    def endpoint():
        return Endpoints.INDICATORS