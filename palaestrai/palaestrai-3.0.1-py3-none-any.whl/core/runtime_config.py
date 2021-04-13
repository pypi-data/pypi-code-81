from os import getcwd

import appdirs
import ruamel.yaml

from . import LOG


class _RuntimeConfig:
    """Application-wide runtime configuration.

    This singleton class provides an application-wide runtime configuration
    and transparently hides all sources from the rest of the application.
    """

    CONFIG_FILE_PATHS = [
        "%s/runtime-conf.yaml"
        % appdirs.user_config_dir("palaestrai", "OFFIS"),
        "%s/runtime-conf.yaml"
        % appdirs.site_config_dir("palaestrai", "OFFIS"),
        "%s/arl-runtime.conf.yaml" % getcwd(),
    ]
    _instance = None

    def __init__(self):
        self._conf_dict = {}
        self._logging = None
        self._store_uri = None
        self._public_bind = None
        self._executor_bus_port = None

        self._config_file_path = None
        self.config_search_path = _RuntimeConfig.CONFIG_FILE_PATHS

    def _get(self, key, default=None, exception=None):
        """Retrives an config key

        Retrieves any config key; if not set, it queries the config dictionary;
        if it isn't present there, it returns the given default value. It also
        sets the value in the current object as a side-effect.
        """
        lkey = "_%s" % key
        if lkey not in self.__dict__ or not self.__dict__[lkey]:
            try:
                self.__dict__[lkey] = self._conf_dict[key]
            except KeyError:
                self.__dict__[lkey] = default
                if exception:
                    raise KeyError(exception)
        return self.__dict__[lkey]

    @property
    def logging(self):
        """Configuration of all subsystem loggers

        :return: A logging configuration that can be fed into
            `logging.DictConfig`.
        :rtype: dict
        """
        return self._get(
            "logging",
            default={},
            exception="Sorry, no logging config in the config file",
        )

    @property
    def store_uri(self):
        """URI to the store database for results

        This must be any standards-compliant string in the form of
        `transport://user:password@host-or-path:port/db`. For example,
        `postgresql://myuser:mypass@localhost/arl`.

        :return: The URI string.
        :rtype: str
        """
        return self._get(
            "store_uri",
            default=None,
            exception="No store configuration available",
        )

    @property
    def executor_bus_port(self):
        """Port of the executor's messaging bus

        palaestrai needs one bus to start it all, which is managed by the
        executor. All other buses and topics can be communicated over this
        initial bus.

        :return: The bus URI, default: 4242
        :rtype: int
        """
        return self._get("executor_bus_port", default=4242)

    @property
    def public_bind(self):
        """Indicates whether to bind to all public adresses or to localhost

        This configuration setting allows the Executor and all other message
        buses to bind to all public IP addresses if set to `True`. If not,
        the buses will bind to `localhost` only.

        :return: Whether to bind to all available IP adresses (`True`) or not.
        :rtype: bool
        """
        return self._get("public_bind", default=False)

    def load(self, stream=None):
        """Loads the configuration from an external source.

        This overwrites the current configuration in the singleton, effectively
        resetting it.

        :param stream: Reads the runtime YAML config from this stream, if
        given. If no stream is given, the default files in
        ::`.CONFIG_FILE_PATHS` will be tried, in order of appeareance, until
        one can be opened as a stream.
        """
        yml = ruamel.yaml.YAML(typ="safe")
        if stream:
            self._conf_dict = yml.load(stream)
            self._config_file_path = stream
            return
        else:
            for file in _RuntimeConfig.CONFIG_FILE_PATHS:
                try:
                    LOG.debug("Trying to open configuration file: %s", file)
                    with open(file, "r") as fp:
                        self._conf_dict = yml.load(fp)
                        self._config_file_path = file
                        return
                except IOError:
                    continue
        raise FileNotFoundError(
            "None of %s found" % (", ".join(_RuntimeConfig.CONFIG_FILE_PATHS))
        )

    def __str__(self):
        return "<RuntimeConfig id=0x%x> at %s" % (
            id(self),
            self._config_file_path,
        )


def RuntimeConfig():
    if _RuntimeConfig._instance is None:
        _RuntimeConfig._instance = _RuntimeConfig()
        try:
            _RuntimeConfig._instance.load()
        except FileNotFoundError:
            pass  # Ignore it here, because we load implicitly.
    return _RuntimeConfig._instance
