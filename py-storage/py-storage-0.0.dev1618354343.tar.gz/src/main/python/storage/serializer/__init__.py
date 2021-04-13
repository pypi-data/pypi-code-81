import json
from json import JSONDecoder, JSONEncoder
from typing import Iterator, Generic, Sequence

import toml
import yaml

from storage import E


class Serializer(Generic[E]):

    @classmethod
    def json(cls, decoder=JSONDecoder, encoder=JSONEncoder, indent=2):
        return cls(
            lambda input_stream: json.load(input_stream, cls=decoder),
            lambda output_stream, data: json.dump(data, output_stream, cls=encoder, indent=indent),
            default_extension='json',
        )

    @classmethod
    def yaml(cls, decoder=yaml.Loader, dumper=yaml.Dumper):
        return cls(
            lambda input_stream: yaml.load(input_stream, Loader=decoder),
            lambda output_stream, data: yaml.dump(data, output_stream, Dumper=dumper),
            default_extension='yml',
        )

    @classmethod
    def toml(cls, root_key='_'):
        return cls(
            lambda input_stream: toml.load(input_stream)[root_key],
            lambda output_stream, data: toml.dump({root_key: data}, output_stream),
            lambda input_stream: toml.load(input_stream),
            lambda output_stream, data: toml.dump(data, output_stream),
            default_extension='toml',
        )

    def __init__(self,
                 deserialize_many,
                 serialize_many,
                 deserialize_one=None,
                 serialize_one=None,
                 default_extension: str = None,
                 supported_extensions: Sequence[str] = None):
        self.deserialize_many = deserialize_many
        self.serialize_many = serialize_many
        self.deserialize_one = deserialize_one or deserialize_many
        self.serialize_one = serialize_one or serialize_many
        self.default_extension = default_extension
        self.supported_extension = supported_extensions or [default_extension]

    def read_one(self, input_stream) -> E:
        return self.deserialize_one(input_stream)

    def write_one(self, output_stream, item: E):
        self.serialize_one(output_stream, item)

    def read_many(self, input_stream) -> Iterator[E]:
        yield from self.deserialize_many(input_stream)

    def write_many(self, output_stream, data):
        self.serialize_many(output_stream, data)
