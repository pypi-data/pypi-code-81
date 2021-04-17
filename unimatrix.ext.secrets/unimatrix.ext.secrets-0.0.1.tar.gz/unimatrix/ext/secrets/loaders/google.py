"""Declares :class:`GoogleSecretLoader`."""
import asyncio
import itertools

import google.api_core.exceptions
import marshmallow.fields
from google.cloud import secretmanager
from google.cloud.secretmanager import SecretVersion

from .base import BaseLoader


class GoogleSecretLoader(BaseLoader):
    """A :class:`BaseLoader` implementation that uses Google Secret Manager
    as the secret storage backend.
    """

    project = marshmallow.fields.String(
        required=True
    )

    filters = marshmallow.fields.List(
        marshmallow.fields.String,
        missing=list,
        default=list
    )

    @staticmethod
    def _get_secretmanager_client():
        return secretmanager.SecretManagerServiceAsyncClient()

    async def prefetch(self):
        """Invoke the Google Secret Manager API to fetch all secrets included
        by the search predicate.
        """
        secretmanager = self._get_secretmanager_client()
        futures = []
        async for secret in await self._list_secrets(secretmanager):
            futures.append(self._load_versions(secretmanager, secret))
        for result in itertools.chain(*await asyncio.gather(*futures)):
            yield result

    async def _list_secrets(self, secretmanager):
        request = {
            'parent': f'projects/{self.opts.project}'
        }
        if len(self.opts.filters):
            raise NotImplementedError("Filtering is not supported.")
        try:
            return await secretmanager.list_secrets(request)
        except google.api_core.exceptions.NotFound:
            return []

    async def _load_versions(self, secretmanager, secret):
        futures = []
        async for version in\
        await secretmanager.list_secret_versions({'parent': secret.name}):
            if version.state != SecretVersion.State.ENABLED:
                continue
            futures.append(secretmanager.access_secret_version({
                'name': version.name
            }))

            *_, name, _, version_number = str.split(version.name, '/')

        return [(name, int(version_number), x.payload.data)
            for x in await asyncio.gather(*futures)]
