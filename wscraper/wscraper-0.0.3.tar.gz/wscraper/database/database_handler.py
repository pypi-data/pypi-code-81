# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..analysis import *
from ..language import *
from .table import *
from .w_scraper_database_error import *


class DatabaseHandler:

    targets = {
        "entry": Entry,
        "redirection": Redirection,
        "document": Document
    }

    @classmethod
    def command_database_migrate(cls, *, reset = False):
        instance = cls.load()
        instance.migrate(reset = reset)

    @classmethod
    def command_database_seed(cls, names, *, reset = False):
        config = Config()
        instance = cls.load()
        xml_directory = config.get_wikipedia_xml_directory(must = True)
        language = Language.get_class(config.get_language(must = True))
        instance.seed(xml_directory, language, names = names, reset = reset)

    @classmethod
    def load(cls, task_name = None):
        config = Config(task_name)
        parameters = config.get_parameter("database", must = True)
        return cls(parameters)

    def __init__(self, parameters):
        dialect = parameters.get("dialect")
        driver = "+" + parameters.get("driver") if parameters.get("driver") else ""
        user = parameters.get("user")
        password = parameters.get("password")
        host = parameters.get("host")
        port = parameters.get("port")
        database = parameters.get("database")
        charset = parameters.get("charset") or "utf8"

        self.uri = "{dialect}{driver}://{user}:{password}@{host}:{port}/{database}?charset={charset}".format(
            dialect = dialect,
            driver = driver,
            user = user,
            password = password,
            host = host,
            port = port,
            database = database,
            charset = charset
        )

        self.engine = create_engine(self.uri)
        self.session_class = sessionmaker(self.engine)

    def get_session(self):
        return self.session_class()

    @contextmanager
    def session_scope(self):
        session = self.session_class()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise WScraperDatabaseError("An error occurred.")
        finally:
            session.close()

    def migrate(self, *, reset = False):
        if reset:
            Base.metadata.drop_all(self.engine)

        Base.metadata.create_all(self.engine)

    def seed(self, xml_directory, language, *, names = None, reset = False):
        if names is None or len(names) == 0:
            names = self.targets.keys()

        invalid_targets = [name for name in names if name not in self.targets.keys()]

        if len(invalid_targets) > 0:
            raise WScraperDatabaseError(f"invalid target: {', '.join(invalid_targets)}")

        pager = PageIterator(xml_directory)
        progress = ProgressManager(pager)

        with self.session_scope() as session, progress:
            if reset:
                tables = [self.targets[name].__table__ for name in names]
                Base.metadata.drop_all(self.engine, tables = tables)
                Base.metadata.create_all(self.engine, tables = tables)

            for page in pager:
                progress.update()

                entry = Parser.page_to_class(page, language = language, entry_only = False)

                if entry is None:
                    continue

                if entry["type"] == "entry":
                    if "entry" in names:
                        session.add(Entry(title = entry["title"], mediawiki = entry["mediawiki"]))
                        session.flush()

                    if "document" in names:
                        document = Parser.to_plain_text(entry["mediawiki"], language = language)
                        session.add(Document(title = entry["title"], text = document))
                        session.flush()

                elif entry["type"] == "redirection":
                    if "redirection" in names:
                        session.add(Redirection(source = entry["source"], target = entry["target"]))
                        session.flush()

                else:
                    raise NotImplementedError(f"Unexpected entry type `{entry['type']}` appeared.")
