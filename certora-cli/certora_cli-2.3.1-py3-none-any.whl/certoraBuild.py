import json
import os
import traceback
from Crypto.Hash import keccak
import shutil
import re
import argparse
import subprocess
import sys
from collections import OrderedDict
from certora_cli.certoraUtils import debug_print_, read_json_file  # type: ignore
from typing import Any, Dict, List, Tuple, Optional, Set
from certora_cli.certoraUtils import safe_create_dir, get_file_basename, get_file_extension, prepare_call_args
from certora_cli.certoraUtils import OPTION_OUTPUT_VERIFY, fatal_error, is_windows, remove_and_recreate_dir, getcwd, as_posix
from certora_cli.certoraUtils import CERTORA_CONFIG_DIR, CERTORA_BUILD_FILE, CERTORA_VERIFY_FILE
from certora_cli.certoraUtils import is_hex, decimal_str_to_cvt_compatible, hex_str_to_cvt_compatible

BUILD_IS_LIBRARY = False
DEBUG = False


def exit_if_not_library(code: int) -> None:
    if BUILD_IS_LIBRARY:
        return
    else:
        sys.exit(code)


def fatal_error_if_not_library(msg: str) -> None:
    if BUILD_IS_LIBRARY:
        print(msg)
        raise Exception(msg)
    else:
        fatal_error(msg)


def print_failed_to_run(cmd: str) -> None:
    print()
    print(f"Failed to run {cmd}")
    if is_windows() and cmd.find('solc') != -1 and cmd.find('exe') == -1:
        print("did you forget the .exe extension for solcXX.exe??")
    print()


def run_cmd(cmd: str, name: str, config_path: str, input: bytes = None, shell: bool = False, debug: bool = False) \
        -> None:

    debug_print_(f"Running cmd {cmd}", debug)

    stdout_name = f"{config_path}/{name}.stdout"
    stderr_name = f"{config_path}/{name}.stderr"
    debug_print_(f"stdout, stderr = {stdout_name}, {stderr_name}", debug)

    with open(stdout_name, 'w+') as stdout:
        with open(stderr_name, 'w+') as stderr:
            try:
                args = prepare_call_args(cmd)
                if shell:
                    shell_args = ' '.join(args)
                    exitcode = subprocess.run(shell_args, stdout=stdout, stderr=stderr,
                                              input=input, shell=shell).returncode
                else:
                    exitcode = subprocess.run(args, stdout=stdout, stderr=stderr, input=input, shell=shell).returncode
                if exitcode:
                    msg = f"Failed to run {cmd}, exit code {exitcode}"
                    with open(stderr_name, 'r') as stderr_read:
                        for line in stderr_read:
                            print(line)
                    raise Exception(msg)
                else:
                    debug_print_(f"Exitcode {exitcode}", debug)
            except Exception as e:
                print(f"Error: {e}")
                print_failed_to_run(cmd)
                raise


def debug_print(s: str) -> None:
    debug_print_(s, DEBUG)


class InputConfig:
    def __init__(self, args: argparse.Namespace) -> None:
        """
        A class holding relevant attributes for the build string.
        :param args: command line input argument in an argparse.Namespace
        """

        self.parsed_options = args  # type: argparse.Namespace

        # populate fields relevant for build, handle defaults
        self.files = args.file_paths
        self.solc = args.solc
        self.solc_args = args.solc_args
        self.packages = args.packages
        self.verify = args.verify
        self.assert_contracts = args.assert_contracts
        self.path = args.path
        self.debug = args.debug
        self.link = args.link
        self.struct_link = args.struct_link
        self.internal_functions = args.internal_funcs

        if args.solc_map is not None:
            self.solc_mappings = args.solc_map  # type: Dict[str, str]
        else:
            self.solc_mappings = {}

        if args.address is not None:
            self.address = args.address  # type: Dict[str, int]
        else:
            self.address = dict()

        self.fileToContractName = args.file_to_contract


class SolidityType:
    def __init__(self,
                 base_type: str,  # The source code representation of the base type (e.g., the base type of A[][] is A)
                 components: List[Any],  # List[SolidityType]
                 array_dims: List[int],
                 # If this is an array, the i-th element is its i-th dimension size; -1 denotes a dynamic array
                 is_storage: bool,  # Whether it's a storage pointer (only applicable to library functions)
                 is_tuple: bool,  # Whether it's a tuple or a user-defined struct
                 is_address_alias: bool,  # Whether it's an alias of address type (e.g., contract, 'address payable')
                 is_uint8_alias: bool,  # Whether it's an alias of uint8 type (e.g., enum)
                 lib_canonical_signature: str = None
                 # If this is a library function param, this signature used to compute the sighash of the function
                 ):
        self.base_type = base_type
        self.components = components
        self.array_dims = array_dims
        self.is_storage = is_storage
        self.is_tuple = is_tuple
        self.is_address_alias = is_address_alias
        self.is_uint8_alias = is_uint8_alias
        self.lib_canonical_signature = lib_canonical_signature

    def as_dict(self) -> Dict[str, Any]:
        return {
            "baseType": self.base_type,
            "components": [x.as_dict() for x in self.components],
            "arrayDims": self.array_dims,
            "isStorage": self.is_storage,
            "isTuple": self.is_tuple,
            "isAddressAlias": self.is_address_alias,
            "isUint8Alias": self.is_uint8_alias
        }

    def __repr__(self) -> str:
        return repr(self.as_dict())

    def array_dims_signature(self) -> str:
        return "".join([(lambda x: "[]" if (x == -1) else f"[{x}]")(dim_size) for dim_size in self.array_dims[::-1]])

    def canonical_tuple_signature(self) -> str:
        return "(" + ",".join([x.signature() for x in self.components]) + ")"

    # Returns a signature in a "canonical form", namely without user-defined types and with decomposed struct members
    def signature(self) -> str:
        base_type_str = self.lib_canonical_signature if self.lib_canonical_signature is not None else (
            "uint8" if self.is_uint8_alias else (self.canonical_tuple_signature() if self.is_tuple else (
                "address" if self.is_address_alias else self.base_type)))
        return base_type_str + self.array_dims_signature() + (" storage" if self.is_storage else "")

    # Returns a signature with user-defined types
    def source_code_signature(self) -> str:
        return self.base_type + self.array_dims_signature() + (" storage" if self.is_storage else "")


class Func:
    def __init__(self,
                 name: str,
                 fullArgs: List[SolidityType],
                 returns: List[SolidityType],
                 sighash: str,
                 notpayable: bool,
                 isABI: bool,
                 fromLib: bool,  # not serialized
                 isConstructor: bool,  # not serialized
                 stateMutability: Dict[str, str]
                 ):
        self.name = name
        self.fullArgs = fullArgs
        self.returns = returns
        self.sighash = sighash
        self.notpayable = notpayable
        self.isABI = isABI
        self.fromLib = fromLib
        self.isConstructor = isConstructor
        self.stateMutability = stateMutability
        self.sighashIsFromOtherName = any([a.lib_canonical_signature is not None for a in fullArgs])

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "fullArgs": list(map(lambda x: x.as_dict(), self.fullArgs)),
            "returns": list(map(lambda x: x.as_dict(), self.returns)),
            "sighash": self.sighash,
            "notpayable": self.notpayable,
            "isABI": self.isABI,
            "stateMutability": self.stateMutability,
            "sighashIsFromOtherName": self.sighashIsFromOtherName
        }

    def __repr__(self) -> str:
        return repr(self.as_dict())

    def signature(self) -> str:
        return Func.compute_signature(self.name, self.fullArgs, lambda x: x.signature())

    def source_code_signature(self) -> str:
        return Func.compute_signature(self.name, self.fullArgs, lambda x: x.source_code_signature())

    @staticmethod
    def compute_signature(name: str, args: List[SolidityType], signature_getter: Any) -> str:
        return name + "(" + ",".join([signature_getter(x) for x in args]) + ")"


class ImmutableReference:
    def __init__(self, offset: str, length: str, varname: str):
        self.offset = offset
        self.length = length
        self.varname = varname

    def as_dict(self) -> Dict[str, Any]:
        return {
            "offset": self.offset,
            "length": self.length,
            "varname": self.varname
        }

    def __repr__(self) -> str:
        return repr(self.as_dict())


class PresetImmutableReference(ImmutableReference):
    def __init__(self,
                 offset: str,
                 length: str,
                 varname: str,
                 value: str
                 ):
        ImmutableReference.__init__(self, offset, length, varname)
        self.value = value

    def as_dict(self) -> Dict[str, Any]:
        _dict = ImmutableReference.as_dict(self)
        _dict["value"] = self.value
        return _dict

    def __repr__(self) -> str:
        return repr(self.as_dict())


# Python3.5 to which we maintain backward-compatibility due to CI's docker image, does not support @dataclass
class ContractInSDC:
    def __init__(self, name: str, original_file: str, file: str, address: str, methods: Set[Any], bytecode: str,
                 constructor_bytecode: str,
                 srcmap: str, varmap: Any, storageLayout: Any, immutables: List[ImmutableReference],
                 internal_functions: Dict[str, str]):
        self.name = name
        self.original_file = original_file
        self.file = file
        self.address = address
        self.methods = methods
        self.bytecode = bytecode
        self.constructor_bytecode = constructor_bytecode
        self.srcmap = srcmap
        self.varmap = varmap
        self.storageLayout = storageLayout
        self.immutables = immutables
        self.internal_functions = internal_functions

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "original_file": self.original_file,
            "file": self.file,
            "address": self.address,
            "methods": list(map(lambda x: x.as_dict(), self.methods)),
            "bytecode": self.bytecode,
            "constructorBytecode": self.constructor_bytecode,
            "srcmap": self.srcmap,
            "varmap": self.varmap,
            "storageLayout": self.storageLayout,
            "immutables": list(map(lambda x: x.as_dict(), self.immutables)),
            "internalFunctions": self.internal_functions
        }

    def __repr__(self) -> str:
        return repr(self.as_dict())


class SDC:
    def __init__(self, primary_contract: str, primary_contract_address: str, sdc_origin_file: str,
                 original_src_list: Dict[Any, Any], src_list: Dict[Any, Any], sdc_name: str,
                 contracts: List[ContractInSDC], library_addresses: List[str], generated_with: str,
                 state: Dict[str, str], struct_linking_info: Dict[str, str]):
        self.primary_contract = primary_contract
        self.primary_contract_address = primary_contract_address
        self.sdc_origin_file = sdc_origin_file
        self.original_srclist = original_src_list
        self.srclist = src_list
        self.sdc_name = sdc_name
        self.contracts = contracts
        self.library_addresses = library_addresses
        self.generated_with = generated_with
        self.state = state
        self.structLinkingInfo = struct_linking_info

    def as_dict(self) -> Dict[str, Any]:
        return {
            "primary_contract": self.primary_contract,
            "primary_contract_address": self.primary_contract_address,
            "sdc_origin_file": self.sdc_origin_file,
            "original_srclist": self.original_srclist,
            "srclist": self.srclist,
            "sdc_name": self.sdc_name,
            "contracts": list(map(lambda x: x.as_dict(), self.contracts)),
            "library_addresses": self.library_addresses,
            "generated_with": self.generated_with,
            "state": self.state,
            "structLinkingInfo": self.structLinkingInfo,
        }


class CertoraBuildGenerator:
    def __init__(self, input_config: InputConfig) -> None:
        self.input_config = input_config
        # SDCs describes the set of all 'Single Deployed Contracts' the solidity file whose contracts comprise a single
        # bytecode of interest. Which one it is - we don't know yet, but we make a guess based on the base filename.
        # An SDC corresponds to a single solidity file.
        self.SDCs = {}  # type: Dict[str, SDC]

        # Note that the the last '/' in config_path is important for solc to succeed, so it should be added
        self.config_path = f"{getcwd()}/{CERTORA_CONFIG_DIR}"
        self.library_addresses = []  # type: List[str]

        # ASTs will be lazily loaded
        self.asts = {}  # type: Dict[str, Dict[str, Dict[int, Any]]]
        remove_and_recreate_dir(self.config_path)

        self.address_generator_idx = 0

    @staticmethod
    def CERTORA_CONTRACT_NAME() -> str:
        return "certora_contract_name"

    def collect_funcs(self, data: Dict[str, Any], contract_file: str,
                      contract_name: str, original_file: str) -> Set[Func]:

        constructor_string = "constructor"

        def is_imported_abi_entry(x: Dict[str, Any]) -> bool:
            return x["type"] == "function" or x["type"] == constructor_string

        def get_abi_entry_name(x: Dict[str, Any]) -> str:
            if x["type"] == "function":
                return x["name"]
            elif x["type"] == constructor_string:
                return constructor_string
            else:
                return ""  # Should be unreachable

        def collect_func_source_code_signatures_from_abi() -> List[str]:
            func_signatures = []
            abi = data["abi"]  # ["contracts"][contract_file][contract_name]["abi"]
            debug_print(abi)
            for f in filter(lambda x: is_imported_abi_entry(x), abi):
                inputs = f["inputs"]
                name = get_abi_entry_name(f)
                debug_print(f"ABI {name}")
                func_signatures.append(name + "(" + ",".join(
                    [input["internalType"] if "internalType" in input else input["type"] for input in inputs]) + ")")
            return func_signatures

        def get_getter_func_node_from_abi(state_var_name: str) -> Dict[str, Any]:
            abi = data["abi"]  # ["contracts"][contract_file][contract_name]["abi"]
            abi_getter_nodes = [g for g in
                                filter(lambda x: x["type"] == "function" and x["name"] == state_var_name, abi)]

            assert len(abi_getter_nodes) != 0, \
                f"Failed to find a getter function of the state variable {state_var_name} in the ABI"
            assert len(abi_getter_nodes) == 1, \
                f"Found multiple candidates for a getter function of the state variable {state_var_name} in the ABI"

            return abi_getter_nodes[0]

        def collect_array_type_from_abi_rec(type_str: str, dims: List[int]) -> str:
            outer_dim = re.findall(r"\[\d*]$", type_str)
            if outer_dim:
                type_rstrip_dim = re.sub(r"\[\d*]$", '', type_str)
                if len(outer_dim[0]) == 2:
                    dims.append(-1)  # dynamic array
                else:
                    assert len(outer_dim[0]) > 2, f"Expected to find a fixed-size array, but found {type_str}"
                    dims.append(int(re.findall(r"\d+", outer_dim[0])[0]))
                return collect_array_type_from_abi_rec(type_rstrip_dim, dims)
            return type_str

        # Returns (list of array dimensions' lengths, the base type of the array)
        def collect_array_type_from_abi(type_str: str) -> Tuple[List[int], str]:
            dims = []  # type: List[int]
            base_type = collect_array_type_from_abi_rec(type_str, dims)
            return dims, base_type

        # Gets the SolidityType of a function parameter (either input or output) from the ABI
        def get_solidity_type_from_abi(abi_param_entry: Dict[str, Any]) -> SolidityType:
            assert "type" in abi_param_entry, f"Invalid ABI function parameter entry: {abi_param_entry}"

            is_tuple = "components" in abi_param_entry and len(abi_param_entry["components"]) > 0
            if is_tuple:
                components = [get_solidity_type_from_abi(x) for x in abi_param_entry["components"]]
            else:
                components = []

            array_dims, base_type = collect_array_type_from_abi(abi_param_entry["type"])

            internal_type_exists = "internalType" in abi_param_entry
            if internal_type_exists:
                array_dims_internal, internal_base_type = collect_array_type_from_abi(abi_param_entry["internalType"])
                assert array_dims_internal == array_dims
                is_address_alias = base_type == "address" and internal_base_type != base_type
                is_uint8_alias = base_type == "uint8" and internal_base_type != base_type
            else:
                internal_base_type = ""
                is_address_alias = False
                is_uint8_alias = False

            return SolidityType(
                internal_base_type if internal_type_exists else base_type,
                components,
                array_dims,
                False,  # ABI functions cannot have storage references as parameters
                is_tuple,
                is_address_alias,
                is_uint8_alias
            )

        def get_external_public_func_def_nodes(contract_file_ast: Dict[int, Any]) -> List[Dict[str, Any]]:
            fun_defs_in_file = [contract_file_ast[node_id] for node_id in filter(
                lambda node_id: "nodeType" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["nodeType"] == "FunctionDefinition" and
                                (("kind" in contract_file_ast[node_id] and
                                  (contract_file_ast[node_id]["kind"] == "function" or contract_file_ast[node_id][
                                      "kind"] == constructor_string)) or
                                 ("isConstructor" in contract_file_ast[node_id] and
                                  contract_file_ast[node_id]["isConstructor"] is False and
                                  "name" in contract_file_ast[node_id] and
                                  contract_file_ast[node_id]["name"] != "")) and  # Not the fallback function (< solc6)
                                "visibility" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["visibility"] in ["public", "external"], contract_file_ast)]

            assert all(self.CERTORA_CONTRACT_NAME() in fd for fd in fun_defs_in_file)

            fun_defs_in_given_contract = [fd for fd in fun_defs_in_file if fd[self.CERTORA_CONTRACT_NAME()] == c_name]
            return fun_defs_in_given_contract

        def get_public_state_var_def_nodes(contract_file_ast: Dict[int, Any]) -> List[Dict[str, Any]]:
            public_var_defs_in_file = [contract_file_ast[node_id] for node_id in filter(
                lambda node_id: "nodeType" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["nodeType"] == "VariableDeclaration" and
                                "visibility" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["visibility"] == "public" and
                                "stateVariable" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["stateVariable"] is True, contract_file_ast)]

            assert all(self.CERTORA_CONTRACT_NAME() in vd for vd in public_var_defs_in_file)

            var_defs_in_given_contract = [vd for vd in public_var_defs_in_file if
                                          vd[self.CERTORA_CONTRACT_NAME()] == c_name]
            return var_defs_in_given_contract

        def is_library_def_node(file: str, node_ref: int) -> bool:
            contract_def_node = self.asts[original_file][file][node_ref]
            return "contractKind" in contract_def_node and contract_def_node["contractKind"] == "library"

        def get_contract_def_node_ref() -> int:
            contract_file_ast = self.asts[original_file][contract_file]
            contract_def_refs = [node_id for node_id in filter(
                lambda node_id: "nodeType" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["nodeType"] == "ContractDefinition" and
                                "name" in contract_file_ast[node_id] and
                                contract_file_ast[node_id]["name"] == contract_name, contract_file_ast)]

            assert len(contract_def_refs) != 0, \
                f'Failed to find a "ContractDefinition" ast node id for the contract {contract_name}'
            assert len(
                contract_def_refs) == 1, f'Found multiple "ContractDefinition" ast node ids for the same contract ' \
                                         f'{contract_name}: {contract_def_refs}'
            return contract_def_refs[0]

        def retrieve_base_contracts_list_rec(base_contracts_queue: List[Any],
                                             base_contracts_lst: List[Tuple[str, str, bool]]) -> None:
            (curr_contract_file, curr_contract_def_node_ref) = base_contracts_queue.pop()

            curr_contract_def = self.asts[original_file][curr_contract_file][curr_contract_def_node_ref]
            assert "baseContracts" in curr_contract_def, \
                f'Got a "ContractDefinition" ast node without a "baseContracts" key: {curr_contract_def}'
            for bc in curr_contract_def["baseContracts"]:
                assert "nodeType" in bc and bc["nodeType"] == "InheritanceSpecifier"
                assert "baseName" in bc and "referencedDeclaration" in bc["baseName"]
                next_bc_ref = bc["baseName"]["referencedDeclaration"]
                next_bc = get_contract_file_of(next_bc_ref)
                if next_bc not in base_contracts_lst:
                    base_contracts_lst.append((next_bc, self.asts[original_file][next_bc][next_bc_ref]["name"],
                                               is_library_def_node(next_bc, next_bc_ref)))
                    base_contracts_queue.insert(0, (next_bc, bc["baseName"]["referencedDeclaration"]))

            if base_contracts_queue:
                retrieve_base_contracts_list_rec(base_contracts_queue, base_contracts_lst)

        # For each base contract, returns (base_contract_file, base_contract_name)
        def retrieve_base_contracts_list() -> List[Tuple[str, str, bool]]:
            contract_def_node_ref = get_contract_def_node_ref()
            base_contracts_queue = [(contract_file, contract_def_node_ref)]
            base_contracts_lst = [
                (contract_file, contract_name, is_library_def_node(contract_file, contract_def_node_ref))]
            retrieve_base_contracts_list_rec(base_contracts_queue, base_contracts_lst)
            return base_contracts_lst

        def get_original_def_node(reference: int) -> Dict[str, Any]:
            return self.asts[original_file][get_contract_file_of(reference)][reference]

        def get_contract_file_of(reference: int) -> str:
            original_file_asts = self.asts[original_file]
            for contract in original_file_asts:
                if reference in original_file_asts[contract]:
                    return contract
            # error if got here
            fatal_error_if_not_library(f"Could not find reference AST node {reference}")
            return ""

        def get_function_selector(f_entry: Dict[str, Any], f_name: str,
                                  input_types: List[SolidityType]) -> str:
            if "functionSelector" in f_entry:
                return f_entry["functionSelector"]

            f_base = Func.compute_signature(f_name, input_types, lambda x: x.signature())

            assert f_base in data["evm"]["methodIdentifiers"], \
                f"Was about to compute the sighash of {f_name} based on the signature {f_base}.\n" \
                f"Expected this signature to appear in \"methodIdentifiers\"."

            f_hash = keccak.new(digest_bits=256)
            f_hash.update(str.encode(f_base))

            result = f_hash.hexdigest()[0:8]
            expected_result = data["evm"]["methodIdentifiers"][f_base]

            assert expected_result == result, \
                f"Computed the sighash {result} of {f_name} based on a (presumably) correct signature ({f_base}), " \
                f"but got an incorrect result. Expected result: {expected_result}"

            return result

        def collect_array_type_from_type_name_rec(type_name: Dict[str, Any], dims: List[int]) -> Dict[str, Any]:
            """
            Returns the base type (node) of the specified array type, e.g., returns A for A[][3][]
            @param type_name:
            @param dims:
            @return:
            """
            assert "nodeType" in type_name, f"Expected a \"nodeType\" key, but got {type_name}"
            if type_name["nodeType"] == "ArrayTypeName":
                if "length" in type_name:
                    length = type_name["length"]
                    if type(length) is dict and "value" in length:
                        dims.append(int(length["value"]))  # Fixed-size array
                    else:
                        dims.append(-1)  # Dynamic array
                else:  # Dynamic array (in solc7)
                    dims.append(-1)
                assert "baseType" in type_name, f"Expected an array type with a \"baseType\" key, but got {type_name}"
                return collect_array_type_from_type_name_rec(type_name["baseType"], dims)

            return type_name

        def collect_array_type_from_type_name(type_name: Dict[str, Any]) -> Tuple[List[int], Dict[str, Any]]:
            """
            Returns (list of array type dimensions, ast node of the array's base type).
            E.g., Returns ([-1, 3, -1], A) for A[][3][].
            If given a non-array type A, returns ([],A)
            @param type_name:
            @return:
            """
            assert "nodeType" in type_name, f"Expected a \"nodeType\" key, but got {type_name}"
            dims = []  # type: List[int]
            if type_name["nodeType"] == "ArrayTypeName":
                base_type_node = collect_array_type_from_type_name_rec(type_name, dims)
            else:
                base_type_node = type_name
            return dims, base_type_node

        def is_payable_address_type(base_type_node: Dict[str, Any]) -> bool:
            if "stateMutability" in base_type_node:
                assert "name" in base_type_node and base_type_node["name"] == "address", \
                    f"Expected an address type, but got {base_type_node}"

                assert base_type_node["stateMutability"] == "nonpayable" or \
                       base_type_node["stateMutability"] == "payable"

                return base_type_node["stateMutability"] == "payable"

            return False

        def get_solidity_type_from_ast_param(p: Dict[str, Any]) -> SolidityType:
            assert "typeName" in p, f"Expected a \"typeName\" key, but got {p}"
            (array_dims, base_type_node) = collect_array_type_from_type_name(p["typeName"])

            base_type_is_user_defined = base_type_node["nodeType"] == "UserDefinedTypeName"
            lib_canonical_base_type_str = None  # Used to compute the function sighash in case of a library function
            if base_type_is_user_defined:
                orig_user_defined_type = get_original_def_node(base_type_node["referencedDeclaration"])
                is_valid_node = orig_user_defined_type is not None and "nodeType" in orig_user_defined_type
                is_struct = is_valid_node and orig_user_defined_type["nodeType"] == "StructDefinition"
                is_contract = is_valid_node and orig_user_defined_type["nodeType"] == "ContractDefinition"
                is_enum = is_valid_node and orig_user_defined_type["nodeType"] == "EnumDefinition"
                if c_is_lib:
                    if "canonicalName" in orig_user_defined_type:  # prefer the "canonicalName", if available
                        lib_canonical_base_type_str = orig_user_defined_type["canonicalName"]
                    elif "name" in orig_user_defined_type:
                        lib_canonical_base_type_str = orig_user_defined_type["name"]
            else:
                is_struct = False
                is_contract = False
                is_enum = False

            is_payable_address = is_payable_address_type(base_type_node)

            # For a struct parameter, recursively add a solidity type to its components list for each of its members.
            def collect_struct_member_types() -> List[SolidityType]:
                components = []
                if is_struct:
                    struct_def_node_id = base_type_node["referencedDeclaration"]
                    struct_def_node = get_original_def_node(struct_def_node_id)  # type: Dict[str, Any]
                    assert ("nodeType" in struct_def_node and struct_def_node["nodeType"] == "StructDefinition")

                    if not struct_def_node:
                        fatal_error(f"Expected to find a definition of {base_type_str} in the contracts asts")

                    # Proceed recursively on each member of the struct
                    components.extend(
                        [get_solidity_type_from_ast_param(struct_member) for struct_member in
                         struct_def_node["members"]])

                return components

            base_type_str = base_type_node["typeDescriptions"]["typeString"]
            is_storage_ref = p["storageLocation"] == "storage"
            return SolidityType(base_type_str, collect_struct_member_types(), array_dims, is_storage_ref,
                                is_struct, is_contract or is_payable_address, is_enum, lib_canonical_base_type_str)

        def is_constructor_func(name: str) -> bool:
            # Turns out constructor is a function with no name
            return name == ""

        def is_abi_func(name: str, input_arg_types: List[SolidityType],
                        out_arg_types: List[SolidityType]) -> bool:
            return (is_constructor_func(name) or Func.compute_signature(
                name, input_arg_types, lambda x: x.source_code_signature()
            ) in abi_func_signatures or Func.compute_signature(
                name, input_arg_types, lambda x: x.signature()
            ) in abi_func_signatures) and not (
                # if a function is in library and any argument is of storage, then it's not ABI.
                any([arg.is_storage for arg in input_arg_types]) or any([arg.is_storage for arg in out_arg_types])
            )

        abi_func_signatures = collect_func_source_code_signatures_from_abi()
        funcs = set()
        collected_func_selectors = set()
        base_contract_files = retrieve_base_contracts_list()  # List[str]
        for c_file, c_name, c_is_lib in base_contract_files:
            if c_is_lib:
                debug_print(f"{c_name} is a library")
            for func_def in get_external_public_func_def_nodes(self.asts[original_file][c_file]):
                func_name = func_def["name"]
                params = [p for p in func_def["parameters"]["parameters"]]
                solidity_type_args = [get_solidity_type_from_ast_param(p) for p in params]
                is_constructor = is_constructor_func(func_name)

                if not is_constructor:
                    func_selector = get_function_selector(func_def, func_name, solidity_type_args)
                    if func_selector in collected_func_selectors:
                        continue
                    collected_func_selectors.add(func_selector)
                else:
                    func_name = constructor_string
                    func_selector = "0"  # constructor doesn't have calldata (!!) so it doesn't really matter what we
                    # put here

                # Refer to https://github.com/OpenZeppelin/solidity-ast/blob/master/schema.json for more info
                return_params = func_def["returnParameters"]["parameters"]
                solidity_type_outs = [get_solidity_type_from_ast_param(p) for p in return_params]

                is_abi = is_abi_func(func_name, solidity_type_args, solidity_type_outs)

                func = Func(
                    func_name,
                    solidity_type_args,
                    solidity_type_outs,
                    func_selector,
                    func_def["stateMutability"] in ["nonpayable", "view", "pure"],
                    is_abi,
                    c_is_lib,
                    is_constructor,
                    {"keyword": func_def["stateMutability"]}
                )
                funcs.add(func)
                debug_print(f"Function {func}")

                if not is_abi:
                    debug_print(
                        f"Added an instance of the function {func.source_code_signature()} that is not part of the ABI")

            # Add automatically generated getter functions for public state variables.
            for public_state_var in get_public_state_var_def_nodes(self.asts[original_file][c_file]):
                getter_name = public_state_var["name"]
                debug_print(f"Getter {getter_name}")
                getter_abi_data = get_getter_func_node_from_abi(getter_name)

                params = [p for p in getter_abi_data["inputs"]]
                solidity_type_args = [get_solidity_type_from_abi(p) for p in params]

                getter_selector = get_function_selector(public_state_var, getter_name, solidity_type_args)
                if getter_selector in collected_func_selectors:
                    continue
                collected_func_selectors.add(getter_selector)

                return_params = [p for p in getter_abi_data["outputs"]]
                solidity_type_outs = [get_solidity_type_from_abi(p) for p in return_params]

                if "payable" not in getter_abi_data:
                    is_not_payable = False
                else:  # Only if something is definitely non-payable, we treat it as such
                    is_not_payable = not getter_abi_data["payable"]

                if "stateMutability" not in getter_abi_data:
                    state_mutability = "nonpayable"
                else:
                    state_mutability = getter_abi_data["stateMutability"]
                    # in solc6 there is no json field "payable", so we infer that if state_mutability is view or pure,
                    # then we're also non-payable by definition
                    # (state_mutability is also a newer field)
                    if not is_not_payable and state_mutability in ["view", "pure", "nonpayable"]:
                        is_not_payable = True  # definitely not payable

                is_abi = is_abi_func(getter_name, solidity_type_args, solidity_type_outs)

                funcs.add(
                    Func(
                        getter_name,
                        solidity_type_args,
                        solidity_type_outs,
                        getter_selector,
                        is_not_payable,
                        is_abi,
                        c_is_lib,
                        False,
                        {"keyword": state_mutability}
                    )
                )
                debug_print(f"Added an automatically generated getter function for {getter_name}")

        collected = [f.source_code_signature() for f in funcs if f.isABI and f.name != constructor_string]
        abi_funcs_cnt = len(collected)
        assert abi_funcs_cnt == len([f for f in abi_func_signatures if not f.startswith(constructor_string)]), \
            f"There are functions in the ABI that were not added. Added functions ({abi_funcs_cnt}): " \
            f"{collected}\n. Functions in ABI ({len(abi_func_signatures)}): {abi_func_signatures}"
        return funcs

    @staticmethod
    def collect_srcmap(data: Dict[str, Any]) -> Any:
        return data["evm"]["deployedBytecode"]["sourceMap"]  # data["contracts"][contract]["srcmap-runtime"]

    @staticmethod
    def collect_varmap(contract: str, data: Dict[str, Any]) -> Any:
        return data["contracts"][contract]["local-mappings"]

    @staticmethod
    def collect_storage_layout(data: Dict[str, Any]) -> Any:
        return data.get("storageLayout", None)

    def get_standard_json_data(self, sdc_name: str) -> Dict[str, Any]:
        return read_json_file("%s/%s.standard.json.stdout" % (self.config_path, sdc_name))

    @staticmethod
    def address_as_str(address: int) -> str:
        return "%0.40x" % address
        # ^ A 40 digits long hexadecimal string representation of address, filled by leading zeros

    def find_contract_address_str(self, contract_file: str, contract_name: str,
                                  contracts_with_chosen_addresses: List[Tuple[int, Any]]) -> str:
        address_and_contracts = [e for e in contracts_with_chosen_addresses
                                 if e[1] == f"{contract_file}:{contract_name}"]
        if len(address_and_contracts) == 0:
            msg = f"Failed to find a contract named {contract_name} in file {contract_file}. " \
                  f"Please make sure there is a file named like the contract, " \
                  f"or a file containing a contract with this name. Available contracts: " \
                  f"{','.join(map(lambda x: x[1], contracts_with_chosen_addresses))}"
            fatal_error_if_not_library(msg)
        address_and_contract = address_and_contracts[0]
        address = address_and_contract[0]
        contract = address_and_contract[1].split(":")[1]

        debug_print(f"Custom addresses: {self.input_config.address}, looking for a match of "
                    f"{address_and_contract} from {contract_name} in {self.input_config.address.keys()}")
        if contract_name in self.input_config.address.keys():
            address = self.input_config.address[contract_name]
            address = int(str(address), 0)
        debug_print(f"Candidate address for {contract} is {address}")
        # Can't have more than one! Otherwise we will have conflicting same address for different contracts
        assert len(set(address_and_contracts)) == 1
        return self.address_as_str(address)

    def collect_and_link_bytecode(self,
                                  contract_name: str,
                                  contracts_with_chosen_addresses: List[Tuple[int, Any]],
                                  bytecode: str,
                                  links: Dict[str, Any]
                                  ) -> str:
        debug_print(f"Working on contract {contract_name}")
        debug_print("Contracts with chosen addresses: %s" %
                    ([("0x%X" % x[0], x[1]) for x in contracts_with_chosen_addresses]))

        if links:
            # links are provided by solc as a map file -> contract -> (length, start)
            # flip the links from the "where" to the chosen contract address (based on file:contract).
            linked_bytecode = bytecode
            replacements = {}
            for link_file in links:
                for link_contract in links[link_file]:
                    for where in links[link_file][link_contract]:
                        replacements[where["start"]] = {"length": where["length"],
                                                        "address": self.find_contract_address_str(
                                                            link_file,
                                                            link_contract,
                                                            contracts_with_chosen_addresses)
                                                        }
            debug_print(f"Replacements= {replacements}")
            where_list = list(replacements.keys())
            where_list.sort()
            where_list.reverse()
            for where in where_list:
                offset = where * 2
                length = replacements[where]["length"] * 2
                addr = replacements[where]["address"]
                debug_print(f"replacing in {offset} of len {length} with {addr}")
                linked_bytecode = f"{linked_bytecode[0:offset]}{addr}{linked_bytecode[(offset + length):]}"
                self.library_addresses.append(addr)
            return linked_bytecode

        return bytecode

    def get_relevant_solc(self, contract: str) -> str:
        if contract in self.input_config.solc_mappings:
            base = self.input_config.solc_mappings[contract]
        else:
            base = self.input_config.solc
        if is_windows() and not base.endswith(".exe"):
            base = base + ".exe"
        debug_print(f"relevant solc is {base}")
        return base

    def get_extra_solc_args(self) -> str:
        if self.input_config.solc_args is not None:
            extra_solc_args = ' '.join(self.input_config.solc_args)
            return extra_solc_args
        return ""

    def standard_json(self, contract_file: str, remappings: List[str]) -> Dict[str, Any]:
        """
        when calling solc with the standard_json api, instead of passing it flags, we pass it json to request what we
        want -- currently we only use this to retrieve storage layout as this is the only way to do that,
        it would probably be good to migrate entirely to this API.
        @param contract_file:
        @param remappings:
        @return:
        """
        sources_dict = {contract_file: {"urls": [contract_file]}}
        solc_args = self.get_extra_solc_args()
        settings_dict = \
            {
                "remappings": remappings,
                "outputSelection": {
                    "*": {
                        "*": ["storageLayout", "abi", "evm.bytecode", "evm.deployedBytecode", "evm.methodIdentifiers"],
                        "": ["id", "ast"]
                    }
                }
            }

        def split_arg_hack(arg_name: str, args_: str) -> str:
            return args_.split(arg_name)[1].strip().split(" ")[0].strip()  # String-ops FTW

        EVM_VERSION = "--evm-version"
        OPTIMIZE = "--optimize"
        OPTIMIZE_RUNS = "--optimize-runs"

        if EVM_VERSION in solc_args:
            evmVersion = split_arg_hack(EVM_VERSION, solc_args)
            settings_dict["evmVersion"] = evmVersion
        if OPTIMIZE in solc_args or OPTIMIZE_RUNS in solc_args:
            enabled = OPTIMIZE in solc_args
            if OPTIMIZE_RUNS in solc_args:
                runs = int(split_arg_hack(OPTIMIZE_RUNS, solc_args))
                settings_dict["optimizer"] = {"enabled": enabled, "runs": runs}
            else:
                settings_dict["optimizer"] = {"enabled": enabled}

        result_dict = {"language": "Solidity", "sources": sources_dict, "settings": settings_dict}
        # debug_print("Standard json input")
        # debug_print(json.dumps(result_dict, indent=4))
        return result_dict

    def get_compilation_path(self, sdc_name: str) -> str:
        return "%s/%s" % (self.config_path, sdc_name)

    def build_srclist(self, data: Dict[str, Any], sdc_name: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        # srclist - important for parsing source maps
        srclist = {data["sources"][k]["id"]: k for k in data["sources"]}
        debug_print(f"Source list= {srclist}")

        fetched_srclist = {}

        map_idx_in_src_list_to_orig_file = {v: k for k, v in srclist.items()}
        for orig_file in map_idx_in_src_list_to_orig_file:
            idx_in_src_list = map_idx_in_src_list_to_orig_file[orig_file]

            # Copy contract_file to compilation path directory
            new_name = f"{idx_in_src_list}_{get_file_basename(orig_file)}.{get_file_extension(orig_file)}"
            shutil.copy2(orig_file,
                         f'{self.get_compilation_path(sdc_name)}/{new_name}')
            fetched_source = f'{sdc_name}/{new_name}'

            fetched_srclist[idx_in_src_list] = fetched_source

        return srclist, fetched_srclist

    def collect_asts(self, original_file: str, contract_sources: Dict[str, Dict[str, Any]]) -> None:
        """
        This function fetches the AST provided by solc and flattens it so that each node_id is mapped to a dict object,
        representing the node's contents.

        @param original_file: Path to a file
        @param contract_sources: represents the AST. Every sub-object with an "id" key is an AST node.
                                 The ast object is keyed by the original file for which we invoked solc.
        """

        def stamp_value_with_contract_name(popped_dict: Dict[str, Any], curr_value: Any) -> None:
            if isinstance(curr_value, dict):
                if popped_dict["nodeType"] == "ContractDefinition":
                    assert "name" in popped_dict
                    curr_value[self.CERTORA_CONTRACT_NAME()] = popped_dict["name"]
                elif self.CERTORA_CONTRACT_NAME() in popped_dict:
                    curr_value[self.CERTORA_CONTRACT_NAME()] = popped_dict[self.CERTORA_CONTRACT_NAME()]
            elif isinstance(curr_value, list):
                for node in curr_value:
                    stamp_value_with_contract_name(popped_dict, node)

        self.asts[original_file] = {}
        for c in contract_sources:
            debug_print(f"Adding ast of {original_file} for {c}")
            container = {}  # type: Dict[int, Any]
            self.asts[original_file][c] = container
            if "ast" not in contract_sources[c]:
                fatal_error_if_not_library(
                    f"Invalid AST format for original file {original_file} - "
                    f"got object that does not contain an \"ast\" {contract_sources[c]}")
            queue = [contract_sources[c]["ast"]]
            while queue:
                pop = queue.pop(0)
                if isinstance(pop, dict) and "id" in pop:
                    container[int(pop["id"])] = pop
                    for key, value in pop.items():
                        stamp_value_with_contract_name(pop, value)
                        if isinstance(value, dict):
                            queue.append(value)
                        if isinstance(value, list):
                            queue.extend(value)

    @staticmethod
    def get_node_from_asts(asts: Dict[str, Dict[str, Dict[int, Any]]], original_file: str, node_id: int) -> Any:
        debug_print(f"Available keys in ASTs: {asts.keys()}")
        debug_print(f"Available keys in AST of original file: {asts[original_file].keys()}")
        for contract_file in asts[original_file]:
            node = asts[original_file].get(contract_file, {}).get(node_id)
            if node is not None:
                debug_print(f"In original file {original_file} in contract file {contract_file} found for node id "
                            f"{node_id} the node {node}")
                return node  # Found the ast node of the given node_id
        return {}  # an ast node with the given node_id was not found

    def collect_immutables(self,
                           contract_data: Dict[str, Any],
                           original_file: str
                           ) -> List[ImmutableReference]:
        out = []
        immutable_references = contract_data["evm"]["deployedBytecode"].get("immutableReferences", [])
        # Collect and cache the AST(s). We collect the ASTs of ALL contracts' files that appear in
        # contract_sources; the reason is that a key of an item in immutableReferences
        # is an id of an ast node that may belong to any of those contracts.
        debug_print(f"Got immutable references in {original_file}: {immutable_references}")
        for astnode_id in immutable_references:
            astnode = self.get_node_from_asts(self.asts, original_file, int(astnode_id))
            name = astnode.get("name", None)
            if name is None:
                fatal_error_if_not_library(
                    f"immutable reference does not point to a valid ast node {astnode} in {original_file}, "
                    f"node id {astnode_id}"
                )

            debug_print(f"Name of immutable reference is {name}")
            for elem in immutable_references[astnode_id]:
                out.append(ImmutableReference(elem["start"], elem["length"], name))
        return out

    def address_generator(self) -> int:
        # 12,14,04,06,00,04,10 is 0xce4604a aka certora.
        const = (12 * 2 ** 24 + 14 * 2 ** 20 + 4 * 2 ** 16 + 6 * 2 ** 12 + 0 + 4 * 2 ** 4 + 10 * 2 ** 0)
        address = const * 2 ** 100 + self.address_generator_idx
        # Don't forget for addresses there are only 160 bits
        self.address_generator_idx += 1
        return address

    def collect_for_file(self, file: str, file_index: int, debug: bool = False) -> SDC:
        primary_contract = self.input_config.fileToContractName[file]
        sdc_name = f"{file.split('/')[-1]}_{file_index}"
        compilation_path = self.get_compilation_path(sdc_name)
        safe_create_dir(compilation_path, debug=debug)

        solc_ver_to_run = self.get_relevant_solc(primary_contract)
        file_abs_path = as_posix(os.path.abspath(file))

        # ABI and bin-runtime cmds preparation
        if self.input_config.packages is not None:
            remappings = self.input_config.packages
            debug_print(f"remappings={remappings}")
            paths_for_remappings = map(lambda remap: remap.split("=")[1], remappings)
            debug_print(f"paths_for_remappings={list(paths_for_remappings)}")

            join_remappings = ','.join(paths_for_remappings)

            debug_print(f"Join remappings: {join_remappings}")
            collect_cmd = f"{solc_ver_to_run} -o {compilation_path}/ --overwrite " \
                          f"--allow-paths {self.input_config.path},{join_remappings},. --standard-json"
        else:
            remappings = []
            collect_cmd = f"{solc_ver_to_run} -o {compilation_path}/ --overwrite " \
                          f"--allow-paths {self.input_config.path},. --standard-json"

        # Standard JSON
        input_for_solc = self.standard_json(file_abs_path, remappings)
        standard_json_input = json.dumps(input_for_solc).encode("utf-8")
        debug_print(f"about to run {collect_cmd}")
        debug_print(json.dumps(input_for_solc, indent=4))
        run_cmd(collect_cmd, f"{sdc_name}.standard.json", self.config_path, input=standard_json_input,
                shell=False, debug=DEBUG)

        debug_print(f"Collecting standard json: {collect_cmd}")
        standard_json_data = self.get_standard_json_data(sdc_name)
        debug_print("Standard json data")
        debug_print(json.dumps(standard_json_data, indent=4))

        for error in standard_json_data.get("errors", []):
            # is an error not a warning
            if error.get("severity", None) == "error":
                debug_print(f"Error: standard-json invocation of solc encountered an error: {error}")
                friendly_message = f"Got error from {solc_ver_to_run} of type {error['type']}:\n" \
                                   f"{error['formattedMessage']}"
                fatal_error_if_not_library(friendly_message)

        # load data
        data = standard_json_data  # Note we collected for just ONE file
        self.collect_asts(file, data["sources"])
        contracts_with_libraries = {}
        # Need to add all library dependencies that are in a different file:
        seen_link_refs = {file_abs_path}
        contract_work_list = [file_abs_path]
        while contract_work_list:
            contract_file = contract_work_list.pop()
            contract_list = sorted([c for c in data["contracts"][contract_file]])
            contracts_with_libraries[contract_file] = contract_list

            for contract_name in contract_list:
                contract_object = data["contracts"][contract_file][contract_name]
                link_refs = contract_object["evm"]["deployedBytecode"]["linkReferences"]
                for linkRef in link_refs:
                    if linkRef not in seen_link_refs:
                        contract_work_list.append(linkRef)
                        seen_link_refs.add(linkRef)

        debug_print(f"Contracts in {sdc_name}: {contracts_with_libraries[file_abs_path]}")
        contracts_with_chosen_addresses = \
            [(self.address_generator(), f"{contract_file}:{contract_name}") for contract_file, contract_list in
             sorted(contracts_with_libraries.items(), key=lambda entry: entry[0]) for contract_name in
             contract_list]  # type: List[Tuple[int, Any]]

        debug_print(f"Contracts with their chosen addresses: {contracts_with_chosen_addresses}")

        srclist, fetched_srclist = self.build_srclist(data, sdc_name)
        fetched_source = fetched_srclist[[idx for idx in srclist if srclist[idx] == contract_file][0]]
        contracts_in_sdc = []
        debug_print(f"finding primary contract address of {file_abs_path}:{primary_contract} in "
                    f"{contracts_with_chosen_addresses}")
        primary_contract_address = \
            self.find_contract_address_str(file_abs_path,
                                           primary_contract,
                                           contracts_with_chosen_addresses)
        debug_print(f"For contracts of primary {primary_contract}")

        for contract_file, contract_list in contracts_with_libraries.items():
            for contract_name in contract_list:
                contract_in_sdc = self.get_contract_in_sdc(
                    contract_file,
                    contract_name,
                    contracts_with_chosen_addresses,
                    data,
                    fetched_source,
                    primary_contract,
                    file
                )
                contracts_in_sdc.append(contract_in_sdc)

        debug_print(f"Contracts in SDC {sdc_name}: {contracts_in_sdc}")
        # Need to deduplicate the library_addresses list without changing the order
        deduplicated_library_addresses = list(OrderedDict.fromkeys(self.library_addresses))
        sdc = SDC(primary_contract,
                  primary_contract_address,
                  file,
                  srclist,
                  fetched_srclist,
                  sdc_name,
                  contracts_in_sdc,
                  deduplicated_library_addresses,
                  ' '.join(sys.argv),
                  {},
                  {})
        self.library_addresses.clear()  # Reset library addresses
        return sdc

    def get_bytecode(self,
                     bytecode_object: Dict[str, Any],
                     contract_name: str,
                     primary_contract: str,
                     contracts_with_chosen_addresses: List[Tuple[int, Any]],
                     fail_if_no_bytecode: bool
                     ) -> str:
        """
        Computes the linked bytecode object from the Solidity compiler output.
        First fetches the bytecode objects and then uses link references to replace library addresses.

        @param bytecode_object - the output from the Solidity compiler
        @param contract_name - the contract that we are working on
        @param contracts_with_chosen_addresses - a list of tuples of addresses and the
            associated contract identifier
        @param fail_if_no_bytecode - true if the function should fail if bytecode object is missing,
            false otherwise
        @returns linked bytecode object
        """
        # TODO: Only contract_name should be necessary. This requires a lot more test cases to make sure we're not
        # missing any weird solidity outputs.
        bytecode_ = bytecode_object["object"]
        bytecode = self.collect_and_link_bytecode(contract_name, contracts_with_chosen_addresses,
                                                  bytecode_, bytecode_object["linkReferences"])
        if contract_name == primary_contract and len(bytecode) == 0:
            msg = f"Contract {contract_name} has no bytecode. " \
                  f"It may be caused because the contract is abstract, " \
                  f"or is missing constructor code. Please check the output of the Solidity compiler."
            if fail_if_no_bytecode:
                fatal_error_if_not_library(f"Error: {msg}")
            else:
                debug_print(f"Warning: {msg}")

        debug_print(f"linked bytecode for {contract_name}: {bytecode}")
        return bytecode

    def get_contract_in_sdc(self,
                            contract_file: str,
                            contract_name: str,
                            contracts_with_chosen_addresses: List[Tuple[int, Any]],
                            data: Dict[str, Any],
                            fetched_source: str,
                            primary_contract: str,
                            original_file: str
                            ) -> ContractInSDC:
        contract_data = data["contracts"][contract_file][contract_name]
        debug_print(f"Name, File of contract: {contract_name}, {contract_file}")
        funcs = self.collect_funcs(contract_data, contract_file, contract_name, original_file)
        debug_print(f"Functions of {contract_name}: {funcs}")
        srcmap = self.collect_srcmap(contract_data)
        debug_print(f"Source maps of {contract_name}: {srcmap}")

        varmap = ""
        deployed_bytecode = self.get_bytecode(contract_data["evm"]["deployedBytecode"], contract_name, primary_contract,
                                              contracts_with_chosen_addresses, True)
        constructor_bytecode = self.get_bytecode(contract_data["evm"]["bytecode"], contract_name, primary_contract,
                                                 contracts_with_chosen_addresses, False)
        address = self.find_contract_address_str(contract_file,
                                                 contract_name,
                                                 contracts_with_chosen_addresses)
        storage_layout = \
            self.collect_storage_layout(contract_data)
        immutables = self.collect_immutables(contract_data, original_file)

        if self.input_config.internal_functions is not None:
            all_internal_functions: Dict[str, Any] = \
                read_json_file(self.input_config.internal_functions)
            debug_print_("Found all internal functions {}".format(all_internal_functions))
            if contract_name in all_internal_functions:
                internal_functions = all_internal_functions[contract_name]
            else:
                internal_functions = {}
        else:
            internal_functions = {}

        debug_print(f"Found internal functions for contract {contract_name}: {internal_functions}")

        return ContractInSDC(contract_name,
                             contract_file,
                             fetched_source,
                             address,
                             funcs,
                             deployed_bytecode,
                             constructor_bytecode,
                             srcmap,
                             varmap,
                             storage_layout,
                             immutables,
                             internal_functions
                             )

    @staticmethod
    def get_sdc_key(contract: str, address: str) -> str:
        return f"{contract}_{address}"

    @staticmethod
    def get_primary_contract_from_sdc(contracts: List[ContractInSDC], primary: str) -> List[ContractInSDC]:
        return [x for x in contracts if x.name == primary]

    def build(self) -> None:
        for i, f in enumerate(sorted(self.input_config.files)):
            debug_print(f"building file {f}")
            sdc = self.collect_for_file(f, i, self.input_config.debug)

            # First, add library addresses as SDCs too (they should be processed first)
            debug_print(f"Libraries to add = {sdc.library_addresses}")
            for library_address in sdc.library_addresses:
                library_contract_candidates = [contract for contract in sdc.contracts
                                               if contract.address == library_address]
                if len(library_contract_candidates) != 1:
                    fatal_error_if_not_library(
                        f"Error: Expected to have exactly one library address for {library_address}, "
                        f"got {library_contract_candidates}")

                library_contract = library_contract_candidates[0]
                debug_print(f"Found library contract {library_contract}")
                # TODO: What will happen to libraries with libraries?
                sdc_lib = SDC(library_contract.name,
                              library_address,
                              library_contract.original_file,
                              sdc.original_srclist,
                              sdc.srclist,
                              f"{sdc.sdc_name}_{library_contract.name}",
                              self.get_primary_contract_from_sdc(sdc.contracts, library_contract.name),
                              [],
                              sdc.generated_with,
                              {},
                              {})
                self.SDCs[self.get_sdc_key(sdc_lib.primary_contract, sdc_lib.primary_contract_address)] = sdc_lib

            # Filter out irrelevant contracts, now that we extracted the libraries, leave just the primary
            sdc.contracts = self.get_primary_contract_from_sdc(sdc.contracts, sdc.primary_contract)
            self.SDCs[self.get_sdc_key(sdc.primary_contract, sdc.primary_contract_address)] = sdc

        self.handle_links()
        self.handle_struct_links()

    def handle_links(self) -> None:
        # Link processing
        if self.input_config.link is not None:
            links = self.input_config.link
            for link in links:
                src, dst = link.split("=", 2)
                src_contract, reference_to_replace_with_link = src.split(":", 2)
                sources_to_update = self.get_matching_sdc_names_from_SDCs(src_contract)
                if len(sources_to_update) > 1:
                    fatal_error(
                        f"Not expecting to find multiple SDC matches {sources_to_update} for {src_contract}")
                if len(sources_to_update) == 0:
                    fatal_error(f"No contract to link to with the name {src_contract}")
                source_to_update = sources_to_update[0]
                # Primary contract name should match here
                if self.has_sdc_name_from_SDCs_starting_with(dst):
                    example_dst = self.get_one_sdc_name_from_SDCs(dst)  # Enough to pick one
                    dst_address = self.SDCs[example_dst].primary_contract_address
                else:
                    if is_hex(dst):
                        dst = hex_str_to_cvt_compatible(dst)
                        # The jar doesn't accept numbers with 0x prefix
                    dst_address = dst  # Actually, just a number

                # Decide how to link
                matching_immutable = list({(c, x.varname) for c in self.SDCs[source_to_update].contracts for x in
                                           c.immutables
                                           if
                                           x.varname == reference_to_replace_with_link and c.name == src_contract})
                if len(matching_immutable) > 1:
                    fatal_error(
                        f"Not expecting to find multiple immutables with the name {reference_to_replace_with_link}, "
                        f"got matches {matching_immutable}")
                """
                Three kinds of links, resolved in the following order:
                1. Immutables. We expect at most one pair of (src_contract, immutableVarName) that matches
                2. Field names. Allocated in the storage - we fetch their slot number. (TODO: OFFSET)
                3. Slot numbers in EVM. Requires knowledge about the Solidity compilation. (TODO: OFFSET)
                """
                debug_print(f"Candidate immutable names: {matching_immutable}")
                debug_print(f"Reference to replace with link: {reference_to_replace_with_link}")
                if len(matching_immutable) == 1 and reference_to_replace_with_link == matching_immutable[0][1]:
                    contract_match = matching_immutable[0][0]

                    def map_immut(immutable_reference: ImmutableReference) -> ImmutableReference:
                        if immutable_reference.varname == reference_to_replace_with_link:
                            return PresetImmutableReference(immutable_reference.offset, immutable_reference.length,
                                                            immutable_reference.varname, dst_address)
                        else:
                            return immutable_reference

                    contract_match.immutables = [map_immut(immutable_reference) for immutable_reference in
                                                 contract_match.immutables]

                    continue
                elif not reference_to_replace_with_link.isnumeric() and not is_hex(reference_to_replace_with_link):
                    # We need to convert the string to a slot number
                    resolved_src_slot = self.resolve_slot(src_contract, reference_to_replace_with_link)
                else:
                    # numeric case
                    if is_hex(reference_to_replace_with_link):
                        # if hex, need to remove the 0x
                        reference_to_replace_with_link = hex_str_to_cvt_compatible(reference_to_replace_with_link)
                    else:
                        # need to convert the dec to hex
                        reference_to_replace_with_link = decimal_str_to_cvt_compatible(reference_to_replace_with_link)
                    resolved_src_slot = reference_to_replace_with_link
                debug_print(f"Linking slot {resolved_src_slot} of {src_contract} to {dst}")
                debug_print(' '.join(k for k in self.SDCs.keys()))

                debug_print(f"Linking {src_contract} ({source_to_update}) to {dst_address} in slot {resolved_src_slot}")
                self.SDCs[source_to_update].state[resolved_src_slot] = dst_address

    def handle_struct_links(self) -> None:
        # struct link processing
        if self.input_config.struct_link is not None:
            debug_print('handling struct linking')
            links = self.input_config.struct_link
            for link in links:
                src, dst = link.split("=", 2)
                src_contract, reference_to_replace_with_link = src.split(":", 2)
                sources_to_update = self.get_matching_sdc_names_from_SDCs(src_contract)
                if len(sources_to_update) > 1:
                    fatal_error(f"Not expecting to find multiple SDC matches {sources_to_update} for {src_contract}")
                source_to_update = sources_to_update[0]
                # Primary contract name should match here
                if self.has_sdc_name_from_SDCs_starting_with(dst):
                    example_dst = self.get_one_sdc_name_from_SDCs(dst)  # Enough to pick one
                    dst_address = self.SDCs[example_dst].primary_contract_address
                else:
                    dst_address = dst  # Actually, just a number

                debug_print(f"STRUCT Reference to replace with link: {reference_to_replace_with_link}")

                if not reference_to_replace_with_link.isnumeric() and not is_hex(reference_to_replace_with_link):
                    # We need to convert the string to a slot number
                    fatal_error_if_not_library(f"error: struct link slot '{reference_to_replace_with_link}' not a "
                                               f"hexadecimal number")
                else:
                    if is_hex(reference_to_replace_with_link):
                        resolved_src_slot = hex_str_to_cvt_compatible(reference_to_replace_with_link)
                        # The jar doesn't accept numbers with 0x or 0X as prefix
                    else:
                        resolved_src_slot = decimal_str_to_cvt_compatible(reference_to_replace_with_link)
                debug_print(f"STRUCT Linking slot {resolved_src_slot} of {src_contract} to {dst}")
                debug_print(' '.join(k for k in self.SDCs.keys()))

                debug_print(f"STRUCT Linking {src_contract} ({source_to_update}) to {dst_address} in slot "
                            f"{resolved_src_slot}")
                self.SDCs[source_to_update].structLinkingInfo[resolved_src_slot] = dst_address

    def has_sdc_name_from_SDCs_starting_with(self, potential_contract_name: str) -> bool:
        candidates = self.get_matching_sdc_names_from_SDCs(potential_contract_name)
        return len(candidates) > 0

    def get_one_sdc_name_from_SDCs(self, contract: str) -> str:
        return [k for k, v in self.SDCs.items() if k.startswith(f"{contract}_")][0]

    def get_matching_sdc_names_from_SDCs(self, contract: str) -> List[str]:
        return [k for k, v in self.SDCs.items() if k.startswith(f"{contract}_")]

    def resolve_slot_from_storage_layout(self, primary_contract: str, slot_name: str, sdc: SDC) -> Optional[str]:
        """
        @param primary_contract: Name of the contract
        @param slot_name: Name of the field we wish to associate with a slot number
        @param sdc: The object representing an invocation of solc where we hope to find storageLayout
        @return: If there is a valid storage layout, returns the slot number associated with slot_name as hex without
        preceding 0x (or 0X)
        """
        storage_layouts = [c.storageLayout for c in sdc.contracts if
                           c.name == primary_contract and c.storageLayout is not None]
        if len(storage_layouts) != 1:
            debug_print(f"Expected exactly one storage layout matching {primary_contract}, got {len(storage_layouts)}")
            return None

        storage_layout = storage_layouts[0]
        if storage_layout is None or "storage" not in storage_layout:
            debug_print(f"Storage layout should be an object containing a 'storage' field, but got {storage_layout}")
            return None

        relevant_slots = [slot for slot in storage_layout["storage"] if
                          "label" in slot and slot["label"] == slot_name]
        debug_print(f"Found relevant slots in storage layout of {primary_contract}: {relevant_slots}")
        if len(relevant_slots) == 1:
            slot_number = relevant_slots[0]["slot"]
            # slot_number from storage layout is already in decimal.
            return decimal_str_to_cvt_compatible(slot_number)
        else:
            debug_print(
                f"Found multiple matches of {slot_name} "
                f"in storage layout of contract {primary_contract}: {relevant_slots}")
            return None

    def resolve_slot(self, primary_contract: str, slot_name: str) -> str:
        """
        @param primary_contract: Name of the contract
        @param slot_name: Name of the field we wish to associate with a slot number
        @return: The resolved slot number as hex without preceding 0x (or 0X)
        """
        debug_print(f"Resolving slots for {primary_contract} out of {self.SDCs.keys()}")
        sdc = self.SDCs[self.get_one_sdc_name_from_SDCs(primary_contract)]  # Enough to pick one

        slot_number_from_storage_layout = self.resolve_slot_from_storage_layout(primary_contract, slot_name, sdc)
        if slot_number_from_storage_layout is not None:
            return slot_number_from_storage_layout

        debug_print(f"Storage layout not available for contract {primary_contract}. "
                    f"Matching slots from ASM output instead")

        file = sdc.sdc_origin_file
        solc_ver_to_run = self.get_relevant_solc(primary_contract)
        solc_add_extra_args = self.get_extra_solc_args()

        asm_collect_cmd = f"{solc_ver_to_run} {solc_add_extra_args} -o {self.config_path}/ --overwrite --asm " \
                          f"--allow-paths {self.input_config.path} {file}"
        if self.input_config.packages is not None:
            asm_collect_cmd = f"{asm_collect_cmd} {' '.join(self.input_config.packages)}"

        run_cmd(asm_collect_cmd, f"{primary_contract}.asm", self.config_path, shell=False, debug=DEBUG)

        with open(f"{self.config_path}/{primary_contract}.evm", "r") as asm_file:
            debug_print(f"Got asm {asm_file}")
            saw_match = False
            candidate_slots = []
            for line in asm_file:
                if saw_match:
                    candidate_slots.append(line)
                    saw_match = False
                else:
                    regex = r'/\* "[a-zA-Z0-9./_\-:]+":[0-9]+:[0-9]+\s* %s \*/' % (slot_name,)
                    saw_match = re.search(regex, line) is not None
                    if saw_match:
                        debug_print(f"Saw match for {regex} on line {line}")
            debug_print(f"Candidate slots: {candidate_slots}")
            normalized_candidate_slots = [x.strip() for x in candidate_slots]
            debug_print(f"Candidate slots: {normalized_candidate_slots}")
            filtered_candidate_slots = [x for x in normalized_candidate_slots if re.search('^0[xX]', x)]
            set_candidate_slots = set(filtered_candidate_slots)
            debug_print(f"Set of candidate slots: {set_candidate_slots}")
            if len(set_candidate_slots) == 1:
                # Auto detect base (should be 16 though thanks to 0x)
                slot_number = hex(int(list(set_candidate_slots)[0], 0))[2:]
                debug_print(f"Got slot number {slot_number}")
            else:
                raise Exception(f"Failed to resolve slot for {slot_name} in {primary_contract}, "
                                f"valid candidates: {set_candidate_slots}")

        return slot_number


class CertoraVerifyGenerator:
    def __init__(self, build_generator: CertoraBuildGenerator):
        self.build_generator = build_generator
        self.input_config = build_generator.input_config
        self.certora_verify_struct = []
        self.verify = {}  # type: Dict[str, List[str]]
        if self.input_config.verify is not None \
                or self.input_config.assert_contracts is not None:
            if self.input_config.verify is not None:
                verification_queries = self.input_config.verify
                for verification_query in verification_queries:
                    vq_contract, vq_spec = verification_query.split(":", 2)
                    vq_spec = as_posix(os.path.abspath(vq_spec))  # get full abs path
                    if self.verify.get(vq_contract, None) is None:
                        self.verify[vq_contract] = []
                    self.verify[vq_contract].append(vq_spec)
                    self.certora_verify_struct.append(
                        {"type": "spec",
                         "primary_contract": vq_contract,
                         "specfile": self.get_path_to_spec(vq_contract, vq_spec)}
                    )

            if self.input_config.assert_contracts is not None:
                for contractToCheckAssertsFor in self.input_config.assert_contracts:
                    self.certora_verify_struct.append(
                        {"type": "assertion",
                         "primary_contract": contractToCheckAssertsFor}
                    )

        else:
            # if no --verify or --assert, remove verify json file
            try:
                os.remove(f'{OPTION_OUTPUT_VERIFY}.json')
            except OSError:
                pass

    def get_spec_idx(self, contract: str, spec: str) -> int:
        return self.verify[contract].index(spec)

    def get_path_to_spec(self, contract: str, spec: str) -> str:
        spec_basename = get_file_basename(spec)
        return f".certora_config/{self.get_spec_idx(contract, spec)}_{spec_basename}.spec"

    def copy_specs(self) -> None:
        for contract, specs in self.verify.items():
            for spec in specs:
                shutil.copy2(spec, self.get_path_to_spec(contract, spec))

    def check(self) -> None:
        for contract in self.verify:
            if len(self.build_generator.get_matching_sdc_names_from_SDCs(contract)) == 0:
                fatal_error_if_not_library(
                    f"Error: Could not find contract {contract} in contracts "
                    f"[{','.join(map(lambda x: x[1].primary_contract, self.build_generator.SDCs.items()))}]")

    def dump(self) -> None:
        debug_print(f"writing {CERTORA_VERIFY_FILE}")
        with open(CERTORA_VERIFY_FILE, 'w+') as output_file:
            json.dump(self.certora_verify_struct, output_file, indent=4, sort_keys=True)


def build(args: argparse.Namespace, is_library: bool = False) -> None:
    """
    This is the main function of certoraBuild
    @param args: A namespace including command line arguments. We expect the namespace to include validated arguments
    @param is_library: True if we run this function from a library, like in regTest.py
    """
    global BUILD_IS_LIBRARY
    BUILD_IS_LIBRARY = is_library
    global DEBUG

    try:
        if args.debug:
            DEBUG = True

        input_config = InputConfig(args)

        # Start to collect information from solc
        certora_build_generator = CertoraBuildGenerator(input_config)
        certora_build_generator.build()

        # Build .certora_verify.json
        certora_verify_generator = CertoraVerifyGenerator(certora_build_generator)
        certora_verify_generator.check()
        certora_verify_generator.copy_specs()
        certora_verify_generator.dump()

        # Output
        debug_print(f"writing file {CERTORA_BUILD_FILE}")
        with open(CERTORA_BUILD_FILE, 'w+') as output_file:
            json.dump({k: v.as_dict() for k, v in certora_build_generator.SDCs.items()},
                      output_file,
                      indent=4,
                      sort_keys=True)

    except Exception as e:
        print("Encountered an error configuring the verification environment:", e)
        debug_print(traceback.format_exc())
        exit_if_not_library(1)
