"""Declares :class:`SecretRepository`."""
import collections

import ioc

from .provider import DEFAULT_LOADER


class SecretRepository:
    """Provides an abstraction for the secret storage layer. This repository
    implementation uses a dictionary to maintain local state of secrets. It is
    populated using concrete :class:`~unimatrix.ext.secrets.loaders.BaseLoader`
    implementations.
    """
    __module__ = 'unimatrix.ext.secrets'
    SecretDoesNotExist = type('SecretDoesNotExist', (LookupError,), {})

    def __init__(self):
        self.__secrets = collections.defaultdict(dict)

    def _add_secret(self, using, name, version, payload):
        pass

    def get(self, name, version=None, using=DEFAULT_LOADER):
        """Lookup a :class:`~unimatrix.ext.secrets.Secret` instance from the
        local storage backend.

        If the secret identified by the input parameter is not present, and
        the `using` argument is provided, use the given storage backend to
        lookup the secret in the remote storage (TODO).
        """
        try:
            return self.__secrets[using][name][version]
        except LookupError:
            raise self.SecretDoesNotExist

    @ioc.inject('provider', 'SecretLoaderProvider')
    async def prefetch(self, provider):
        """Run all configured secret loaders and ensure that the secrets are
        locally available through the repository.
        """
        for loader in provider.prefetching():
            await self.run_loader(loader)

    async def run_loader(self, loader):
        """Invoke the :meth:`~unimatrix.ext.secrets.loader.BaseLoader.prefetch`
        method to lookup all secrets from the storage backend and populate the
        internal state of the :class:`SecretRepository`.
        """
        async for name, version, payload in loader.prefetch():
            if name not in self.__secrets[loader.name]:
                self.__secrets[loader.name][name] = collections.defaultdict(
                    lambda: payload
                )
            self.__secrets[loader.name][name][version] = payload
