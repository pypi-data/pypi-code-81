import socket
import logging
import re
import itertools
from urllib.parse import urlparse
from typing import *
from .scpi_transport_base import ScpiTransportBase
from .scpi_resource import ScpiResource
from .scpi_exceptions import ScpiTransportException


class ScpiTcpIpTransport(ScpiTransportBase):
    DEFAULT_PORT: int = 5025

    _transport_class = 'ScpiTcpIpTransport'
    _transport_info = 'TCP/IP SCPI Transport'
    _transport_type = 'TCP/IP'

    _sock: Optional[socket.socket] = None

    @classmethod
    def discover(cls,
                 dnssd_services: List[str] = ('_scpi-raw._tcp.local.',),
                 dnssd_domains: List[str] = ('local',),
                 dnssd_names: List[str] = ('.*',),
                 dnssd_timeout: float = 0.5) -> List[ScpiResource]:
        from zeroconf import Zeroconf, ServiceListener, ServiceBrowser
        import time

        class Listener(ServiceListener):
            def __init__(self):
                self.services = {}

            def remove_service(self, zeroconf, zc_type, zc_name):
                self.services.pop(zc_name)

            def add_service(self, zeroconf, zc_type, zc_name):
                self.services.update({zc_name: zeroconf.get_service_info(zc_type, zc_name)})

            def update_service(self, zeroconf, zc_type, zc_name):
                self.services.update({zc_name: zeroconf.get_service_info(zc_type, zc_name)})

        # Generate fully qualified service names by permuting given services with given domains
        dnssd_services_fq = [f'{s}.{d}' + ('.' if not d.endswith('.') else '')
                             for s, d in itertools.product(dnssd_services, dnssd_domains)]

        # Find devices via zeroconf mDNS
        # TODO: Implement DNS-SD for non-.local domains
        listener = Listener()
        ServiceBrowser(Zeroconf(), dnssd_services_fq, listener=listener)

        # Wait for some time to get answers
        time.sleep(dnssd_timeout)

        # Patterns to check name against
        patterns = [re.compile(pattern) for pattern in dnssd_names]

        return [ScpiResource(transport=ScpiTcpIpTransport,
                             location=f'dnssd:{service.name}',
                             address=(service.parsed_addresses()[0], int(service.port)),
                             name=service.get_name(),
                             manufacturer=service.properties[b'Manufacturer'].decode(
                                 'utf-8') if b'Manufacturer' in service.properties else None,
                             model=service.properties[b'Model'].decode(
                                 'utf-8') if b'Model' in service.properties else None,
                             serialnum=service.properties[b'SerialNumber'].decode(
                                 'utf-8') if b'SerialNumber' in service.properties else None,
                             info=service
                             ) for service in listener.services.values()
                if any([pattern.fullmatch(service.get_name()) for pattern in patterns])]

    @classmethod
    def from_resource_name(cls, resource_name: str) -> Optional[ScpiResource]:
        m = re.match((
            r'^(?P<prefix>(?P<type>TCPIP)(?P<board>\d+)?)'
            r'::(?P<host_address>.+)'
            r'::(?P<port>([0-9]+))'
            r'(::(?P<suffix>SOCKET))?$'
        ), resource_name, re.IGNORECASE)

        if m is None:
            # Does not match the regex
            return None

        groupdict = m.groupdict()

        return ScpiResource(
            transport=ScpiTcpIpTransport,
            address=(groupdict["host_address"], int(groupdict["port"]))
        )

    @classmethod
    def to_resource_name(cls, resource: ScpiResource) -> str:
        address = resource.address
        return f'TCPIP::{address[0]}::{address[1]}::SOCKET'

    def __init__(self, address: str, timeout: float = 5, **kwargs):
        super().__init__(**kwargs)
        self._logger = logging.getLogger(__name__)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._sock.settimeout(timeout)
        self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # Get hostname and port
        if isinstance(address, tuple):
            # Convert from tuple to string first
            address = f'{address[0]}:{address[1]}'

        addr = urlparse('//' + address)
        if (addr.hostname is None):
            raise ScpiTransportException(f'{address} is not a valid hostname')

        try:
            # Try to connect
            self._sock.connect((addr.hostname,
                                addr.port if addr.port is not None else self.DEFAULT_PORT))

            # Make a file interface for easier handling
            self._io = self._sock.makefile('rwb', buffering=0)
            self._io.flush()
        except OSError as e:
            raise ScpiTransportException(e) from e

    def close(self) -> None:
        # Do regular closing
        super().close()

        # Close socket as well
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()
        self._sock = None
