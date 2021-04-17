"""Declares :class:`SecretLoaderProvider`."""
import ioc.loader
from unimatrix.exceptions import ImproperlyConfigured


DEFAULT_LOADER = 'default'


class SecretLoaderProvider:
    """Maintains a registry of configured secret loaders."""

    def __init__(self):
        self.__loaders = {}
        self.__prefetching = list()

    def configure(self, config):
        """Configure the :class:`SecretLoaderProvider` instance with the
        loaders specified in the `config` dictionary.

        The string keys in the `config` mapping specify a symbolic name
        for each loader, with its members being dictionaries holding the
        configuration options. It must provide at least the ``'default'``
        key.

        The following members are supported in each configuration dictionary:

        - ``class`` - (Required) The qualified name to a concrete implementation
          of :class:`~unimatrix.ext.secrets.loaders.base.BaseLoader`.
        - ``prefetch`` - (Optional) Indicates if secrets are prefetched from the
          storage on application boot (default is ``False``).
        - ``options`` - (Required) A dictionary holding loader-specific options.
        """
        if DEFAULT_LOADER not in config:
            raise ImproperlyConfigured(
                "Loader configuration must provide 'default'.")
        for name, params in list(dict.items(config)):
            self._add_loader(
                name,
                ioc.loader.import_symbol(params['class']),
                **dict(params)
            )

    def prefetching(self):
        """Return all loader instances that are configured to prefetch secrets
        from the storage backend.
        """
        return list(self.__prefetching)

    def _add_loader(self, name, cls, **params):
        self.__loaders[name] = loader = cls(params['options'])
        loader.name = name
        if bool(params.get('prefetch')):
            self.__prefetching.append(loader)
