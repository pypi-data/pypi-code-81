import uuid

from invenio_db import db
from invenio_indexer.api import RecordIndexer
from invenio_pidstore.errors import PIDDoesNotExistError
from invenio_pidstore.models import PIDStatus
from invenio_pidstore.models import PersistentIdentifier
from invenio_records import Record
from invenio_search import RecordsSearch
from sqlalchemy.orm.exc import NoResultFound

from nr_theses.record import PublishedThesisRecord


class ThesisSearch(RecordsSearch):
    pass


class ThesisAPI:

    def __init__(self, app):
        """
        API initialization.

        :param app: invenio application
        """
        self.app = app
        self.indexer = RecordIndexer()

    @staticmethod
    def create_draft_record(record: dict, pid_type=None, pid_value=None):
        if not pid_type:
            pid_type = "dnr"
        if not pid_value:
            pid_value = record["control_number"]
        id_ = uuid.uuid4()
        pid = PersistentIdentifier.create(
            pid_type,
            pid_value,
            pid_provider=None,
            object_type="rec",
            object_uuid=id_,
            status=PIDStatus.REGISTERED,
        )
        db_record = PublishedThesisRecord.create(record, id_=id_)
        return db_record

    @staticmethod
    def delete_draft_record(record: Record):
        record.delete()

    @staticmethod
    def get_record_by_id(pid_type, pid_value):
        try:
            existing_pid = PersistentIdentifier.get(pid_type, pid_value)
            try:
                existing_record = PublishedThesisRecord.get_record(id_=existing_pid.object_uuid)
            except NoResultFound:
                # check it if has not been deleted and salvage if so
                existing_record = PublishedThesisRecord.get_record(id_=existing_pid.object_uuid,
                                                                   with_deleted=True)
                existing_record = existing_record.revert(-1)
        except PIDDoesNotExistError:
            return
        except NoResultFound:  # pragma: no cover
            return
        return existing_record
