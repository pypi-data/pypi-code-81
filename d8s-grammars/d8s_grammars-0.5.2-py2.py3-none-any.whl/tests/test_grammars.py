from d8s_grammars import *
from d8s_grammars.grammars_temp_utils import list_flatten


def test_pyparsing_parse_result_get_token_dict_1():
    test_grammar = Word(nums)('number')
    s = '012'
    colors = test_grammar.searchString(s)
    results = pyparsing_parse_result_get_token_dict(colors[0])
    assert isinstance(results, dict)
    # todo: any system that requires the user to do something like the line below is fundamentally broken - there has to be an easier way...
    assert results['number'][0].tup[0] == '012'


def test_color_grammar():
    s = 'test #333 #4444 #55555 #666666 ing'
    results = list_flatten(rgb_color.searchString(s).asList())
    print("results {}".format(results))
    assert len(results) == 4
    assert '#333' in results
    assert '#4444' in results
    assert '#55555' in results
    assert '#666666' in results


def test_base64_find():
    s = """yte sequence of 8-bit-padded ASCII characters encoded in MIME's Base64 scheme as follows (newlines and whitespaces may be present anywhere but are to be ignored on decoding):

TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIGJ1dCBieSB0aGlz
IHNpbmd1bGFyIHBhc3Npb24gZnJvbSBvdGhlciBhbmltYWxzLCB3aGljaCBpcyBhIGx1c3Qgb2Yg
dGhlIG1pbmQsIHRoYXQgYnkgYSBwZXJzZXZlcmFuY2Ugb2YgZGVsaWdodCBpbiB0aGUgY29udGlu
dWVkIGFuZCBpbmRlZmF0aWdhYmxlIGdlbmVyYXRpb24gb2Yga25vd2xlZGdlLCBleGNlZWRzIHRo
ZSBzaG9ydCB2ZWhlbWVuY2Ugb2YgYW55IGNhcm5hbCBwbGVhc3VyZS4=
In the above quote, the encoded value of Man is TWFu. En"""
    results = list_flatten(base_64.searchString(s))
    assert len(results) == 5

    s = """yte sequence of 8-bit-padded ASCII characters encoded in MIME's Base64 scheme as follows (newlines and whitespaces may be present anywhere but are to be ignored on decoding):

TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIGJ1dCBieSB0aGlzIHNpbmd1bGFyIHBhc3Npb24gZnJvbSBvdGhlciBhbmltYWxzLCB3aGljaCBpcyBhIGx1c3Qgb2YgdGhlIG1pbmQsIHRoYXQgYnkgYSBwZXJzZXZlcmFuY2Ugb2YgZGVsaWdodCBpbiB0aGUgY29udGludWVkIGFuZCBpbmRlZmF0aWdhYmxlIGdlbmVyYXRpb24gb2Yga25vd2xlZGdlLCBleGNlZWRzIHRoZSBzaG9ydCB2ZWhlbWVuY2Ugb2YgYW55IGNhcm5hbCBwbGVhc3VyZS4= In the above quote, the encoded value of Man is TWFu. En"""
    results = list_flatten(base_64.searchString(s))
    assert len(results) == 1


def test_repeatedly_encoded_base_64_find():
    s = 'Vm0wd2VHUXhUWGROVldSWVYwZDRWRll3Wkc5WFZsbDNXa1JTV0ZKdGVEQmFWVll3VmpBeFdHVkdXbFpXZWxaeVZtMHhTMUl5VGtsaVJtUlhUVEZLVFZac1ZtRldNVnBXVFZWV2FHVnFRVGs9'
    results = repeatedly_encoded_base_64.searchString(s)
    print('results {}'.format(results))
    assert len(results) == 1


def test_hash_tag():
    s = """Climbing #mountains with #friendsinhighplaces"""
    results = list_flatten(hash_tag.searchString(s))
    assert len(results) == 2
    assert '#mountains' in results
    assert '#friendsinhighplaces' in results

    s = """Climbing #mountains with # friendsinhighplaces in#20 days"""
    results = list_flatten(hash_tag.searchString(s))
    assert len(results) == 1

    s = """Climbing #mountains."""
    results = list_flatten(hash_tag.searchString(s))
    assert len(results) == 1
    assert results[0] == '#mountains'

    s = """Climbing "#mountains"."""
    results = list_flatten(hash_tag.searchString(s))
    assert len(results) == 1
    assert results[0] == '#mountains'


def test_twitter_handle():
    s = """Contact me @foobar"""
    results = list_flatten(twitter_handle.searchString(s))
    assert len(results) == 1

    s = """See me foo@bar"""
    results = list_flatten(twitter_handle.searchString(s))
    assert len(results) == 0

    s = """See me @bar."""
    results = list_flatten(twitter_handle.searchString(s))
    assert len(results) == 1
    assert results[0] == '@bar'

    s = """See me "@bar"."""
    results = list_flatten(twitter_handle.searchString(s))
    assert len(results) == 1
    assert results[0] == '@bar'


def test_isbn_parsing():
    s = """test 978-1-4028-9462-6 978-0-306-40615-7"""
    results = list_flatten(isbn_13.searchString(s).asList())
    assert len(results) == 2
    assert '978-1-4028-9462-6' in results
    assert '978-0-306-40615-7' in results

    s = """test 1-4028-9462-7"""
    results = list_flatten(isbn_10.searchString(s).asList())
    assert len(results) == 1
    assert '1-4028-9462-7' in results

    s = """test 978-1-4028-9462-6 978-0-306-40615-7 1-4028-9462-7"""
    results = list_flatten(isbn.searchString(s).asList())
    assert len(results) == 3
    assert '978-1-4028-9462-6' in results
    assert '978-0-306-40615-7' in results
    assert '1-4028-9462-7' in results


def test_file_size_parsing_1():
    # s = "test 40.56 GB"
    # results = list_flatten(number.searchString(s).asList()) # assert len(results) == 1
    # assert results[0] == '40.56'
    # results = list_flatten(file_size_grammar.searchString(s).asList()) # assert len(results) == 1
    # assert results[0] == '40.56 GB'

    s = "test 40.56 bytes"
    results = list_flatten(file_size_grammar.searchString(s).asList())
    assert len(results) == 1
    assert results[0] == '40.56 bytes'

    s = "test 40.56bytes"
    results = list_flatten(file_size_grammar.searchString(s).asList())
    assert len(results) == 1
    assert results[0] == '40.56 bytes'

    s = "test 40.56 foo bytes"
    results = list_flatten(file_size_grammar.searchString(s).asList())
    assert len(results) == 0

    s = "test 40.56 ytes"
    results = list_flatten(file_size_grammar.searchString(s).asList())
    assert len(results) == 0


def test_file_size_parsing_2():
    s = "test 40.56GB"
    results = list_flatten(file_size_grammar.searchString(s).asList())
    assert len(results) == 1
    assert results[0] == '40.56 GB'

    s = "test 40.56 GB"
    results = list_flatten(file_size_grammar.searchString(s).asList())
    assert len(results) == 1
    assert results[0] == '40.56 GB'

    s = "test 40.56   GB"
    results = list_flatten(file_size_grammar.searchString(s).asList())
    assert len(results) == 1
    assert results[0] == '40.56 GB'

    s = "test 40.56 μB"
    results = list_flatten(file_size_grammar.searchString(s).asList())
    assert len(results) == 1
    assert results[0] == '40.56 μB'

    s = "test 40.56 QB"
    results = list_flatten(file_size_grammar.searchString(s).asList())
    assert len(results) == 0

    s = """“ANTIPUBLIC #1” (102.04 GB)
“AP MYR & ZABUGOR #2” (19.49 GB)
“Collection #1” (87.18 GB)
“Collection #2” (528.50 GB)
“Collection #3” (37.18 GB)
“Collection #4” (178.58 GB)
“Collection #5” (40.56 GB)"""
    results = list_flatten(file_size_grammar.searchString(s).asList())
    assert len(results) == 7


def test_twitter_api_token():
    s = '12-3023020310230202302a3020a320302302032023'
    results = list_flatten(twitter_api_token.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == '12-3023020310230202302a3020a320302302032023'

    s = '"12-3023020310230202302a3020a320302302032023"'
    results = list_flatten(twitter_api_token.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == '12-3023020310230202302a3020a320302302032023'


def test_facebook_api_token():
    s = 'EAACEdEose0cBA1'
    results = list_flatten(facebook_api_token.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'EAACEdEose0cBA1'

    s = '"EAACEdEose0cBAfoobar"'
    results = list_flatten(facebook_api_token.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'EAACEdEose0cBAfoobar'


def test_google_creds():
    s = 'AIzaEAACEdEose0cBA1-_test_d-asdf2212341'
    results = list_flatten(google_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'AIzaEAACEdEose0cBA1-_test_d-asdf2212341'

    s = '"AIzaEAACEdEose0cBA1-_test_d-asdf2212341"'
    results = list_flatten(google_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'AIzaEAACEdEose0cBA1-_test_d-asdf2212341'

    s = '0-AIzaEAACEdEpoiujkpoi423AIzaEAAC3.apps.googleusercontent.com'
    results = list_flatten(google_oauth_id.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == '0-AIzaEAACEdEpoiujkpoi423AIzaEAAC3.apps.googleusercontent.com'

    s = '"0-AIzaEAACEdEpoiujkpoi423AIzaEAAC3.apps.googleusercontent.com"'
    results = list_flatten(google_oauth_id.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == '0-AIzaEAACEdEpoiujkpoi423AIzaEAAC3.apps.googleusercontent.com'


def test_picatic_api_key():
    s = 'sk_live_aizaeaacedepoiujkpoi423aizaeaac3'
    results = list_flatten(picatic_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'sk_live_aizaeaacedepoiujkpoi423aizaeaac3'

    s = '"sk_live_aizaeaacedepoiujkpoi423aizaeaac3"'
    results = list_flatten(picatic_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'sk_live_aizaeaacedepoiujkpoi423aizaeaac3'


def test_stripe_api_key():
    s = 'sk_live_aizaeaacedepoiujkpoi423a'
    results = list_flatten(stripe_standard_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'sk_live_aizaeaacedepoiujkpoi423a'

    s = '"sk_live_aizaeaacedepoiujkpoi423a"'
    results = list_flatten(stripe_standard_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'sk_live_aizaeaacedepoiujkpoi423a'

    s = 'rk_live_aizaeaacedepoiujkpoi423a'
    results = list_flatten(stripe_restricted_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'rk_live_aizaeaacedepoiujkpoi423a'

    s = '"rk_live_aizaeaacedepoiujkpoi423a"'
    results = list_flatten(stripe_restricted_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'rk_live_aizaeaacedepoiujkpoi423a'


def test_square_creds():
    s = 'sq0atp-aizaeaacedepoiujkpoi42'
    results = list_flatten(square_access_token.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'sq0atp-aizaeaacedepoiujkpoi42'

    s = '"sq0atp-aizaeaacedepoiujkpoi42"'
    results = list_flatten(square_access_token.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'sq0atp-aizaeaacedepoiujkpoi42'

    s = 'sq0csp-aizaeaacedepoiujkpoi42aizaeaacedaizaeaacede'
    results = list_flatten(square_oauth_secret.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'sq0csp-aizaeaacedepoiujkpoi42aizaeaacedaizaeaacede'

    s = '"sq0csp-aizaeaacedepoiujkpoi42aizaeaacedaizaeaacede"'
    results = list_flatten(square_oauth_secret.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'sq0csp-aizaeaacedepoiujkpoi42aizaeaacedaizaeaacede'


def test_paypal_braintree_access_token():
    s = 'access_token$production$aizaeaacede12345$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    results = list_flatten(paypal_braintree_access_token.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'access_token$production$aizaeaacede12345$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    s = '"access_token$production$aizaeaacede12345$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"'
    results = list_flatten(paypal_braintree_access_token.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'access_token$production$aizaeaacede12345$aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'


def test_amazon_mws():
    s = 'amzn.mws.abcdef01-abcd-0123-def0-abcdef012345'
    results = list_flatten(amazon_mws_auth_token.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'amzn.mws.abcdef01-abcd-0123-def0-abcdef012345'

    s = '"amzn.mws.abcdef01-abcd-0123-def0-abcdef012345"'
    results = list_flatten(amazon_mws_auth_token.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'amzn.mws.abcdef01-abcd-0123-def0-abcdef012345'


def test_twilio():
    s = 'SKaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    results = list_flatten(twilio_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'SKaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    s = '"SKaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"'
    results = list_flatten(twilio_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'SKaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'


def test_mailgun():
    s = 'key-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    results = list_flatten(mailgun_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'key-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

    s = '"key-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"'
    results = list_flatten(mailgun_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'key-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'


def test_mailchimp():
    s = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-us0'
    results = list_flatten(mailchimp_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-us0'

    s = '"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-us91"'
    results = list_flatten(mailchimp_api_key.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-us91'


def test_iaas_amazon_aws():
    s = 'AKIAAAAAAAAAAAAAAAAA'
    results = list_flatten(iaas_amazon_aws_access_key_id.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'AKIAAAAAAAAAAAAAAAAA'

    s = '"AKIAAAAAAAAAAAAAAAAA"'
    results = list_flatten(iaas_amazon_aws_access_key_id.searchString(s).asList())
    print('results {}'.format(results))
    assert len(results) == 1
    assert results[0] == 'AKIAAAAAAAAAAAAAAAAA'


def test_ssn():
    s = '111-22-3333'
    results = list_flatten(social_security_number.searchString(s).asList())
    assert len(results) == 1
    assert results[0] == '111-22-3333'

    s = '012-34-5678 111-22-3333'
    results = list_flatten(social_security_number.searchString(s).asList())
    assert len(results) == 2
    assert '012-34-5678' in results
    assert '111-22-3333' in results
