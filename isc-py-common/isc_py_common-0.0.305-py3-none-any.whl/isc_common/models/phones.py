import logging

from isc_common.fields.code_field import CodeStrictField
from isc_common.models.audit import AuditQuerySet, AuditManager, AuditModel

logger = logging.getLogger(__name__)


class PhonesQuerySet(AuditQuerySet):
    def delete(self):
        return super().delete()

    def create(self, **kwargs):
        return super().create(**kwargs)

    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)


class PhonesManager(AuditManager):

    @staticmethod
    def getRecord(record):
        res = {
            'id': record.id,
            'description': record.description,
            'editing': record.editing,
            'deliting': record.deliting,
        }
        return res

    def get_queryset(self):
        return PhonesQuerySet(self.model, using=self._db)


class Phones(AuditModel):
    phone = CodeStrictField()
    objects = PhonesManager()

    def __str__(self):
        return f'ID:{self.id}'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name = 'Телефоны'
