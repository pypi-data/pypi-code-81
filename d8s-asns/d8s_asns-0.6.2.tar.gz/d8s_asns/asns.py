"""Helpful functions for working with ASNs."""

import functools
import re
from typing import Dict, Iterable, List, Optional, Tuple

from d8s_csv import csv_read_as_dict, csv_read_as_list
from d8s_html import html_to_json
from d8s_networking import get

from .asns_temp_utils import enumerate_human_readable_range, stringify_first_arg


@stringify_first_arg
def asn_standardize(as_number: str) -> Optional[str]:
    """Standardize the ASN format."""
    numbers = re.findall('[0-9]{1,10}', as_number)
    if numbers:
        return 'ASN{}'.format(numbers[0])
    else:
        message = f'The given data ({as_number}) cannot be formatted as an ASN.'
        print(message)
        return None


def standardize_asn_decorator(func):
    """Standardize the first argument as an ASN."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg = args[0]
        other_args = args[1:]

        standardized_first_arg = asn_standardize(first_arg)
        return func(standardized_first_arg, *other_args, **kwargs)

    return wrapper


def _cidr_report_org_asn_format(as_number: str) -> str:
    """Return the as_number in the format required by cidr-report.org (e.g. "AS1234")."""
    return as_number.replace('N', '')


@standardize_asn_decorator
def asn_announced_prefixes(as_number: str) -> Iterable[str]:
    """."""
    as_number = _cidr_report_org_asn_format(as_number)

    url = f'https://www.cidr-report.org/cgi-bin/as-report/as-report?as={as_number}&view=2.0&v=4&filter=pass'
    html_repsponse = get(url, process_response=True)
    d = html_to_json(html_repsponse)
    prefix_data = d['html'][0]['body'][0]['pre'][0]['a']
    # the prefix_data variable looks like:
    # [{'_attributes': {'href': 'https://62.220.244.0.22.potaroo.net', 'class': ['black']}, '_value': '62.220.244.0/22'}, ...]  # noqa: E501

    for prefix in prefix_data:
        yield prefix['_value']


@standardize_asn_decorator
def asn_adjacent_asns(as_number: str) -> Iterable[str]:
    """."""
    as_number = _cidr_report_org_asn_format(as_number)

    url = f'https://www.cidr-report.org/cgi-bin/as-report?as={as_number}&view=2.0'
    html_repsponse = get(url, process_response=True)
    d = html_to_json(html_repsponse)
    adjacency_report = d['html'][0]['body'][0]['p'][1]['p'][0]['ul'][0]['p'][0]['pre'][0]
    # the adjacency_report variable looks like:
    # {'a': [{'_attributes': {'href': '/cgi-bin/as-report?as=AS6702&v=4&view=2.0'}, '_value': 'AS6702'}, {'_attributes': {'href': '/cgi-bin/as-report?as=AS3326&v=4&view=2.0'}, '_value': 'AS3326'}, {'_attributes': {'href': '/cgi-bin/as-report?as=AS1&v=4&view=2.0'}, '_value': 'AS1'}], '_values': ['48085 IDATACENTER, CZ\n\n  Adjacency:     3  Upstream:     2  Downstream:     1\n  Upstream Adjacent AS list', 'APEXNCC-AS Gagarina avenue, building 7, room 61, RU', 'DATAGROUP "Datagroup" PJSC, UA\n  Downstream Adjacent AS list', 'LVLT-1, US']}  # noqa: E501

    for link in adjacency_report['a']:
        yield link['_value']


# @standardize_asn_decorator
# def asn_whois(as_number: str) -> str:
#     from d8s_html import website_get_section_containing

#     as_number = _cidr_report_org_asn_format(as_number)

#     url = f'https://www.cidr-report.org/cgi-bin/as-report?as={as_number}&view=2.0'
#     whois_data = website_get_section_containing(url, 'whois: 399260')
#     return whois_data


def asns_find(text: str) -> Iterable[str]:
    """Parse ASNs from the given text."""
    from ioc_finder import ioc_finder

    yield from ioc_finder.parse_asns(text)


def asns() -> Iterable[Tuple[str, str]]:
    """Get a list of ASNs from http://bgp.potaroo.net/as1221/asnames.txt."""
    url = 'http://bgp.potaroo.net/as1221/asnames.txt'

    raw_data = get(url, process_response=True)
    raw_data = re.sub(r'\s(?:\s)+', '\t', raw_data)
    csv_asn_names = csv_read_as_list(raw_data, delimiter='\t')

    for data_point in csv_asn_names:
        asn = asn_standardize(data_point[0])
        asn_temp_name = data_point[1]
        yield asn, asn_temp_name


@standardize_asn_decorator
def asn_number(as_number: str) -> int:
    """Get the number value of the given ASN."""
    return int(as_number.lstrip('ASN'))


def asn_is_private(as_number: str) -> bool:
    """Check if the given ASN is private."""
    private_asn_numbers = asns_private_numbers()
    return asn_number(as_number) in private_asn_numbers


def asns_private_numbers() -> Iterable[int]:
    """Return the reserved (private) ASN numbers.

    Data is collected from:

    https://www.iana.org/assignments/iana-as-numbers-special-registry/iana-as-numbers-special-registry.xhtml

    This function only returns the private ASN numbers.
    The `asns_private_ranges` function returns more information about the private ASN ranges.
    """
    private_asn_data = asns_private_ranges()

    for private_asn_entry in private_asn_data:
        private_asn_numbers = private_asn_entry['AS Number']
        if '-' in private_asn_numbers:
            yield from enumerate_human_readable_range(private_asn_numbers)
        else:
            yield int(private_asn_numbers)


def asns_private_ranges() -> List[Dict[str, str]]:
    """Return the reserved (private) ASN ranges.

    Data is collected from:

    https://www.iana.org/assignments/iana-as-numbers-special-registry/iana-as-numbers-special-registry.xhtml
    """
    private_asns = csv_read_as_dict(
        get(
            'https://www.iana.org/assignments/iana-as-numbers-special-registry/special-purpose-as-numbers.csv',
            process_response=True,
        ),
    )
    return private_asns


@standardize_asn_decorator
def asn_name(as_number: str) -> Optional[str]:
    """Get the name of the given asn."""
    matching_name: Optional[str] = None
    all_asns = asns()

    for asn, name in all_asns:
        if asn == as_number:
            matching_name = name

    return matching_name
