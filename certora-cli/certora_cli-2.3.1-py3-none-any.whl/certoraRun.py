#!/usr/bin/env python3

import os
import sys
import subprocess
import traceback
from certora_cli.certoraDualArg import check_arg_and_setting_consistency  # type: ignore
from certora_cli.certoraUtils import get_certora_root_directory  # type: ignore
from certora_cli.certoraUtils import DEFAULT_SOLC, DEFAULT_CLOUD_ENV, DEFAULT_STAGING_ENV
from certora_cli.certoraUtils import debug_print_
from certora_cli.certoraUtils import sanitize_path, prepare_call_args, split_by_commas_ignore_parenthesis
from certora_cli.certoraUtils import check_results_from_file
from certora_cli.certoraUtils import is_windows
from certora_cli.certoraUtils import CERTORA_BUILD_FILE, CERTORA_VERIFY_FILE, LEGAL_CERTORA_KEY_LENGTHS, PACKAGE_FILE
from certora_cli.certoraUtils import which, print_warning, Mode, get_version
from certora_cli.certoraUtils import print_completion_message, print_error
from certora_cli.certoraConfigIO import read_from_conf, current_conf_to_file  # type: ignore
from certora_cli.certoraCloudIO import CloudVerification  # type: ignore
import argparse
import re
import ast
from typing import Dict, List, Optional, Tuple, Any, Set
import json

RUN_IS_LIBRARY = False
DEBUG = False
BUILD_SCRIPT_PATH = "certoraBuild.py"


def print_version() -> None:
    print("certora-cli", get_version())


def exit_if_not_library(code: int) -> None:
    # Uri - we can use our own exception...
    if RUN_IS_LIBRARY:
        return
    else:
        sys.exit(code)


def debug_print(s: str) -> None:
    # TODO: We should have a logger for this - Uri
    # TODO: (Alex:) I would love if we prepended something like `[certoraRun.py DEBUG:]` everytime we log something
    debug_print_(s, DEBUG)


def run_cmd(cmd: str, override_exit_code: bool, custom_error_message: Optional[str] = None) -> None:
    args = None
    try:
        args = prepare_call_args(cmd)
        debug_print(f"Running: {' '.join(args)}")
        exitcode = subprocess.call(args, shell=False)
        if exitcode:

            default_msg = f"Execution of command \"{' '.join(args)}\" terminated with exitcode {exitcode}."
            if custom_error_message is not None:
                debug_print(default_msg)
                print(custom_error_message, flush=True)
            else:
                print(default_msg, flush=True)
            debug_print(f"Path is {os.getenv('PATH')}")
            if not override_exit_code:
                exit_if_not_library(1)
        else:
            debug_print(f"Exitcode {exitcode}")
    except Exception as e:
        debug_print(str(args))

        default_msg = f"Failed to run {cmd}: {e}"
        if custom_error_message is not None:
            debug_print(default_msg)
            print(custom_error_message, flush=True)
        else:
            print(default_msg, flush=True)
        debug_print(str(sys.exc_info()))
        exit_if_not_library(1)


def get_local_run_cmd(args: argparse.Namespace) -> str:
    """
    Assembles a jar command for local run
    @param args: A namespace including all command line input arguments
    @return: A command for running the prover locally
    """
    run_args = []
    if args.mode == Mode.TAC:
        run_args.append(args.files[0])
    if args.cache is not None:
        run_args.extend(['-cache', args.cache])
    if args.tool_output is not None:
        run_args.extend(['-json', args.tool_output])
    if args.settings is not None:
        for setting in args.settings:
            run_args.extend(setting.split('='))

    if args.jar is not None:
        jar_path = args.jar
    else:
        certora_root_dir = sanitize_path(get_certora_root_directory())
        jar_path = f"{certora_root_dir}/emv.jar"

    if args.java_args is not None:
        return " ".join(["java", args.java_args, "-jar", jar_path] + run_args)
    return " ".join(["java", "-jar", jar_path] + run_args)


def run_local_type_check() -> None:
    # Check if java exists on the machine
    java = which("java")
    if java is None:
        print(
            "`java` is not installed. It is highly recommended to install Java to check specification files locally.")
        return  # if user doesn't have java installed, user will have to wait for remote type checking

    # Find path to typechecker jar
    certora_root_dir = sanitize_path(get_certora_root_directory())
    local_certora_path = sanitize_path(os.path.join(certora_root_dir, "certora_jars", "Typechecker.jar"))
    installed_certora_path = \
        sanitize_path(os.path.join(os.path.split(__file__)[0], "..", "certora_jars", "Typechecker.jar"))

    path_to_typechecker = local_certora_path if os.path.isfile(local_certora_path) else installed_certora_path
    # if typechecker jar does not exist, we just skip this step
    if not os.path.isfile(path_to_typechecker):
        print_error("Error", f"Could not run type checker locally: file not found {path_to_typechecker}")
        return

    # args to typechecker
    debug_print(f"Path to typechecker is {path_to_typechecker}")
    typecheck_cmd = f"java -jar {path_to_typechecker} {CERTORA_BUILD_FILE} {CERTORA_VERIFY_FILE}"

    # run it - exit with code 1 if failed
    run_cmd(typecheck_cmd, False, "Failed to compile spec file")


def main_with_args(args: List[str], is_library: bool = False) -> None:
    parsed_args = get_args(args)  # Parse arguments

    global RUN_IS_LIBRARY
    RUN_IS_LIBRARY = is_library
    global DEBUG
    try:
        if parsed_args.debug:
            DEBUG = True

        # When a TAC file is provided, no build arguments will be processed
        if parsed_args.mode != Mode.TAC:
            debug_print(f"There is no TAC file. Going to script {BUILD_SCRIPT_PATH} to main_with_args()")
            from certora_cli.certoraBuild import build  # type: ignore
            build(parsed_args, is_library)

        if parsed_args.build_only:
            exit_if_not_library(0)
        else:
            if parsed_args.local:
                check_cmd = get_local_run_cmd(parsed_args)

                compare_with_tool_output = parsed_args.tool_output is not None
                if compare_with_tool_output:
                    # Remove actual before starting the current test
                    try:
                        os.remove(parsed_args.tool_output)
                    except OSError:
                        pass

                debug_print(f"Verifier run command:\n {check_cmd}")
                run_cmd(check_cmd, compare_with_tool_output)

                if compare_with_tool_output:
                    print("Comparing tool output to the expected output:")
                    result = check_results_from_file(parsed_args.tool_output)
                    if result:
                        exit_if_not_library(0)
                    else:
                        exit_if_not_library(1)
            else:  # Remote run
                # In cloud mode, we first run a local type checker
                if parsed_args.mode != Mode.TAC:
                    if parsed_args.disableLocalTypeChecking:
                        print("Local checks of specification files disabled. It is recommended to enable the checks.")
                    else:
                        run_local_type_check()
                        print_completion_message("Local type checking finished successfully", )

                cv = CloudVerification(parsed_args)
                result = cv.cli_verify(parsed_args, ' '.join(args), debug=DEBUG)
                if result:
                    exit_if_not_library(0)
                else:
                    exit_if_not_library(1)

    except Exception as e:
        print_error("Encountered an error running Certora Prover:",
                    f"{e}.\nConsider running the script again with --debug to find out why", flush=True)
        debug_print(traceback.format_exc())
        exit_if_not_library(1)
    except KeyboardInterrupt:
        print('Interrupted by user', flush=True)


'''
########################################################################################################################
############################################### Argument types #########################################################
########################################################################################################################
'''


def type_non_negative_integer(string: str) -> str:
    """
    :param string: A string
    :return: The same string, if it represents a decimal integer
    :raises argparse.ArgumentTypeError if the string does not represent a non-negative decimal integer
    """
    if not re.match(r'^\d+$', string):
        raise argparse.ArgumentTypeError(f'expected a non-negative integer, instead given {string}')
    return string


def type_jar(filename: str) -> str:
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError(f"file {filename} does not exist.")
    if not os.access(filename, os.X_OK):
        raise argparse.ArgumentTypeError(f"no execute permission for jar file {filename}")

    basename = os.path.basename(filename)  # extract file name from path.
    # NOTE: expects Linux file paths, all Windows file paths will fail the check below!
    if re.search(r"^[\w.]+\.jar$", basename):
        # Base file name can contain only alphanumeric characters or underscores
        return filename

    raise argparse.ArgumentTypeError(f"file {filename} is not of type .jar")


def type_readable_file(filename: str) -> str:
    if not os.path.exists(filename):
        raise argparse.ArgumentTypeError(f"file {filename} not found")
    if os.path.isdir(filename):
        raise argparse.ArgumentTypeError(f"{filename} is a directory and not a file")
    if not os.access(filename, os.R_OK):
        raise argparse.ArgumentTypeError(f"no read permissions for {filename}")
    return filename


def is_solc_file_valid(orig_filename: Optional[str]) -> str:
    """
    Verifies that a given --solc argument is valid:
        1. The file exists
        2. We have executable permissions for it
    :param orig_filename: Path to a solc executable file. If it is None, a default path is used instead,
                          which is also checked
    :return: Default solc executable if orig_filename was None, orig_filename is returned otherwise
    :raises argparse.ArgumentTypeException if the argument is invalid (including the default if it is used)
    """
    if orig_filename is None:
        filename = DEFAULT_SOLC
        err_prefix = f'No --solc path given, but default solidity executable {DEFAULT_SOLC} had an error. '
    else:
        filename = orig_filename
        err_prefix = ''

    if is_windows() and not re.search(r"\.exe$", filename):
        filename += ".exe"

    common_mistakes_suffixes = ['sol', 'conf', 'tac', 'spec', 'cvl']
    for suffix in common_mistakes_suffixes:
        if re.search(r'^[^.]+\.' + suffix + '$', filename):
            raise argparse.ArgumentTypeError(f"wrong solidity executable given: {filename}")

    # TODO: find a better way to iterate over all directories in path
    for dirname in os.environ['PATH'].split(os.pathsep) + [os.getcwd()]:
        dirname = os.path.expanduser(dirname)  # Expand ~ in unix systems
        candidate = os.path.join(dirname, filename)
        if os.path.exists(candidate):
            if os.path.isfile(candidate):
                if os.access(candidate, os.X_OK):
                    sanitized = sanitize_path(candidate)
                    return sanitized
                else:
                    raise argparse.ArgumentTypeError(
                        err_prefix + f"No execution permissions for Solidity executable {orig_filename}")
            else:
                raise argparse.ArgumentTypeError(err_prefix + f"{orig_filename} is a directory, not a file")

    raise argparse.ArgumentTypeError(err_prefix + f"Solidity executable {orig_filename} not found in path")


def type_solc_map(args: str) -> Dict[str, str]:
    """
    Checks that the argument is of form <contract_1>=<solc_1>,<contract_2>=<solc_2>,..
    and if all solc files are valid: they were found, and we have execution permissions for them

    :param args: argument of --solc_map
    :return: {contract: solc}.
             For example, if --solc_args a=solc4.25 is used, returned value will be:
             {'a': 'solc4.25'}
    :raises argparse.ArgumentTypeError if the format is wrong
    """
    args = args.replace(' ', '')  # remove whitespace
    solc_matches = re.search(r'^([^=,]+=[^=,]+,)*([^=,]+=[^=,]+)$', args)
    if solc_matches is None:
        raise argparse.ArgumentTypeError(f"--solc_map argument {args} is of wrong format. Must be of format:"
                                         f"<contract>=<solc>[,..]")

    solc_map = {}  # type: Dict[str, str]
    map_dest = set()  # If all --solc_args point to the same solc version, it is better to use --solc and we warn
    all_warnings = set()

    for match in args.split(','):
        contract, solc_file = match.split('=')
        is_solc_file_valid(solc_file)  # raises an exception if file is bad
        if contract in solc_map:
            if solc_map[contract] == solc_file:
                all_warnings.add(f"solc mapping {contract}={solc_file} appears multiple times and is redundant")
            else:
                raise argparse.ArgumentTypeError(f"contradicting definition in --solc_map for contract {contract}: "
                                                 f"it was given two different Solidity compilers: {solc_map[contract]}"
                                                 f" and {solc_file}")
        else:
            solc_map[contract] = solc_file
            map_dest.add(solc_file)

    if len(map_dest) == 1:
        all_warnings.add(f'all files are pointing to the same Solidity compiler in --solc_args. '
                         f'--solc {list(map_dest)[0]} can be used instead')

    for warning in all_warnings:
        print_warning(warning)

    debug_print_(f"solc_map = {solc_map}", True)  # Currently, always print debug here. Solve when we have a logger...
    return solc_map


def type_dir(dirname: str) -> str:
    if not os.path.exists(dirname):
        raise argparse.ArgumentTypeError(f"path {dirname} does not exist")
    if os.path.isfile(dirname):
        raise argparse.ArgumentTypeError(f"{dirname} is a file and not a directory")
    if not os.access(dirname, os.R_OK):
        raise argparse.ArgumentTypeError(f"no read permissions to {dirname}")
    return os.path.realpath(dirname).replace('\\', '/')  # We want the full path, UNIX style


def type_tool_output_path(filename: str) -> str:
    if os.path.isdir(filename):
        raise argparse.ArgumentTypeError(f"--toolOutputPath {filename} is a directory")
    if os.path.isfile(filename):
        print_warning(f"--toolOutPutpath {filename} file already exists")
        if not os.access(filename, os.W_OK):
            raise argparse.ArgumentTypeError(f'No permission to rewrite --toolOutPutpath file {filename}')
    else:
        try:
            with open(filename, 'w') as f:
                f.write('try')
            os.remove(filename)
        except (ValueError, IOError, OSError) as e:
            raise argparse.ArgumentTypeError(f"could not create --toolOutputPath file {filename}. Error: {e}")

    return filename


def type_list(candidate: str) -> List[str]:
    """
    Verifies the argument can be evaluated by python as a list
    """
    v = ast.literal_eval(candidate)
    if type(v) is not list:
        raise argparse.ArgumentTypeError(f"Argument \"{candidate}\" is not a list")
    return v


def type_input_file(file: str) -> str:
    # [file[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac

    if '.sol' in file:
        if not re.search(r'^.+\.sol(:[^.:]+)?$', file):
            raise argparse.ArgumentTypeError(f"Bad input file format of {file}. Expected <file_path>:<contract>")

        if ':' in file:
            if is_windows():  # We might have a path with : like C:\Users...
                if file.count(':') == 2:  # : for both drive and a contract name
                    file_path, contract = file.rsplit(':', 1)
                elif re.search(r'^[A-Z]:\\', file):  # : just for drive
                    file_path = file
                    contract = os.path.basename(file).replace('.sol', '')
                else:  # A single : for a contract name
                    file_path, contract = file.split(':')
            else:
                file_path, contract = file.split(':')

            if not re.search(r'^\w+$', contract):
                raise argparse.ArgumentTypeError(
                    f"A contract's name {contract} can contain only alphanumeric characters or underscores")
        else:
            file_path = file

        type_readable_file(file_path)
        base_name = os.path.basename(file_path)[0:-4]  # get Path's leaf name and remove the trailing .sol
        if not re.search(r'^\w+$', base_name):
            raise argparse.ArgumentTypeError(
                f"file name {file} can contain only alphanumeric characters or underscores")
        # return file_path
        return file

    elif file.endswith('.tac') or file.endswith('.conf'):
        type_readable_file(file)
        return file

    raise argparse.ArgumentTypeError(f"input file {file} is not in one of the supported types (.sol, .tac, .conf)")


def type_verify_arg(candidate: str) -> str:
    if not re.search(r'^\w+:[^:]+\.(spec|cvl)$', candidate):
        # Regex: name has only one ':', has at least one letter before, one letter after and ends in .spec
        raise argparse.ArgumentTypeError(f"argument {candidate} for --verify option is in incorrect form. "
                                         "Must be formatted contractName:specName.spec")
    spec_file = candidate.split(':')[1]
    type_readable_file(spec_file)

    return candidate


def type_link_arg(link: str) -> str:
    if not re.search(r'^\w+:\w+=\w+$', link):
        raise argparse.ArgumentTypeError(f"Link argument {link} must be of the form contractA:slot=contractB or "
                                         f"contractA:slot=<number>")
    return link


def type_struct_link(link: str) -> str:
    search_res = re.search(r'^\w+:([^:=]+)=\w+$', link)
    # We do not require firm form of slot number so we can give more informative warnings

    if search_res is None:
        raise argparse.ArgumentTypeError(f"Struct link argument {link} must be of the form contractA:number=contractB")
    try:
        parsed_int = int(search_res[1], 0)  # an integer or a hexadecimal
        if parsed_int < 0:
            raise argparse.ArgumentTypeError(f"struct link slot number negative at {link}")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Struct link argument {link} must be of the form contractA:number=contractB")
    return link


def type_contract(contract: str) -> str:
    if not re.match(r'^\w+$', contract):
        raise argparse.ArgumentTypeError(
            f"Contract name {contract} can include only alphanumeric characters or underscores")
    return contract


def type_package(package: str) -> str:
    if not re.search("^[^=]+=[^=]+", package):
        raise argparse.ArgumentTypeError("a package must have the form name=path")
    path = package.split('=')[1]
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"Package path {path} does not exist")
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(f"No read permissions for for packages directory {path}")
    return package


def type_settings_arg(settings: str) -> str:
    """
    Gets a string representing flags to be passed to another tool via --settings, in the form '-a,-b=2[,..]'
    @raise argparse.ArgumentTypeError
    """
    debug_print(f"settings pre-parsing= {settings}")
    settings = settings.lstrip()

    '''
    Split by commas UNLESS the commas are inside parenthesis, for example:
    "-b=2, -assumeUnwindCond, -rule=bounded_supply, -m=withdrawCollateral(uint256, uint256), -regressionTest"

    will become:
    ['-b=2',
    '-assumeUnwindCond',
    '-rule=bounded_supply',
    '-m=withdrawCollateral(uint256, uint256)',
    '-regressionTest']
    '''
    flags = split_by_commas_ignore_parenthesis(settings)
    '''
    Regex explanation:
    We want to match a comma.
    ?! is a negative lookahead. We do not match the comma if there is any number of non-parenthesis characters
    ending in a closing parenthesis.
    We also strip all whitespaces following commas, if any.
    '''

    debug_print("settings after-split= " + str(settings))
    for flag in flags:
        debug_print(f"checking setting {flag}")
        if not re.search('^-[^-=]+(=[^-=]+)?', flag):
            raise argparse.ArgumentTypeError(f"illegal argument in --settings: {flag}")
    return settings


def type_java_arg(java_args: str) -> str:
    if not re.search('^".+"$', java_args):
        raise argparse.ArgumentTypeError(f'java argument must be wrapped in "", instead found {java_args}')
    return java_args


def type_address(candidate: str) -> str:
    if not re.search(r'^[^:]+:[0-9A-Fa-fxX]+$', candidate):
        # Regex: name has only one ':', has at least one letter before, one letter after and ends in .spec
        raise argparse.ArgumentTypeError(f"Argument {candidate} of --address option is in incorrect form. "
                                         "Must be formatted <contractName>:<non-negative number>")
    return candidate


def check_files_input(file_list: List[str]) -> None:
    """
    Verifies that correct input was inserted as input to files.
    As argparser verifies the files exist and the correctness of the format, we only check if only a single operation
    mode was used.
    The allowed disjoint cases are:
    1. Use a single .conf file
    2. Use a single .tac file
    3. Use any number of [contract.sol:nickname ...] (at least one is guaranteed by argparser)
    @param file_list: A list of strings representing file paths
    @raise argparse.ArgumentTypeError if more than one of the modes above was used
    """
    num_files = len(file_list)
    if num_files > 1:  # if there is a single file, there cannot be a mix between file types
        for file in file_list:
            if '.tac' in file:
                raise argparse.ArgumentTypeError(f'Only a single .tac file can be used, given {num_files} files')
            if '.conf' in file:
                raise argparse.ArgumentTypeError(f'Only a single .conf file can be used, given {num_files} files')


def _get_trivial_contract_name(contract: str) -> str:
    """
    Gets a path to a .sol file and returns its trivial contract name. The trivial contract name is the basename of the
    path of the file, without file type suffix.
    For example: for file/Test/opyn/vault.sol, the trivial contract name is vault.
    @param contract: A path to a .sol file
    @return: The trivial contract name of a file
    """
    # contract = contract.split('/')[-1]  # Breaking path
    contract = os.path.basename(sanitize_path(contract))
    contract = contract.split('.')[0]
    return contract


def warn_verify_file_args(files: List[str]) -> Tuple[Set[str], Set[str], Dict[str, str], Dict[str, str]]:
    """
    Verifies all file inputs are legal. If they are not, throws an exception.
    If there are any redundancies or duplication, warns the user.
    Otherwise, it returns a set of all legal contract names.
    @param files: A list of string of form: [contract.sol[:contract_name] ...]
    @return: (contracts, files, contract_to_file, file_to_contract)
        contracts - a set of contract names
        files - a set of paths to files containing contracts
        contract_to_file - a mapping from contract name -> file containing it
        file_to_contract - a mapping from a file path -> name of the contract within it we verify
                           (we can currently only verify a single contract per file)
    """

    """
    The logic is complex, and better shown by examples.
    Legal use cases:
    1. A.sol B.sol
        -> returns (A, B)
    2. A.sol:a B.sol:b C.sol
        -> returns (A, a, B, b, C)
    3. A.sol:B B.sol:c
        -> The contract names do not collide

    Warning cases:
    4. A.sol A.sol
        -> A.sol is redundant
    5. A.sol:a A.sol:a
        -> A.sol is redundant
    6. A.sol:A
        -> contract name A is redundant

    Illegal cases:
    7. A.sol:a A.sol:b
        -> The same file cannot contain two different contracts
    8. A.sol:a B.sol:a
        -> The same contract name cannot be used twice
    9. ../A.sol A.sol
        -> The same contract name cannot be used twice
    10. A.sol:B B.sol
        -> The same contract name cannot be used twice
    11. A.sol:a A.sol
        -> The same file cannot contain two different contracts
    12. A.sol A.sol:a
        -> The same file cannot contain two different contracts

    Warning are printed only if the input is legal
    @raise argparse.ArgumentTypeError in an illegal case (see above)
    """
    if len(files) == 1 and (files[0].endswith(".conf") or files[0].endswith(".tac")):
        return set(), set(), dict(), dict()  # No legal contract names

    declared_contracts = set()
    file_paths = set()
    all_warnings = set()

    contract_to_file: Dict[str, str] = dict()
    file_to_contract: Dict[str, str] = dict()

    for f in files:
        if ':' in f:
            # Can be either for contract name declaration or because we have a drive in windows path e.g. C:\Users...

            warn_contract = True  # Only warn if the : marked a contract name and not a drive in path

            if is_windows():  # colon might be for a contract name or for a drive in path or both
                num_colons = f.count(':')
                assert num_colons <= 2
                if num_colons == 2:  # We have two colons: one for a contract name, one for a drive in path
                    filepath, contract_name = f.rsplit(':', 1)
                else:
                    if re.search(r'^[A-Z]:\\', f):  # colon is for a drive in path. No contract name
                        filepath = f
                        contract_name = _get_trivial_contract_name(filepath)
                        warn_contract = False
                    else:  # colon was for a contract name. No drive in path
                        filepath, contract_name = f.split(':')
            else:
                filepath, contract_name = f.split(':')

            if warn_contract:
                natural_contract_name = _get_trivial_contract_name(filepath)
                if contract_name == natural_contract_name:
                    all_warnings.add(f"contract name {contract_name} is the same as the file name and can be omitted")
        else:
            filepath = f
            contract_name = _get_trivial_contract_name(filepath)

        if is_windows():
            filepath = filepath.replace('\\', '/')  # linux path
            # filepath = sanitize_path(filepath)

        if filepath in file_to_contract:
            if contract_name != file_to_contract[filepath]:
                raise argparse.ArgumentTypeError(f"file {filepath} was given two different contract names: "
                                                 f"{file_to_contract[filepath]} and {contract_name}")
            else:
                all_warnings.add(f"file argument {f} is redundant")

        if contract_name in contract_to_file and contract_to_file[contract_name] != filepath:
            # A.sol:a B.sol:a
            raise argparse.ArgumentTypeError(f"A contract named {contract_name} was declared twice for files "
                                             f"{contract_to_file[contract_name]}, {filepath}")

        contract_to_file[contract_name] = filepath
        file_to_contract[filepath] = contract_name
        declared_contracts.add(contract_name)
        file_paths.add(filepath)

    for warning in all_warnings:
        print_warning(warning)

    return declared_contracts, file_paths, contract_to_file, file_to_contract


def check_dedup_link_args(args: argparse.Namespace) -> None:
    """
    Detects contradicting definitions of slots in link and throws.
    If no contradiction was found, removes duplicates if they exist.
    DOES NOT for file existence, format legality, or anything else
    @param args: A namespace, where args.link includes a list of strings that are the link arguments
    @raise argparse.ArgumentTypeError if a slot was given two different definitions
    """
    dedup_links: Set[str] = set()
    double_def_warns = set()
    for link in args.link:
        for seen_link in dedup_links:
            slot = link.split('=')[0]
            if slot == seen_link.split('=')[0]:
                if link == seen_link:
                    double_def_warns.add(f"link {link} was defined multiple times")
                else:
                    raise argparse.ArgumentTypeError(f"slot {slot} was defined multiple times: {link}, {seen_link}")

        dedup_links.add(link)

    for warning in double_def_warns:
        print_warning(warning)

    args.link = list(dedup_links)


def flatten_list(nested_list: Optional[List[list]]) -> Optional[list]:
    """
    @param nested_list: A list of lists: [[a], [b, c], []]
    @return: a flat list, in our example [a, b, c]. If None was entered, returns None
    """
    if nested_list is None:
        return None
    return [item for sublist in nested_list for item in sublist]


def flatten_arg_lists(args: argparse.Namespace) -> None:
    """
    Flattens lists of lists arguments in a given namespace.
    For example,
    [[a], [b, c], []] -> [a, b, c]

    This is applicable to all options that can be used multiple times, and each time get multiple arguments.
    @param args: Namespace containing all command line arguments, generated by get_args()
    """
    layered_args_list = ['assert_contracts', 'verify', 'link']
    for args_list in layered_args_list:
        flat_list = flatten_list(getattr(args, args_list))
        setattr(args, args_list, flat_list)


def __remove_parsing_whitespace(arg_list: List[str]) -> None:
    """
    Removes all whitespaces added to args by __alter_args_before_argparse():
    1. A leading space before a dash (if added)
    2. space between commas
    :param arg_list: A list of options as strings.
    """
    for idx, arg in enumerate(arg_list):
        arg_list[idx] = arg.strip().replace(', ', ',')


def __cannonize_settings(args: argparse.Namespace) -> None:
    """
    Converts the args.settings into a standard form.
    The standard form is a single list of strings in ascending order, containing no duplicate values, and
    each string contains no whitespace.

    @param args: Namespace containing all command line arguments, generated by get_args()
    """
    if not hasattr(args, 'settings') or args.settings is None:
        return

    all_settings = set()
    all_warnings = set()

    for setting_list in args.settings:
        # Split by commas UNLESS they are inside parenthesis, like -m 'foo(uint, uint)'
        for setting in split_by_commas_ignore_parenthesis(setting_list):

            '''
            Lines below remove whitespaces inside the setting argument.

            An example for when the might occur:
            -m 'foo(uint, uint)'
            will result in settings ['-m', 'foo(uint, uint)']
            We wish to replace it to be ['-m', '-foo(uint,uint)'], without the space after the comma
            '''
            setting_split = setting.strip().split('=')
            for i, setting_word in enumerate(setting_split):
                setting_split[i] = setting_word.replace(' ', '')

            setting = '='.join(setting_split)
            if setting in all_settings:
                all_warnings.add(f'setting {setting} appears multiple times')
            else:
                all_settings.add(setting)

    for warning in sorted(list(all_warnings)):
        print_warning(warning)

    args.settings = sorted(list(all_settings))


def check_contract_name_arg_inputs(args: argparse.Namespace) -> None:
    """
    This function verifies that all options that expect to get contract names get valid contract names.
    If they do, nothing happens. If there is any error, an exception is thrown.
    @param args: Namespace containing all command line arguments, generated by get_args()
    @raise argparse.ArgumentTypeError if a contract name argument was expected, but not given.
    """
    contract_names, file_paths, contract_to_file, file_to_contract = warn_verify_file_args(args.files)
    args.contracts = contract_names
    args.file_paths = file_paths
    args.file_to_contract = file_to_contract

    # we print the warnings at the end of this function, only if no errors were found. Each warning appears only once
    all_warnings = set()

    # Link arguments can be either: contractName:slot=contractName
    #   or contractName:slot=integer(decimal or hexadecimal)
    if args.link is not None:
        for link in args.link:
            executable = link.split(':')[0]
            executable = _get_trivial_contract_name(executable)
            if executable not in contract_names:
                raise argparse.ArgumentTypeError(f"link {link} doesn't match any contract name")

            library_or_const = link.split('=')[1]
            try:
                parsed_int = int(library_or_const, 0)  # can be either a decimal or hexadecimal number
                if parsed_int < 0:
                    raise argparse.ArgumentTypeError(f"slot number is negative at {link}")
            except ValueError:
                library_name = _get_trivial_contract_name(library_or_const)
                if library_name not in contract_names:
                    raise argparse.ArgumentTypeError(f"linked contract {library_name} doesn't match any contract name")

        check_dedup_link_args(args)

    assert_args = set()
    if args.assert_contracts is not None:
        for assert_arg in args.assert_contracts:
            contract = _get_trivial_contract_name(assert_arg)
            if contract not in contract_names:
                raise argparse.ArgumentTypeError(f"--assert argument {contract} doesn't match any contract name")
            if assert_arg in assert_args:
                all_warnings.add(f'--assert argument {assert_arg} was given multiple times')
            else:
                assert_args.add(assert_arg)

    args.assert_contracts = list(assert_args)

    verify_args = set()
    args.spec_files = None
    if args.verify is not None:
        spec_files = set()
        for ver_arg in args.verify:
            contract, spec = ver_arg.split(':')
            contract = _get_trivial_contract_name(contract)
            if contract not in contract_names:
                raise argparse.ArgumentTypeError(f"--verify argument {contract} doesn't match any contract name")

            if ver_arg in verify_args:
                all_warnings.add(f"the same verification was inserted multiple times: {ver_arg}")
            else:
                verify_args.add(ver_arg)
            spec_files.add(spec)
        args.spec_files = sorted(list(spec_files))

    # remove duplications:
    args.verify = list(verify_args)

    contract_to_address = dict()
    if args.address:
        for address_str in args.address:
            contract = address_str.split(':')[0]
            if contract not in contract_names:
                raise argparse.ArgumentTypeError(f"unrecognized contract in --address argument {address_str}")
            number = address_str.split(':')[1]
            if contract not in contract_to_address:
                contract_to_address[contract] = number
            elif contract_to_address[contract] != number:
                raise argparse.ArgumentTypeError(f'contract {contract} was given two different addresses: '
                                                 f'{contract_to_address[contract]} and {number}')
            else:
                all_warnings.add(f'address {number} for contract {contract} defined twice')
    args.address = contract_to_address

    if args.struct_link:
        contract_slot_to_contract = dict()
        for link in args.struct_link:
            location = link.split('=')[0]
            destination = link.split('=')[1]
            origin = location.split(":")[0]
            if origin not in contract_names:
                raise argparse.ArgumentTypeError(
                    f"--struct link argument {link} is illegal: {origin} is not a defined contract name")
            if destination not in contract_names:
                raise argparse.ArgumentTypeError(
                    f"--struct link argument {link} is illegal: {destination} is not a defined contract name")

            if location not in contract_slot_to_contract:
                contract_slot_to_contract[location] = destination
            elif contract_slot_to_contract[location] == destination:
                all_warnings.add(f"--structLink argument {link} appeared more than once")
            else:
                raise argparse.ArgumentTypeError(f"{location} has two different definitions in --structLink: "
                                                 f"{contract_slot_to_contract[location]} and {destination}")

    for warning in all_warnings:
        print_warning(warning)


def check_mode_of_operation(args: argparse.Namespace) -> None:
    """
    Ascertains we have only one mode of operation in use and updates args.mode to store it as an enum.
    The four modes are:
    1. There is a single .tac file
    2. There is a single .conf file
    3. --assert
    4. --verify

    This function ascertains there is no overlap between the modes. The correctness of each mode is checked in other
    functions.
    @param args: A namespace including all CLI arguments provided
    @raise an argparse.ArgumentTypeError when:
        1. .conf|.tac file is used with --assert|--verify flags
        2. when both --assert and --verify flags were given
        3. when the file is not .tac|.conf and neither --assert not --verify were used
    """
    assert args.files
    is_verifying = args.verify is not None and len(args.verify) > 0
    is_asserting = args.assert_contracts is not None and len(args.assert_contracts) > 0

    if is_verifying and is_asserting:
        raise argparse.ArgumentTypeError("only one option of --assert and --verify can be used")

    special_file_type = None

    if len(args.files) == 1:
        # We already checked that this is the only case where we might encounter CONF or TAC files
        input_file = args.files[0]
        if re.search(r'\.tac$', input_file):
            special_file_type = '.tac'
        elif re.search(r'\.conf$', input_file):
            special_file_type = '.conf'

        if special_file_type is not None:
            if is_verifying:
                raise argparse.ArgumentTypeError(
                    f"Option --verify cannot be used with a {special_file_type} file {input_file}")
            if is_asserting:
                raise argparse.ArgumentTypeError(
                    f"Option --assert cannot be used with a {special_file_type} file {input_file}")

    if special_file_type is None and not is_asserting and not is_verifying:
        raise argparse.ArgumentTypeError("Must use either --assert or --verify option")

    # If we made it here, exactly a single mode was used. We update the namespace entry mode accordingly:
    if is_verifying:
        args.mode = Mode.VERIFY
    elif is_asserting:
        args.mode = Mode.ASSERT
    elif special_file_type == '.conf':
        args.mode = Mode.CONF
    elif special_file_type == '.tac':
        args.mode = Mode.TAC
    else:
        raise ValueError(f"Special file type not recognized: {special_file_type}")


def check_packages_arguments(args: argparse.Namespace) -> None:
    """
    Performs checks on the --packages_path and --packages options.
    @param args: A namespace including all CLI arguments provided
    @raise an argparse.ArgumentTypeError if:
        1. both options --packages_path and --packages options were used
        2. in --packages the same name was given multiples paths
    """
    from certora_cli.certoraUtils import getcwd
    if args.packages_path is None:
        args.packages_path = os.getenv("NODE_PATH", f"{getcwd()}/node_modules")
        debug_print(f"args.packages_path is {args.packages_path}")

    if args.packages is not None and len(args.packages) > 0:

        package_name_to_path: Dict[str, str] = dict()
        for package_str in args.packages:
            package = package_str.split("=")[0]
            path = package_str.split("=")[1]
            if package in package_name_to_path:
                raise argparse.ArgumentTypeError(
                    f"package {package} was given two paths: {package_name_to_path[package]}, {path}")
            package_name_to_path[package] = path

        args.packages = sorted(args.packages, key=str.lower)

    else:
        if not os.path.exists(PACKAGE_FILE):
            print_warning(f"Default package file {PACKAGE_FILE} not found")
        elif not os.access(PACKAGE_FILE, os.R_OK):
            print_warning(f"No read permissions for default package file {PACKAGE_FILE} not found")
        else:
            try:
                with open("package.json", "r") as package_json_file:
                    package_json = json.load(package_json_file)
                    deps = set(list(package_json["dependencies"].keys()) if "dependencies" in package_json else
                               list(package_json["devDependencies"].keys()) if "devDependencies" in package_json
                               else list())  # May need both

                    packages_path = args.packages_path
                    packages_to_path_list = [f"{package}={packages_path}/{package}"for package in deps]
                    args.packages = sorted(packages_to_path_list, key=str.lower)

            except EnvironmentError:
                ex_type, ex_value, _ = sys.exc_info()
                print_warning(f"Failed in processing {PACKAGE_FILE}: {ex_type}, {ex_value}")


def validate_certora_key(args: argparse.Namespace) -> None:
    """
    Checks that the environment variable CERTORAKEY is set with a valid key and adds it to args.key
    @param args: A namespace including all CLI arguments provided
    @raise argparse.ArgumentTypeError if CERTORAKEY is not defined or has an illegal value
    """
    if "CERTORAKEY" not in os.environ:
        raise argparse.ArgumentTypeError("Please set the environment variable CERTORAKEY")
    args.key = os.environ["CERTORAKEY"]
    if not re.match(r'^[0-9A-Fa-f]+$', args.key):
        raise argparse.ArgumentTypeError("environment variable CERTORAKEY has an illegal value")
    if not len(args.key) in LEGAL_CERTORA_KEY_LENGTHS:
        raise argparse.ArgumentTypeError("environment variable CERTORAKEY has an illegal length")


def check_deployment_args(args: argparse.Namespace) -> None:
    """
    Checks that the user didn't choose both --staging and --cloud
    @param args: A namespace including all CLI arguments provided
    @raise argparse.ArgumentTypeError if both --staging and --cloud options are present in args
    """
    if args.staging:
        if args.cloud:
            raise argparse.ArgumentTypeError("cannot use both --staging and --cloud")
        args.env = DEFAULT_STAGING_ENV
    else:
        args.env = DEFAULT_CLOUD_ENV


def check_solc_solc_map(args: argparse.Namespace) -> None:
    """
    Executes all post-parsing checks of --solc and --solc_map arguments:
    1. --solc and --solc_map cannot be used together
    2. if both --solc and --solc_map were not used, and we are not in conf file mode,
       take the default solc and check its validity
    3. if --solc_map is used and we are not in .conf file mode:
       verify that every contract appears exactly once in the map and that every mapping has a valid contract as a
       key
    @param args: A namespace including all CLI arguments provided
    @raise argparse.ArgumentTypeError if:
                1. both --solc and --solc_map options are present in args
                2. A key in the solc mapping is not a valid contract
                3. Some contracts do not appear as keys in the solc map
    """
    if args.solc is not None and args.solc_map is not None:
        raise argparse.ArgumentTypeError("You cannot use both --solc and --solc_map arguments")

    if args.solc_map is None:
        args.solc = is_solc_file_valid(args.solc)
    else:  # we use solc_map, check its validity
        from copy import deepcopy
        orphan_contracts = deepcopy(args.contracts)

        for (contract, solc) in args.solc_map.items():
            if contract not in args.contracts:
                raise argparse.ArgumentTypeError(
                    f"--solc_args argument {contract}={solc}: {contract} is not a contract")
            orphan_contracts.remove(contract)

        if len(orphan_contracts) > 0:
            raise argparse.ArgumentTypeError(
                f"Some contracts do not appear in --solc_map: {', '.join(orphan_contracts)}")


def check_rule(args: argparse.Namespace) -> None:
    """
    We accept two syntaxes for rules: --rule or --settings -rule.
    This function checks that:
    1. The two syntaxes are consistent within the same command line (give the same rule)
    2. The --settings -rule syntax is consistent (gets a single rule at most)
    3. The rule exists in the spec file - this is not a bulletproof check, which might return a false positive
        but not a false negative. It still causes a quick failure in most cases.
    @param args: a namespace containing command line arguments
    """
    if args.rule is None:
        return

    # search for rule
    rule_found = False
    if args.verify:
        for spec_file in args.spec_files:
            with open(spec_file, 'r') as f:
                file_content = f.read()
            if re.search(r'(\s|\n)+' + str(args.rule) + r'(\s+|\(|\{)', file_content):  # Very basic check
                rule_found = True
                break

    if not rule_found:
        raise argparse.ArgumentTypeError(f"rule {args.rule} was not found in any of the specification files!")


class UniqueStore(argparse.Action):
    """
    This class makes the argparser throw an error for a given flag if it was inserted more than once
    """

    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: Any,  # type: ignore
                 option_string: str) -> None:
        if getattr(namespace, self.dest, self.default) is not self.default:
            parser.error(f"{option_string} appears several times.")
        setattr(namespace, self.dest, values)


def __alter_args_before_argparse(args_list: List[str]) -> None:
    """
    This function is a hack so we can accept the old syntax and still use argparse.
    This function alters the CL input so that it will be parsed correctly by argparse.

    Currently, it fixes two issues:

    1. We want to accept --javaArgs '-a,-b'
    By argparse's default, it is parsed as two different arguments and not one string.
    The hack is to preprocess the arguments, replace the comma with a commaspace.

    2. A problem with --javaArgs -single_flag. The fix is to add a space before the dash artificially.

    NOTE: Must use remove_parsing_whitespace() to undo these changes on argparse.ArgumentParser.parse_args() ouput!
    :param args_list: A list of CLI options as strings
    """
    for idx, arg in enumerate(args_list):
        if isinstance(arg, str):
            if ',' in arg:
                args_list[idx] = arg.replace(",", ", ")
                arg = args_list[idx]
            if len(arg) > 1 and arg[0] == "-" and arg[1] != "-":  # fixes a problem with --javaArgs -single_flag
                args_list[idx] = " " + arg


def check_args_post_argparse(args: argparse.Namespace) -> None:
    """
    Performs checks over the arguments after basic argparse parsing

    argparse parses option one by one. This is the function that checks all relations between different options and
    arguments. We assume here that basic syntax was already checked.
    @param args: A namespace including all CLI arguments provided
    @raise argparse.ArgumentTypeError if input is illegal
    """
    global DEBUG
    DEBUG = args.debug

    if args.path is None:
        args.path = __default_path()
    __cannonize_settings(args)
    check_files_input(args.files)
    check_contract_name_arg_inputs(args)  # Here args.contracts is set
    check_packages_arguments(args)
    check_solc_solc_map(args)
    check_arg_and_setting_consistency(args)
    check_rule(args)

    certora_root_dir = sanitize_path(get_certora_root_directory())
    default_jar_path = f"{certora_root_dir}/emv.jar"
    if args.jar is not None or \
            (os.path.isfile(default_jar_path) and args.staging is None and args.cloud is None):
        args.local = True
    else:
        args.local = False
        check_deployment_args(args)
        validate_certora_key(args)

    if args.java_args is not None:
        args.java_args = ' '.join(args.java_args).replace('"', '')


def __default_path() -> str:
    path = os.path.join(os.getcwd(), "contracts")
    if os.path.isdir(path):
        return os.path.realpath(path)
    path = os.path.realpath(os.getcwd())
    return path


def pre_arg_fetching_checks(args_list: List[str]) -> None:
    """
    This function runs checks on the raw arguments before we attempt to read them with argparse.
    We also replace certain argument values so the argparser will accept them.
    NOTE: use remove_parsing_whitespace() on argparse.ArgumentParser.parse_args() output!
    :param args_list: A list of CL arguments
    :raises argparse.ArgumentTypeError if there are errors (see individual checks for more details):
        - There are wrong quotation marks “ in use
    """
    __check_no_pretty_quotes(args_list)
    __alter_args_before_argparse(args_list)


def __check_no_pretty_quotes(args_list: List[str]) -> None:
    """
    :param args_list: A list of CL arguments
    :raises argparse.ArgumentTypeError if there are wrong quotation marks “ in use (" are the correct ones)
    """
    for arg in args_list:
        if '“' in arg:
            raise argparse.ArgumentTypeError('Please replace “ with " quotation marks')


def handle_version_flag(args_list: List[str]) -> None:
    for arg in args_list:
        if arg == "--version":
            print_version()  # exits the program
            exit(0)


def __get_argparser() -> argparse.ArgumentParser:
    """
    @return: argparse.ArgumentParser with all relevant option arguments, types and logic
    """
    parser = argparse.ArgumentParser(prog="certora-cli arguments and options", allow_abbrev=False)
    parser.add_argument('files', type=type_input_file, nargs='+',
                        help='[contract.sol[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac')

    operation_args = parser.add_argument_group("mode of operation. Please choose one")
    # Must include exactly one of the options in this group
    operation_args.add_argument("--verify", nargs='+', type=type_verify_arg, action='append',
                                help='Matches specification files to contracts. '
                                     'For example: --verify [contractName:specName.spec ...]')
    operation_args.add_argument("--assert", nargs='+', dest='assert_contracts', type=type_contract, action='append',
                                help='The list of contracts to assert. Usage: --assert [contractName ...]')

    optional_args = parser.add_argument_group("optional arguments")
    optional_args.add_argument("--cache", help='name of cache to use', action=UniqueStore)
    optional_args.add_argument("--msg", help='Add a message description to your run', action=UniqueStore)

    optional_args.add_argument("--solc", action=UniqueStore, help="path to the solidity compiler executable file")
    optional_args.add_argument("--solc_args", type=type_list, action=UniqueStore,
                               help="list of string arguments to pass for the solidity compiler, for example: "
                                    "\"['--optimize', '--optimize-runs', '200']\"")
    optional_args.add_argument("--solc_map", action=UniqueStore, type=type_solc_map,
                               help="path to the solidity compiler executable file")
    optional_args.add_argument("--link", nargs='+', type=type_link_arg, action='append',
                               help='Links a slot in a contract with another contract. Usage: ContractA:slot=ContractB')
    optional_args.add_argument("--address", nargs='+', type=type_address, action=UniqueStore,
                               help='Set an address manually. Default: automatic assignment by the python script.'
                                    'Format: <contractName>:<number>')
    optional_args.add_argument("--jar", type=type_jar, action=UniqueStore,
                               help="Path to the Certora prover's .jar file")

    optional_args.add_argument("--structLink", nargs='+', type=type_struct_link, action=UniqueStore, dest='struct_link',
                               help='linking a struct, <contractName>:<number>=<contractName>')
    optional_args.add_argument("--toolOutput", type=type_tool_output_path, action=UniqueStore, dest='tool_output',
                               help="Path to a directory at which tool output files will be saved")
    optional_args.add_argument("--path", type=type_dir, action=UniqueStore,
                               help='Use the given path as the root of the source tree instead of the root of the '
                                    'filesystem. Default: $PWD/contracts if exists, else $PWD')
    optional_args.add_argument("--javaArgs", type=type_java_arg, action='append', dest='java_args',
                               help='arguments to pass to the .jar file')
    optional_args.add_argument("--settings", type=type_settings_arg, action='append',
                               help='advanced settings. To view, use --advanced_help')

    # Currently the jar can only accepts a single rule with -rule
    optional_args.add_argument("--rule", action=UniqueStore, help="Name of a specific rule you want to verify.")
    optional_args.add_argument("--method", action=UniqueStore,
                               help="Parametric rules will only verify given method. Usage: --method 'fun(int,bool)'")
    optional_args.add_argument("--loop_iter", type=type_non_negative_integer, action=UniqueStore,
                               help="The maximal number of loop iterations we verify for. Default: 1")

    # Package arguments (mutually exclusive)
    optional_args.add_argument("--packages_path", type=type_dir, action=UniqueStore,
                               help="Path to a directory including solidity packages (default: $NODE_PATH)")
    optional_args.add_argument("--packages", nargs='+', type=type_package, action=UniqueStore,
                               help='A mapping [package_name=path, ...]')

    optional_args.add_argument("--internal_funcs", type=type_input_file, action=UniqueStore,
                               help="A json file containing a map from public function signatures to internal "
                                    "function signatures for function finding purposes")

    """
    Behavior:
    if --cloud is not used, args.cloud is None
    if --cloud is used without an argument, arg.cloud == DEFAULT_CLOUD_ENV (currently 'production')
    if --cloud is used with an argument, stores it under args.cloud
    same for --staging, except the default is 'master'
    """
    optional_args.add_argument("--staging", nargs='?', action=UniqueStore, const=DEFAULT_STAGING_ENV,
                               help="name of the environment to run on the amazon server")
    optional_args.add_argument("--cloud", nargs='?', action=UniqueStore, const=DEFAULT_CLOUD_ENV,
                               help="name of the environment to run on the amazon server")

    optional_args.add_argument("--debug", action='store_true', help="Use this flag to see debug prints")
    optional_args.add_argument("--no_compare", action='store_true', help="Do not compare the verification results with "
                                                                         "expected.json")

    # --version was handled before, it is here just for the help message
    optional_args.add_argument('--version', action='version', help='show the tool version',
                               version='This message should never be reached')

    # Hidden flags

    # user for debugging the build only
    parser.add_argument('--build_only', action='store_true', help=argparse.SUPPRESS)

    # used for debugging command line option parsing.
    parser.add_argument('--check_args', action='store_true', help=argparse.SUPPRESS)

    # A setting for disabling the local type checking (e.g., if we have a bug in the jar published with the python and
    # want users not to get stuck and get the type checking from the cloud instead).
    parser.add_argument('--disableLocalTypeChecking', action='store_true', help=argparse.SUPPRESS)

    parser.add_argument('--queue_wait_minutes', type=type_non_negative_integer, action=UniqueStore,
                        help=argparse.SUPPRESS)
    parser.add_argument('--max_poll_minutes', type=type_non_negative_integer, action=UniqueStore,
                        help=argparse.SUPPRESS)
    parser.add_argument('--log_query_frequency_seconds', type=type_non_negative_integer, action=UniqueStore,
                        help=argparse.SUPPRESS)
    parser.add_argument('--max_attempts_to_fetch_output', type=type_non_negative_integer, action=UniqueStore,
                        help=argparse.SUPPRESS)
    parser.add_argument('--delay_fetch_output_seconds', type=type_non_negative_integer, action=UniqueStore,
                        help=argparse.SUPPRESS)
    parser.add_argument('--process', action=UniqueStore, default='emv', help=argparse.SUPPRESS)
    return parser


def get_args(args_list: Optional[List[str]] = None) -> argparse.Namespace:
    if args_list is None:
        args_list = sys.argv

    '''
    Why do we handle --version before argparse?
    Because on some platforms, mainly CI tests, we cannot fetch the installed distribution package version of
    certora-cli. We want to calculate the version lazily, only when --version was invoked.
    We do it pre-argparse, because we do not care bout the input validity of anything else if we have a --version flag
    '''
    handle_version_flag(args_list)

    pre_arg_fetching_checks(args_list)
    parser = __get_argparser()

    # if there is a --help flag, we want to ignore all parsing errors, even those before it:
    for arg in args_list:
        if arg == '--help':
            parser.print_help()
            exit(0)

    args = parser.parse_args(args_list)

    __remove_parsing_whitespace(args_list)

    flatten_arg_lists(args)

    check_mode_of_operation(args)  # Here args.mode is set

    if args.mode == Mode.CONF:
        read_from_conf(args)
    else:
        # Store current options
        current_conf_to_file(args)

    check_args_post_argparse(args)

    debug_print("parsed args successfully.")
    debug_print(f"args= {args}")
    if args.check_args:
        exit(0)
    return args


def main() -> None:
    main_with_args(sys.argv[1:])


if __name__ == '__main__':
    main()
