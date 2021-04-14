import re

exceptions = dict(git_lab='gitlab', _i_p='_ip', d_b_='db_', _c_i='_ci', _p_r_d='_prd', _t_r='_tr')


def handle_non_alphanum(c: str) -> str:
    """Function for replacing the non-alphanumeric chars in a string with '_'

    Args:
        c (str): the input string

    Returns:
        str: the processed string
    """
    if c.isalnum():
        return c
    else:
        return '_'


# noinspection SpellCheckingInspection
symbol_replacements = {
    ' * ': '_mul_',
    ' + ': '_add_',
    ' - ': '_sub_',
    ' / ': '_div_',
    ' % ': '_mod_',
    '.': 'p',
    ' || ': '_conc_',
    "'": '',
    "#": '',
    '[': '',
    ']': ''
}


def sql_str_to_name(x: str) -> str:
    """Convert a piece of SQL to a valid python variable name

    Args:
        x (str): input SQL string

    Returns:
        str: generated snake-case python name string
    """
    out = x
    for k, v in symbol_replacements.items():
        out = out.replace(k, v)
    return to_snake_case(''.join(handle_non_alphanum(c) for c in out))


def to_snake_case(camel_case_str: str) -> str:
    """Convert a camel case string to a snake case string

    Args:
        camel_case_str (str): input camel case string

    Returns:
        str: generated snake case string
    """
    a = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
    cleaned_str = "".join(camel_case_str.split())
    snake_case = a.sub(r'_\1', cleaned_str).lower()
    for k, v in exceptions.items():
        if k in snake_case:
            snake_case = snake_case.replace(k, v)

    return snake_case


def indent_str(s: str, n: int = 3):
    """Generate a string that's indented by some number of spaces.

    Args:
        s (str): the input string. Can be a multiline string (contains '\n').
        n (int): in number of spaces to indent. Defaults to 3.

    Returns:
        str: the indented version of the string.
    """
    indent = ' ' * n
    return "\n".join(map(lambda x: f"{indent}{x}", s.split('\n')))


def in_quotes(x: str) -> str:
    """Put quotes around a string.

    Args:
        x (str): the input string.

    Returns:
        str: the output string with quotes.
    """
    return f"'{x}'"


def prettify_tree(tree_string: str) -> str:
    """Joins up branches of a tree prinout with vertical lines if there's vertical whitespace between them.
    Used for visualising query expression trees.

    For example:
        └•

        └•
    becomes:
        ├•
        │
        └•

    Args:
        tree_string (str): input tree string that uses the └• connector chars

    Returns:
        str: prettified tree string with the aligned bits joined up.

    """
    lines = tree_string.split('\n')

    for i, line in enumerate(lines):
        loc = line.find('└')
        if loc < 0:
            continue

        j = i - 1
        while True:
            c = lines[j][loc]

            if c not in ['└', ' '] or j < 0:
                break

            above = list(lines[j])
            above[loc] = '│' if c == ' ' else '├'
            lines[j] = "".join(above)

            j -= 1

    return '\n'.join(lines)


def pretty_sql(sql_str: str) -> str:
    """Make a readable SQL string broken over lines.

    Args:
        sql_str (str): input SQL string

    Returns:
        str: readable SQL string.
    """
    key_words = [
        'from ', 'select ', 'where ',
        'limit ', 'order by ', 'group by ',
        'having ', 'union all ', ' union ', ' on ', 'left join ', 'inner join '
    ]
    for kw in key_words:
        sql_str = sql_str.replace(kw, '\n'+kw[:-1] + '\n  ')
    return sql_str


def handle_available_string(string: object, default: str = '[Not Available]') -> str:
    """If input is not a string or if it's an empty string, replace with a default.

    Args:
        string (object): object to check for an available string.
        default (str): string to replace it with in case input is not a valid string.

    Returns:
        str: the input string if valid, else the default string value.
    """
    if isinstance(string, str) and len(string) > 0:
        return string
    else:
        return default


connector = '└•'
