from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import sessionmaker


class SessionFactory:
    def create(self, engine: Engine):
        return sessionmaker(bind=engine)()
