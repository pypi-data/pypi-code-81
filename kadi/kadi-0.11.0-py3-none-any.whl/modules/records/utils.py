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

from .extras import is_nested_type
from .models import File
from .models import Record
from .models import RecordLink
from .schemas import FileSchema
from .schemas import RecordSchema
from kadi.ext.db import db
from kadi.lib.conversion import truncate
from kadi.lib.format import filesize
from kadi.lib.format import pretty_type_name
from kadi.lib.pdf import PDF
from kadi.lib.utils import parse_datetime_string
from kadi.lib.web import url_for
from kadi.modules.permissions.core import get_permitted_objects


class RecordPDF(PDF):
    """Record PDF generation class.

    :param record: The record to generate a PDF from.
    """

    def __init__(self, record):
        self.record = record
        super().__init__(title=self.record.title)

        self.render_header_section()
        self.render_basic_metadata()
        self.render_extras()
        self.render_file_list()

    def render_header_section(self):
        """Render the header section of the record.

        The header sections contains the title, identifier and type of the record in the
        top left and a QR code pointing to the record in the top right, including a link
        pointing to the same location.
        """

        # Top right content.
        image_size = 20
        view_record_url = url_for(
            "records.view_record", id=self.record.id, _external=True
        )
        image = qrcode.make(view_record_url)

        cursor_y = self.get_y() - 2
        self.image(
            image.get_image(),
            self.w - self.r_margin - image_size,
            cursor_y,
            image_size,
            image_size,
            link=view_record_url,
        )
        self.rect(self.w - self.r_margin - image_size, cursor_y, image_size, image_size)

        # Top left content.
        cell_width = self.epw * 0.85

        self.set_text_color(r=0, g=0, b=0)
        self.set_font(style="B", size=14)
        self.truncated_cell(cell_width, txt=self.record.title)
        self.set_font(style="", size=11)
        self.ln(6)

        self.truncated_cell(cell_width, txt=f"@{self.record.identifier}")
        self.ln(11)

        self.set_font(style="B")
        self.truncated_cell(cell_width, txt=f"Type: {self.record.type or '-'}")
        self.set_font(style="")
        self.ln(10)

    def render_basic_metadata(self):
        """Render the basic metadata of the record."""
        line_height = 5

        self.set_text_color(r=0, g=0, b=0)
        self.set_font(style="", size=11)

        # Description.
        if self.record.description:
            self.write(line_height, txt=self.record.description)
        else:
            self.set_font(style="I")
            self.write(line_height, txt="No description.")
            self.set_font(style="")

        self.ln(13)

        # Creator.
        displayname = self.record.creator.identity.displayname

        self.write(line_height, "Created by")
        self.set_font(style="B")
        self.write(line_height, f" {displayname}")
        self.set_font(style="")
        self.link(
            self.get_x() - self.get_string_width(displayname),
            self.get_y(),
            self.get_string_width(displayname),
            line_height,
            link=url_for(
                "accounts.view_user", id=self.record.creator.id, _external=True
            ),
        )

        # Creation date.
        self.ln(line_height + 1)
        self.write(
            line_height, txt=f"Created at {self.format_date(self.record.created_at)}"
        )
        self.section(top=line_height * 2, bottom=line_height)

        # License and tags.
        if self.record.license or self.record.tags.count() > 0:
            if self.record.license:
                title = self.record.license.title

                self.set_font(style="B")
                self.write(line_height, "License: ")
                self.set_font(style="")
                self.write(line_height, title)
                self.link(
                    self.get_x() - self.get_string_width(title),
                    self.get_y(),
                    self.get_string_width(title),
                    line_height,
                    link=self.record.license.url,
                )
                self.ln(line_height)

            if self.record.tags.count() > 0:
                self.ln(1)
                self.set_font(style="B")
                self.write(line_height, "Tags: ")
                self.set_font(style="")
                self.write(
                    line_height, "; ".join([tag.name for tag in self.record.tags])
                )
                self.ln(line_height)

            self.section(top=line_height, bottom=line_height)

    def render_extras(self):
        """Render the extra metadata of the record."""
        self.set_draw_color(r=200, g=200, b=200)
        self.set_text_color(r=0, g=0, b=0)

        self.set_font(size=11, style="B")
        self.write(5, "Extra metadata")
        self.set_font(style="")
        self.ln(10)

        if self.record.extras:
            self.set_font(size=9)
            self._render_extras(self.record.extras)
            self.set_font(size=11)
        else:
            self.set_font(style="I")
            self.write(5, txt="No extras.")
            self.set_font(style="")
            self.ln(3)

        self.section(top=7, bottom=5)

    def _render_extras(self, extras, depth=0):
        for index, extra in enumerate(extras):
            if is_nested_type(extra["type"]):
                self._render_extra(index, extra, depth)
                self._render_extras(extra["value"], depth=depth + 1)
            else:
                self._render_extra(index, extra, depth)

        if depth == 0:
            self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())

    def _set_depth_color(self, depth):
        if depth % 2 == 1:
            self.set_fill_color(r=245, g=245, b=245)
        else:
            self.set_fill_color(r=256, g=256, b=256)

    def _render_extra(self, index, extra, depth):
        cell_height = 7
        nested_margin = 5
        column_width = (self.epw - nested_margin * depth) / 10

        # Render the "boxes" of the nested parent metadata entry, which automatically
        # gives us the correct left margin.
        for i in range(0, depth):
            self._set_depth_color(i)
            self.cell(nested_margin, h=cell_height, border="L", fill=True)

        self._set_depth_color(depth)

        if is_nested_type(extra["type"]):
            self.set_font(style="B")
            cell_width = column_width * 9
            key_border = "LT"
            type_border = "RT"
        else:
            cell_width = column_width * 5
            key_border = "LTB"
            type_border = "RTB"

        self.cell(
            cell_width,
            h=cell_height,
            border=key_border,
            fill=True,
            txt=self.truncate_string(extra.get("key", f"({index + 1})"), cell_width),
        )
        self.set_font(style="")

        if not is_nested_type(extra["type"]):
            if extra["value"] is not None:
                if extra["type"] == "date":
                    date_time = parse_datetime_string(extra["value"])
                    value = self.format_date(date_time, include_micro=True)
                else:
                    value = str(extra["value"])
            else:
                self.set_font(style="I")
                value = "null"

            cell_width = column_width * 4
            if extra.get("unit"):
                cell_width = column_width * 3

            self.cell(
                cell_width,
                h=cell_height,
                border="TB",
                fill=True,
                txt=self.truncate_string(value, cell_width),
            )
            self.set_font(style="")

            if extra.get("unit"):
                self.set_text_color(r=150, g=150, b=150)
                self.cell(
                    column_width,
                    h=cell_height,
                    border="TB",
                    fill=True,
                    txt=self.truncate_string(extra["unit"], cell_width),
                )

        self.set_text_color(r=150, g=150, b=150)
        self.cell(
            column_width,
            h=cell_height,
            border=type_border,
            fill=True,
            align="R",
            txt=pretty_type_name(extra["type"]).capitalize(),
        )
        self.set_text_color(r=0, g=0, b=0)
        self.ln()

    def render_file_list(self):
        """Render the file list of the record."""
        self.set_text_color(r=0, g=0, b=0)
        self.set_font(size=11, style="B")

        self.write(5, "Files")
        self.set_font(style="")
        self.ln(10)

        if self.record.active_files.count() > 0:
            for file in self.record.active_files.order_by(File.created_at):
                width = self.epw * 0.85

                self.set_text_color(r=0, g=0, b=0)
                self.set_font(size=11)
                self.cell(
                    width,
                    txt=self.truncate_string(file.name, width),
                    link=url_for(
                        "records.view_file",
                        record_id=self.record.id,
                        file_id=file.id,
                        _external=True,
                    ),
                )
                self.set_text_color(r=150, g=150, b=150)
                self.set_font(size=9)
                self.cell(self.epw * 0.15, txt=filesize(file.size), align="R")
                self.ln(8)
        else:
            self.set_font(style="I")
            self.write(5, txt="No files.")
            self.set_font(style="")
            self.ln(10)


def get_export_data(record, export_type):
    """Export a record in a given format.

    :param record: The record to export.
    :param export_type: The export format, one of ``"dict"``, ``"json"`` ``"pdf"`` or
        ``"qr"``.
    :return: The exported record data, depending on the given export type, or ``None``
        if an unknown export type was given.
    """
    if export_type in ["dict", "json"]:
        schema = RecordSchema(exclude=["_actions", "_links", "creator._links"])
        data = schema.dump(record)

        schema = FileSchema(many=True, exclude=["_actions", "_links", "creator._links"])
        data["files"] = schema.dump(
            record.active_files.order_by(File.last_modified.desc())
        )

        if export_type == "json":
            return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)

        return data

    if export_type == "qr":
        image = qrcode.make(
            url_for("records.view_record", id=record.id, _external=True)
        )

        data = BytesIO()
        image.save(data, format="PNG")
        data.seek(0)

        return data

    if export_type == "pdf":
        pdf = RecordPDF(record)

        data = BytesIO()
        pdf.output(data)
        data.seek(0)

        return data

    return None


def _append_node(nodes, record):
    nodes.append(
        {
            "id": record.id,
            "identifier": truncate(record.identifier, 25),
            "identifier_full": record.identifier,
            "type": truncate(record.type, 15),
            "type_full": record.type,
            "url": url_for("records.view_record", id=record.id),
        }
    )


def _get_record_links(
    record_id, filter_query, nodes, links, processed_record_ids, added_record_ids
):
    new_record_ids = set()
    link_indices = {}
    link_lengths = {}

    # Limit the maximum amount of links per record to 100 for now.
    record_links = (
        RecordLink.query.filter(
            db.or_(
                db.and_(
                    RecordLink.record_from_id == record_id,
                    RecordLink.record_to_id.in_(filter_query),
                ),
                db.and_(
                    RecordLink.record_to_id == record_id,
                    RecordLink.record_from_id.in_(filter_query),
                ),
            )
        )
        .order_by(RecordLink.created_at)
        .limit(100)
    )

    for record_link in record_links:
        # Skip all links involving records that were already checked for their links.
        if (
            record_link.record_from_id in processed_record_ids
            or record_link.record_to_id in processed_record_ids
        ):
            continue

        source = record_link.record_from
        target = record_link.record_to

        for record in [source, target]:
            new_record_ids.add(record.id)

            if record.id not in added_record_ids:
                _append_node(nodes, record)
                added_record_ids.add(record.id)

        # The link indices are used to calculate the "curve" of a link when rendering
        # it. The index of a link is increased for each link that has the same source
        # and target, starting at 1.
        link_index = 1
        key = (source.id, target.id)

        if key in link_indices:
            link_indices[key] += 1
            link_index = link_indices[key]
        else:
            link_indices[key] = link_index

        # The link lengths are used to apply varying strengths of link forces to the
        # corresponding nodes based on the length of the (truncated) link name. Only the
        # largest length between each source and target record is taken, after all links
        # have been processed.
        link_name = truncate(record_link.name, 15)
        link_length = len(link_name)
        key = (
            (source.id, target.id) if source.id < target.id else (target.id, source.id)
        )

        if key in link_lengths:
            link_lengths[key] = max(link_length, link_lengths[key])
        else:
            link_lengths[key] = link_length

        links.append(
            {
                "source": source.id,
                "target": target.id,
                "name": link_name,
                "name_full": record_link.name,
                "link_index": link_index,
                "link_length": link_length,
            }
        )

    for link in links:
        key = (
            (link["source"], link["target"])
            if link["source"] < link["target"]
            else (link["target"], link["source"])
        )

        if key in link_lengths:
            link["link_length"] = link_lengths[key]

    processed_record_ids.add(record_id)
    return new_record_ids


def get_record_links_graph(record, depth=1, user=None):
    """Get all links of a record for visualizing them in a graph.

    Used in conjunction with "d3" to visualize all returned nodes and links in a force
    directed graph.

    :param record: The record to start with.
    :param depth: (optional) The link depth.
    :param user: (optional) The user to check for access permissions regarding the
        linked records. Defaults to the current user.
    :return: A dictionary containing the record links (``"links"``) as well as all
        records involved in the links (``"nodes"``).
    """
    user = user if user is not None else current_user

    filter_query = (
        get_permitted_objects(user, "read", "record").active().with_entities(Record.id)
    )
    nodes = []
    links = []

    # Records to still check for their links.
    record_ids_to_process = {record.id}
    # Records already checked for their links.
    processed_record_ids = set()
    # Records already added to the node list.
    added_record_ids = set()

    # Add the start record itself to the nodes.
    _append_node(nodes, record)
    added_record_ids.add(record.id)

    for _ in range(0, depth):
        # Newly added records in the last iteration that are not processed yet.
        new_record_ids = set()

        for record_id in record_ids_to_process:
            new_record_ids |= _get_record_links(
                record_id,
                filter_query,
                nodes,
                links,
                processed_record_ids,
                added_record_ids,
            )

        record_ids_to_process = new_record_ids

    return {"nodes": nodes, "links": links}
