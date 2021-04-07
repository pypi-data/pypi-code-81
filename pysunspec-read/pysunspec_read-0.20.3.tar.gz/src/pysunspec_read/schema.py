from pathlib import Path

from marshmallow import fields, ValidationError, Schema, post_dump, post_load

from pysunspec_read.connect_options import ConnectOptions, ConnectOptionsTcp, ConnectOptionsRtu, ConnectOptionsFile
from pysunspec_read.output_options import OutputOptions


class PathField(fields.Field):
    """Field that serializes to a string
        deserializes to a Path.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return str(value.as_posix())

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return Path(value)
        except ValueError as error:
            raise ValidationError("PathField must be a string") from error


class BaseSchema(Schema):
    # SKIP_VALUES = {None}

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items()
            # if value not in BaseSchema.SKIP_VALUES
            if value is not None
        }


class OutputOptionsSchema(BaseSchema):
    output_file_path = PathField()
    console = fields.Boolean()
    scale = fields.Boolean()
    log_reading = fields.Boolean()
    save_reading = fields.Boolean()
    omit_zero_readings = fields.Boolean()
    omit_none_readings = fields.Boolean()
    add_timestamp_to_reading = fields.Boolean()
    add_timestamp_to_filename = fields.Boolean()

    @post_load
    def make_request(self, data, **kwargs):
        return OutputOptions(**data)


class ConnectOptionsTcpSchema(BaseSchema):
    ip_address = fields.String()
    ip_port = fields.Integer()
    timeout = fields.Float()
    ctx = fields.String()
    max_count = fields.Integer()
    test = fields.Boolean()

    @post_load
    def make_request(self, data, **kwargs):
        return ConnectOptionsTcp(**data)


class ConnectOptionsRtuSchema(BaseSchema):
    slave_id = fields.Integer()
    name = fields.String()
    baudrate = fields.Integer()
    parity = fields.String()
    timeout = fields.Float()
    ctx = fields.Raw()
    max_count = fields.Integer()

    @post_load
    def make_request(self, data, **kwargs):
        return ConnectOptionsRtu(**data)


class ConnectOptionsFileSchema(BaseSchema):
    filename = fields.String()
    addr = fields.Integer()

    @post_load
    def make_request(self, data, **kwargs):
        return ConnectOptionsFile(**data)


class ConnectOptionsSchema(BaseSchema):
    tcp: ConnectOptionsTcp = fields.Nested(ConnectOptionsTcpSchema)
    rtu: ConnectOptionsRtu = fields.Nested(ConnectOptionsRtuSchema)
    file: ConnectOptionsFile = fields.Nested(ConnectOptionsFileSchema)

    @post_load
    def make_request(self, data, **kwargs):
        return ConnectOptions(**data)
