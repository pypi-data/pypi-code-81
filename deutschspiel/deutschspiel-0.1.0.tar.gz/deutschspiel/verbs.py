
def get_stam(verb):
    return verb[:-1] if verb[-2] != 'e' else verb[:-2]


def conjugate_regular(verb, rules, tense="present"):
    if rules.get(tense) is None:
        return
    rule = rules[tense]
    stam = get_stam(verb)
    end = rule["special"][stam[-1]] if rule["special"].get(stam[-1]) else rule["standard"]
    return {
        "1": stam+end[0], "2": stam+end[1], "3": stam+end[2],
        "4": verb if tense == "present" else stam+end[3]
    }


def conjugate_irregular(verb, data, tense="present"):
    if tense not in data.columns:
        return
    result = data[tense].loc[verb]
    return {i: j for i, j in result.iteritems()}


def conjug_prefix(verb, prefix=None, separable=None):
    if prefix is not None and separable is False:
        return (f"{prefix}{verb}")
    if prefix is not None and separable is True:
        return verb, prefix
    return (verb)


def partizip_prefix(verb, prefix=None, separable=None):
    stam = get_stam(verb)
    if prefix is not None and separable is True:
        return f'{prefix}ge'
    if prefix is not None and separable is False:
        return f'{prefix}'
    if stam[-3:] == 'ier':
        return ''
    return 'ge'


def conjug_partizip(verb, data=None, conjug_rules=None, irregular=False):
    if irregular:
        return data.loc[verb]
    return conjugate_regular(verb, conjug_rules)['3']


def build_partizip(verb, data=None, conjug_rules=None, prefix=None, separable=None, irregular=False):
    broke_verb = verb.strip(prefix)
    print(broke_verb)
    prefix = partizip_prefix(broke_verb, prefix, separable)
    conjug = conjug_partizip(broke_verb, data, conjug_rules, irregular)
    return f'{prefix}{conjug}'

