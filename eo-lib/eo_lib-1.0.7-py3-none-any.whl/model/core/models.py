from sqlalchemy import Column, String,ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import UUIDType, URLType
from eo_lib.config.base import Entity

class ApplicationType (Entity):

    """ Represents a Type of Application."""

    __tablename__ = "application_type"
    application = relationship("Application", back_populates="application_type")

class Application(Entity):

    """ Represents an Application."""

    __tablename__ = "application"
    application_type_id = Column(Integer, ForeignKey('application_type.id'))
    application_type = relationship("ApplicationType", back_populates="application")
    configuration = relationship("Configuration", back_populates="application")

    def __str__(self):
        return self.name

class Configuration(Entity):

    """ Represents an Configuation of an application."""

    __tablename__ = "configuration"

    secret = Column(String(200), nullable=False)
    url = Column(URLType)

    application_id = Column(Integer, ForeignKey('application.id'))
    application = relationship("Application", back_populates="configuration")


class ApplicationReference(Entity):

    """ Represents an referece of an entity in an application."""

    __tablename__ = "application_reference"
    # external application's data
    configuration = Column(Integer, ForeignKey('configuration.id'))

    external_id = Column(String(200), nullable=False)
    external_url = Column(URLType)
    external_type_entity = Column(String(200), nullable=False)

    #Internal BD
    internal_uuid = Column(UUIDType(binary=False))
    entity_name = Column(String(200), nullable=False)

