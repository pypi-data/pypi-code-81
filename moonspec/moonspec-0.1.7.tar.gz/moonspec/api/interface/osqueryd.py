import logging
from typing import Dict, Optional, Any, Union, List

LOGGER = logging.getLogger('moonspec')

has_osquery: bool = False
try:
    import osquery  # type: ignore
    from osquery import SpawnInstance
    from osquery.extensions.ExtensionManager import Client  # type: ignore

    has_osquery = True
except ImportError:
    has_osquery = False
    SpawnInstance = None
    Client = None


class OSQueryApi:
    _instance_ref: Optional[Any] = None

    @staticmethod
    def supports() -> bool:
        return has_osquery

    # TODO: thread safety
    @staticmethod
    def _instance() -> SpawnInstance:
        if not has_osquery:
            raise RuntimeError('OSQuery is not supported')

        if OSQueryApi._instance_ref is not None:
            return OSQueryApi._instance_ref

        instance = SpawnInstance()

        try:
            instance.open(timeout=0.05)
        except BaseException as e:
            LOGGER.exception('Failed to connect to osquery', e)
            raise RuntimeError('Failed to connect to osquery')

        OSQueryApi._instance_ref = instance

        return OSQueryApi._instance_ref

    @staticmethod
    def client() -> Client:
        instance = OSQueryApi._instance()

        if not instance:
            LOGGER.warning('osquery not available')
            raise RuntimeError('OSQuery is not supported')

        return instance.client

    @staticmethod
    def query(query: str) -> Optional[Union[Dict, List, float, int, bool]]:
        instance = OSQueryApi._instance()

        if not instance:
            LOGGER.warning('osquery not available - %s', query)
            raise RuntimeError('OSQuery is not supported')

        result = instance.client.query(query)

        if result.status.code != 0:
            LOGGER.error('osquery query failed - %d %s, for %s', result.status.code, result.status.message, query)
            return None

        return result.response
