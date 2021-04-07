import re

ENCODING_CHARACTER = "'"


def clean_query(query, sql_dialect) -> str:
    """

    :param query:
    :param sql_dialect:
    :return:
    """
    cleaned_query = strip_comments(query=query)
    cleaned_query = pad_comparisons(query=cleaned_query)
    cleaned_query = clean_spaces(query=cleaned_query)
    return cleaned_query.lower()


def pad_comparisons(query):
    import re
    cleaned_query = re.sub(
        '([\s\(][\d\w\.\_\{\}]*)(<=|>=|<>|==|!=|<|>|=|\|\||::|\+|-|/|\*|~)([\d\w\.\_\{\}]*[\)\s]*)', r' \1 \2 \3',
        query)
    return cleaned_query


def clean_spaces(query) -> str:
    """

    :param query:
    :return:
    """
    cleaned_query = re.sub('\s+', ' ', query)
    cleaned_query = re.sub('\(\s', '(', cleaned_query)
    cleaned_query = re.sub('\s\)', ')', cleaned_query)
    return cleaned_query.strip()


def strip_comments(query) -> str:
    """

    :param query:
    :return:
    """
    return re.sub('((\n)+(\s)*(--)(.+\n))|((\n)+(\s)*(\#)(.+\n))', ' ', query)


def wrap_variables(query, encoding_character='', wrap_character="'", encoded=False):
    """

    :param query:
    :param encoding_character:
    :param wrap_character:
    :param encoded:
    :param skip_characters:
    :param feature_name:
    :return:
    """
    if encoded and encoding_character:
        encoding_character = '\\' + encoding_character
    regex = '(' + encoding_character + '[\w\d\_]*\{\S+\}[\w\d\_]*' + encoding_character + ')'
    variables = set()
    query = re.sub(regex, r"{0}\1{0}".format(wrap_character), query)
    for match in re.findall('(' + wrap_character + '[\w\d\_]*\{\S+\}[\w\d\_]*' + wrap_character + ')', query):
        new_name = match
        variables.add(new_name)

    return query, variables


def unwrap_variables(query, encoding_character='', encoded=False, skip_characters=0):
    if encoded and encoding_character:
        encoding_character = '\\' + encoding_character
    regex = '(' + encoding_character + '[\w\d\_]*\{\S+\}[\w\d\_]*' + encoding_character + ')'
    for match in re.findall(regex, query):
        new_name = match
        new_string = new_name[skip_characters:len(new_name) - skip_characters]
        query = query.replace(
            match,
            new_string
        )
    return query


def prune_ast(json, parent=None):
    """ Recursive function to remove partial or nulled values from the AST

    :param json: json query AST
    :param parent: the parent key of the ast
    :return: cleaned query AST
    """
    pruned = type(json)()
    if isinstance(json, dict):
        for k, v in json.items():
            child = prune_ast(json=v, parent=k)
            if child:
                pruned[k] = child
        pruned = validate_tree(k=parent, json=pruned)
    elif isinstance(json, list):
        for v in json:
            child = prune_ast(json=v, parent=None)
            if child:
                pruned.append(child)
        pruned = validate_tree(k=parent, json=pruned)
    else:
        if json is not None:
            pruned = json
    return pruned


def validate_tree(k, json):
    """ Validates whether the query ast has the required number of values

    :param k: the query key
    :param json: the query AST
    :return: None if invalid and the query_ast if valid.
    """
    from camtono.parser.parse import min_keys
    if k is None or len(json) >= min_keys.get(k, 1):
        return json
    else:
        return None
