import datetime

import pytest

from d8s_domains import (
    domain_as_punycode,
    domain_as_unicode,
    domain_certificate_peers,
    domain_dns,
    domain_examples,
    domain_is_member,
    domain_rank,
    domain_second_level_name,
    domain_subdomains,
    domain_tld,
    domain_whois,
    domains_find,
    is_domain,
    is_tld,
    tlds,
)


def test_domain_certificate_peers_docs_1():
    assert 'android.com' in domain_certificate_peers('google.com')
    # make sure that the domain name is parsed from a URL when a URL is given to the domain_certificate_peers function
    assert 'android.com' in domain_certificate_peers('https://google.com/')


def test_domain_examples_docs_1():
    assert len(domain_examples()) == 10
    assert len(domain_examples(n=101)) == 101


def test_domains_find_docs_1():
    s = '''foo.com
    bingo.co.uk
    BAR.COM'''
    domain_list = domains_find(s)
    assert len(domain_list) == 3
    assert 'foo.com' in domain_list
    assert 'bingo.co.uk' in domain_list
    assert 'bar.com' in domain_list


@pytest.mark.network
def test_domain_rank_docs_1():
    domain = 'example.com'
    assert domain_rank(domain) < 10000


@pytest.mark.network
def test_domain_rank_given_url():
    domain = 'https://example.com/test/bingo.php'
    assert domain_rank(domain) < 10000


@pytest.mark.network
def test_tlds_docs_1():
    assert len(tlds()) > 1500


def test_domain_as_punycode_docs_1():
    assert domain_as_punycode('☁.com') == 'xn--l3h.com'
    assert domain_as_punycode('ドメイン.テスト') == 'xn--eckwd4c7c.xn--zckzah'
    assert domain_as_punycode('http://例子.卷筒纸') == 'xn--fsqu00a.xn--3lr804guic'
    assert domain_as_punycode('example.com') == 'example.com'
    assert domain_as_punycode('Ἐν ἀρχῇ ἦν ὁ λόγος') == 'xn--    -emd6arkdyo6a6bye7519ciharniqk5f'


def test_domain_as_unicode_docs_1():
    assert domain_as_unicode('xn--l3h.com') == '☁.com'
    assert domain_as_unicode('https://xn--l3h.com/test/bingo.php') == '☁.com'


def test_domain_dns_docs_1():
    assert domain_dns('example.com') == '93.184.216.34'

def test_domain_is_member():
    assert domain_is_member('example.com', 'example.com') is True
    assert domain_is_member('example.com', 'google.com') is False
    assert domain_is_member('test.example.com', 'example.com') is True
    assert domain_is_member('example.com', 'test.example.com') is False
    assert domain_is_member('t.example.com', 'test.example.com') is False
    assert domain_is_member('test1.example.com', 'test.example.com') is False
    assert domain_is_member('example.com.notdomain.com', 'example.com') is False
    assert domain_is_member('test.example.com.notdomain.com', 'example.com') is False
    assert domain_is_member('1.test.example.com.notdomain.com', 'test.example.com') is False
    assert domain_is_member('test.example.com', 'test.example.com') is True
    assert domain_is_member('subdomain.test.example.com', 'test.example.com') is True
    assert domain_is_member('testexample.com', 'example.com') is False
    assert domain_is_member('test.testexample.com', 'example.com') is False
    assert domain_is_member('test.testexample.com', 'test.example.com') is False
    assert domain_is_member('example.com', 'testexample.com') is False
    assert domain_is_member('example.com', 'test.testexample.com') is False
    assert domain_is_member('test.example.com', 'test.testexample.com') is False
    assert domain_is_member('example.com', 'example.com.br') is False

def test_domain_second_level_name_docs_1():
    assert domain_second_level_name('http://example.com/test/bingo') == 'example'
    assert domain_second_level_name('example.com') == 'example'
    assert domain_second_level_name('forums.bbc.co.uk') == 'bbc'
    assert domain_second_level_name('http://www.worldbank.org.kg/') == 'worldbank'


def test_domain_subdomains_docs_1():
    assert domain_subdomains('https://foo.bar.example.com') == 'foo.bar'
    assert domain_subdomains('https://foo.bar.example.co.uk') == 'foo.bar'
    assert domain_subdomains('foo.bar.google.co.uk') == 'foo.bar'
    assert domain_subdomains('http://www.worldbank.org.kg/') == 'www'


def test_domain_tld_docs_1():
    assert domain_tld('google.com') == 'com'
    assert domain_tld('forums.bbc.co.uk') == 'co.uk'
    assert domain_tld('http://www.worldbank.org.kg/') == 'org.kg'


def test_domain_whois_docs_1():
    assert domain_whois('google.com') == {
        'name': 'google.com',
        'registrar': 'MarkMonitor Inc.',
        'creation_date': datetime.datetime(1997, 9, 15, 4, 0),
        'expiration_date': datetime.datetime(2028, 9, 14, 4, 0),
        'last_updated': None,
        'status': 'clientDeleteProhibited https://icann.org/epp#clientDeleteProhibited',
        'name_servers': {
            'ns2.google.com',
            'ns2.google.com\r',
            'ns1.google.com\r',
            'ns4.google.com',
            'ns3.google.com\r',
            'ns4.google.com\r',
            'ns3.google.com',
            'ns1.google.com',
        },
    }
    assert domain_whois('example.com') is None


def test_is_domain_docs_1():
    assert is_domain('example.com')
    assert is_domain('forums.bbc.co.uk')
    assert is_domain('foo.bar')
    assert not is_domain('foo')


def test_is_tld_docs_1():
    assert is_tld('com')
    assert is_tld('org')
    assert not is_tld('foobar')
    assert not is_tld('ocx')
    assert not is_tld('dotm')
    assert is_tld('.com')
