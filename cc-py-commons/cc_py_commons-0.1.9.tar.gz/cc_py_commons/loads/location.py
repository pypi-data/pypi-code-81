from dataclasses import dataclass, field

@dataclass
class Location:

    city: str
    state: str
    postcode: str
    county: str = field(default=None)
    country: str = field(default=None)
