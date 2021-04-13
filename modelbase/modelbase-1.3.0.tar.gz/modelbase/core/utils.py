"""Write me."""

# Standard Library
import inspect as inspect
import re as re
import subprocess

RE_LAMBDA_FUNC = re.compile(r".*(lambda)(.+?):(.*?)")
RE_LAMBDA_RATE_FUNC = re.compile(r".*(lambda)(.+?):(.*?),")
RE_LAMBDA_ALGEBRAIC_MODULE_FUNC = re.compile(r".*(lambda)(.+?):(.*[\(\[].+[\)\]]),")
RE_TO_SBML = re.compile(r"([^0-9_a-zA-Z])")
RE_FROM_SBML = re.compile(r"__(\d+)__")
SBML_DOT = "__SBML_DOT__"


def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    """Format warnings to only show the message."""
    return f"{category.__name__}: {message}\n"


##########################################################################
# Source code functions
##########################################################################


def get_function_source_code(function):
    """Get source code of a function.

    Parameters
    ----------
    function : callable

    Returns
    -------
    function_source_code : str
    """
    try:
        return inspect.getsource(function)[:-1]  # Remove line break
    except OSError:
        return function.__source__


def patch_lambda_function_name(function, name):
    """Add a name to a lambda function.

    Parameters
    ----------
    function : callable
    name : str
    """
    function_source = get_function_source_code(function)
    if "lambda" in function_source:
        function.__name__ = name


def get_formatted_function_source_code(function_name, function, function_type):
    """Get source code of a function and format it with black.

    Parameters
    ----------
    function_name : str
    function : callable
    function_type : {rate, module}
        Whether the function is a rate function or algebraic module. This
        is needed for regex asssignment

    Returns
    -------
    source_code : str
    """
    try:
        source = inspect.getsource(function)[:-1]  # Remove line break
    except OSError:
        source = function.__source__

    if "lambda" in source:
        if function_type == "rate":
            source = functionify_lambda(
                lambda_function_code=source,
                function_name=function_name,
                pattern=RE_LAMBDA_RATE_FUNC,
            )
        elif function_type == "module":
            source = functionify_lambda(
                lambda_function_code=source,
                function_name=function_name,
                pattern=RE_LAMBDA_ALGEBRAIC_MODULE_FUNC,
            )
        elif function_type == "function":
            source = functionify_lambda(
                lambda_function_code=source,
                function_name=function_name,
                pattern=RE_LAMBDA_FUNC,
            )
        else:
            raise ValueError("Can only handle rate or module functions")
    blacked_string = subprocess.run(["black", "-c", source], stdout=subprocess.PIPE)
    return blacked_string.stdout.decode("utf-8")[:-2]  # Removing new lines


def functionify_lambda(lambda_function_code, function_name, pattern):
    """Convert lambda function to a proper function.

    Parameters
    ----------
    lambda_function_code : str
    function_name : str

    Returns
    -------
    source_code : str
    """
    _, args, code = re.match(pattern=pattern, string=lambda_function_code).groups()
    return f"def {function_name}({args.strip()}):\n    return {code.strip()}"


##########################################################################
# SBML functions
##########################################################################


def escape_non_alphanumeric(re_sub):
    """Convert a non-alphanumeric charactor to a string representation of its ascii number.

    Parameters
    ----------
    re_sub : re.sub

    Returns
    -------
    escaped_character : str
    """
    return f"__{ord(re_sub.group(0))}__"


def ascii_to_character(re_sub):
    """Convert an escaped non-alphanumeric character.

    Parameters
    ----------
    re_sub : re.sub

    Returns
    -------
    character : str
    """
    return chr(int(re_sub.group(1)))


def convert_id_to_sbml(id_, prefix):
    """Add prefix if id startswith number.

    Parameters
    ----------
    id_ : str
    prefix : str

    Returns
    -------
    id_ : str
    """
    new_id = RE_TO_SBML.sub(escape_non_alphanumeric, id_).replace(".", SBML_DOT)
    if not new_id[0].isalpha():
        return f"{prefix}_{new_id}"
    return new_id


def convert_sbml_id(sbml_id, prefix):
    """Convert an model object id to sbml-compatible string.

    Adds a prefix if the id starts with a number.

    Parameters
    ----------
    sbml_id : str
    prefix : str
    """
    new_id = sbml_id.replace(SBML_DOT, ".")
    new_id = RE_FROM_SBML.sub(ascii_to_character, new_id)
    return new_id.lstrip(f"{prefix}_")
