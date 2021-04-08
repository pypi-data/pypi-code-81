# -*- coding: utf-8 -*-
import os
import sys
from distutils.util import strtobool

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base

import mo9mo9db.dbconfig as cfg  # noqa: E402

Base = declarative_base()


def get_db_session():
    """
    SQL Alchemy のDBセッションを生成して使い回す
    :rtype : scoped_session
    """
    # DBセッションの生成
    engine = get_db_engine()
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    return db_session


def db_path():
    user = cfg.DB_user
    pw = cfg.DB_password
    host = cfg.DB_host
    port = cfg.DB_port
    db = cfg.DB_database
    return f'mysql+pymysql://{user}:{pw}@{host}:{port}/{db}'


def get_db_engine():
    engine = create_engine(db_path(),
                           encoding='utf-8',
                           pool_size=5,
                           convert_unicode=True,
                           echo=strtobool(cfg.DB_echo))
    if not database_exists(engine.url):  # DBの存在チェックと作成用
        create_database(engine.url)
    return engine
