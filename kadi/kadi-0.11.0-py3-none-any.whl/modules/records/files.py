# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from contextlib import contextmanager

from flask import send_file
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from .models import File
from .models import TemporaryFile
from .models import Upload
from kadi.ext.db import db
from kadi.lib.archives import create_archive
from kadi.lib.db import update_object
from kadi.lib.revisions.core import create_revision as _create_revision
from kadi.lib.revisions.utils import delete_revisions
from kadi.lib.storage.core import create_filepath
from kadi.lib.storage.core import create_storage
from kadi.lib.storage.local import LocalStorage
from kadi.lib.utils import is_iterable
from kadi.lib.validation import validate_mimetype
from kadi.plugins import run_hook


def aquire_file_lock(file):
    """Aquire a lock on the given file and refresh it.

    Only relevant for local files, as locks are used for updating existing local files'
    data.

    :param file: The file to aquire a lock from.
    :return: The refreshed file.
    """
    if file.storage_type != "local":
        return file

    return (
        File.query.populate_existing()
        .with_for_update()
        .filter(File.id == file.id)
        .first()
    )


def update_file(file, **kwargs):
    r"""Update an existing file.

    Note that this function may aquire a lock on the given file and may issue one or
    more database commits.

    :param file: The file to update.
    :param \**kwargs: Keyword arguments that will be passed to
        :func:`kadi.lib.db.update_object`.
    :return: ``True`` if the file was updated successfully, ``False`` otherwise.
    """
    file = aquire_file_lock(file)

    if file.state != "active" or file.record.state != "active":
        return False

    update_object(file, **kwargs)

    update_timestamp = False
    if db.session.is_modified(file):
        update_timestamp = True

    try:
        db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return False

    _create_revision(file)

    # Release the file lock.
    db.session.commit()

    if update_timestamp:
        file.record.update_timestamp()

    db.session.commit()
    return True


def delete_file(file, create_revision=True, revision_user=None):
    """Delete an existing file.

    This will mark the file for deletion, i.e. the files's state will be set to
    ``"inactive"``. Note that this function may aquire a lock on the given file and may
    issue one or more database commits.

    :param file: The file to delete.
    :param create_revision: (optional) Flag indicating whether a revision should be
        created for the deletion.
    :param revision_user: (optional) The user that triggered the file deletion revision.
        Defaults to the current user.
    """
    from .uploads import delete_upload

    file = aquire_file_lock(file)
    file.state = "inactive"

    update_timestamp = False
    if db.session.is_modified(file):
        update_timestamp = True

    if create_revision:
        revision_user = revision_user if revision_user is not None else current_user
        _create_revision(file, user=revision_user)

    # Release the file lock.
    db.session.commit()

    if update_timestamp:
        file.record.update_timestamp()

    # Check if there are any uploads attached to the file and mark them for deletion as
    # well.
    uploads = Upload.query.filter(Upload.file_id == file.id)
    for upload in uploads:
        delete_upload(upload)

    db.session.commit()


def remove_files(files, delete_from_db=True):
    """Remove multiple files from storage.

    Note that this function may issue one or more database commits.

    :param files: A single :class:`.File` or an iterable of files.
    :param delete_from_db: (optional) A flag indicating whether the file should be
        deleted from the database as well, instead of just doing a soft deletion (i.e.
        setting the file's state to ``"deleted"``).
    """
    from .uploads import remove_uploads

    if not is_iterable(files):
        files = [files]

    for file in files:
        delete_file(file, create_revision=False)

        filepath = create_filepath(str(file.id), storage_type=file.storage_type)
        storage = create_storage(storage_type=file.storage_type)

        if filepath is not None and storage is not None:
            storage.delete(filepath)

            if file.storage_type == "local":
                # Check if there are any uploads attached to the file and remove them as
                # well.
                uploads = Upload.query.filter(Upload.file_id == file.id)
                remove_uploads(uploads)

                storage.remove_empty_parent_dirs(filepath, num_dirs=3)

            if delete_from_db:
                delete_revisions(file)
                db.session.delete(file)
            else:
                file.state = "deleted"

        db.session.commit()


@contextmanager
def open_file(file, mode="rb", encoding=None):
    """Context manager that yields an open file.

    Note that this context manager yields ``None`` if the file has an incompatible
    storage type.

    **Example:**

    .. code-block:: python3

        with open_file(file) as file_object:
            pass

    :param file: The :class:`.File` to open.
    :param mode: (optional) The mode to open the file with.
    :param encoding: (optional) The encoding of the file if opening it in text mode.
    """
    filepath = create_filepath(str(file.id), storage_type=file.storage_type)
    storage = create_storage(storage_type=file.storage_type)

    if filepath is None or storage is None:
        yield None
        return

    f = storage.open(filepath, mode=mode, encoding=encoding)

    try:
        yield f
    finally:
        storage.close(f)


def download_file(file):
    """Send a file to a client for downloading.

    :param file: The :class:`.File` to download.
    :return: The response object or ``None`` if the given file could not be found or has
        an incompatible storage type.
    """
    filepath = create_filepath(str(file.id), storage_type=file.storage_type)
    storage = create_storage(storage_type=file.storage_type)

    if filepath is None or storage is None or not storage.exists(filepath):
        return None

    if file.storage_type == "local":
        return send_file(
            filepath,
            mimetype=file.mimetype,
            attachment_filename=file.name,
            as_attachment=True,
        )

    return None


def get_custom_mimetype(file, base_mimetype=None):
    """Get a custom MIME type of a file based on its content.

    Uses the ``"kadi_get_custom_mimetype"`` plugin hook for custom MIME types based on
    the file's content.

    :param file: The file to get the MIME type of.
    :param base_mimetype: (optional) The base MIME type of the file on which to base the
        custom MIME type.
    :return: The custom MIME type or ``None`` if no valid custom MIME type was found.
    """
    if base_mimetype is None:
        storage = create_storage(storage_type=file.storage_type)
        filepath = create_filepath(str(file.id), storage_type=file.storage_type)

        if storage is not None and filepath is not None:
            base_mimetype = storage.get_mimetype(filepath)

    try:
        custom_mimetype = run_hook(
            "kadi_get_custom_mimetype", file=file, base_mimetype=base_mimetype
        )
        validate_mimetype(custom_mimetype)
    except:
        return None

    return custom_mimetype


def package_files(record, creator, task=None):
    """Package multiple local files of a record together in a ZIP archive.

    Note that this function may issue one or more database commits.

    Uses :func:`kadi.lib.archives.create_archive`.

    :param record: The record the files belong to.
    :param creator: The user that will be set as the creator of the archive.
    :param task: (optional) A :class:`.Task` object that can be provided if this
        function is executed in a task.
    :return: The archive as a :class:`TemporaryFile` object or ``None`` if the archive
        was not packaged successfully.
    """
    files = record.active_files.filter(File.storage_type == "local")
    size = files.with_entities(db.func.sum(File.size)).scalar() or 0

    archive = TemporaryFile.create(
        record=record, creator=creator, name=f"{record.identifier}.zip", size=size
    )
    db.session.commit()

    filepath = create_filepath(str(archive.id))
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    entries = [
        {"path": create_filepath(str(file.id)), "name": file.name, "size": file.size}
        for file in files
    ]

    def callback(count, current_size):
        if task:
            if task.is_revoked:
                return False

            task.update_progress(current_size / size * 100)
            db.session.commit()

        return True

    if create_archive(filepath, entries, callback):
        archive.state = "active"
        db.session.commit()
        return archive

    return None


def download_temporary_file(temporary_file):
    """Send a temporary file to a client as attachment for download.

    :param temporary_file: The :class:`.TemporaryFile` to download.
    :return: The response object or ``None`` if the given temporary file could not be
        found.
    """
    filepath = create_filepath(str(temporary_file.id))
    storage = create_storage()

    if not storage.exists(filepath):
        return None

    return send_file(
        filepath,
        mimetype=temporary_file.mimetype,
        attachment_filename=temporary_file.name,
        as_attachment=True,
    )


def remove_temporary_files(temporary_files):
    """Remove multiple temporary files from storage.

    Note that this function may issue one or more database commits.

    :param temporary_files: A single :class:`.TemporaryFile` or an iterable of temporary
        files.
    """
    if not is_iterable(temporary_files):
        temporary_files = [temporary_files]

    for temporary_file in temporary_files:
        temporary_file.state = "inactive"
        db.session.commit()

        storage = LocalStorage()
        filepath = create_filepath(str(temporary_file.id))

        storage.delete(filepath)
        storage.remove_empty_parent_dirs(filepath, num_dirs=3)

        db.session.delete(temporary_file)
        db.session.commit()
