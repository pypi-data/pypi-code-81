import socket
import ssl
from typing import Any, Dict, List, Optional

import tldextract
from d8s_hypothesis import hypothesis_get_strategy_results
from d8s_networking import get
from hypothesis.provisional import domains
from ioc_finder import ioc_finder

from .domains_temp_utils import get_first_arg_url_domain


def is_domain(possible_domain: str) -> bool:
    """Check if the given string is a domain."""
    domains = domains_find(possible_domain)
    if len(domains) == 1 and domains[0] == possible_domain:
        return True

    return False


# TODO: this function will sometimes create/return duplicates... probably need to have some option to prevent duplicates
def domain_examples(n: int = 10) -> List[str]:
    """Create n domain names."""
    results = hypothesis_get_strategy_results(domains, n=n)

    return results


def domains_find(text: str, **kwargs: bool) -> List[str]:
    """Parse domain names from the given text."""
    return ioc_finder.parse_domain_names(text, **kwargs)


@get_first_arg_url_domain
def domain_dns(domain: str) -> str:
    """Get the DNS results for the given domain."""
    return socket.gethostbyname(domain)


@get_first_arg_url_domain
def domain_certificate_peers(domain: str) -> List[str]:
    """Return a list of all domains sharing a certificate with the given domain."""
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.socket(), server_hostname=domain)
    s.connect((domain, 443))
    cert = s.getpeercert()
    return [domain_name[1] for domain_name in cert['subjectAltName']]  # type: ignore


@get_first_arg_url_domain
def domain_whois(domain: str) -> Optional[Dict[str, Any]]:
    """."""
    import whois

    whois_data = whois.query(domain)
    if whois_data:
        return whois_data.__dict__
    else:
        return None


@get_first_arg_url_domain
def domain_subdomains(domain_name: str) -> str:
    """Get the subdomains for the given domain name."""
    return tldextract.extract(domain_name).subdomain


@get_first_arg_url_domain
def domain_second_level_name(domain_name: str) -> str:
    """Get the second level name for the given domain name (e.g. google from https://google.co.uk)."""
    return tldextract.extract(domain_name).domain


@get_first_arg_url_domain
def domain_tld(domain_name: str) -> str:
    """Get the top level domain for the given domain name."""
    return tldextract.extract(domain_name).suffix


@get_first_arg_url_domain
def domain_rank(domain_name: str) -> int:
    """."""
    onemillion_api_url = f'http://onemillion.hightower.space/onemillion/{domain_name}'
    return get(onemillion_api_url, process_response=True)


@get_first_arg_url_domain
def domain_is_member(domain_to_check: str, domain_base: str) -> bool:
    """Given two domains, check if the first domain is a member of the second domain.
    A member means it is either the domain itself, or a subdomain of the domain.
    """
    if domain_to_check == domain_base:
        return True

    name = domain_second_level_name(domain_to_check)
    tld = domain_tld(domain_to_check)

    if domain_tld(domain_base) == tld and domain_second_level_name(domain_base) == name:
        subdomain_str = domain_subdomains(domain_to_check)
        subdomains = subdomain_str.split('.')
        last_subdomain = subdomains[-1]

        base_subdomain_str = domain_subdomains(domain_base)
        base_subdomains = base_subdomain_str.split('.')
        base_last_subdomain = base_subdomains[-1]

        if not base_last_subdomain:
            return domain_to_check.endswith("." + domain_base)
        elif last_subdomain == base_last_subdomain:
            return True
    return False


@get_first_arg_url_domain
def domain_as_punycode(domain_name: str) -> str:
    """Convert the given domain name to Punycode (https://en.wikipedia.org/wiki/Punycode)."""
    return domain_name.encode('idna').decode('utf-8')


@get_first_arg_url_domain
def domain_as_unicode(domain_name: str) -> str:
    """Convert a given domain name to Unicode (https://en.wikipedia.org/wiki/Unicode)."""
    return domain_name.encode('utf-8').decode('idna')


# TODO: cache this data
def tlds() -> List[str]:
    """Get the top level domains from https://iana.org/."""
    top_level_domains = get('https://data.iana.org/TLD/tlds-alpha-by-domain.txt', process_response=True).split('\n')[
        1:-1
    ]
    return [tld.lower() for tld in top_level_domains]


def is_tld(possible_tld: str) -> bool:
    """Return whether or not the possible_tld is a valid tld."""
    # remove any periods from the beginning (in case someone provides the TLD like `.com` rather than just `com`)
    possible_tld = possible_tld.lstrip('.')

    valid_tlds = [tld.lower() for tld in tlds()]
    tld_is_valid = possible_tld.lower() in valid_tlds
    return tld_is_valid
