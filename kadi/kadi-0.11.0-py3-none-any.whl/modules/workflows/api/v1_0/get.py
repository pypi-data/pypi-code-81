# Copyright 2021 Karlsruhe Institute of Technology
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
from functools import partial

from flask_login import current_user
from flask_login import login_required

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import json_response
from kadi.lib.api.core import scopes_required
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.api.utils import status
from kadi.lib.conversion import strip
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.records.models import File
from kadi.modules.records.models import Record
from kadi.modules.records.schemas import FileSchema


route = partial(bp.route, methods=["GET"])


@route("/workflows")
@login_required
@scopes_required("record.read")
@paginated
@qparam(
    "filter",
    "",
    parse=strip,
    description="A query to filter the workflow files by name.",
)
@status(
    200,
    "Return a paginated list of workflow files, sorted by last modification date in"
    " descending order.",
)
def get_workflows(page, per_page, qparams):
    """Get all workflow files.

    For convenience, each file additionally contains the identifier of its record.
    """
    record_ids = (
        get_permitted_objects(current_user, "read", "record")
        .active()
        .with_entities(Record.id)
    )

    paginated_files = (
        File.query.join(File.record)
        .filter(
            Record.id.in_(record_ids),
            File.state == "active",
            File.storage_type == "local",
            File.mimetype == "application/x-flow+json",
            File.name.ilike(f"%{qparams['filter']}%"),
        )
        .order_by(File.last_modified.desc())
        .paginate(page, per_page, False)
    )

    items = [
        {"record_identifier": file.record.identifier, **FileSchema().dump(file)}
        for file in paginated_files.items
    ]

    data = {
        "items": items,
        **create_pagination_data(
            paginated_files.total, page, per_page, "api.get_workflows"
        ),
    }

    return json_response(200, data)
