import typing
from typing import Any, Dict, Iterator, Optional, Tuple, Union

from mode.utils.collections import LRUCache

try:  # pragma: no cover
    import aerospike
except ImportError:  # pragma: no cover
    aerospike = None  # noqa

from yarl import URL

from faust.stores import base
from faust.types import TP, AppT, CollectionT

if typing.TYPE_CHECKING:  # pragma: no cover
    from aerospike import SCAN_PRIORITY_MEDIUM, TTL_NEVER_EXPIRE, Client
else:

    class Client:  # noqa
        """Dummy Client."""

    TTL_NEVER_EXPIRE = -1
    SCAN_PRIORITY_MEDIUM = 2


if typing.TYPE_CHECKING:  # pragma: no cover
    import aerospike.exception.RecordGenerationError
    import aerospike.exception.RecordNotFound
else:

    class RecordNotFound:  # noqa
        """Dummy Exception."""

    class RecordGenerationError:  # noqa
        """Dummy Exception."""


aerospike_client: Client = None


class AeroSpikeStore(base.SerializedStore):
    """Aerospike table storage."""

    client: Client
    ttl: int
    policies: typing.Mapping[str, Any]
    _key_index: LRUCache[bytes, int]
    BIN_KEY = "value_key"
    USERNAME_KEY = "username"
    HOSTS_KEY = "hosts"
    PASSWORD_KEY = "password"  # nosec
    NAMESPACE_KEY = "namespace"
    TTL_KEY = "ttl"
    POLICIES_KEY = "policies"
    CLIENT_OPTIONS_KEY = "client"
    GENERATION_KEY = "gen"

    def __init__(
        self,
        url: Union[str, URL],
        app: AppT,
        table: CollectionT,
        options: typing.Mapping[str, Any] = None,
        **kwargs: Any,
    ) -> None:
        try:
            self.client = AeroSpikeStore.get_aerospike_client(options)
            self.namespace = options.get(self.NAMESPACE_KEY, "")
            self.ttl = options.get(self.TTL_KEY, aerospike.TTL_NEVER_EXPIRE)
            self.policies = options.get(self.POLICIES_KEY, None)
            table.use_partitioner = True
            self._key_index = LRUCache(limit=4096)
        except Exception as ex:
            self.logger.error(f"Error configuring aerospike client {ex}")
            raise ex
        super().__init__(url, app, table, **kwargs)

    @staticmethod
    def get_aerospike_client(aerospike_config: Dict[Any, Any]) -> Client:
        global aerospike_client
        if aerospike_client:
            return aerospike_client
        else:
            client = aerospike.client(
                aerospike_config.get(AeroSpikeStore.CLIENT_OPTIONS_KEY)
            )
            try:
                client.connect(
                    aerospike_config.get(AeroSpikeStore.USERNAME_KEY),
                    aerospike_config.get(AeroSpikeStore.PASSWORD_KEY),
                )
                aerospike_client = client
                return client
            except Exception as e:
                raise e

    def _get(self, key: bytes) -> Optional[bytes]:
        aerospike_key = (self.namespace, self.table_name, key)
        try:
            (aerospike_key, meta, bins) = self.client.get(key=aerospike_key)
            gen = meta.get(self.GENERATION_KEY, 0)
            self._key_index[key] = gen
            if bins:
                return bins[self.BIN_KEY]
            return None
        except aerospike.exception.RecordNotFound as ex:
            self.log.debug(f"key not found {key} exception {ex}")
            raise KeyError(f"key not found {key}")
        except Exception as ex:
            self.log.error(
                f"Error in set for table {self.table_name} exception {ex} key {key}"
            )
            if self.app.conf.crash_app_on_aerospike_exception:
                self.app._crash(
                    ex
                )  # crash the app to prevent the offset from progressing
            raise ex

    def _set(self, key: bytes, value: Optional[bytes]) -> None:
        try:
            aerospike_key = (self.namespace, self.table_name, key)
            vt = {self.BIN_KEY: value}
            gen = self._key_index.get(key, None)
            write_policy = self.policies.get("write", None)
            if not gen and write_policy and write_policy.get("gen", None) == 1:
                (aerospike_key, meta) = self.client.exists(key=aerospike_key)
                if meta:
                    gen = meta.get(self.GENERATION_KEY, 0)
                else:
                    gen = 0
            self.client.put(
                key=aerospike_key,
                bins=vt,
                meta={"ttl": self.ttl, self.GENERATION_KEY: gen},
                policy={
                    "exists": aerospike.POLICY_EXISTS_IGNORE,
                    "key": aerospike.POLICY_KEY_SEND,
                },
            )
            self._key_index.pop(key, None)
        except aerospike.exception.RecordGenerationError as ex:
            self.log.warning(
                f"RecordGenerationError key {key} exception {ex} generation {gen}"
            )
            raise ex
        except Exception as ex:
            self.log.error(
                f"Error in set for table {self.table_name} exception {ex} key {key}"
            )
            if self.app.conf.crash_app_on_aerospike_exception:
                self.app._crash(
                    ex
                )  # crash the app to prevent the offset from progressing
            raise ex

    def _del(self, key: bytes) -> None:
        try:
            aerospike_key = (self.namespace, self.table_name, key)
            self.client.remove(key=aerospike_key)
            self._key_index.pop(key, None)
        except aerospike.exception.RecordNotFound as ex:
            self.log.warning(
                f"Error in delete for table {self.table_name} exception {ex} key {key}"
            )
        except Exception as ex:
            self.log.error(
                f"Error in delete for table {self.table_name} exception {ex} key {key}"
            )
            if self.app.conf.crash_app_on_aerospike_exception:
                self.app._crash(
                    ex
                )  # crash the app to prevent the offset from progressing
            raise ex

    def _iterkeys(self) -> Iterator[bytes]:
        try:
            scan: aerospike.Scan = self.client.scan(
                namespace=self.namespace, set=self.table_name
            )
            for result in scan.results():
                yield result[0][2]
        except Exception as ex:
            self.log.error(
                f"Error in _iterkeys for table {self.table_name} exception {ex}"
            )
            if self.app.conf.crash_app_on_aerospike_exception:
                self.app._crash(
                    ex
                )  # crash the app to prevent the offset from progressing
            raise ex

    def _itervalues(self) -> Iterator[bytes]:
        try:
            scan: aerospike.Scan = self.client.scan(
                namespace=self.namespace, set=self.table_name
            )
            for result in scan.results():
                (key, meta, bins) = result
                if bins:
                    yield bins[self.BIN_KEY]
                else:
                    yield None
        except Exception as ex:
            self.log.error(
                f"Error in _itervalues for table {self.table_name} exception {ex}"
            )
            if self.app.conf.crash_app_on_aerospike_exception:
                self.app._crash(
                    ex
                )  # crash the app to prevent the offset from progressing
            raise ex

    def _iteritems(self) -> Iterator[Tuple[bytes, bytes]]:
        try:

            scan: aerospike.Scan = self.client.scan(
                namespace=self.namespace, set=self.table_name
            )
            for result in scan.results():
                (key_data, meta, bins) = result
                (ns, set, policy, key) = key_data

                if bins:
                    bins = bins[self.BIN_KEY]
                yield key, bins
        except Exception as ex:
            self.log.error(
                f"Error in _iteritems for table {self.table_name} exception {ex}"
            )
            if self.app.conf.crash_app_on_aerospike_exception:
                self.app._crash(
                    ex
                )  # crash the app to prevent the offset from progressing
            raise ex

    def _size(self) -> int:
        return 0

    def _contains(self, key: bytes) -> bool:
        try:
            if self.app.conf.store_check_exists:
                aerospike_key = (self.namespace, self.table_name, key)
                (aerospike_key, meta) = self.client.exists(key=aerospike_key)
                if meta:
                    gen = meta.get(self.GENERATION_KEY, 0)
                    self._key_index[key] = gen
                    return True
                else:
                    return False
            else:
                return True
        except Exception as ex:
            self.log.error(
                f"Error in _contains for table {self.table_name} exception "
                f"{ex} key {key}"
            )
            if self.app.conf.crash_app_on_aerospike_exception:
                self.app._crash(
                    ex
                )  # crash the app to prevent the offset from progressing
            raise ex

    def _clear(self) -> None:
        pass

    def reset_state(self) -> None:
        pass

    def persisted_offset(self, tp: TP) -> Optional[int]:
        """Return the persisted offset.

        This always returns :const:`None` when using the aerospike store.
        """
        return None
