from dataclasses import dataclass
from pathlib import Path

import yaml
from marshmallow import fields, post_load
from pysunspec_read.connect_options import ConnectOptions
from pysunspec_read.output_options import OutputOptions
from pysunspec_read.schema import ConnectOptionsSchema, OutputOptionsSchema, BaseSchema


@dataclass
class PvOutputOptions:
    secret_api_key: str
    system_id: int
    publish_limit: int = 30
    net_flag: int = None
    cumulative_flag: int = None
    is_donation_mode: bool = False


class PvOutputOptionsSchema(BaseSchema):
    secret_api_key = fields.String()
    system_id = fields.Integer()
    publish_limit = fields.Integer()
    net_flag = fields.Integer()
    cumulative_flag = fields.Integer()
    is_donation_mode = fields.Boolean()

    @post_load
    def make_request(self, data, **kwargs):
        return PvOutputOptions(**data)


@dataclass
class Config:
    connect_options: ConnectOptions = None
    output_options: OutputOptions = None
    pvoutput_publish_options: PvOutputOptions = None


def load_config(config_path: Path) -> Config:
    with open(config_path) as configFile:
        yaml_conf = yaml.safe_load(configFile)
    config = Config()

    config.pvoutput_publish_options = PvOutputOptionsSchema().load(yaml_conf.get("pvoutput_publish_options"),
                                                                   partial=True)
    config.connect_options = ConnectOptionsSchema().load(yaml_conf.get("connect_options"), partial=True)
    config.output_options = OutputOptionsSchema().load(yaml_conf.get("output_options"), partial=True)
    config.pvoutput_publish_options.cache_path = config.output_options.output_file_path.parent
    return config
