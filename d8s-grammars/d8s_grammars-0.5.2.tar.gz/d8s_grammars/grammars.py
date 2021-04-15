import sys

import pyparsing
from d8s_strings import string_entropy
from pyparsing import (
    CaselessLiteral,
    Combine,
    OneOrMore,
    Optional,
    Or,
    Regex,
    Word,
    WordEnd,
    WordStart,
    alphanums,
    alphas,
    hexnums,
    nums,
    printables,
)


def pyparsing_parse_result_get_token_dict(parse_result: pyparsing.ParseResults):
    """."""
    token_dict = parse_result._ParseResults__tokdict

    return token_dict


number = Combine(Word(nums) + Optional(Word(nums + ',')) + Optional(Word('.') + Word(nums)))

alphanum_word_start = WordStart(wordChars=alphanums)
alphanum_word_end = WordEnd(wordChars=alphanums)
alphanums_underscore = alphanums + '_'

# TODO: write auto-generated functions for these which will let users search a string for each grammar (?)

unicode_characters = ''.join(chr(c) for c in range(sys.maxunicode) if not chr(c).isspace())
unicode_printables = Word(unicode_characters)

rgb_color = Word('#', bodyChars=hexnums, min=4, max=7)

base_64 = Combine(Word(alphanums)).addCondition(
    lambda tokens: (string_entropy(tokens[0]) >= 4) and (string_entropy(tokens[0]) >= 5 or len(tokens[0]) > 20)
)
# see https://www.imperva.com/blog/the-catch-22-of-base64-attacker-dilemma-from-a-defender-point-of-view/
repeatedly_encoded_base_64 = alphanum_word_start + Combine('Vm' + base_64)

# TODO: not sure if there are other ways to declare a variable in javascript which could easily be found with a grammar - I could also find arguments to a given function
javascript_variables = 'var' + Word(printables)
# TODO: not sure if there is another way to declare a function
javascript_functions = 'function' + Word(printables.replace('(', '').replace(')', ''))

hash_tag = WordStart(wordChars=alphanums + '#') + Word('#', bodyChars=alphanums, min=2)
twitter_handle = WordStart(wordChars=alphanums + '@') + Word('@', bodyChars=alphanums_underscore, min=2)

isbn_13 = (
    alphanum_word_start
    + Word(nums + '-').addCondition(lambda tokens: len(tokens[0]) == 17 and tokens[0].count('-') == 4)
    + alphanum_word_end
)
isbn_10 = (
    alphanum_word_start
    + Word(nums + '-').addCondition(lambda tokens: len(tokens[0]) == 13 and tokens[0].count('-') == 3)
    + alphanum_word_end
)
isbn = Or([isbn_10, isbn_13])

metric_prefixes = Or(
    [
        Word('Y'),
        Word('Z'),
        Word('E'),
        Word('P'),
        Word('T'),
        Word('G'),
        Word('M'),
        Word('k'),
        Word('h'),
        Word('da'),
        Word('d'),
        Word('c'),
        Word('m'),
        Word('μ'),
        Word('n'),
        Word('p'),
        Word('f'),
        Word('a'),
        Word('z'),
        Word('y'),
    ]
)

file_size_grammar = (
    Combine(
        number + Or([Combine(metric_prefixes + Word('bB')), CaselessLiteral('bytes')]),
        adjacent=False,
        joinString=' ',
    )
    + alphanum_word_end
)

# these are taken/adapted from https://www.ndss-symposium.org/wp-content/uploads/2019/02/ndss2019_04B-3_Meli_paper.pdf
credential_regexes = {
    'twitter_api_token': '[1-9][0-9]+-[0-9a-zA-Z]{40}',
    'facebook_api_token': 'EAACEdEose0cBA[0-9A-Za-z]+',
    'google_api_key': r'AIza[0-9A-Za-z\-_]{35}',
    'google_oauth_id': '[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com',
    'picatic_api_key': 'sk_live_[0-9a-z]{32}',
    'stripe_standard_api_key': 'sk_live_[0-9a-zA-Z]{24}',
    'stripe_restricted_api_key': 'rk_live_[0-9a-zA-Z]{24}',
    'square_access_token': r'sq0atp-[0-9A-Za-z\-_]{22}',
    'square_oauth_secret': r'sq0csp-[0-9A-Za-z\-_]{43}',
    'paypal_braintree_access_token': 'access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}',
    'amazon_mws_auth_token': 'amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
    'twilio_api_key': 'SK[0-9a-fA-F]{32}',
    'mailgun_api_key': 'key-[0-9a-zA-Z]{32}',
    'mailchimp_api_key': '[0-9a-f]{32}-us[0-9]{1,2}',
    'iaas_amazon_aws_access_key_id': 'AKIA[0-9A-Z]{16}',
    'amazon_aws_client_secret': '[0-9a-zA-Z/+=]{40}',
    'amazon_mws_aws_client_id': 'AKIA[0-9A-Z]{16}',
    'auth_token_aws_secret_key': '[0-9a-zA-Z/+=]{40}',
    'google_oauth_secret': r'[0-9a-zA-Z\-_]{24}',
    'google_oauth_auth_code': r'4/[0-9A-Za-z\-_]+',
    'google_oauth_refresh_token': r'1/[0-9A-Za-z\-_]{43}|1/[0-9A-Za-z\-_]{64}',
    'google_oauth_access_token': r'ya29\.[0-9A-Za-z\-_]+',
    'google_api_key': r'AIza[0-9A-Za-z\-_]{35}',
    'twilio_api_secret': '[0-9a-zA-Z]{32}',
    'twitter_access_token_secret': '[0-9a-zA-Z]{45}',
}

for credential_name, credential_regex in credential_regexes.items():
    exec('{} = Combine(Regex("{}")) + alphanum_word_end'.format(credential_name, credential_regex.replace('"', '\\"')))

social_security_number = Combine(
    Word(nums, exact=3) + Word('-') + Word(nums, exact=2) + Word('-') + Word(nums, exact=4)
)

python_formatted_string_literal = Combine(Word('{') + Word(printables.replace('}', ''), min=1) + Word('}'))

zip_code = alphanum_word_start + Word(nums, exact=5) + alphanum_word_end

yara_rule_scopes_list = ('private', 'global')
yara_rule_scopes = OneOrMore(Or(yara_rule_scopes_list))
# yara rule names are alphanumeric with '_' and cannot start with a number
yara_rule_name = Word(alphas + '_', bodyChars=alphanums + '_')
# yara rule tags have the same stipulations as the yara rule names (alphanumeric with underscores (see: https://yara.readthedocs.io/en/latest/writingrules.html#rule-tags))
yara_rule_tags = OneOrMore(yara_rule_name)
yara_rule_prefix = (
    Optional(yara_rule_scopes)('yara_rule_scopes')
    + Word('rule')
    + yara_rule_name('yara_rule_name')
    + Optional(Word(':') + yara_rule_tags)
)
# for the rule body, find any printable character and make sure the last character is a '}' representing the end of the yara rule
rule_body = OneOrMore(
    Word(printables).addCondition(lambda tokens: tokens[0] != 'rule' and tokens[0] not in yara_rule_scopes_list)
).addCondition(lambda tokens: tokens[-1] == '}')
yara_rule = yara_rule_prefix + '{' + rule_body
