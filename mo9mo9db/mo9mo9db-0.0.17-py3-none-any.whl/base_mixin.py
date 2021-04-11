from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.functions import current_timestamp

from mo9mo9db.dbsession import get_db_session


class DBBaseMixin(object):
    id = Column('id', Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return '<{0}.{1} object at {2}>'.format(
            self.__module__, type(self).__name__, hex(id(self)))

    @declared_attr
    def created_at(cls):
        return Column(DateTime, 
            default=datetime.now, 
            nullable=True, 
            server_default=current_timestamp())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, 
            default=datetime.now, 
            nullable=True, 
            onupdate=datetime.now, 
            server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def session(cls):
        return get_db_session()

    @classmethod
    def objects(cls, session):
        """
        :rtype : sqlalchemy.orm.query.Query
        """
        return session.query(cls)

    @classmethod
    def get(cls, session, pk):
        # primarykeyをフィルターに取得する方法
        return cls.objects(session).get(pk)

    @classmethod
    def select(cls, session, conditions):
        return cls.objects(session).filter(conditions).all()

    @classmethod
    def insert(cls, obj):
        session = cls.session()
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    def bulk_insert(cls, session, objs):
        session.add_all(objs)
        session.commit()
        return objs

    def delete(self, session):
        self.objects(session).filter(self.__class__.id == self.id).delete()
        session.commit()

    def save(self, session):
        session.add(self)
        session.commit()
        return self
