# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import collections
import json

try:
    import fastavro
except ImportError:  # pragma: NO COVER
    fastavro = None
import google.api_core.exceptions

try:
    import pandas
except ImportError:  # pragma: NO COVER
    pandas = None
try:
    import pyarrow
except ImportError:  # pragma: NO COVER
    pyarrow = None
import six

try:
    import pyarrow
except ImportError:  # pragma: NO COVER
    pyarrow = None


_STREAM_RESUMPTION_EXCEPTIONS = (google.api_core.exceptions.ServiceUnavailable,)

# The Google API endpoint can unexpectedly close long-running HTTP/2 streams.
# Unfortunately, this condition is surfaced to the caller as an internal error
# by gRPC. We don't want to resume on all internal errors, so instead we look
# for error message that we know are caused by problems that are safe to
# reconnect.
_STREAM_RESUMPTION_INTERNAL_ERROR_MESSAGES = (
    # See: https://github.com/googleapis/google-cloud-python/pull/9994
    "RST_STREAM",
)

_FASTAVRO_REQUIRED = (
    "fastavro is required to parse ReadRowResponse messages with Avro bytes."
)
_PANDAS_REQUIRED = "pandas is required to create a DataFrame"
_PYARROW_REQUIRED = (
    "pyarrow is required to parse ReadRowResponse messages with Arrow bytes."
)


class ReadRowsStream(object):
    """A stream of results from a read rows request.

    This stream is an iterable of
    :class:`~google.cloud.bigquery_storage_v1.types.ReadRowsResponse`.
    Iterate over it to fetch all row messages.

    If the fastavro library is installed, use the
    :func:`~google.cloud.bigquery_storage_v1.reader.ReadRowsStream.rows()`
    method to parse all messages into a stream of row dictionaries.

    If the pandas and fastavro libraries are installed, use the
    :func:`~google.cloud.bigquery_storage_v1.reader.ReadRowsStream.to_dataframe()`
    method to parse all messages into a :class:`pandas.DataFrame`.
    """

    def __init__(self, wrapped, client, name, offset, read_rows_kwargs):
        """Construct a ReadRowsStream.

        Args:
            wrapped (Iterable[ \
                ~google.cloud.bigquery_storage.types.ReadRowsResponse \
            ]):
                The ReadRows stream to read.
            client ( \
                ~google.cloud.bigquery_storage_v1.services. \
                    big_query_read.BigQueryReadClient \
            ):
                A GAPIC client used to reconnect to a ReadRows stream. This
                must be the GAPIC client to avoid a circular dependency on
                this class.
            name (str):
                Required. Stream ID from which rows are being read.
            offset (int):
                Required. Position in the stream to start
                reading from. The offset requested must be less than the last
                row read from ReadRows. Requesting a larger offset is
                undefined.
            read_rows_kwargs (dict):
                Keyword arguments to use when reconnecting to a ReadRows
                stream.

        Returns:
            Iterable[ \
                ~google.cloud.bigquery_storage.types.ReadRowsResponse \
            ]:
                A sequence of row messages.
        """

        # Make a copy of the read position so that we can update it without
        # mutating the original input.
        self._wrapped = wrapped
        self._client = client
        self._name = name
        self._offset = offset
        self._read_rows_kwargs = read_rows_kwargs

    def __iter__(self):
        """An iterable of messages.

        Returns:
            Iterable[ \
                ~google.cloud.bigquery_storage_v1.types.ReadRowsResponse \
            ]:
                A sequence of row messages.
        """

        # Infinite loop to reconnect on reconnectable errors while processing
        # the row stream.
        while True:
            try:
                for message in self._wrapped:
                    rowcount = message.row_count
                    self._offset += rowcount
                    yield message

                return  # Made it through the whole stream.
            except google.api_core.exceptions.InternalServerError as exc:
                resumable_error = any(
                    resumable_message in exc.message
                    for resumable_message in _STREAM_RESUMPTION_INTERNAL_ERROR_MESSAGES
                )
                if not resumable_error:
                    raise
            except _STREAM_RESUMPTION_EXCEPTIONS:
                # Transient error, so reconnect to the stream.
                pass

            self._reconnect()

    def _reconnect(self):
        """Reconnect to the ReadRows stream using the most recent offset."""
        self._wrapped = self._client.read_rows(
            read_stream=self._name, offset=self._offset, **self._read_rows_kwargs
        )

    def rows(self, read_session):
        """Iterate over all rows in the stream.

        This method requires the fastavro library in order to parse row
        messages in avro format.  For arrow format messages, the pyarrow
        library is required.

        .. warning::
            DATETIME columns are not supported. They are currently parsed as
            strings in the fastavro library.

        Args:
            read_session ( \
                ~google.cloud.bigquery_storage_v1.types.ReadSession \
            ):
                The read session associated with this read rows stream. This
                contains the schema, which is required to parse the data
                messages.

        Returns:
            Iterable[Mapping]:
                A sequence of rows, represented as dictionaries.
        """
        return ReadRowsIterable(self, read_session)

    def to_arrow(self, read_session):
        """Create a :class:`pyarrow.Table` of all rows in the stream.

        This method requires the pyarrow library and a stream using the Arrow
        format.

        Args:
            read_session ( \
                ~google.cloud.bigquery_storage_v1.types.ReadSession \
            ):
                The read session associated with this read rows stream. This
                contains the schema, which is required to parse the data
                messages.

        Returns:
            pyarrow.Table:
                A table of all rows in the stream.
        """
        return self.rows(read_session).to_arrow()

    def to_dataframe(self, read_session, dtypes=None):
        """Create a :class:`pandas.DataFrame` of all rows in the stream.

        This method requires the pandas libary to create a data frame and the
        fastavro library to parse row messages.

        .. warning::
            DATETIME columns are not supported. They are currently parsed as
            strings.

        Args:
            read_session ( \
                ~google.cloud.bigquery_storage_v1.types.ReadSession \
            ):
                The read session associated with this read rows stream. This
                contains the schema, which is required to parse the data
                messages.
            dtypes ( \
                Map[str, Union[str, pandas.Series.dtype]] \
            ):
                Optional. A dictionary of column names pandas ``dtype``s. The
                provided ``dtype`` is used when constructing the series for
                the column specified. Otherwise, the default pandas behavior
                is used.

        Returns:
            pandas.DataFrame:
                A data frame of all rows in the stream.
        """
        if pandas is None:
            raise ImportError(_PANDAS_REQUIRED)

        return self.rows(read_session).to_dataframe(dtypes=dtypes)


class ReadRowsIterable(object):
    """An iterable of rows from a read session.

    Args:
        reader (google.cloud.bigquery_storage_v1.reader.ReadRowsStream):
            A read rows stream.
        read_session (google.cloud.bigquery_storage_v1.types.ReadSession):
            A read session. This is required because it contains the schema
            used in the stream messages.
    """

    # This class is modelled after the google.cloud.bigquery.table.RowIterator
    # and aims to be API compatible where possible.

    def __init__(self, reader, read_session):
        self._reader = reader
        self._read_session = read_session
        self._stream_parser = _StreamParser.from_read_session(self._read_session)

    @property
    def pages(self):
        """A generator of all pages in the stream.

        Returns:
            types.GeneratorType[google.cloud.bigquery_storage_v1.ReadRowsPage]:
                A generator of pages.
        """
        # Each page is an iterator of rows. But also has num_items, remaining,
        # and to_dataframe.
        for message in self._reader:
            yield ReadRowsPage(self._stream_parser, message)

    def __iter__(self):
        """Iterator for each row in all pages."""
        for page in self.pages:
            for row in page:
                yield row

    def to_arrow(self):
        """Create a :class:`pyarrow.Table` of all rows in the stream.

        This method requires the pyarrow library and a stream using the Arrow
        format.

        Returns:
            pyarrow.Table:
                A table of all rows in the stream.
        """
        record_batches = []
        for page in self.pages:
            record_batches.append(page.to_arrow())

        if record_batches:
            return pyarrow.Table.from_batches(record_batches)

        # No data, return an empty Table.
        self._stream_parser._parse_arrow_schema()
        return pyarrow.Table.from_batches([], schema=self._stream_parser._schema)

    def to_dataframe(self, dtypes=None):
        """Create a :class:`pandas.DataFrame` of all rows in the stream.

        This method requires the pandas libary to create a data frame and the
        fastavro library to parse row messages.

        .. warning::
            DATETIME columns are not supported. They are currently parsed as
            strings in the fastavro library.

        Args:
            dtypes ( \
                Map[str, Union[str, pandas.Series.dtype]] \
            ):
                Optional. A dictionary of column names pandas ``dtype``s. The
                provided ``dtype`` is used when constructing the series for
                the column specified. Otherwise, the default pandas behavior
                is used.

        Returns:
            pandas.DataFrame:
                A data frame of all rows in the stream.
        """
        if pandas is None:
            raise ImportError(_PANDAS_REQUIRED)

        if dtypes is None:
            dtypes = {}

        # If it's an Arrow stream, calling to_arrow, then converting to a
        # pandas dataframe is about 2x faster. This is because pandas.concat is
        # rarely no-copy, whereas pyarrow.Table.from_batches + to_pandas is
        # usually no-copy.
        schema_type = self._read_session._pb.WhichOneof("schema")

        if schema_type == "arrow_schema":
            record_batch = self.to_arrow()
            df = record_batch.to_pandas()
            for column in dtypes:
                df[column] = pandas.Series(df[column], dtype=dtypes[column])
            return df

        frames = [page.to_dataframe(dtypes=dtypes) for page in self.pages]

        if frames:
            return pandas.concat(frames)

        # No data, construct an empty dataframe with columns matching the schema.
        # The result should be consistent with what an empty ARROW stream would produce.
        self._stream_parser._parse_avro_schema()
        schema = self._stream_parser._avro_schema_json

        column_dtypes = self._dtypes_from_avro(schema["fields"])
        column_dtypes.update(dtypes)

        df = pandas.DataFrame(columns=column_dtypes.keys())
        for column in df:
            df[column] = pandas.Series([], dtype=column_dtypes[column])

        return df

    def _dtypes_from_avro(self, avro_fields):
        """Determine Pandas dtypes for columns in Avro schema.

        Args:
            avro_fields (Iterable[Mapping[str, Any]]):
                Avro fields' metadata.

        Returns:
            colelctions.OrderedDict[str, str]:
                Column names with their corresponding Pandas dtypes.
        """
        result = collections.OrderedDict()

        type_map = {"long": "int64", "double": "float64", "boolean": "bool"}

        for field_info in avro_fields:
            # If a type is an union of multiple types, pick the first type
            # that is not "null".
            if isinstance(field_info["type"], list):
                type_info = next(item for item in field_info["type"] if item != "null")

            if isinstance(type_info, six.string_types):
                field_dtype = type_map.get(type_info, "object")
            else:
                logical_type = type_info.get("logicalType")
                if logical_type == "timestamp-micros":
                    field_dtype = "datetime64[ns, UTC]"
                else:
                    field_dtype = "object"

            result[field_info["name"]] = field_dtype

        return result


class ReadRowsPage(object):
    """An iterator of rows from a read session message.

    Args:
        stream_parser (google.cloud.bigquery_storage_v1.reader._StreamParser):
            A helper for parsing messages into rows.
        message (google.cloud.bigquery_storage_v1.types.ReadRowsResponse):
            A message of data from a read rows stream.
    """

    # This class is modeled after google.api_core.page_iterator.Page and aims
    # to provide API compatibility where possible.

    def __init__(self, stream_parser, message):
        self._stream_parser = stream_parser
        self._message = message
        self._iter_rows = None
        self._num_items = self._message.row_count
        self._remaining = self._message.row_count

    def _parse_rows(self):
        """Parse rows from the message only once."""
        if self._iter_rows is not None:
            return

        rows = self._stream_parser.to_rows(self._message)
        self._iter_rows = iter(rows)

    @property
    def num_items(self):
        """int: Total items in the page."""
        return self._num_items

    @property
    def remaining(self):
        """int: Remaining items in the page."""
        return self._remaining

    def __iter__(self):
        """A ``ReadRowsPage`` is an iterator."""
        return self

    def next(self):
        """Get the next row in the page."""
        self._parse_rows()
        if self._remaining > 0:
            self._remaining -= 1
        return six.next(self._iter_rows)

    # Alias needed for Python 2/3 support.
    __next__ = next

    def to_arrow(self):
        """Create an :class:`pyarrow.RecordBatch` of rows in the page.

        Returns:
            pyarrow.RecordBatch:
                Rows from the message, as an Arrow record batch.
        """
        return self._stream_parser.to_arrow(self._message)

    def to_dataframe(self, dtypes=None):
        """Create a :class:`pandas.DataFrame` of rows in the page.

        This method requires the pandas libary to create a data frame and the
        fastavro library to parse row messages.

        .. warning::
            DATETIME columns are not supported. They are currently parsed as
            strings in the fastavro library.

        Args:
            dtypes ( \
                Map[str, Union[str, pandas.Series.dtype]] \
            ):
                Optional. A dictionary of column names pandas ``dtype``s. The
                provided ``dtype`` is used when constructing the series for
                the column specified. Otherwise, the default pandas behavior
                is used.

        Returns:
            pandas.DataFrame:
                A data frame of all rows in the stream.
        """
        if pandas is None:
            raise ImportError(_PANDAS_REQUIRED)

        return self._stream_parser.to_dataframe(self._message, dtypes=dtypes)


class _StreamParser(object):
    def to_arrow(self, message):
        raise NotImplementedError("Not implemented.")

    def to_dataframe(self, message, dtypes=None):
        raise NotImplementedError("Not implemented.")

    def to_rows(self, message):
        raise NotImplementedError("Not implemented.")

    @staticmethod
    def from_read_session(read_session):
        schema_type = read_session._pb.WhichOneof("schema")
        if schema_type == "avro_schema":
            return _AvroStreamParser(read_session)
        elif schema_type == "arrow_schema":
            return _ArrowStreamParser(read_session)
        else:
            raise TypeError(
                "Unsupported schema type in read_session: {0}".format(schema_type)
            )


class _AvroStreamParser(_StreamParser):
    """Helper to parse Avro messages into useful representations."""

    def __init__(self, read_session):
        """Construct an _AvroStreamParser.

        Args:
            read_session (google.cloud.bigquery_storage_v1.types.ReadSession):
                A read session. This is required because it contains the schema
                used in the stream messages.
        """
        if fastavro is None:
            raise ImportError(_FASTAVRO_REQUIRED)

        self._read_session = read_session
        self._avro_schema_json = None
        self._fastavro_schema = None
        self._column_names = None

    def to_arrow(self, message):
        """Create an :class:`pyarrow.RecordBatch` of rows in the page.

        Args:
            message (google.cloud.bigquery_storage_v1.types.ReadRowsResponse):
                Protocol buffer from the read rows stream, to convert into an
                Arrow record batch.

        Returns:
            pyarrow.RecordBatch:
                Rows from the message, as an Arrow record batch.
        """
        raise NotImplementedError("to_arrow not implemented for Avro streams.")

    def to_dataframe(self, message, dtypes=None):
        """Create a :class:`pandas.DataFrame` of rows in the page.

        This method requires the pandas libary to create a data frame and the
        fastavro library to parse row messages.

        .. warning::
            DATETIME columns are not supported. They are currently parsed as
            strings in the fastavro library.

        Args:
            dtypes ( \
                Map[str, Union[str, pandas.Series.dtype]] \
            ):
                Optional. A dictionary of column names pandas ``dtype``s. The
                provided ``dtype`` is used when constructing the series for
                the column specified. Otherwise, the default pandas behavior
                is used.

        Returns:
            pandas.DataFrame:
                A data frame of all rows in the stream.
        """
        self._parse_avro_schema()

        if dtypes is None:
            dtypes = {}

        columns = collections.defaultdict(list)
        for row in self.to_rows(message):
            for column in row:
                columns[column].append(row[column])
        for column in dtypes:
            columns[column] = pandas.Series(columns[column], dtype=dtypes[column])
        return pandas.DataFrame(columns, columns=self._column_names)

    def _parse_avro_schema(self):
        """Extract and parse Avro schema from a read session."""
        if self._avro_schema_json:
            return

        self._avro_schema_json = json.loads(self._read_session.avro_schema.schema)
        self._column_names = tuple(
            (field["name"] for field in self._avro_schema_json["fields"])
        )

    def _parse_fastavro(self):
        """Convert parsed Avro schema to fastavro format."""
        self._parse_avro_schema()
        self._fastavro_schema = fastavro.parse_schema(self._avro_schema_json)

    def to_rows(self, message):
        """Parse all rows in a stream message.

        Args:
            message ( \
                ~google.cloud.bigquery_storage_v1.types.ReadRowsResponse \
            ):
                A message containing Avro bytes to parse into rows.

        Returns:
            Iterable[Mapping]:
                A sequence of rows, represented as dictionaries.
        """
        self._parse_fastavro()
        messageio = six.BytesIO(message.avro_rows.serialized_binary_rows)
        while True:
            # Loop in a while loop because schemaless_reader can only read
            # a single record.
            try:
                # TODO: Parse DATETIME into datetime.datetime (no timezone),
                #       instead of as a string.
                yield fastavro.schemaless_reader(messageio, self._fastavro_schema)
            except StopIteration:
                break  # Finished with message


class _ArrowStreamParser(_StreamParser):
    def __init__(self, read_session):
        if pyarrow is None:
            raise ImportError(_PYARROW_REQUIRED)

        self._read_session = read_session
        self._schema = None

    def to_arrow(self, message):
        return self._parse_arrow_message(message)

    def to_rows(self, message):
        record_batch = self._parse_arrow_message(message)

        # Iterate through each column simultaneously, and make a dict from the
        # row values
        for row in zip(*record_batch.columns):
            yield dict(zip(self._column_names, row))

    def to_dataframe(self, message, dtypes=None):
        record_batch = self._parse_arrow_message(message)

        if dtypes is None:
            dtypes = {}

        df = record_batch.to_pandas()

        for column in dtypes:
            df[column] = pandas.Series(df[column], dtype=dtypes[column])

        return df

    def _parse_arrow_message(self, message):
        self._parse_arrow_schema()

        return pyarrow.ipc.read_record_batch(
            pyarrow.py_buffer(message.arrow_record_batch.serialized_record_batch),
            self._schema,
        )

    def _parse_arrow_schema(self):
        if self._schema:
            return

        self._schema = pyarrow.ipc.read_schema(
            pyarrow.py_buffer(self._read_session.arrow_schema.serialized_schema)
        )
        self._column_names = [field.name for field in self._schema]
