from deci_client.deci_api.client import DeciPlatformClient
from deci_client.rtic.client import DeciRTICClient


class DeciClient:
    def __init__(self,
                 rtic_host: str = 'localhost',
                 rtic_port: int = 8000,
                 grpc_port: int = 8001,
                 rtic_https: bool = False,
                 platform_host: str = 'api.deci.ai',
                 platform_port: int = 443,
                 platform_https: bool = True,
                 max_workers: int = None,
                 shared_tensor_provider=None):
        self._rtic_host = rtic_host,
        self._rtic_port = rtic_port,
        self._grpc_port = grpc_port,
        self._rtic_https = rtic_https,
        self._platform_https = platform_https,
        self._max_workers = max_workers,
        self._shared_tensor_provider = shared_tensor_provider
        self._platform_host = platform_host
        self._platform_port = platform_port
        self._platform_https = platform_https

        # Setting the clients
        self.__rtic_client: DeciRTICClient = DeciRTICClient(api_host=rtic_host, api_port=rtic_port,
                                                            grpc_port=grpc_port,
                                                            https=rtic_https,
                                                            max_workers=max_workers,
                                                            shared_tensor_provider=shared_tensor_provider)
        self.__platform_client: DeciPlatformClient = DeciPlatformClient(api_host=platform_host, api_port=platform_port,
                                                                        https=platform_https)

        # Immutability after initialization (singleton)
        DeciClient.__slots__ = []

    @property
    def rtic(self) -> DeciRTICClient:
        return self.__rtic_client

    @property
    def platform(self) -> DeciPlatformClient:
        return self.__platform_client
