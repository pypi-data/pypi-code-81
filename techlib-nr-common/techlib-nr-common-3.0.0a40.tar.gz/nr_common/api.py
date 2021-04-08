import uuid

from invenio_indexer.api import RecordIndexer
from invenio_pidstore.models import PersistentIdentifier, PIDStatus

from nr_common.record import PublishedCommonRecord


class CommonAPI:

    def __init__(self, app):
        """
        API initialization.

        :param app: invenio application
        """
        self.app = app
        self.indexer = RecordIndexer()

    # def import_old_nusl_record(self, record):
    #     # validate json schema and save
    #     existing_record = self.get_record_by_id("dnr", record["control_number"])
    #
    #     if not existing_record:
    #         db_record = self.create_draft_record(record)
    #     else:
    #         # remove everything from the record except of id and pid - keep them
    #         db_record = self.update_draft_record(existing_record, record)
    #
    #     db.session.commit()
    #     self.index_draft_record(db_record)
    #
    # def index_draft_record(self, db_record):
    #     self.indexer.index(db_record)
    #
    # @staticmethod
    # def update_draft_record(existing_record, record):
    #     previous_id = existing_record['id']
    #     previous_identifier = existing_record['identifier']
    #     existing_record.clear()
    #     existing_record['id'] = previous_id
    #     existing_record['identifier'] = previous_identifier
    #     for k, v in record.items():
    #         existing_record[k] = v
    #     existing_record.commit()
    #     db_record = existing_record
    #     return db_record
    #
    # TODO: používá se někde?
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
        db_record = PublishedCommonRecord.create(record, id_=id_)
        return db_record
    #
    # @staticmethod
    # def delete_draft_record(record: Record):
    #     record.delete()
    #
    # @staticmethod
    # def get_record_by_id(pid_type, pid_value):
    #     try:
    #         existing_pid = PersistentIdentifier.get(pid_type, pid_value)
    #         try:
    #             existing_record = PublishedThesisRecord.get_record(id_=existing_pid.object_uuid)
    #         except NoResultFound:
    #             # check it if has not been deleted and salvage if so
    #             existing_record = PublishedThesisRecord.get_record(id_=existing_pid.object_uuid,
    #                                                                with_deleted=True)
    #             existing_record = existing_record.revert(-1)
    #     except PIDDoesNotExistError:
    #         return
    #     except NoResultFound:
    #         return
    #     return existing_record
