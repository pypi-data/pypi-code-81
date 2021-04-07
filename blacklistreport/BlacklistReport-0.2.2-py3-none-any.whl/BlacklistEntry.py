from typing import List, Union
from ipaddress import ip_address, IPv4Address, IPv6Address

from BlacklistReport.__threat_data import ThreatData


class BlacklistEntry:
    def __init__(self, src: str, dst: str, ports: List[int]):
        self.src = self.IpEntry(address=src, ports=[])
        self.__destinations: List = [self.IpEntry(address=dst, ports=ports)]

    def add_destination(self, dst: str, ports: List[int]):
        for entry in self.__destinations:
            if entry.ip == dst:
                return
        self.__destinations.append(self.IpEntry(address=dst, ports=ports))

    def to_dict(self):
        return dict(src=self.src.to_dict(), destinations=[d.to_dict() for d in self.destinations])

    @property
    def destinations(self):
        return self.__destinations.copy()

    class IpEntry:
        def __init__(self, address: str, ports: List[int]):
            try:
                self.__ip: Union[IPv4Address, IPv6Address] = ip_address(address=address)
            except ValueError:
                self.__ip = address
            finally:
                self.__ports = ports
                if type(self.__ip) in [IPv4Address, IPv6Address] and self.__ip.is_global:
                    self.__origin_country = ThreatData.fetch_country(address)
                    self.__opswat: str = ThreatData.fetch_OPSWAT_summary(address)
                    self.__talos: str = ThreatData.fetch_TALOS_summary(address)
                else:
                    self.__origin_country = 'Internal'
                    self.__opswat = None
                    self.__talos = None

        def to_dict(self) -> dict:
            return dict(ip=self.ip,
                        ports=self.ports,
                        origin_country=self.origin_country,
                        opswat=self.opswat,
                        talos=self.talos)

        @property
        def ip(self) -> str:
            return str(self.__ip)

        @property
        def ports(self) -> str:
            return ', '.join(list(set([str(port) for port in self.__ports])))

        @property
        def origin_country(self):
            return self.__origin_country or 'Unavailable'

        @property
        def opswat(self):
            return self.__opswat or 'Unavailable'

        @property
        def talos(self):
            return self.__talos or 'Unavailable'
