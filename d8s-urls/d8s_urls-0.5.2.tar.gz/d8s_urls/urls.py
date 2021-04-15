import functools
import re
import urllib.parse as urlparse
from typing import Optional, List, Dict

import requests

# TODO: write functions to return a URL's:
# - username
# - password
# - port


def url_scheme(url: str) -> str:
    """Return the scheme of the url."""
    parsed_url = urlparse.urlparse(url)
    return parsed_url.scheme


def url_fragment(url: str) -> str:
    """Return the fragment of the url."""
    parsed_url = urlparse.urlparse(url)
    return parsed_url.fragment


def url_examples(n: int = 10) -> List[str]:
    """Create n URLs."""
    from hypothesis.provisional import urls
    from d8s_hypothesis import hypothesis_get_strategy_results

    return hypothesis_get_strategy_results(urls, n=n)


def urls_find(text: str, *, domain_name: str = '', **kwargs) -> List[str]:
    """Parse URLs from the given text. If a domain name is given, only urls with the given domain name will be returned."""
    from ioc_finder import ioc_finder

    urls = ioc_finder.parse_urls(text, **kwargs)
    yield from urls


def url_canonical_form(url: str) -> str:
    """Get the canonical url."""
    import werkzeug

    return werkzeug.urls.url_fix(url)


def url_scheme_remove(url: str):
    """Remove the scheme from the given URL."""
    from d8s_strings import string_remove_before, string_remove_from_start

    url_sans_scheme = string_remove_before(url, '://')
    return string_remove_from_start(url_sans_scheme, '://')


def url_query_strings_remove(url: str) -> str:
    """Return the URL without any query strings."""
    parsed_url = urlparse.urlparse(url)
    new_url = '{}://{}{}{}'.format(parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params)
    if parsed_url.fragment:
        new_url = '{}#{}'.format(new_url, parsed_url.fragment)
    return new_url


def url_query_strings(url: str) -> Dict[str, List[str]]:
    """Return all of the query strings in the url."""
    return urlparse.parse_qs(urlparse.urlparse(url).query)


def url_query_string(url: str, query_string: str) -> List[str]:
    """Return the value of the given query string in the given url."""
    query_strings = url_query_strings(url)
    matching_query_string = query_strings.get(query_string, [])
    return matching_query_string


def url_query_string_add(url: str, query_string_field: str, query_string_value: str) -> str:
    existing_query_strings = url_query_strings(url)
    new_query_string = urlparse.urlencode({query_string_field: query_string_value})

    if not existing_query_strings:
        return '{}?{}'.format(url, new_query_string)
    else:
        return '{}&{}'.format(url, new_query_string)


def url_query_string_remove(url: str, query_string_field_to_remove: str) -> str:
    """Remove the query string at the given field."""
    existing_query_strings = url_query_strings(url)
    base_url = url_query_strings_remove(url)

    # TODO: there may be an easier/more efficient way to do this
    # add all of the query strings from the original url that do not match the given field
    for query_string_field in existing_query_strings:
        if query_string_field != query_string_field_to_remove:
            for query_string_value in existing_query_strings[query_string_field]:
                base_url = url_query_string_add(base_url, query_string_field, query_string_value)

    return base_url


def url_query_string_replace(url: str, query_string_field: str, query_string_value: str) -> str:
    existing_query_strings = url_query_strings(url)

    if query_string_field in existing_query_strings:
        url = url_query_string_remove(url, query_string_field)
        return url_query_string_add(url, query_string_field, query_string_value)
    else:
        return url_query_string_add(url, query_string_field, query_string_value)


def url_path(url: str) -> str:
    """Return the path of the url."""
    return urlparse.urlparse(url).path


def url_path_segments(url: str) -> List[str]:
    """Return all of the segments of the url path."""
    from d8s_strings import string_split_without_empty

    return string_split_without_empty(url_path(url), '/')


def url_fragments_remove(url: str) -> str:
    """Return the URL without any fragments."""
    return urlparse.urldefrag(url).url


# TODO: write a function for `url_as_punycode` and `url_as_unicode`


# TODO: can this be genericized to work with file names as well? - or can the file_name function from the files module be used here?
def url_file_name(url: str) -> str:
    """Get the file name of the URL."""
    return url.split('/')[-1]


def url_domain(url: str) -> str:
    """Return the domain of the given URL."""
    if is_url(url):
        o = urlparse.urlparse(url)
        return o.netloc
    else:
        return url


def get_first_arg_url_domain(func):
    """If the first argument is a url, get the domain of the url and pass that into the function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        domain_arg = args[0]
        other_args = args[1:]

        if is_url(domain_arg):
            domain_arg = url_domain(domain_arg)

        return func(domain_arg, *other_args, **kwargs)

    return wrapper


def url_domain_second_level_name(url: str) -> str:
    """Find the second level domain name for the URL (e.g. 'http://example.com/test/bingo' => 'example') (see https://en.wikipedia.org/wiki/Domain_name#Second-level_and_lower_level_domains)."""
    from d8s_domains import domain_second_level_name

    if is_url(url):
        o = urlparse.urlparse(url)
        return domain_second_level_name(o.netloc)
    else:
        return domain_second_level_name(url)


# TODO: expand the types accepted for the first argument of this function
def url_join(url: str, path: str):
    """Join the URL to the URL path."""
    # the block below makes sure that, if the last section of the url's path does not appear to be a file, the url ends in a '/' so that the last section of the url path is not replaced. IMO, python's normal implementation of urlparse.urljoin can be unexpected when a URL does not end in a '/'. I would expect url_join('https://foo.com/test', 'bingo.php') to return 'https://foo.com/test/bingo.php', but python's default implementation of url_join would produce 'https://foo.com/bingo.php'.
    url_path_of_url = url_path(url)
    url_path_of_url_last_section = url_path_of_url.split('/')[-1]
    if '.' not in url_path_of_url_last_section:
        url = url + '/'

    return urlparse.urljoin(url, path)


def is_url(possible_url: str) -> bool:
    """Check if the given string is a URL."""
    try:
        o = urlparse.urlparse(possible_url)
    except Exception:
        # if there is a problem reading the possible_url, assume it is not a url
        return False
    else:
        if o.scheme == '' or o.netloc == '':
            return False
        else:
            return True


def url_screenshot(url: str, output_file_path: str = '') -> bytes:
    """."""
    from d8s_networking import get
    from d8s_file_system import file_write

    screenshot_api_url = 'https://render-tron.appspot.com/screenshot/{}?width=1920&height=1099'.format(url)

    result = get(screenshot_api_url, process_response_as_bytes=True)

    # try again - result will be a requests.Response if the request fails
    if isinstance(result, requests.Response):
        result = get(screenshot_api_url, process_response_as_bytes=True)

    # TODO: I would like to remove this feature from this function
    if output_file_path:
        file_write(output_file_path, result)

    return result


def url_as_punycode(url: str) -> str:
    """Convert the domain name of the URL to Punycode."""
    from d8s_domains import domain_as_punycode

    domain = url_domain(url)
    return url.replace(domain, domain_as_punycode(domain), 1)


def url_as_unicode(url: str) -> str:
    """Convert the domain name of the URL to Unicode."""
    from d8s_domains import domain_as_unicode

    domain = url_domain(url)
    return url.replace(domain, domain_as_unicode(domain), 1)


def url_simple_form(url: str) -> str:
    """Return the URL without query strings or fragments."""
    new_url = url
    new_url = url_query_strings_remove(new_url)
    new_url = url_fragments_remove(new_url)
    return new_url


def url_schemes() -> List[str]:
    """Get the url schemes from https://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml."""
    from d8s_csv import csv_read_as_list
    from d8s_networking import get

    url_schemes = list(
        csv_read_as_list(get('https://www.iana.org/assignments/uri-schemes/uri-schemes-1.csv', process_response=True))
    )[1:]
    return [entry[0] for entry in url_schemes]


def url_from_google_redirect(url: str) -> Optional[str]:
    """Get the url from the google redirect."""
    import html

    new_url = None
    domain_name = url_domain(url)
    # I'm not sure if the second case will ever be true, but I put it in for good measure
    if domain_name == 'www.google.com' or domain_name == 'google.com':
        new_url = html.unescape(url)
        google_url_pattern = '.*?q=(http.*?)&'
        matches = re.findall(google_url_pattern, new_url)
        if matches and len(matches) == 1:
            new_url = urlparse.unquote(matches[0])
        else:
            google_url_pattern_2 = '.*?url=(http.*?)&'
            matches = re.findall(google_url_pattern_2, new_url)
            if len(matches) == 1:
                new_url = urlparse.unquote(matches[0])
            else:
                print('Unable to parse the redirection URL from {}'.format(new_url))
                new_url = None
    else:
        print(
            'The domain name ({}) for this URL ({}) was not detected as a google domain name. If this is incorrect, please raise an issue here: https://gitlab.com/fhightower/ioc-utility/.'.format(
                domain_name, url
            )
        )
        new_url = None
    return new_url


# TODO: what is the difference between urlparse.(un)quote_plus and urlparse.(un)quote ? I also need to update the comments in both url_encode and url_decode
def url_encode(url: str) -> str:
    """Encode the URL using percent encoding (see https://en.wikipedia.org/wiki/Percent-escape)."""
    # TODO: is there a difference between encoding a url path and a query string/parameter?
    return urlparse.quote_plus(url)


def url_decode(url: str) -> str:
    """Decode a percent encoded URL (see https://en.wikipedia.org/wiki/Percent-escape)."""
    return urlparse.unquote_plus(url)


def url_base_form(url: str) -> str:
    """Get the base URL without a path, query strings, or other junk."""
    parsed_url = urlparse.urlparse(url)
    return '{}://{}/'.format(parsed_url.scheme, parsed_url.netloc)


@get_first_arg_url_domain
def url_rank(url: str) -> int:
    """."""
    from d8s_domains import domain_rank

    return domain_rank(url)
