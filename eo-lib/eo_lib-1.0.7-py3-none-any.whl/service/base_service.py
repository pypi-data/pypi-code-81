from abc import ABC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from eo_lib.config.config import engine
from eo_lib.model.core.models import ApplicationReference

class BaseService(ABC):

    """ Abstract Class responsible for implemeting functions that are common in a service. """

    def __init__(self, object):
        self.object = object
        self.type = self.object.__tablename__

    def __create_session_connection(self):
        Session = sessionmaker(bind=engine,autocommit=True)
        self.session = Session()
        self.session.begin(subtransactions=True)

    def __close_session_connection(self):
        self.session.close()

    def find_all(self):
        self.__create_session_connection()
        results = self.session.query(self.object).order_by(self.object.id).all()
        return results

    def find_by_uuid(self, uuid):
        self.__create_session_connection()
        return self.session.query(self.object).filter(self.object.uuid == uuid).first()

    def create(self, object):
        self.__create_session_connection()
        try:
            local_object = self.session.merge(object)
            self.session.add(local_object)
            self.session.commit()
        except:
            self.session.rollback() 
            raise

    def update(self, object):
        self.__create_session_connection()
        try:
            self.session.query(self.object).filter(self.object.id == object.id).update({column: getattr(object, column) for column in self.object.__table__.columns.keys()})
            self.session.commit()
        except:
            self.session.rollback() 
            raise

    def delete(self, object):
        self.__create_session_connection()
        try:
            self.session.delete(object)
            self.session.commit()
        except:
            self.session.rollback() 
            raise
