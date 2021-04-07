import importlib
import logging
from pathlib import Path
import shutil

from django.core.files.base import ContentFile

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.documents.literals import STORAGE_NAME_DOCUMENT_FILES
from mayan.apps.permissions.tests.mixins import PermissionTestMixin
from mayan.apps.smart_settings.classes import SettingNamespace

from ..classes import DefinedStorage
from ..models import DownloadFile
from ..utils import mkdtemp

from .literals import TEST_DOWNLOAD_FILE_CONTENT_FILE_NAME


class DownloadFileTestMixin(PermissionTestMixin):
    def _create_test_download_file(self, content=None, content_object=None):
        file_content = None

        if content:
            file_content = ContentFile(
                content=content, name=TEST_DOWNLOAD_FILE_CONTENT_FILE_NAME
            )

        self.test_download_file = DownloadFile.objects.create(
            content_object=content_object, file=file_content
        )

    def _create_test_download_file_with_permission(self, content=None):
        file_content = None

        if content:
            file_content = ContentFile(
                content=content, name=TEST_DOWNLOAD_FILE_CONTENT_FILE_NAME
            )

        self._create_test_permission()

        ModelPermission.register(
            model=DownloadFile, permissions=(
                self.test_permission,
            )
        )

        self.test_download_file = DownloadFile.objects.create(
            file=file_content,
            permission=self.test_permission.stored_permission
        )


class DownloadFileViewTestMixin:
    def _request_test_download_file_delete_view(self):
        return self.post(
            viewname='storage:download_file_delete', kwargs={
                'download_file_id': self.test_download_file.pk
            }
        )

    def _request_test_download_file_download_view(self):
        return self.get(
            viewname='storage:download_file_download', kwargs={
                'download_file_id': self.test_download_file.pk
            }
        )

    def _request_test_download_file_list_view(self):
        return self.get(viewname='storage:download_file_list')


class StorageProcessorTestMixin:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.defined_storage = DefinedStorage.get(
            name=STORAGE_NAME_DOCUMENT_FILES
        )
        cls.document_storage_kwargs = cls.defined_storage.kwargs

    def setUp(self):
        super().setUp()
        self.temporary_directory = mkdtemp()
        self.path_temporary_directory = Path(self.temporary_directory)
        self.path_test_file = self.path_temporary_directory / 'test_file.txt'

    def tearDown(self):
        super().tearDown()
        shutil.rmtree(path=self.temporary_directory, ignore_errors=True)
        self.defined_storage.kwargs = self.document_storage_kwargs


class StorageSettingTestMixin:
    def _test_storage_setting_with_invalid_value(
        self, setting, storage_module, storage_name
    ):
        old_value = setting.value
        SettingNamespace.invalidate_cache_all()

        self._set_environment_variable(
            name='MAYAN_{}'.format(
                setting.global_name
            ), value='invalid_value'
        )
        self.test_case_silenced_logger_new_level = logging.FATAL + 10
        self._silence_logger(name='mayan.apps.storage.classes')

        with self.assertRaises(expected_exception=TypeError) as assertion:
            importlib.reload(storage_module)
            DefinedStorage.get(
                name=storage_name
            ).get_storage_instance()

        setting.set(value=old_value)
        importlib.reload(storage_module)

        return assertion
