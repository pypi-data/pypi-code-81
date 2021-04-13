import json
import os

import importlib_resources as pkg_resources
import jsonschema
import ruamel.yaml
from aos_signer.signer.errors import SignerConfigError

from .models.build import Build
from .models.configuration import Configuration
from .models.publish import Publish
from .models.publisher import Publisher


class ServiceConfiguration(object):

    DEFAULT_META_FOLDER = 'meta'
    DEFAULT_CONFIG_FILE_NAME = 'config.yaml'

    def __init__(self, file_path=None):
        if file_path is None:
            file_path = os.path.join(self.DEFAULT_META_FOLDER, self.DEFAULT_CONFIG_FILE_NAME)

        if not os.path.isfile(file_path):
            raise OSError("Config file {} not found. Exiting...".format(file_path))

        yaml = ruamel.yaml.YAML()
        with open(file_path, 'r') as file:
            try:
                schema = pkg_resources.files('aos_signer') / 'files/root_schema.json'
                loaded = yaml.load(file)
                with pkg_resources.as_file(schema) as schema_path:
                    with open(schema_path, 'r') as f:
                        sc = json.loads(f.read())
                        jsonschema.validate(loaded, schema=sc)
                self._publisher = Publisher.from_yaml(loaded.get('publisher'))
                self._publish = Publish.from_yaml(loaded.get('publish'))
                self._build = Build.from_yaml(loaded.get('build'))
                self._configuration = Configuration.from_yaml(loaded.get('configuration'))
            except (ruamel.yaml.parser.ParserError,
                    ruamel.yaml.scanner.ScannerError,
                    jsonschema.exceptions.ValidationError) as exc:
                raise SignerConfigError(str(exc))

    @property
    def publisher(self):
        return self._publisher

    @property
    def publish(self):
        return self._publish

    @property
    def build(self):
        return self._build

    @property
    def configuration(self):
        return self._configuration
