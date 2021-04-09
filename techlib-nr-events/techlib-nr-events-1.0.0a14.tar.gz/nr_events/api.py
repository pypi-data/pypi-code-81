from invenio_indexer.api import RecordIndexer
from invenio_search import RecordsSearch


class ThesisSearch(RecordsSearch):
    pass


class EventsAPI:

    def __init__(self, app):
        """
        API initialization.

        :param app: invenio application
        """
        self.app = app
        self.indexer = RecordIndexer()
