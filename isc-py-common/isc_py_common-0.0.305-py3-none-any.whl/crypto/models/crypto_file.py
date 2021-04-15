import logging
import os
from shutil import copyfile

from django.conf import settings
from django.core.files import File
from django.db.models import BinaryField, BigIntegerField, CharField, TextField
from django.forms import model_to_dict

from isc_common import delAttr
from isc_common.common.UploadItemEx import UploadItemEx
from isc_common.fields.files import FileFieldEx
from isc_common.fields.name_field import NameField
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_managet_with_lookup_fields import CommonManagetWithLookUpFieldsManager, CommonManagetWithLookUpFieldsQuerySet
from isc_common.models.audit import AuditModel

logger = logging.getLogger(__name__)


class CryptoQuerySet(CommonManagetWithLookUpFieldsQuerySet):

    def delete(self):
        for item in self:
            Crypto_file.remove_file(item=item)
        return super().delete()


class CryptoManager(CommonManagetWithLookUpFieldsManager):
    def createFromRequest(self, request, function=None):
        request = DSRequest(request=request)
        data = request.get_data()
        _data = data.copy()
        for key in data:
            if key.find('__') != -1:
                delAttr(_data, key)
        delAttr(_data, 'form')
        if data.get('id') or not data.get('real_name'):
            delAttr(_data, 'id')
            res = super().filter(id=data.get('id')).update(**_data)
            res = model_to_dict(res[0])
            delAttr(res, 'attfile')
            delAttr(res, 'form')
            data.update(res)
        return data

    def updateFromRequest(self, request):
        request = DSRequest(request=request)
        data = request.get_data()
        delAttr(data, 'form')
        super().filter(id=request.get_id()).update(**data)
        return data

    def get_queryset(self):
        return CryptoQuerySet(self.model, using=self._db)


class Crypto_file(AuditModel):
    format = NameField(verbose_name='Формат файла')
    mime_type = NameField(verbose_name='MIME тип файла файла', null=True, blank=True)
    size = BigIntegerField(verbose_name='Размер фала', default=0)
    real_name = TextField(verbose_name='Первоначальное имя файла', null=True, blank=True)
    key = BinaryField(max_length=200, null=True, blank=True)
    attfile = FileFieldEx(verbose_name='Файл', max_length=255, null=True, blank=True)
    file_store = CharField(verbose_name='Каталог хранения файла', max_length=255, null=True, blank=True)

    object = CryptoManager()

    @classmethod
    def remove_file(cls, item):
        old_file_store = item.file_store
        file_path = item.attfile.name

        if old_file_store:
            file_path = file_path.replace(old_file_store, settings.FILES_STORE)

        if isinstance(settings.REPLACE_FILE_PATH, dict):
            for key, value in settings.REPLACE_FILE_PATH.items():
                file_path = file_path.replace(key, value)

        if file_path:
            if os.altsep:
                file_path = file_path.replace(os.altsep, os.sep)

            if os.path.exists(file_path):
                res = os.remove(file_path)
                logger.debug(f'Removed file: {file_path}')
            else:
                logger.warning(f'Removed file: {file_path} not finded.')

    @classmethod
    def copy_file(cls, item):
        copyfile(src=item.real_file_name, dst=item.full_path)
        with open(item.full_path, 'rb') as src:
            fileObj = File(src)
            res, created = cls.objects.update_or_create(
                id=item.id,
                defaults=dict(
                    attfile=fileObj,
                    file_store=item.get_path(fileObj.name),
                    format=item.file_format,
                    mime_type=item.file_mime_type,
                    size=item.file_size,
                    real_name=item.real_file_name,
                )
            )
        os.remove(item.full_path)

        return res, created

    @classmethod
    def create_update(cls, **kwargs):
        item = UploadItemEx(**kwargs)

        action = None
        try:
            res = cls.objects.get(id=item.id)
            if res.size is None or res.size == 0:
                action = 'create'
            elif res.size != item.file_size:
                action = 'update'

            if action is not None:
                if action == 'update':
                    return cls.remove_file(item=res)

                return cls.copy_file(item=item)
            else:
                return None

        except cls.DoesNotExist:
            return cls.copy_file(item=item)

    def __str__(self):
        return f"{self.real_name}"

    class Meta:
        abstract = True
