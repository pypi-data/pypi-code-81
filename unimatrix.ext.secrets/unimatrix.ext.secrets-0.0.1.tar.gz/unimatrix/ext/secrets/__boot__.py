# pylint: skip-file
import ioc
from unimatrix.conf import settings

from .conf import setup as setup_secret_loaders
from .provider import SecretLoaderProvider
from .repository import SecretRepository


def setup_ioc(*args, **kwargs):
    ioc.provide('SecretLoaderProvider', SecretLoaderProvider())
    ioc.provide('SecretRepository', SecretRepository())


@ioc.inject('repo', 'SecretRepository')
@ioc.inject('provider', 'SecretLoaderProvider')
async def on_setup(repo, provider):
    if hasattr(settings, 'SECRET_STORAGE_BACKENDS'):
        setup_secret_loaders(settings.SECRET_STORAGE_BACKENDS)
