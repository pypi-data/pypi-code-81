from ..base import BaseModel

import typing


class Place(BaseModel):
    id: int
    title: str
    latitude: float
    longitude: float
    created: int
    icon: str
    checkins: int
    updated: int
    type: int
    country: int
    city: int
    address: str


class GeoPlace(BaseModel):
    id: int
    title: str
    latitude: int
    longitude: int
    created: int
    icon: str
    country: str
    city: str
    type: int
    group_id: int
    group_photo: str
    checkins: int
    updated: int
    address: int
