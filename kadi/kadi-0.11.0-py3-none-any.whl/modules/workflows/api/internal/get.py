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
from functools import partial

from flask_login import current_user
from flask_login import login_required

from kadi.lib.api.blueprint import bp
from kadi.lib.api.core import internal_endpoint
from kadi.lib.api.core import json_response
from kadi.lib.api.utils import create_pagination_data
from kadi.lib.conversion import strip
from kadi.lib.web import paginated
from kadi.lib.web import qparam
from kadi.modules.permissions.core import get_permitted_objects
from kadi.modules.records.models import File
from kadi.modules.records.models import Record
from kadi.modules.workflows.core import parse_tool_file


route = partial(bp.route, methods=["GET"])


@route("/workflows/tools", v=None)
@login_required
@internal_endpoint
@paginated
@qparam("filter", "", parse=strip)
def get_tools(page, per_page, qparams):
    """Get all tool files.

    For use in the experimental workflow editor.
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
            File.mimetype == "application/x-tool+xml",
            File.name.ilike(f"%{qparams['filter']}%"),
        )
        .order_by(File.name)
        .paginate(page, per_page, False)
    )

    items = [
        {
            "file": {
                "id": file.id,
                "name": file.name,
            },
            "record": {"identifier": file.record.identifier},
            "tool": parse_tool_file(file),
        }
        for file in paginated_files.items
    ]

    data = {
        "items": items,
        **create_pagination_data(
            paginated_files.total, page, per_page, "api.get_tools"
        ),
    }

    return json_response(200, data)
