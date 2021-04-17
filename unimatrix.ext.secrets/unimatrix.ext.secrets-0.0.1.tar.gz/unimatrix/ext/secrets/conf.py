"""Provides the interface to configure secret loaders."""
import ioc


def setup(loaders):
    """Ensure that the inversion-of-control container and loaders are properly
    configured.
    """
    ioc.require('SecretLoaderProvider')\
        .configure(loaders)
