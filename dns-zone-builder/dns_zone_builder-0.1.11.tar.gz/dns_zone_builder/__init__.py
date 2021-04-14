#! /usr/bin/python3
#
# Copyright © 2020 Martin Ibert
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import abc
import datetime
import ipaddress
import re

class DnsZoneBuilderException(Exception):

    def __init__(self, message):
        self.__message = message

    def __str__(self):
        return self.__message

class DuplicateSoaException(DnsZoneBuilderException):
    def __init__(self):
        super().__init__("Duplicate SOA record") 

class DuplicatePtrException(DnsZoneBuilderException):
    def __init__(self, ip_address):
        super().__init__("Duplicate PTR record for %s" % ip_address) 

class NoSoaException(DnsZoneBuilderException):
    def __init__(self):
        super().__init__("No SOA record") 

class UnknownIpVersionException(DnsZoneBuilderException):
    def __init__(self):
        super().__init__("Unknown IP version") 

class MismatchedIpVersionException(DnsZoneBuilderException):
    def __init__(self):
        super().__init__("Mismatched IP version") 

class AbstractDnsZoneBuilder(abc.ABC):

    def __init__(self, origin, ttl=None):
        origin = origin.lower()
        if not origin.endswith("."):
            origin = origin + "."
        self.origin = origin
        self.__ttl = ttl
        self.resource_record = {}

    def __str__(self):

        last_domain = None

        def rr_to_string(domain, rr_type, ttl_values):
            nonlocal last_domain
            domain = self.canonical_domain(domain)
            if domain == last_domain:
                domain = ""
            else:
                last_domain = domain
            ttl = ttl_values[0]
            values = "\t".join([str(v) for v in ttl_values[1]])
            if ttl is not None:
                return "%s\t%d\tIN\t%s\t%s" % (domain, ttl, rr_type, values)
            else:
                return "%s\tIN\t%s\t%s" % (domain, rr_type, values)

        if self.origin not in self.resource_record or "SOA" not in self.resource_record[self.origin]:
            raise NoSoaException

        zone = ["$ORIGIN\t%s" % self.origin]
        if self.__ttl is not None:
            zone.append("$TTL %d" % self.__ttl)

        soa_ttl_values = self.resource_record[self.origin]["SOA"][0]
        zone.append(rr_to_string(self.origin, "SOA", soa_ttl_values))
        del self.resource_record[self.origin]["SOA"]

        for domain in sorted(self.resource_record.keys(), key=lambda domain: ".".join(reversed(domain.split(".")))):
            for rr_type in sorted(self.resource_record[domain]):
                for ttl_values in self.resource_record[domain][rr_type]:
                    zone.append(rr_to_string(domain, rr_type, ttl_values))
        return "\n".join(zone)

    @staticmethod
    def default_serial():
        now = datetime.datetime.utcnow()
        return (((now.year * 100 + now.month) * 100) + now.day) * 100 + now.hour * 4 + int(now.minute / 15)

    @staticmethod
    def escape_quote_str(s):
        s = s.replace('"', '\\"').replace(";", "\\;")
        if re.search("\\s", s):
            return '"%s"' % s
        else:
            return s

    def full_domain(self, domain):
        domain = domain.lower()
        if domain.endswith("."):
            return domain
        if domain == "@":
            return self.origin
        return ".".join((domain, self.origin))

    def canonical_domain(self, domain):
        full_domain = self.full_domain(domain)
        tail = ".%s" % self.origin
        if full_domain == self.origin:
            return "@"
        if full_domain.endswith(tail):
            return full_domain[:-len(tail)]
        return full_domain

    def has_rr_record(self, domain, rr_type):
        domain = self.full_domain(domain)
        return domain in self.resource_record and rr_type.upper() in self.resource_record[domain]

    def add_rr(self, domain, rr_type, values, ttl=None):
        domain = self.full_domain(domain.lower())
        rr_type = rr_type.upper()
        if isinstance(values, str) or not hasattr(values, "__iter__"):
            values = (values, )
        if domain not in self.resource_record:
            self.resource_record[domain] = {}
        if rr_type not in self.resource_record[domain]:
            self.resource_record[domain][rr_type] = []
        self.resource_record[domain][rr_type].append((ttl, values))

    def add_soa_rr(self, mname, rname_email, serial=None, refresh=None, retry=None, expire=None, ttl=None):
        if self.has_rr_record(self.origin, "SOA"):
            raise DuplicateSoaException
        (local, domain) = rname_email.split("@")
        rname = ".".join((local.replace(".", "\\."), domain, ""))
        if serial is None:
            serial = self.default_serial()
        if refresh is None:
            refresh = 86400
        if retry is None:
            retry = 7200
        if expire is None:
            expire = 3600000
        if ttl is None:
            ttl = 3600
        if retry >= refresh:
            retry = refresh - 1
        if expire <= refresh + retry:
            expire = refresh + retry + 1
        self.add_rr(self.origin, "SOA", (self.canonical_domain(mname), self.canonical_domain(rname), serial, refresh, retry, expire, ttl))

    def add_ns_rr(self, domain, ns_domain, ttl=None):
        self.add_rr(domain, "NS", self.canonical_domain(ns_domain), ttl)

    def add_txt_rr(self, domain, spf, ttl=None):
        self.add_rr(domain, "TXT", self.escape_quote_str(spf), ttl)


class DnsZoneBuilder(AbstractDnsZoneBuilder):

    def __init__(self, origin, ttl=None, reverse_origins=None):
        if reverse_origins is None:
            reverse_origins = []
        elif isinstance(reverse_origins, str) or not hasattr(reverse_origins, "__iter__"):
            reverse_origins = (reverse_origins,)
        self.reverse_zones = [ReverseDnsZoneBuilder(ro, ttl) for ro in reverse_origins]
        super().__init__(origin, ttl)

    def add_soa_rr(self, mname, rname_email, serial=None, refresh=None, retry=None, expire=None, ttl=None):
        super().add_soa_rr(mname, rname_email, serial, refresh, retry, expire, ttl)
        for rz in self.reverse_zones:
            rz.add_soa_rr(mname, rname_email, serial, refresh, retry, expire, ttl)

    def add_a_rr(self, domain, ipv4address, ttl=None, add_ptr=True):
        self.add_rr(domain, "A", str(ipaddress.IPv4Address(ipv4address)), ttl)
        if add_ptr:
            for rz in self.reverse_zones:
                if rz.network.version == 4 and rz.network.supernet_of(ipaddress.IPv4Network("%s/32" % ipv4address)):
                    rz.add_ptr_rr(ipv4address, self.full_domain(domain))

    def add_aaaa_rr(self, domain, ipv6address, ttl=None, add_ptr=True):
        self.add_rr(domain, "AAAA", str(ipaddress.IPv6Address(ipv6address)), ttl)
        if add_ptr:
            for rz in self.reverse_zones:
                if rz.network.version == 6 and rz.network.supernet_of(ipaddress.IPv6Network("%s/128" % ipv6address)):
                    rz.add_ptr_rr(ipv6address, self.full_domain(domain))

    def add_cname_rr(self, domain, aliased_domain, ttl=None):
        self.add_rr(domain, "CNAME", self.canonical_domain(aliased_domain), ttl)

    def add_hinfo_rr(self, domain, hardware, os, ttl=None):
        self.add_rr(domain, "HINFO", (self.escape_quote_str(hardware), self.escape_quote_str(os)), ttl)

    def add_mx_rr(self, domain, priority, mx_domain, ttl=None):
        self.add_rr(domain, "MX", (priority, self.canonical_domain(mx_domain)), ttl)

    def add_ns_rr(self, domain, ns_domain, ttl=None):
        super().add_ns_rr(domain, ns_domain, ttl)
        if self.canonical_domain(domain) == "@":
            for rz in self.reverse_zones:
                rz.add_ns_rr("@", self.full_domain(ns_domain), ttl)

    def add_spf_rr(self, domain, text, ttl=None):
        self.add_rr(domain, "SPF", self.escape_quote_str(text), ttl)

class ReverseDnsZoneBuilder(AbstractDnsZoneBuilder):

    def __init__(self, network, ttl=None):
        if not isinstance(network,(ipaddress.IPv4Network, ipaddress.IPv6Network)):
            self.network = ipaddress.ip_network(network)
        else:
            self.network = network
        reverse = self.network.network_address.reverse_pointer.split(".")
        if self.network.version == 4:
            start = int((32 - self.network.prefixlen) // 8)
        elif self.network.version == 6:
            start = (128 - self.network.prefixlen) // 4
        origin = ".".join(reverse[start:])
        super().__init__(origin, ttl)

    def add_ptr_rr(self, ip_address, absolute_domain, ttl=None):
        if not isinstance(ip_address, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            ip_address = ipaddress.ip_address(ip_address)
        if ip_address.version != self.network.version:
            raise MismatchedIpVersionException()
        domain = "%s." % ip_address.reverse_pointer
        if self.has_rr_record(domain, "PTR"):
            raise(DuplicatePtrException(str(ip_address)))
        if not absolute_domain.endswith("."):
            absolute_domain = "%s." % absolute_domain
        self.add_rr(domain, "PTR", (absolute_domain,), ttl)

if __name__ == "__main__":

    dzb = DnsZoneBuilder("example.net")
    dzb.add_soa_rr("dns.example.net.", "john.doe@example.net", 1337)
    print(dzb)

    dzb = DnsZoneBuilder("example.com", 3600, ("10.0.0.0/16", "fd00:feed:dead:beef::/64"))

    dzb.add_soa_rr("dns.example.com.", "john.doe@example.com", None, 900, 900, 900)
    dzb.add_ns_rr("@", "dns.example.com.")
    dzb.add_ns_rr("@", "dnssec.example.com.")
    dzb.add_spf_rr("@", "v=spf1 ip4:10.0.0.0/16 ip6:fd00:feed:dead:beef::/64 -all")
    dzb.add_txt_rr("@", "v=spf1 ip4:10.0.0.0/16 ip6:fd00:feed:dead:beef::/64 -all")
    dzb.add_a_rr("dns", "10.0.0.1")
    dzb.add_a_rr("dnssec", "10.0.0.2")
    dzb.add_aaaa_rr("dns", "fd00:feed:dead:beef::1")
    dzb.add_aaaa_rr("dnssec", "fd00:feed:dead:beef::2")
    dzb.add_mx_rr("@", 10, "mx")
    dzb.add_mx_rr("@", 20, "mx.example.net.")
    dzb.add_a_rr("srv", "10.0.1.1")
    dzb.add_aaaa_rr("srv", "fd00:feed:dead:beef::1:1")
    dzb.add_hinfo_rr("srv", "Generic PC", "Linux/Ubuntu")
    dzb.add_a_rr("host.dynamic", "192.168.13.37", 300)

    print(dzb)

    for rz in dzb.reverse_zones:
        print(rz)
