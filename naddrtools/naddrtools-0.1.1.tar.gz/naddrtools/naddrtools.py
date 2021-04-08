# -*- coding: utf-8 -*-

import netaddr

def buff_range(orig_range: netaddr.ip.IPRange) -> netaddr.ip.IPRange:
    """ Buffs a network range into a single CIDR network, if possible.

    Returns a 'buffed' network range, which has been extended by one IP address in both directions
    (assuming that the new network range is a valid single CIDR block). This is useful for 'repairing'
    a network which has had its network (first) and broadcast (last) addresses removed. If the range
    cannot be cleanly 'buffed' into a single CIDR network, the original range that was input will be returned.

    :param orig_range: The original IPRange object
    :return: The newly-created buffed IPRange object, if applicable (otherwise, the original IPRange object is returned)
    :rtype: netaddr.ip.IPRange
    """

    if type(orig_range) != netaddr.ip.IPRange:
        raise TypeError("The buff_range function expects to recieve a netaddr.ip.IPRange object as its input.")
    new_range = netaddr.ip.IPRange(orig_range[0] - 1, orig_range[-1] + 1)
    networks = new_range.cidrs()
    if len(networks) == 1:
        return new_range
    else:
        return orig_range

def build_ipset(input_list, buff_network_ranges=False):
    """ Constructs an IPSet object from a list of inputs

    :param input_list: The original list of strings and/or netaddr objects
    :param buff_network_ranges: A boolean decision about whether to 'buff' any network ranges in the list
    :return: A new IPSet object
    :rtype: netaddr.IPSet
    """

    ipset = netaddr.IPSet()

    # In case the lookup_list would be valid, but simply needs to be formatted as a list
    if type(input_list) != list:
        input_list = [input_list]

    for item in input_list:
        if type(item) == str:
            nao = get_netaddr_object(item)
        elif type(item) == netaddr.ip.IPRange or type(item) == netaddr.ip.IPNetwork or type(item) == netaddr.ip.IPAddress:
            nao = item
        if nao:
            if type(nao) == netaddr.ip.IPRange and buff_network_ranges == True:
                ipset.add(buff_range(nao))
            else:
                ipset.add(nao)
    return ipset

def convert_ipset_to_ranges_as_string(ipset):
    """ Creates a string 'list' of ip ranges from an IPSet object that is supplied

    Converts an IPSet into a single comma-separated string of IP ranges.
    Useful for creating input lists of values for input into the UI or API
    of network and security tools such as Rapid7.

    :param ipset: The IPSet object to use as the source of information
    :return: A string representation of the list of IP ranges contained in the set
    :rtype: str
    """

    ip_range_list = []
    for range in ipset.iter_ipranges():
        r_string = str(range)
        split = r_string.split("-")
        if split[0] == split[1]:
            ip_range_list.append(split[0])
        else:
            range_string = f"{split[0]} - {split[1]}"
            ip_range_list.append(range_string)
    range_list_string = ', '.join(ip_range_list)
    return range_list_string

def get_netaddr_object(nw_string=None, ignore_type_error=False):
    """ Returns the appropriate netaddr object when presented with a valid string

    Returns a netaddr object in response to a string input. It is capable of interpreting IP addresses, ranges, and CIDR networks.
    By default (if ignore_type_error==False) it will raise a TypeError if the input cannot be converted
    into a netaddr object. If ignore_type_error==True it will return None if a netaddr object cannot be created.

    :param nw_string: A string representation of an IP address, range, or CIDR network
    :param ignore_type_error: A boolean decision about whether to raise a TypeError or a None value
    :return: The appropriate netaddr object
    :rtype: netaddr.ip.IPAddress or netaddr.ip.IPNetwork or netaddr.ip.IPRange
    """

    # Clean up the string
    try:
        str = nw_string.strip()
    except:
        if ignore_type_error == False:
            raise TypeError("The get_netaddr_object function expects a string input.")
        else:
            na_object = None

    # First check if it's an IP range
    try:
        split = nw_string.split("-")
        na_object = netaddr.ip.IPRange(split[0].strip(), split[1].strip())
    except:
        # Next check if it's an IP address
        try:
            na_object = netaddr.ip.IPAddress(nw_string)
        except:
            # Next check if it's an IP CIDR network
            try:
                na_object = netaddr.ip.IPNetwork(nw_string)
            except:
                if ignore_type_error == False:
                    raise TypeError(f"{nw_string} is not a valid IP address, range, or network")
                else:
                    na_object = None
    return na_object

def ip_search_in_list(search_ip, lookup_list, ignore_type_error=False):
    """ Search for an IP in a list of network IPs, ranges, and CIDR networks

    Attempts to look up a single IP address in a list of IP addresses, ranges, and networks. The inputs
    can be either strings or netaddr objects.

    :param search_ip: The IP address to search for
    :param lookup_list: The list of IP addresses, ranges, and networks
    :param ignore_type_error: How to handle a TypeError
    :return: The netaddr object which matched the search IP (or None)
    :rtype: netaddr.ip.IPAddress or netaddr.ip.IPNetwork or netaddr.ip.IPRange or None
    """

    # In case the lookup_list is a None value (e.g., IP targets list data grabbed from R7 API is
    # sometimes a None value instead of being an empty list
    if lookup_list is None:
        return None

    if type(search_ip) != netaddr.ip.IPAddress:
        search_ip = get_netaddr_object(search_ip)
    if lookup_list:
        for entry in lookup_list:
            if type(entry) != netaddr.ip.IPNetwork and type(entry) != netaddr.ip.IPAddress and type(entry) != netaddr.ip.IPRange:
                if ignore_type_error == False:
                    entry = get_netaddr_object(entry)
                elif ignore_type_error == True:
                    entry = get_netaddr_object(entry, ignore_type_error=ignore_type_error)
            try:
                if search_ip in entry:
                    return entry
            except:
                if search_ip == entry:
                    return entry
    else:
        return None
