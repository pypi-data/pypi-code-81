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
from io import BytesIO

import qrcode
from flask_login import current_user

from .schemas import CollectionSchema
from kadi.lib.web import url_for
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.records.models import Record
from kadi.modules.records.utils import get_export_data as get_record_export_data


def get_export_data(collection, export_type):
    """Export a collection in a given format.

    :param collection: The collection to export.
    :param export_type: The export format, ``"json"`` or ``"qr"``.
    :return: The exported collection data, depending on the given export type, or
        ``None`` if an unknown export type was given.
    """
    if export_type == "json":
        schema = CollectionSchema(exclude=["_actions", "_links", "creator._links"])
        data = schema.dump(collection)

        record_ids = (
            get_permitted_objects(current_user, "read", "record")
            .active()
            .with_entities(Record.id)
        )

        data["records"] = []
        for record in collection.records.filter(Record.id.in_(record_ids)):
            data["records"].append(get_record_export_data(record, "dict"))

        return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)

    if export_type == "qr":
        image = qrcode.make(
            url_for("collections.view_collection", id=collection.id, _external=True)
        )

        data = BytesIO()
        image.save(data, format="PNG")
        data.seek(0)

        return data

    return None
