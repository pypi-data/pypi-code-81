import json
import os
from enum import Enum
import pkg_resources
import sys
import platform
import shlex
import shutil
import re
from typing import Any, Dict, List, Optional
from certora_cli.certoraTester import compareResultsWithExpected, get_errors, has_violations, get_violations  # type: ignore


LEGAL_CERTORA_KEY_LENGTHS = [32, 40]

# bash colors
BASH_ORANGE_COLOR = "\033[33m"
BASH_END_COLOR = "\033[0m"
BASH_GREEN_COLOR = "\033[32m"
BASH_RED_COLOR = "\033[31m"

VERIFICATION_ERR_MSG_PREFIX = "Prover found violations:"
VERIFICATION_SUCCESS_MSG = "No errors found by Prover!"

DEFAULT_SOLC = "solc"
DEFAULT_CLOUD_ENV = 'production'
DEFAULT_STAGING_ENV = 'master'
OPTION_OUTPUT_VERIFY = "output_verify"
ENVVAR_CERTORA = "CERTORA"

CERTORA_CONFIG_DIR = ".certora_config"  # folder
CERTORA_BUILD_FILE = ".certora_build.json"
CERTORA_VERIFY_FILE = ".certora_verify.json"
PACKAGE_FILE = "package.json"


def get_version() -> str:
    """
    @return: The version of the Certora CLI's python package in format XX.YY if found, an error message otherwise
    """
    # Note: the only valid reason not to have an installed certora-cli package is in circleci
    try:
        version = pkg_resources.get_distribution("certora-cli").version
        return version
    except pkg_resources.DistributionNotFound:
        return "couldn't find certora-cli distributed package. Try\n pip install certora-cli"


def check_results_from_file(output_path: str) -> bool:
    with open(output_path) as output_file:
        actual = json.load(output_file)
        return check_results(actual)


def check_results(actual: Dict[str, Any]) -> bool:
    actual_results = actual
    expected_filename = "expected.json"
    based_on_expected = os.path.exists(expected_filename)
    if based_on_expected:  # compare actual results with expected
        with open(expected_filename) as expectedFile:
            expected = json.load(expectedFile)
            if "rules" in actual_results and "rules" in expected:
                is_equal = compareResultsWithExpected("test", actual_results["rules"], expected["rules"], {}, {})
            elif "rules" not in actual_results and "rules" not in expected:
                is_equal = True
            else:
                is_equal = False

        if is_equal:
            print_completion_message(f"{VERIFICATION_SUCCESS_MSG} (based on expected.json)")
            return True
        # not is_equal:
        error_str = get_errors()
        if error_str:
            print_error(VERIFICATION_ERR_MSG_PREFIX, error_str)
        if has_violations():
            print_error(VERIFICATION_ERR_MSG_PREFIX)
            get_violations()
        return False

    # if expected results are not defined
    # traverse results and look for violation
    errors = []
    result = True

    if "rules" not in actual_results:
        errors.append("No rules in results")
        result = False
    elif len(actual_results["rules"]) == 0:
        errors.append("No rule results found. Please make sure you wrote the rule and method names correctly.")
        result = False
    else:
        for rule in actual_results["rules"].keys():
            rule_result = actual_results["rules"][rule]
            if isinstance(rule_result, str) and rule_result != 'SUCCESS':
                errors.append("[rule] " + rule)
                result = False
            elif isinstance(rule_result, dict):
                # nested rule - ruleName: {result1: [functions list], result2: [functions list] }
                nesting = rule_result
                violating_functions = ""
                for method in nesting.keys():
                    if method != 'SUCCESS' and len(nesting[method]) > 0:
                        violating_functions += '\n  [func] ' + '\n  [func] '.join(nesting[method])
                        result = False
                if violating_functions:
                    errors.append("[rule] " + rule + ":" + violating_functions)

    if not result:
        print_error(VERIFICATION_ERR_MSG_PREFIX)
        print('\n'.join(errors))
        return False

    print_completion_message(VERIFICATION_SUCCESS_MSG)
    return True


def debug_print_(s: str, debug: bool = False) -> None:
    # TODO: delete this when we have a logger
    if debug:
        print("DEBUG:", s, flush=True)


def print_error(title: str, txt: str = "", flush: bool = False) -> None:
    print(BASH_RED_COLOR + title + BASH_END_COLOR, txt, flush=flush)


def fatal_error(s: str, debug: bool = False) -> None:
    print_error("Fatal error:", s, True)
    if debug:
        raise Exception(s)
    sys.exit(1)


def print_warning(txt: str, flush: bool = False) -> None:
    print(BASH_ORANGE_COLOR + "WARNING:" + BASH_END_COLOR, txt, flush=flush)


def print_completion_message(txt: str, flush: bool = False) -> None:
    print(BASH_GREEN_COLOR + txt + BASH_END_COLOR, flush=flush)


def is_windows() -> bool:
    return platform.system() == 'Windows'


def get_file_basename(file: str) -> str:
    return ''.join(file.split("/")[-1].split(".")[0:-1])


def get_file_extension(file: str) -> str:
    return file.split("/")[-1].split(".")[-1]


def safe_create_dir(path: str, revert: bool = True, debug: bool = False) -> None:
    if os.path.isdir(path):
        debug_print_(f"directory {path} already exists", debug)
        return
    try:
        os.mkdir(path)
    except OSError as e:
        debug_print_(f"Failed to create directory {path}: {e}", debug)
        if revert:
            raise e


def as_posix(path: str) -> str:
    return path.replace("\\", "/")


def getcwd() -> str:
    return as_posix(os.getcwd())


def remove_and_recreate_dir(path: str, debug: bool = False) -> None:
    if os.path.isdir(path):
        shutil.rmtree(path)
    safe_create_dir(path, debug=debug)


def sanitize_path(win_path: str) -> str:
    """
    Converts path from windows to unix
    :param win_path: Path to translate
    :return: A unix path
    """
    return win_path.replace("\\", "/")


def prepare_call_args(cmd: str) -> List[str]:
    split = shlex.split(cmd)
    if split[0].endswith('.py'):
        # sys.executable returns a full path to the current running python, so it's good for running our own scripts
        certora_root = get_certora_root_directory()
        args = [sys.executable] + [sanitize_path(os.path.join(certora_root, split[0]))] + split[1:]
    else:
        args = split
    return args


def get_certora_root_directory() -> str:
    return os.getenv(ENVVAR_CERTORA, os.getcwd())


def which(filename: str) -> Optional[str]:
    if is_windows() and not re.search(r"\.exe$", filename):
        filename += ".exe"

    # TODO: find a better way to iterate over all directories in path
    for dirname in os.environ['PATH'].split(os.pathsep) + [os.getcwd()]:
        candidate = os.path.join(dirname, filename)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return filename

    return None


def read_json_file(file_name: str) -> Dict[str, Any]:
    with open(file_name) as json_str:
        json_obj = json.load(json_str)
        return json_obj


class NoValEnum(Enum):
    """
    A class for an enum where the numerical value has no meaning.
    """

    def __repr__(self) -> str:
        """
        Do not print the value of this enum, it is meaningless
        """
        return f'<{self.__class__.__name__}.{self.name}>'


class Mode(NoValEnum):
    """
    Mode of operation - the 4 modes are mutually exclusive:

    1. There is a single .tac file
    2. There is a single .conf file
    3. --assert
    4. --verify
    """
    TAC = "a single .tac file"
    CONF = "a single .conf file"
    VERIFY = "using --verify"
    ASSERT = "using --assert"


def is_hex_or_dec(s: str) -> bool:
    """
    @param s: A string
    @return: True if it a decimal or hexadecimal number
    """
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def is_hex(number: str) -> bool:
    """
    @param number: A string
    @return: True if the number is a hexadecimal number:
        - Starts with 0
        - Second character is either x or X
        - All other characters are digits 0-9, or letters a-f or A-F
    """
    match = re.search(r'^0[xX][0-9a-fA-F]+$', number)
    return match is not None


def hex_str_to_cvt_compatible(s: str) -> str:
    """
    @param s: A string representing a number in base 16 with '0x' prefix
    @return: A string representing the number in base 16 but without the '0x' prefix
    """
    assert is_hex(s)
    return re.sub(r'^0[xX]', '', s)


def decimal_str_to_cvt_compatible(s: str) -> str:
    """
    @param s: A string representing a number in base 10
    @return: A string representing the hexadecimal representation of the number, without the '0x' prefix
    """
    assert s.isnumeric()
    return re.sub(r'^0[xX]', '', hex(int(s)))


def split_by_commas_ignore_parenthesis(s: str) -> List[str]:
    """
    Split s by commas UNLESS the commas are inside parenthesis, for example:
    s = "-b=2, -assumeUnwindCond, -rule=bounded_supply, -m=withdrawCollateral(uint256, uint256), -regressionTest"

    will return:
    ['-b=2',
    '-assumeUnwindCond',
    '-rule=bounded_supply',
    '-m=withdrawCollateral(uint256, uint256)',
    '-regressionTest']

    @param s a string
    @returns a list of strings
    """
    return re.split(r',(?![^()]*\))\s*', s)
