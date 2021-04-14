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
import json

import chardet
from flask import current_app
from flask import send_file

from .files import open_file
from kadi.lib.archives import get_archive_contents
from kadi.lib.storage.core import create_filepath
from kadi.lib.storage.core import create_storage
from kadi.lib.web import url_for
from kadi.plugins import run_hook


def preview_file(file):
    """Send a file to a client for previewing in a browser.

    Note that this can potentially pose a security risk, so this should only be used for
    files that are safe for displaying. Uses the content-based MIME type of the file to
    set the content type of the response (see :attr:`.File.magic_mimetype`).

    :param file: The :class:`.File` to send to the client.
    :return: The response object or ``None`` if the given file could not be found or has
        an incompatible storage type.
    """
    filepath = create_filepath(str(file.id), storage_type=file.storage_type)
    storage = create_storage(storage_type=file.storage_type)

    if filepath is None or storage is None or not storage.exists(filepath):
        return None

    if file.storage_type == "local":
        return send_file(filepath, mimetype=file.magic_mimetype)

    return None


def _get_encoding(file):
    with open_file(file, mode="rb") as f:
        if f is None:
            return None

        # Chardet can be pretty slow, so we limit the bytes to use for detection.
        encoding = chardet.detect(f.read(16384))["encoding"]

    if encoding is not None:
        try:
            # If an encoding was found, we try to actually read something from the file
            # using that encoding.
            with open_file(file, mode="r", encoding=encoding) as f:
                f.read(1)
        except UnicodeDecodeError:
            return None

    return encoding


def _get_text_content(file, encoding=None, max_chars=16384):
    try:
        with open_file(file, mode="r", encoding=encoding) as f:
            if f is None:
                return None

            return f.read(max_chars)
    except UnicodeDecodeError:
        pass

    return None


def _get_builtin_preview_data(file):
    if file.magic_mimetype in ["image/jpeg", "image/png"]:
        if (
            file.storage_type == "local"
            and file.size < current_app.config["PREVIEW_MAX_SIZE"]
        ):
            return "image", url_for(
                "api.preview_file", record_id=file.record.id, file_id=file.id
            )

    if file.magic_mimetype == "application/pdf":
        if (
            file.storage_type == "local"
            and file.size < current_app.config["PREVIEW_MAX_SIZE"]
        ):
            return "pdf", url_for(
                "api.preview_file", record_id=file.record.id, file_id=file.id
            )

    if file.magic_mimetype in [
        "application/zip",
        "application/gzip",
        "application/x-tar",
        "application/x-bzip2",
    ]:
        filepath = create_filepath(str(file.id))

        if filepath is not None:
            return "archive", get_archive_contents(filepath, file.magic_mimetype)

    if file.magic_mimetype == "text/plain" and file.mimetype == "text/markdown":
        encoding = _get_encoding(file)

        if encoding is not None:
            return f"markdown;{encoding}", _get_text_content(file, encoding=encoding)

    if file.magic_mimetype == "application/x-flow+json":
        return "workflow", url_for(
            "api.download_file", record_id=file.record.id, file_id=file.id
        )

    if (
        file.storage_type == "local"
        and file.size < current_app.config["PREVIEW_MAX_SIZE"]
        and file.magic_mimetype in ["text/plain", "application/octet-stream"]
        and file.mimetype
        in [
            "application/sla",
            "model/stl",
            "model/x.stl-ascii",
            "model/x.stl-binary",
        ]
    ):
        return "stl", url_for(
            "api.download_file", record_id=file.record.id, file_id=file.id
        )

    return None


def get_preview_data(file, use_fallback=True):
    """Get the preview data of a file.

    Uses the ``"kadi_get_preview_data"`` plugin hook for custom preview data.

    :param file: The :class:`.File` to get the preview data of.
    :param use_fallback: (optional) Flag indicating whether the file should be checked
        for textual data as fallback by trying to detect its encoding.
    :return: The preview type and preview data as tuple, which are always guaranteed to
        be JSON serializable. If ``use_fallback`` is ``True`` and the file was detected
        to have textual content, the preview type will also include the encoding in the
        form of ``"text;<encoding>"``. If either the preview type or data could not be
        determined, ``None`` is returned.
    """
    try:
        preview_data = run_hook("kadi_get_preview_data", file=file)
    except:
        return None

    if preview_data is not None:
        if (
            not isinstance(preview_data, tuple)
            or not len(preview_data) == 2
            or None in preview_data
        ):
            return None
        try:
            json.dumps(preview_data)
        except:
            return None

    if preview_data is None and use_fallback:
        encoding = _get_encoding(file)

        if encoding is not None:
            text_content = _get_text_content(file, encoding=encoding)

            if text_content is not None:
                return f"text;{encoding}", text_content

    return preview_data
