from django.db import models

from django_encryption import DataKeeper


class RecordModel(models.Model):

    class Meta:
        abstract = True

    @classmethod
    def from_db(cls, db, field_names, values):
        resp = super().from_db(db, field_names, values)
        for item in values:
            if not isinstance(item, DataKeeper):
                continue
            item.id = resp.pk
        return resp

