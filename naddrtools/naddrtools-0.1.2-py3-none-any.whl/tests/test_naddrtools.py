# -*- coding: utf-8 -*-

"""Tests for naddrtools"""

import netaddr
import naddrtools as nat

test_list = ["100.25.13.11", "172.20.31.0/24", "172.20.30.1 - 172.20.30.254", "172.20.50.0-172.20.60.12"]

# Test creation of netaddr objects
def test_get_netaddr_object():
    assert type(nat.get_netaddr_object(test_list[0])) == netaddr.ip.IPAddress
    assert type(nat.get_netaddr_object(test_list[1])) == netaddr.ip.IPNetwork
    assert type(nat.get_netaddr_object(test_list[2])) == netaddr.ip.IPRange
    assert type(nat.get_netaddr_object(test_list[3])) == netaddr.ip.IPRange

# Test buff_range function
def test_buff_range():
    assert nat.buff_range(orig_range=nat.get_netaddr_object(test_list[2])) == netaddr.ip.IPRange('172.20.30.0', '172.20.30.255')

# Test build_ipset function
def test_build_ipset():
    assert nat.build_ipset(input_list=test_list, buff_network_ranges=False) == netaddr.IPSet(['100.25.13.11/32', '172.20.30.1/32', '172.20.30.2/31', '172.20.30.4/30', '172.20.30.8/29', '172.20.30.16/28', '172.20.30.32/27', '172.20.30.64/26', '172.20.30.128/26', '172.20.30.192/27', '172.20.30.224/28', '172.20.30.240/29', '172.20.30.248/30', '172.20.30.252/31', '172.20.30.254/32', '172.20.31.0/24', '172.20.50.0/23', '172.20.52.0/22', '172.20.56.0/22', '172.20.60.0/29', '172.20.60.8/30', '172.20.60.12/32'])
    assert nat.build_ipset(input_list=test_list, buff_network_ranges=True) == netaddr.IPSet(['100.25.13.11/32', '172.20.30.0/23', '172.20.50.0/23', '172.20.52.0/22', '172.20.56.0/22', '172.20.60.0/29', '172.20.60.8/30', '172.20.60.12/32'])

# Test convert IPSet to string list
def test_convert_to_string():
    ipset = nat.build_ipset(input_list=test_list, buff_network_ranges=True)
    assert nat.convert_ipset_to_ranges_as_string(ipset=ipset) == '100.25.13.11, 172.20.30.0 - 172.20.31.255, 172.20.50.0 - 172.20.60.12'

# Test IP search in list
def test_search_in_list():
    search_ip = '172.20.30.250'
    assert nat.ip_search_in_list(search_ip=search_ip, lookup_list=test_list) == netaddr.ip.IPRange('172.20.30.1', '172.20.30.254')