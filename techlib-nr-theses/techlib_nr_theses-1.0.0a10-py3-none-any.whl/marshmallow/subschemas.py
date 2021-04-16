from invenio_records_rest.schemas.fields import SanitizedUnicode
from marshmallow.fields import List


class StudyFieldMixin:
    AKVO = SanitizedUnicode()
    aliases = List(SanitizedUnicode())
