# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
#

import proto  # type: ignore


from google.cloud.bigquery_storage_v1.types import arrow
from google.cloud.bigquery_storage_v1.types import avro
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.bigquery.storage.v1",
    manifest={"DataFormat", "ReadSession", "ReadStream",},
)


class DataFormat(proto.Enum):
    r"""Data format for input or output data."""
    DATA_FORMAT_UNSPECIFIED = 0
    AVRO = 1
    ARROW = 2


class ReadSession(proto.Message):
    r"""Information about the ReadSession.

    Attributes:
        name (str):
            Output only. Unique identifier for the session, in the form
            ``projects/{project_id}/locations/{location}/sessions/{session_id}``.
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Time at which the session becomes invalid.
            After this time, subsequent requests to read this Session
            will return errors. The expire_time is automatically
            assigned and currently cannot be specified or updated.
        data_format (google.cloud.bigquery_storage_v1.types.DataFormat):
            Immutable. Data format of the output data.
        avro_schema (google.cloud.bigquery_storage_v1.types.AvroSchema):
            Output only. Avro schema.
        arrow_schema (google.cloud.bigquery_storage_v1.types.ArrowSchema):
            Output only. Arrow schema.
        table (str):
            Immutable. Table that this ReadSession is reading from, in
            the form
            ``projects/{project_id}/datasets/{dataset_id}/tables/{table_id}``
        table_modifiers (google.cloud.bigquery_storage_v1.types.ReadSession.TableModifiers):
            Optional. Any modifiers which are applied
            when reading from the specified table.
        read_options (google.cloud.bigquery_storage_v1.types.ReadSession.TableReadOptions):
            Optional. Read options for this session (e.g.
            column selection, filters).
        streams (Sequence[google.cloud.bigquery_storage_v1.types.ReadStream]):
            Output only. A list of streams created with the session.

            At least one stream is created with the session. In the
            future, larger request_stream_count values *may* result in
            this list being unpopulated, in that case, the user will
            need to use a List method to get the streams instead, which
            is not yet available.
    """

    class TableModifiers(proto.Message):
        r"""Additional attributes when reading a table.

        Attributes:
            snapshot_time (google.protobuf.timestamp_pb2.Timestamp):
                The snapshot time of the table. If not set,
                interpreted as now.
        """

        snapshot_time = proto.Field(
            proto.MESSAGE, number=1, message=timestamp.Timestamp,
        )

    class TableReadOptions(proto.Message):
        r"""Options dictating how we read a table.

        Attributes:
            selected_fields (Sequence[str]):
                Names of the fields in the table that should be read. If
                empty, all fields will be read. If the specified field is a
                nested field, all the sub-fields in the field will be
                selected. The output field order is unrelated to the order
                of fields in selected_fields.
            row_restriction (str):
                SQL text filtering statement, similar to a WHERE clause in a
                query. Aggregates are not supported.

                Examples: "int_field > 5" "date_field = CAST('2014-9-27' as
                DATE)" "nullable_field is not NULL" "st_equals(geo_field,
                st_geofromtext("POINT(2, 2)"))" "numeric_field BETWEEN 1.0
                AND 5.0"

                Restricted to a maximum length for 1 MB.
            arrow_serialization_options (google.cloud.bigquery_storage_v1.types.ArrowSerializationOptions):

        """

        selected_fields = proto.RepeatedField(proto.STRING, number=1)

        row_restriction = proto.Field(proto.STRING, number=2)

        arrow_serialization_options = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="output_format_serialization_options",
            message=arrow.ArrowSerializationOptions,
        )

    name = proto.Field(proto.STRING, number=1)

    expire_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp,)

    data_format = proto.Field(proto.ENUM, number=3, enum="DataFormat",)

    avro_schema = proto.Field(
        proto.MESSAGE, number=4, oneof="schema", message=avro.AvroSchema,
    )

    arrow_schema = proto.Field(
        proto.MESSAGE, number=5, oneof="schema", message=arrow.ArrowSchema,
    )

    table = proto.Field(proto.STRING, number=6)

    table_modifiers = proto.Field(proto.MESSAGE, number=7, message=TableModifiers,)

    read_options = proto.Field(proto.MESSAGE, number=8, message=TableReadOptions,)

    streams = proto.RepeatedField(proto.MESSAGE, number=10, message="ReadStream",)


class ReadStream(proto.Message):
    r"""Information about a single stream that gets data out of the storage
    system. Most of the information about ``ReadStream`` instances is
    aggregated, making ``ReadStream`` lightweight.

    Attributes:
        name (str):
            Output only. Name of the stream, in the form
            ``projects/{project_id}/locations/{location}/sessions/{session_id}/streams/{stream_id}``.
    """

    name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
