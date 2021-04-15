import pytest

from d8s_asns import asn_name  # asn_whois,
from d8s_asns import (
    asn_adjacent_asns,
    asn_announced_prefixes,
    asn_is_private,
    asn_number,
    asn_standardize,
    asns,
    asns_find,
    asns_private_numbers,
    asns_private_ranges,
    standardize_asn_decorator,
)
from d8s_asns.asns import _cidr_report_org_asn_format


def test__cidr_report_org_asn_format_docs_1():
    assert _cidr_report_org_asn_format('asn1234') == 'asn1234'


def test_asn_adjacent_asns_docs_1():
    assert tuple(asn_adjacent_asns('AS48085')) == ('AS6702', 'AS3326', 'AS1')


def test_asn_announced_prefixes_docs_1():
    assert tuple(asn_announced_prefixes('AS48085')) == ('91.210.36.0/22',)
    assert tuple(asn_announced_prefixes('AS29132')) == (
        '62.220.244.0/22',
        '185.213.224.0/22',
        '212.94.64.0/20',
        '212.94.80.0/23',
        '212.94.88.0/24',
        '212.94.89.0/24',
        '212.94.90.0/23',
        '212.94.92.0/22',
    )


def test_asn_is_private_docs_1():
    assert asn_is_private('0')
    assert asn_is_private('23456')
    assert asn_is_private(23456)
    assert asn_is_private('64496')
    assert asn_is_private('64500')
    assert asn_is_private('64511')
    assert asn_is_private('4294967295')
    assert asn_is_private('64496')
    assert asn_is_private('ASN64496')
    assert asn_is_private('ASN 64496')
    assert asn_is_private('AS64496')
    assert asn_is_private('AS 64496')

    assert not asn_is_private('AS 1234')


def test_asn_name_docs_1():
    assert asn_name('AS1') == 'LVLT-1, US'
    assert asn_name('ASN1') == 'LVLT-1, US'
    assert asn_name('AS 1') == 'LVLT-1, US'


def test_asn_number_docs_1():
    assert asn_number('64496') == 64496
    assert asn_number('ASN64496') == 64496
    assert asn_number('ASN 64496') == 64496
    assert asn_number('AS64496') == 64496
    assert asn_number('AS 64496') == 64496


def test_asn_standardize_docs_1():
    assert asn_standardize('1234') == 'ASN1234'
    assert asn_standardize('AS1234') == 'ASN1234'
    assert asn_standardize('AS 1234') == 'ASN1234'
    assert asn_standardize('ASN1234') == 'ASN1234'
    assert asn_standardize('ASN 1234') == 'ASN1234'
    assert asn_standardize('1234') == 'ASN1234'
    assert asn_standardize(1234) == 'ASN1234'
    assert asn_standardize('foo') is None


def test_asns_private_ranges_docs_1():
    assert tuple(asns_private_ranges()) == (
        {'AS Number': '0', 'Reason for Reservation': 'Reserved by [RFC7607]', 'Reference': '[RFC7607]'},
        {
            'AS Number': '112',
            'Reason for Reservation': 'Used by the AS112 project to sink misdirected DNS queries; see [RFC7534]',
            'Reference': '[RFC7534]',
        },
        {'AS Number': '23456', 'Reason for Reservation': 'AS_TRANS; reserved by [RFC6793]', 'Reference': '[RFC6793]'},
        {
            'AS Number': '64496-64511',
            'Reason for Reservation': 'For documentation and sample code; reserved by [RFC5398]',
            'Reference': '[RFC5398]',
        },
        {
            'AS Number': '64512-65534',
            'Reason for Reservation': 'For private use; reserved by [RFC6996]',
            'Reference': '[RFC6996]',
        },
        {'AS Number': '65535', 'Reason for Reservation': 'Reserved by [RFC7300]', 'Reference': '[RFC7300]'},
        {
            'AS Number': '65536-65551',
            'Reason for Reservation': 'For documentation and sample code; reserved by [RFC5398]',
            'Reference': '[RFC5398]',
        },
        {
            'AS Number': '4200000000-4294967294',
            'Reason for Reservation': 'For private use; reserved by [RFC6996]',
            'Reference': '[RFC6996]',
        },
        {'AS Number': '4294967295', 'Reason for Reservation': 'Reserved by [RFC7300]', 'Reference': '[RFC7300]'},
    )


# def test_asn_whois_docs_1():
#     results = asn_whois('AS209711')
#     print('results {}'.format(results))
#     assert results.startswith('whois: 399260')
#     assert results.endswith(')')
#     assert '% This query was served by the RIPE Database Query Service version ' in results
#     assert 'IANA has recorded AS209711 as orig' in results
#     assert 'organisation:   ORG-MBVT3-RIPE' in results

#     results = asn_whois('209711')
#     assert results.startswith('whois: 399260')
#     assert results.endswith(')')
#     assert '% This query was served by the RIPE Database Query Service version ' in results
#     assert 'IANA has recorded AS209711 as orig' in results
#     assert 'organisation:   ORG-MBVT3-RIPE' in results


def test_asns_find_docs_1():
    s = 'AS1234 AS 4321 ASN 5678'
    asn_list = list(asns_find(s))
    assert len(asn_list) == 3
    assert 'ASN1234' in asn_list
    assert 'ASN4321' in asn_list
    assert 'ASN5678' in asn_list


@pytest.mark.network
def test_asns_docs_1():
    data = asns()
    data_list = list(data)
    assert len(data_list) >= 62934
    assert isinstance(data_list[0], tuple)
    assert isinstance(data_list[0][0], str)


@pytest.mark.network
def test_asns_private_numbers_docs_1():
    private_numbers = asns_private_numbers()
    data_list = list(private_numbers)
    assert len(data_list) == 94968355
    assert isinstance(data_list[0], int)


@standardize_asn_decorator
def standardize_asn_decorator_test(a):
    """."""
    return a


def test_standardize_asn_decorator_1():
    assert standardize_asn_decorator_test('123') == 'ASN123'
    assert standardize_asn_decorator_test('123') == 'ASN123'
    assert standardize_asn_decorator_test(123) == 'ASN123'
