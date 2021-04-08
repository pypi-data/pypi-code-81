from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

from mo9mo9db.base_mixin import DBBaseMixin
from mo9mo9db.dbsession import get_db_engine

engine = get_db_engine()
Base = declarative_base()


class Studytimelogs(DBBaseMixin, Base):
    study_dt = Column(DateTime, unique=False)
    guild_id = Column(String(20), unique=False)
    member_id = Column(String(20), unique=False)
    voice_id = Column(String(20), unique=False)
    access = Column(String(10), unique=False)
    studytime_min = Column(Integer, unique=False)
    studytag_no = Column(String(10), unique=False)
    excluded_record = Column(Boolean)

    def __init__(self,
                 study_dt=None,
                 guild_id=None,
                 member_id=None,
                 voice_id=None,
                 access=None,
                 studytime_min=None,
                 studytag_no=None,
                 excluded_record=None):
        self.study_dt = study_dt
        self.guild_id = guild_id
        self.member_id = member_id
        self.access = access
        self.voice_id = voice_id
        self.studytime_min = studytime_min
        self.studytag_no = studytag_no
        self.excluded_record = excluded_record


class Studymembers(DBBaseMixin, Base):
    guild_id = Column(String(20), unique=False)
    member_id = Column(String(20), unique=True, primary_key=True)
    member_name = Column(String(50))
    selfintroduction_id = Column(String(20), unique=True)
    times_id = Column(String(20), unique=True)
    joined_dt = Column(DateTime, unique=False)
    norecord_onemonth = Column(Boolean)
    norecord_twomonth = Column(Boolean)
    enrollment = Column(Boolean)

    def __init__(self,
                 guild_id=None,
                 member_id=None,
                 member_name=None,
                 selfintroduction_id=None,
                 times_id=None,
                 joined_dt=None,
                 norecord_onemonth=None,
                 norecord_twomonth=None,
                 enrollment=None):
        self.guild_id = guild_id
        self.member_id = member_id
        self.member_name = member_name
        self.selfintroduction_id = selfintroduction_id
        self.times_id = times_id
        self.joined_dt = joined_dt
        self.norecord_onemonth = norecord_onemonth
        self.norecord_twomonth = norecord_twomonth
        self.enrollment = enrollment


class Studytags(DBBaseMixin, Base):
    member_id = Column(String(20), unique=True)
    tag_name = Column(String(40), unique=True)
    tag_default = Column(Boolean)
    member_id = Column(String(20), unique=True)
    existence = Column(Boolean)

    def __init__(self,
                 member_id=None,
                 tag_name=None,
                 tag_default=None,
                 existence=None):
        self.member_id = member_id
        self.tag_name = tag_name
        self.tag_default = tag_default
        self.existence = existence

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
