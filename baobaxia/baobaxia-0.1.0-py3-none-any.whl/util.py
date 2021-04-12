from pydantic import BaseModel

class GeoLocation(BaseModel):
    latitude: float = .0
    longitude: float = .0
    description: str = ''

