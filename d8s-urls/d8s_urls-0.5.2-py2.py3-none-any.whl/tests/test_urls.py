from d8s_urls import (
    url_examples,
    urls_find,
    url_canonical_form,
    url_scheme_remove,
    url_query_strings_remove,
    url_query_strings,
    url_query_string,
    url_query_string_add,
    url_query_string_remove,
    url_query_string_replace,
    url_path,
    url_path_segments,
    url_fragments_remove,
    url_file_name,
    url_domain,
    url_domain_second_level_name,
    url_join,
    is_url,
    url_as_punycode,
    url_as_unicode,
    url_simple_form,
    url_schemes,
    url_from_google_redirect,
    url_encode,
    url_decode,
    url_base_form,
    url_rank,
    url_screenshot,
    url_scheme,
    url_fragment,
)


def test_url_scheme_1():
    result = url_scheme('https://username:password@example.com:9000/test?a=1&b=2#hello')
    assert result == 'https'


def test_url_fragment_1():
    result = url_fragment('https://username:password@example.com:9000/test?a=1&b=2#hello')
    assert result == 'hello'


def test_is_url_docs_1():
    assert is_url('https://example.com/test/bingo.php') == True
    assert is_url('test') == False
    assert (
        is_url(
            'Lorem ipsum dolor sit amet, https://example.com/test consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,'
        )
        == False
    )
    assert is_url(True) == False


def test_url_as_punycode_docs_1():
    assert url_as_punycode('https://☁.com/test') == 'https://xn--l3h.com/test'
    assert url_as_punycode('https://☁.com/☁') == 'https://xn--l3h.com/☁'


def test_url_as_unicode_docs_1():
    assert url_as_unicode('https://xn--l3h.com/test') == 'https://☁.com/test'


def test_url_base_form_docs_1():
    assert url_base_form('https://example.com') == 'https://example.com/'
    assert url_base_form('https://example.com/projects/') == 'https://example.com/'
    assert url_base_form('https://example.com/projects?s=1') == 'https://example.com/'
    assert url_base_form('https://example.com/projects/s=1') == 'https://example.com/'
    assert url_base_form('https://example.com/projects/bingo%20') == 'https://example.com/'
    assert url_base_form('https://example.com/projects/a/b/c') == 'https://example.com/'
    assert url_base_form('https://example.com/projects#testing') == 'https://example.com/'
    assert url_base_form('https://example.com/projects/#testing') == 'https://example.com/'
    assert url_base_form('https://example.com/?test=bingo&q=t') == 'https://example.com/'
    assert url_base_form('https://example.com?test=bingo&q=t') == 'https://example.com/'


def test_url_canonical_form_docs_1():
    assert url_canonical_form('http://www.google.com/') == 'http://www.google.com/'
    assert url_canonical_form('http://www.google.com/blah/..') == 'http://www.google.com/blah/..'
    assert url_canonical_form('www.google.com/') == 'http://www.google.com/'
    assert url_canonical_form('www.google.com') == 'http://www.google.com/'
    assert url_canonical_form('http://www.evil.com/blah#frag') == 'http://www.evil.com/blah'
    assert url_canonical_form('http://www.GOOgle.com/') == 'http://www.google.com/'
    assert url_canonical_form('http://www.google.com.../') == 'http://www.google.com/'
    assert url_canonical_form('http://www.google.com/foo\tbar\rbaz\n2') == 'http://www.google.com/foobarbaz2'
    assert url_canonical_form('http://www.google.com/q?') == 'http://www.google.com/q?'
    assert url_canonical_form('http://www.google.com/q?r?') == 'http://www.google.com/q?r?'
    assert url_canonical_form('http://www.google.com/q?r?s') == 'http://www.google.com/q?r?s'
    assert url_canonical_form('http://evil.com/foo#bar#baz') == 'http://evil.com/foo'
    assert url_canonical_form('http://evil.com/foo;') == 'http://evil.com/foo;'
    assert url_canonical_form('http://evil.com/foo?bar;') == 'http://evil.com/foo?bar;'
    assert url_canonical_form('http://\x01\x80.com/') == 'http://%01%80.com/'
    assert url_canonical_form('http://notrailingslash.com') == 'http://notrailingslash.com/'
    assert url_canonical_form('http://www.gotaport.com:1234/') == 'http://www.gotaport.com/'
    assert url_canonical_form('  http://www.google.com/  ') == 'http://www.google.com/'
    assert url_canonical_form('http:// leadingspace.com/') == 'http://%20leadingspace.com/'
    assert url_canonical_form('http://%20leadingspace.com/') == 'http://%20leadingspace.com/'
    assert url_canonical_form('%20leadingspace.com/') == 'http://%20leadingspace.com/'
    assert url_canonical_form('https://www.securesite.com/') == 'https://www.securesite.com/'
    assert url_canonical_form('http://host.com/ab%23cd') == 'http://host.com/ab%23cd'
    assert url_canonical_form('http://host.com//twoslashes?more//slashes') == 'http://host.com/twoslashes?more//slashes'


def test_url_decode_docs_1():
    assert url_decode('%2F') == '/'


def test_url_domain_docs_1():
    assert url_domain('https://example.com/projects/') == 'example.com'
    assert url_domain('example.com') == 'example.com'


def test_url_domain_second_level_name_docs_1():
    assert url_domain_second_level_name('http://example.com/test/bingo') == 'example'
    assert url_domain_second_level_name('example.com') == 'example'


def test_url_encode_docs_1():
    assert url_encode('/') == '%2F'
    assert url_encode('/test/') == '%2Ftest%2F'
    assert url_encode('bingo test') == 'bingo+test'


# def test_url_examples_docs_1():
#     assert url_examples(n=Num) == 'fill'  # fill


def test_url_file_name_docs_1():
    assert url_file_name('https://foo.com/test/') == ''
    assert url_file_name('https://foo.com/test') == 'test'


def test_url_fragments_remove_docs_1():
    assert url_fragments_remove('https://example.com/projects/') == 'https://example.com/projects/'
    assert url_fragments_remove('https://example.com/projects?s=1') == 'https://example.com/projects?s=1'
    assert url_fragments_remove('https://example.com/projects/?s=1') == 'https://example.com/projects/?s=1'
    assert url_fragments_remove('https://example.com/projects/bingo%20') == 'https://example.com/projects/bingo%20'
    assert url_fragments_remove('https://example.com/projects/a/b/c') == 'https://example.com/projects/a/b/c'
    assert url_fragments_remove('https://example.com/projects#testing') == 'https://example.com/projects'
    assert url_fragments_remove('https://example.com/projects/#testing') == 'https://example.com/projects/'
    assert (
        url_fragments_remove('https://example.com/projects/?test=bingo&q=t#test')
        == 'https://example.com/projects/?test=bingo&q=t'
    )


def test_url_from_google_redirect_docs_1():
    assert (
        url_from_google_redirect(
            'https://www.google.com/url?q=https%3A%2F%2Fwebmail.helsingor.dk%2Fowa%2Fredir.aspx%3FC%3DiN3lskTD_4ItZaDxsLe0d-3yBMbVhDqMiHJd442Po8vbP4omOITVCA..%26URL%3Dhttp%253a%252f%252fwww.google.com%252furl%253fq%253dhttp%25253A%25252F%25252Fsitesumo.com%25252Fccff%25252Fmain.html%2526sa%253dD%2526sntz%253d1%2526usg%253dAFQjCNGLOdDHK3rXm0xfJjyoo_rAFB5y6g&amp;sa=D&amp;sntz=1&amp;usg=AFQjCNFyB3x8dfKsi2-Q21IzELCGEe_b3Q'
        )
        == 'https://webmail.helsingor.dk/owa/redir.aspx?C=iN3lskTD_4ItZaDxsLe0d-3yBMbVhDqMiHJd442Po8vbP4omOITVCA..&URL=http%3a%2f%2fwww.google.com%2furl%3fq%3dhttp%253A%252F%252Fsitesumo.com%252Fccff%252Fmain.html%26sa%3dD%26sntz%3d1%26usg%3dAFQjCNGLOdDHK3rXm0xfJjyoo_rAFB5y6g'
    )
    assert (
        url_from_google_redirect(
            'https://www.example.com/url?q=https%3A%2F%2Fwebmail.helsingor.dk%2Fowa%2Fredir.aspx%3FC%3DiN3lskTD_4ItZaDxsLe0d-3yBMbVhDqMiHJd442Po8vbP4omOITVCA..%26URL%3Dhttp%253a%252f%252fwww.google.com%252furl%253fq%253dhttp%25253A%25252F%25252Fsitesumo.com%25252Fccff%25252Fmain.html%2526sa%253dD%2526sntz%253d1%2526usg%253dAFQjCNGLOdDHK3rXm0xfJjyoo_rAFB5y6g&amp;sa=D&amp;sntz=1&amp;usg=AFQjCNFyB3x8dfKsi2-Q21IzELCGEe_b3Q'
        )
        == None
    )
    assert (
        url_from_google_redirect(
            'https://www.google.com/url?url=https%3A%2F%2Fwebmail.helsingor.dk%2Fowa%2Fredir.aspx%3FC%3DiN3lskTD_4ItZaDxsLe0d-3yBMbVhDqMiHJd442Po8vbP4omOITVCA..%26URL%3Dhttp%253a%252f%252fwww.google.com%252furl%253fq%253dhttp%25253A%25252F%25252Fsitesumo.com%25252Fccff%25252Fmain.html%2526sa%253dD%2526sntz%253d1%2526usg%253dAFQjCNGLOdDHK3rXm0xfJjyoo_rAFB5y6g&amp;sa=D&amp;sntz=1&amp;usg=AFQjCNFyB3x8dfKsi2-Q21IzELCGEe_b3Q'
        )
        == 'https://webmail.helsingor.dk/owa/redir.aspx?C=iN3lskTD_4ItZaDxsLe0d-3yBMbVhDqMiHJd442Po8vbP4omOITVCA..&URL=http%3a%2f%2fwww.google.com%2furl%3fq%3dhttp%253A%252F%252Fsitesumo.com%252Fccff%252Fmain.html%26sa%3dD%26sntz%3d1%26usg%3dAFQjCNGLOdDHK3rXm0xfJjyoo_rAFB5y6g'
    )


def test_url_join_docs_1():
    assert url_join('https://example.com/foo/', '/bar') == 'https://example.com/bar'
    assert url_join('https://example.com/foo', '/bar') == 'https://example.com/bar'
    assert url_join('https://example.com/foo.fun/', '/bar') == 'https://example.com/bar'
    assert url_join('https://example.com/foo.fun', '/bar') == 'https://example.com/bar'
    assert url_join('https://example.com/foo/', 'bar') == 'https://example.com/foo/bar'
    assert url_join('https://example.com/foo', 'bar') == 'https://example.com/foo/bar'
    assert url_join('https://example.com/foo.fun/', 'bar') == 'https://example.com/foo.fun/bar'
    assert url_join('https://example.com/foo.fun', 'bar') == 'https://example.com/bar'


def test_url_path_docs_1():
    assert url_path('https://api.ooni.io/api/v1/measurements?offset=100&limit=100') == '/api/v1/measurements'


def test_url_path_segments_docs_1():
    assert url_path_segments('https://api.ooni.io/api/v1/measurements?offset=100&limit=100') == [
        'api',
        'v1',
        'measurements',
    ]


def test_url_query_string_docs_1():
    assert url_query_string('https://example.com?a=b', 'a') == ['b']
    assert url_query_string('https://example.com?a=b', 'foo') == []


def test_url_query_string_add_docs_1():
    assert url_query_string_add('https://example.com/test/', 'a', 'b') == 'https://example.com/test/?a=b'
    assert url_query_string_add('https://example.com/test', 'a', 'b') == 'https://example.com/test?a=b'
    assert url_query_string_add('https://example.com/test/?c=d', 'a', 'b') == 'https://example.com/test/?c=d&a=b'
    assert (
        url_query_string_add('https://example.com/test/?bingo=test&foo=bar', 'a', 'b')
        == 'https://example.com/test/?bingo=test&foo=bar&a=b'
    )
    assert url_query_string_add('https://example.com/test/?a=b', 'a', 'b') == 'https://example.com/test/?a=b&a=b'
    assert url_query_string_add('https://example.com/test/', 'a', '{}') == 'https://example.com/test/?a=%7B%7D'


def test_url_query_string_remove_docs_1():
    assert url_query_string_remove('https://example.com/test/?a=b', 'a') == 'https://example.com/test/'
    assert url_query_string_remove('https://example.com/test?a=b', 'a') == 'https://example.com/test'
    assert url_query_string_remove('https://example.com/test/?c=d&a=b', 'a') == 'https://example.com/test/?c=d'
    assert (
        url_query_string_remove('https://example.com/test/?bingo=test&foo=bar&a=b', 'a')
        == 'https://example.com/test/?bingo=test&foo=bar'
    )


def test_url_query_string_replace_docs_1():
    assert url_query_string_replace('https://example.com/test/?a=b', 'a', 'c') == 'https://example.com/test/?a=c'
    assert url_query_string_replace('https://example.com/test?a=b', 'a', '1') == 'https://example.com/test?a=1'
    assert (
        url_query_string_replace('https://example.com/test/?c=d&a=b', 'a', 'foo')
        == 'https://example.com/test/?c=d&a=foo'
    )
    assert (
        url_query_string_replace('https://example.com/test/?bingo=test&foo=bar&a=b', 'a', '20')
        == 'https://example.com/test/?bingo=test&foo=bar&a=20'
    )
    assert (
        url_query_string_replace('https://example.com/test/?a=b', 'foo', 'bar')
        == 'https://example.com/test/?a=b&foo=bar'
    )


def test_url_query_strings_docs_1():
    assert url_query_strings('https://example.com/test/?a=b') == {'a': ['b']}
    assert url_query_strings('https://example.com/test/') == {}


def test_url_query_strings_remove_docs_1():
    assert url_query_strings_remove('https://example.com/projects/') == 'https://example.com/projects/'
    assert url_query_strings_remove('https://example.com/projects?s=1') == 'https://example.com/projects'
    assert url_query_strings_remove('https://example.com/projects/?s=1') == 'https://example.com/projects/'
    assert url_query_strings_remove('https://example.com/projects/bingo%20') == 'https://example.com/projects/bingo%20'
    assert url_query_strings_remove('https://example.com/projects/a/b/c') == 'https://example.com/projects/a/b/c'
    assert url_query_strings_remove('https://example.com/projects#testing') == 'https://example.com/projects#testing'
    assert url_query_strings_remove('https://example.com/projects/#testing') == 'https://example.com/projects/#testing'
    assert (
        url_query_strings_remove('https://example.com/projects/?test=bingo&q=t#test')
        == 'https://example.com/projects/#test'
    )


def test_url_rank_docs_1():
    assert url_rank('https://example.com') < 10000


def test_url_schemes_docs_1():
    schemes = url_schemes()
    assert len(schemes) >= 337
    assert isinstance(schemes, list)
    assert isinstance(schemes[0], str)


def test_url_simple_form_docs_1():
    assert url_simple_form('https://example.com/projects/') == 'https://example.com/projects/'
    assert url_simple_form('https://example.com/projects?s=1') == 'https://example.com/projects'
    assert url_simple_form('https://example.com/projects/?s=1') == 'https://example.com/projects/'
    assert url_simple_form('https://example.com/projects/bingo%20') == 'https://example.com/projects/bingo%20'
    assert url_simple_form('https://example.com/projects/a/b/c') == 'https://example.com/projects/a/b/c'
    assert url_simple_form('https://example.com/projects#testing') == 'https://example.com/projects'
    assert url_simple_form('https://example.com/projects/#testing') == 'https://example.com/projects/'
    assert url_simple_form('https://example.com/projects/?test=bingo&q=t#test') == 'https://example.com/projects/'


def test_urls_find_docs_1():
    s = 'foo bar https://example.com/testing ftp://test.example.com'
    url_list = list(urls_find(s))
    assert len(url_list) == 2
    assert 'https://example.com/testing' in url_list
    assert 'ftp://test.example.com' in url_list


def test_url_examples_docs_1():
    assert len(url_examples()) == 10
    assert len(url_examples(n=101)) == 101


def test_url_screenshot_docs_1():
    result = url_screenshot('https://example.com')
    assert isinstance(result, bytes)
