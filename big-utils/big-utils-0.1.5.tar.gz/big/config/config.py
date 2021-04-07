"""
Configuration utilities
"""
import os
import json
import toml
import yaml
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union
from dataclasses import is_dataclass, fields
from configparser import ConfigParser, MissingSectionHeaderError
from dacite import from_dict, Config
from big.utils.strutil import trim, trim_to_lower, string_2_bool


def load_from_json_file(file_name: Path) -> dict:
    logger = logging.getLogger(__name__)
    logger.debug('Parsing JSON file [%s]', file_name)
    with open(file_name, 'r') as f:
        return json.load(f)


def load_from_yaml_file(file_name: Path) -> dict:
    logger = logging.getLogger(__name__)
    logger.debug('Parsing YAML file [%s]', file_name)
    with open(file_name, 'r') as f:
        return yaml.safe_load(f)


def load_from_toml_file(file_name: Path) -> dict:
    logger = logging.getLogger(__name__)
    logger.debug('Parsing TOML file [%s]', file_name)
    with open(file_name, 'r') as f:
        return toml.load(f)


def load_from_ini_file(file_name: Path) -> dict:
    logger = logging.getLogger(__name__)
    logger.debug('Parsing INI file [%s]', file_name)
    cp = ConfigParser()
    # we need this, otherwise all keys get converted to lowercase
    cp.optionxform = lambda option: option
    cp.read(file_name)
    return {s: dict(cp.items(s)) for s in cp.sections()}


def load_from_properties_file(file_name: Path) -> dict:
    logger = logging.getLogger(__name__)
    logger.debug('Parsing Java properties file [%s]', file_name)
    cp = ConfigParser(strict=False)
    # we need this, otherwise all keys get converted to lowercase
    cp.optionxform = lambda option: option

    # java property files don't require headers, but the Python
    # ConfigParser does require them. If we encounter a nasty
    # MissingSectionHeaderError, we fake a header to keep the
    # parser happy
    fake_header = 'FAKE_HEADER'
    fake_header_used = False
    try:
        cp.read(file_name)
    except MissingSectionHeaderError:
        logger.debug('File [%s] is missing a section header, providing a fake one', file_name)
        text = f'[{fake_header}]\n{file_name.read_text()}'
        fake_header_used = True
        cp.read_string(text)
    return dict(cp.items(fake_header)) if fake_header_used else {s: dict(cp.items(s)) for s in cp.sections()}


# maps file name extension (aka suffix) to the loader function
EXT_LIST = [
    '.yaml',
    '.yml',
    '.json',
    '.ini',
    '.toml',
    '.properties'
]
EXT_MAP = {
    EXT_LIST[0]: load_from_yaml_file,
    EXT_LIST[1]: load_from_yaml_file,
    EXT_LIST[2]: load_from_json_file,
    EXT_LIST[3]: load_from_ini_file,
    EXT_LIST[4]: load_from_toml_file,
    EXT_LIST[5]: load_from_properties_file
}


def load_config_from_file(file_name: Union[Path, str], default_ext: Optional[str] = None) -> dict:
    """
    Loads configuration from the specified file and returns it as a Python dictionary.
    Currently supported file formats include:

        * JSON
        * YAML
        * TOML
        * INI
        * Java Properties (rudimentary support)

    The type of the file is determined based on the file extension. If the specified
    :code:`file_name` is missing the extension, an optional :code:`default_ext`
    argument is used. If the :code:`default_ext` argument is not provided or it is
    :code:`None`, a :code:`ValueError` is raised. If we don't know how to handle the
    format (type) of the specified file, as determined by the file extension,
    a :code:`KeyError` is raised.

    :param file_name: a file path of the configuration file.
    :param default_ext: a default file name extension in case the file extension is missing.
    :return: a dictionary with the contents of the configuration file.
    :raises ValueError: if the file extension is missing and the default_ext argument is not
        provided or it is None.
    :raises KeyError: if we don't know how to handle the format (type) of the specified file, as
        determined by the file extension.
    """
    file_name = Path(file_name)
    ext = trim_to_lower(file_name.suffix, trim_to_lower(default_ext))
    if not ext:
        raise ValueError('A file name must have an extension or a default extension must be provided')

    # this will throw a KeyError exception if the extension is unknown.
    return EXT_MAP[ext](file_name)


def str2bool_converter(val):
    return val if isinstance(val, bool) else string_2_bool(str(val))


class Configurator:
    """Base class supporting our configuration """

    def __init__(self, config_file_list, ignore_missing=True, include_env=True):
        """
        Initializes the :code:`BaseConfigurator` with a list of the configuration files. Each configuration file
        can be of any of the supported formats (see the :code:`load_config_from_file' for the detailed list).

        :param config_file_list: a list of the configuration files.
        """
        self.config_file_list = config_file_list
        self.ignore_missing = ignore_missing
        self.include_env = include_env
        self.converters = {
            bool: str2bool_converter,
            int: int
        }

    def __deep_dict_update(self, orig_dict, new_dict):
        for key, new_val in new_dict.items():
            old_val = orig_dict.get(key)
            if old_val is not None and isinstance(new_val, dict) and isinstance(old_val, dict):
                self.__deep_dict_update(old_val, new_val)
            elif new_val is not None:
                orig_dict[key] = new_val

    def load_configuration(self):
        logger = logging.getLogger(__name__)
        config_dict = dict()
        for config_file in self.config_file_list:
            file_name = Path(config_file)
            if file_name.is_file():
                try:
                    new_dict = load_config_from_file(file_name)
                    self.__deep_dict_update(config_dict, new_dict)
                except IOError:
                    logger.exception('Failed to load the configuration from file [%s]', file_name)
            elif not self.ignore_missing:
                logger.error("We're not suppose to ignore missing files -> raising exception")
                raise FileNotFoundError(file_name)
        return config_dict

    def configure(self, data_class):
        """
        This is where the magic happens - we're loading the configuration from the file(s),
        potentially overriding it with the values specified in the environment, if there
        are environment variables specified that match the names of the dataclass fields.

        :param data_class: a dataclass type.
        :return: an instance of the data class.
        """
        if not is_dataclass(data_class):
            raise TypeError(f'{data_class} type must be a dataclass')

        # load configuration from the file(s)
        config_dict = self.load_configuration()

        if self.include_env:
            # override and/or extend it with the values from the environment
            # using the names of the fields as the names of the env variables.
            # We follow the path of the dataclasses - that is, if the field
            # is another dataclass, we check for the environment variables
            # named after the original field and the current field, separated
            # with a '.' (period)
            def env_override(dc, current_dict, name_root):
                for field in fields(dc):
                    env_name = field.metadata.get('env', field.name)
                    env_name = f'{name_root}__{env_name}' if name_root else env_name
                    if is_dataclass(field.type):
                        # the value associated with this key may or may
                        # not exist - but if it exists, it must be a
                        # dictionary
                        field_dict = current_dict.get(field.name, {})
                        if not isinstance(field_dict, dict):
                            raise TypeError(f'The value for key [{field.name}] must a dict')
                        env_override(field.type, field_dict, env_name)
                        # assign or re-assign (if it existed)
                        current_dict[field.name] = field_dict
                    elif env_name in os.environ:
                        current_dict[field.name] = os.environ[env_name]

            env_override(data_class, config_dict, '')

        return from_dict(data_class, config_dict, config=Config(type_hooks=self.converters))


class ConfigStrategy(ABC):
    """
    An abstract base class defining a 'contract' for the different configuration file strategies.
    The purpose of the strategy is to generate a list of configuration files
    """

    def __init__(self, app_name):
        self.app_name = app_name

    @property
    @abstractmethod
    def config_file_list(self):
        pass

    @staticmethod
    def resolve_relative_to_file(anchor_file_path, file_name_path) -> Path:
        anchor = Path(anchor_file_path)
        return anchor.parent / file_name_path if anchor.is_file() else anchor / file_name_path

    @property
    def system_config_dir(self):
        return Path('/etc') / self.app_name

    @property
    def user_config_dir(self):
        return Path.home() / f'.{self.app_name}'


class MultiEnvironmentStrategy(ConfigStrategy, ABC):
    """
    An abstract base class for the configuration strategies that support multiple environments
    (e.g. 'development', 'testing' and 'production').
    """

    # standard environments
    ENV_DEVELOPMENT = 'development'
    ENV_TESTING = 'testing'
    ENV_PRODUCTION = 'production'
    ENV_STAGING = 'staging'
    ENV_QA = 'qa'
    ENV_UAT = 'uat'

    ABBREVIATIONS = {
        ENV_DEVELOPMENT: 'dev',
        ENV_TESTING: 'test',
        ENV_PRODUCTION: 'prod',
    }

    DEFAULT_ENV = ENV_DEVELOPMENT

    def __init__(self, app_name, env_name=None):
        super().__init__(app_name)
        self.env_name = trim(env_name) or self.DEFAULT_ENV

    @property
    def short_env_name(self):
        return self.ABBREVIATIONS.get(self.env_name, self.env_name)


class StandardStrategy(MultiEnvironmentStrategy):
    """The most common strategy that includes the support for the multiple files,
    multiple files and multiple directories"""
    DEFAULT_EXT = '.yaml'

    def __init__(self, project_root_dir, app_name, ext=None, env_name=None):
        super().__init__(app_name, env_name)

        # verify we have a valid directory or a file - if file, we use
        # the parent directory as the project root
        project_root_dir = Path(project_root_dir)
        if not project_root_dir.exists():
            raise FileNotFoundError(project_root_dir)
        self.project_root_dir = project_root_dir if project_root_dir.is_dir() else project_root_dir.parent

        # ensure we have a valid known extension, if specified (defaults to YAML)
        # also ensure that the extension does, indeed, start with a '.'
        ext = trim_to_lower(ext) or self.DEFAULT_EXT
        ext = ext if ext.startswith('.') else f'.{ext}'
        if ext not in EXT_MAP:
            raise ValueError(f'Unknown extension [{ext}]: must be one of {EXT_LIST}')
        self.__ext = ext
        self.config_name_root = 'config'
        self.__config_file_list = None

    @property
    def ext(self):
        return self.__ext

    @property
    def config_file_list(self):
        if not self.__config_file_list:
            self.__config_file_list = [
                self.project_root_dir / f'{self.config_name_root}{self.ext}',
                self.project_root_dir / f'{self.config_name_root}-{self.short_env_name}{self.ext}',
                self.system_config_dir / f'{self.config_name_root}{self.ext}',
                self.system_config_dir / f'{self.config_name_root}-{self.short_env_name}{self.ext}',
                self.user_config_dir / f'{self.config_name_root}{self.ext}',
                self.user_config_dir / f'{self.config_name_root}-{self.short_env_name}{self.ext}',
            ]
        return self.__config_file_list
