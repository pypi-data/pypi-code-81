from .qradarmodel import QRadarModel


class CustomProperty(QRadarModel):

    def __init__(self, *, id: int = None, identifier: str = None, name: str = None, username: str = None, description: str = None, property_type: str = None,
                 use_for_rule_engine: bool = None, datetime_format: str = None, locale: str = None, auto_discovered: bool = None):
        self.id = id
        self.identifier = identifier
        self.name = name
        self.username = username
        self.description = description
        self.property_type = property_type
        self.use_for_rule_engine = use_for_rule_engine
        self.datetime_format = datetime_format
        self.locale = locale
        self.auto_discovered = auto_discovered
