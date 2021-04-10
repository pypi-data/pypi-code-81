from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environs import Env
import os

try:
    env = Env()
    env.read_env()
    SQLALCHEMY_DATABASE_URI = f"postgres://{os.environ['USERDB']}:{os.environ['PASSWORDDB']}@{os.environ['HOST']}/{os.environ['DBNAME']}"

except Exception as e:
    print(e)
    print("Favor configurar as variaveis de ambiente: [USERDB, PASSWORDDB, HOST, DBNAME]")
    exit(1)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)
session = session()
Base = declarative_base()

class Config():
    """ Represents an abstract class that will be used to another models."""

    def create_database(self):
        Base.metadata.create_all(engine)
