import copy
import json
import logging
import os
import re
from copy import deepcopy
from pathlib import Path
from typing import Optional, Dict, Mapping, Set, Tuple, Callable, Any, List

import deep_merge
import hcl2

from checkov.common.runners.base_runner import filter_ignored_directories
from checkov.common.util.consts import DEFAULT_EXTERNAL_MODULES_DIR, RESOLVED_MODULE_ENTRY_NAME
from checkov.common.variables.context import EvaluationContext
from checkov.terraform.graph_builder.graph_components.block_types import BlockType
from checkov.terraform.graph_builder.graph_components.module import Module
from checkov.terraform.graph_builder.utils import remove_module_dependency_in_path
from checkov.terraform.module_loading.registry import module_loader_registry as default_ml_registry, \
    ModuleLoaderRegistry
from checkov.terraform.parser_utils import eval_string, find_var_blocks

external_modules_download_path = os.environ.get('EXTERNAL_MODULES_DIR', DEFAULT_EXTERNAL_MODULES_DIR)

def _filter_ignored_directories(d_names):
    filter_ignored_directories(d_names)
    [d_names.remove(d) for d in list(d_names) if d in [default_ml_registry.external_modules_folder_name]]


class Parser:
    def __init__(self, module_class=Module):
        self.module_class = module_class
        self._parsed_directories = set()

        # This ensures that we don't try to double-load modules
        # Tuple is <file>, <module_index>, <name> (see _load_modules)
        self._loaded_modules: Set[Tuple[str, int, str]] = set()
        self.external_variables_data = []

    def _init(self, directory: str, out_definitions: Optional[Dict],
              out_evaluations_context: Dict[str, Dict[str, EvaluationContext]],
              out_parsing_errors: Dict[str, Exception],
              env_vars: Mapping[str, str],
              download_external_modules: bool,
              external_modules_download_path: str):
        self.directory = directory
        self.out_definitions = out_definitions
        self.out_evaluations_context = out_evaluations_context
        self.out_parsing_errors = out_parsing_errors
        self.env_vars = env_vars
        self.download_external_modules = download_external_modules
        self.external_modules_download_path = external_modules_download_path

        if self.out_evaluations_context is None:
            self.out_evaluations_context = {}
        if self.out_parsing_errors is None:
            self.out_parsing_errors = {}
        if self.env_vars is None:
            self.env_vars = dict(os.environ)

    def _check_process_dir(self, directory):
        if directory not in self._parsed_directories:
            self._parsed_directories.add(directory)
            return True
        else:
            return False

    def parse_directory(self, directory: str, out_definitions: Optional[Dict],
                        out_evaluations_context: Dict[str, Dict[str, EvaluationContext]] = None,
                        out_parsing_errors: Dict[str, Exception] = None,
                        env_vars: Mapping[str, str] = None,
                        download_external_modules: bool = False,
                        external_modules_download_path: str = DEFAULT_EXTERNAL_MODULES_DIR):
        self._init(directory, out_definitions, out_evaluations_context, out_parsing_errors, env_vars,
                   download_external_modules, external_modules_download_path)
        self._parsed_directories.clear()
        default_ml_registry.download_external_modules = download_external_modules
        default_ml_registry.external_modules_folder_name = external_modules_download_path

        self._parse_directory(dir_filter=lambda d: self._check_process_dir(d))

    @staticmethod
    def parse_file(file: str, parsing_errors: Dict[str, Exception] = None) -> Optional[Dict]:
        if not file.endswith(".tf") and not file.endswith(".tf.json"):
            return None
        return _load_or_die_quietly(Path(file), parsing_errors)

    def _parse_directory(self, include_sub_dirs: bool = True,
                         module_loader_registry: ModuleLoaderRegistry = default_ml_registry,
                         dir_filter: Callable[[str], bool] = lambda _: True):
        """
    Load and resolve configuration files starting in the given directory, merging the
    resulting data into `tf_definitions`. This loads data according to the Terraform Code Organization
    specification (https://www.terraform.io/docs/configuration/index.html#code-organization), starting
    in the given directory and possibly moving out from there.

    The resulting data dictionary generally follows the layout of HCL parsing with a couple distinctions:
    - Data is broken out by file from which the data was loaded. So: <file>: <data>
      - Loaded modules will also be keyed by referrer info: <file>[<referring_file>#<index>]: <data>
    - Module block will included a "__resolved__" key with a list of the file/referrer names under
      which data for the file was loaded. For example: "__resolved__": ["main.tf#0"]. The values will
      correspond to the file names mentioned in the first bullet.
    - All variables that can be resolved will be resolved.


        :param include_sub_dirs:           If true, subdirectories will be walked.

        :param module_loader_registry:     Registry used for resolving modules. This allows customization of how
                                           much resolution is performed (and easier testing) by using a manually
                                           constructed registry rather than the default.
        :param dir_filter:                 Determines whether or not a directory should be processed. Returning
                                           True will allow processing. The argument will be the absolute path of
                                           the directory.
        """
        keys_referenced_as_modules: Set[str] = set()

        if include_sub_dirs:
            for sub_dir, d_names, f_names in os.walk(self.directory):
                _filter_ignored_directories(d_names)
                if dir_filter(os.path.abspath(sub_dir)):
                    self._internal_dir_load(sub_dir, module_loader_registry, dir_filter,
                                            keys_referenced_as_modules)
        else:
            self._internal_dir_load(self.directory, module_loader_registry, dir_filter,
                                    keys_referenced_as_modules)

        # Ensure anything that was referenced as a module is removed
        for key in keys_referenced_as_modules:
            if key in self.out_definitions:
                del self.out_definitions[key]

    def _internal_dir_load(self, directory: str,
                           module_loader_registry: ModuleLoaderRegistry,
                           dir_filter: Callable[[str], bool],
                           keys_referenced_as_modules: Set[str],
                           specified_vars: Optional[Mapping[str, str]] = None,
                           module_load_context: Optional[str] = None):
        """
    See `parse_directory` docs.
        :param directory:                  Directory in which .tf and .tfvars files will be loaded.
        :param module_loader_registry:     Registry used for resolving modules. This allows customization of how
                                       much resolution is performed (and easier testing) by using a manually
                                       constructed registry rather than the default.
        :param dir_filter:                 Determines whether or not a directory should be processed. Returning
                                       True will allow processing. The argument will be the absolute path of
                                       the directory.
        :param specified_vars:     Specifically defined variable values, overriding values from any other source.
        """

        # Stage 1: Look for applicable files in the directory:
        #          https://www.terraform.io/docs/configuration/index.html#code-organization
        #          Load the raw data for non-variable files, but perform no processing other than loading
        #          variable default values.
        #          Variable files are also flagged for later processing.
        var_value_and_file_map: Dict[str, Tuple[Any, str]] = {}
        hcl_tfvars: Optional[os.DirEntry] = None
        json_tfvars: Optional[os.DirEntry] = None
        auto_vars_files: Optional[List[os.DirEntry]] = None      # lazy creation
        for file in os.scandir(directory):
            # Ignore directories and hidden files
            try:
                if not file.is_file() or file.name.startswith("."):
                    continue
            except OSError:
                # Skip files that can't be accessed
                continue

            # Variable files
            # See: https://www.terraform.io/docs/configuration/variables.html#variable-definitions-tfvars-files
            if file.name == "terraform.tfvars.json":
                json_tfvars = file
                continue
            elif file.name == "terraform.tfvars":
                hcl_tfvars = file
                continue
            elif file.name.endswith(".auto.tfvars.json") or file.name.endswith(".auto.tfvars"):
                if auto_vars_files is None:
                    auto_vars_files = [file]
                else:
                    auto_vars_files.append(file)
                continue

            # Resource files
            if file.name.endswith(".tf"):  # TODO: add support for .tf.json
                data = _load_or_die_quietly(file, self.out_parsing_errors)
            else:
                continue

            if not data:        # failed loads or empty files
                continue

            self.out_definitions[file.path] = data

            # Load variable defaults
            #  (see https://www.terraform.io/docs/configuration/variables.html#declaring-an-input-variable)
            var_blocks = data.get("variable")
            if var_blocks and isinstance(var_blocks, list):
                for var_block in var_blocks:
                    if not isinstance(var_block, dict):
                        continue
                    for var_name, var_definition in var_block.items():
                        if not isinstance(var_definition, dict):
                            continue

                        default_value = var_definition.get("default")
                        if default_value is not None and isinstance(default_value, list):
                            self.external_variables_data.append((var_name, default_value[0], file.path))
                            var_value_and_file_map[var_name] = default_value[0], file.path

        # Stage 2: Load vars in proper order:
        #          https://www.terraform.io/docs/configuration/variables.html#variable-definition-precedence
        #          Defaults are loaded in stage 1.
        #          Then loading in this order with later taking precedence:
        #             - Environment variables
        #             - The terraform.tfvars file, if present.
        #             - The terraform.tfvars.json file, if present.
        #             - Any *.auto.tfvars or *.auto.tfvars.json files, processed in lexical order of
        #               their filenames.
        #          Overriding everything else, variables form `specified_vars`, which are considered
        #          directly set.
        for key, value in self.env_vars.items():                                 # env vars
            if not key.startswith("TF_VAR_"):
                continue
            var_value_and_file_map[key[7:]] = value, f"env:{key}"
            self.external_variables_data.append((key[7:], value, f"env:{key}"))
        if hcl_tfvars:                                                      # terraform.tfvars
            data = _load_or_die_quietly(hcl_tfvars, self.out_parsing_errors,
                                        clean_definitions=False)
            if data:
                var_value_and_file_map.update({k: (_safe_index(v, 0), hcl_tfvars.path) for k, v in data.items()})
                self.external_variables_data.extend([(k, _safe_index(v, 0), hcl_tfvars.path) for k, v in data.items()])
        if json_tfvars:                                                     # terraform.tfvars.json
            data = _load_or_die_quietly(json_tfvars, self.out_parsing_errors)
            if data:
                var_value_and_file_map.update({k: (v, json_tfvars.path) for k, v in data.items()})
                self.external_variables_data.extend([(k, v, json_tfvars.path) for k, v in data.items()])
        if auto_vars_files:                                                 # *.auto.tfvars / *.auto.tfvars.json
            for var_file in sorted(auto_vars_files, key=lambda e: e.name):
                data = _load_or_die_quietly(var_file, self.out_parsing_errors)
                if data:
                    var_value_and_file_map.update({k: (v, var_file.path) for k, v in data.items()})
                    self.external_variables_data.extend([(k, v, var_file.path) for k, v in data.items()])
        if specified_vars:                                                  # specified
            var_value_and_file_map.update({k: (v, "manual specification") for k, v in specified_vars.items()})
            self.external_variables_data.extend([(k, v, "manual specification") for k, v in specified_vars.items()])

        # IMPLEMENTATION NOTE: When resolving `module.` references, access to the entire data map is needed. It
        #                      may be a little overboard, but I don't want to just pass the entire data map down
        #                      because it break encapsulations and I don't want to cause confusion about what data
        #                      set it being processed. To avoid this, here's a Callable that will get the data
        #                      map for a particular module reference. (Might be OCD, but...)
        module_data_retrieval = lambda module_ref: self.out_definitions.get(module_ref)

        # Stage 4: Load modules
        #          This stage needs to be done in a loop (again... alas, no DAG) because modules might not
        #          be loadable until other modules are loaded. This happens when parameters to one module
        #          depend on the output of another. For such cases, the base module must be loaded, then
        #          a parameter resolution pass needs to happen, then the second module can be loaded.
        #
        #          One gotcha is that we need to make sure we load all modules at some point, even if their
        #          parameters don't resolve. So, if we hit a spot where resolution doesn't change anything
        #          and there are still modules to be loaded, they will be forced on the next pass.
        force_final_module_load = False
        for i in range(0, 10):      # circuit breaker - no more than 10 loops
            logging.debug("Module load loop %d", i)

            # Stage 4a: Load eligible modules
            has_more_modules = self._load_modules(directory, module_loader_registry,
                                                  dir_filter, module_load_context,
                                                  keys_referenced_as_modules,
                                                  force_final_module_load)

            # Stage 4b: Variable resolution round 2 - now with (possibly more) modules
            made_var_changes = False
            if not has_more_modules:
                break       # nothing more to do
            elif not made_var_changes:
                # If there are more modules to load but no variables were resolved, then to a final module
                # load, forcing things through without complete resolution.
                force_final_module_load = True

    def _load_modules(self, root_dir: str, module_loader_registry: ModuleLoaderRegistry,
                      dir_filter: Callable[[str], bool], module_load_context: Optional[str],
                      keys_referenced_as_modules: Set[str], ignore_unresolved_params: bool = False) -> bool:
        """
        Load modules which have not already been loaded and can be loaded (don't have unresolved parameters).

        :param ignore_unresolved_params:    If true, not-yet-loaded modules will be loaded even if they are
                                            passed parameters that are not fully resolved.
        :return:                            True if there were modules that were not loaded due to unresolved
                                            parameters.
        """
        all_module_definitions = {}
        all_module_evaluations_context = {}
        skipped_a_module = False
        for file in list(self.out_definitions.keys()):
            # Don't process a file in a directory other than the directory we're processing. For example,
            # if we're down dealing with <top_dir>/<module>/something.tf, we don't want to rescan files
            # up in <top_dir>.
            if os.path.dirname(file) != root_dir:
                continue
            # Don't process a file reference which has already been processed
            if file.endswith("]"):
                continue

            file_data = self.out_definitions.get(file)
            if file_data is None:
                continue
            module_calls = file_data.get("module")
            if not module_calls or not isinstance(module_calls, list):
                continue

            for module_index, module_call in enumerate(module_calls):

                if not isinstance(module_call, dict):
                    continue

                # There should only be one module reference per outer dict, but... safety first
                for module_call_name, module_call_data in module_call.items():
                    if not isinstance(module_call_data, dict):
                        continue

                    module_address = (file, module_index, module_call_name)
                    if module_address in self._loaded_modules:
                        continue

                    # Variables being passed to module, "source" and "version" are reserved
                    specified_vars = {k: v[0] for k, v in module_call_data.items()
                                      if k != "source" and k != "version"}

                    if not ignore_unresolved_params:
                        has_unresolved_params = False
                        for k, v in specified_vars.items():
                            if not is_acceptable_module_param(v) or not is_acceptable_module_param(k):
                                has_unresolved_params = True
                                break
                        if has_unresolved_params:
                            skipped_a_module = True
                            continue
                    self._loaded_modules.add(module_address)

                    source = module_call_data.get("source")
                    if not source or not isinstance(source, list):
                        continue
                    source = source[0]

                    # Special handling for local sources to make sure we aren't double-parsing
                    if source.startswith("./") or source.startswith("../"):
                        source = os.path.normpath(
                            os.path.join(os.path.dirname(_remove_module_dependency_in_path(file)), source))

                    version = module_call_data.get("version", "latest")
                    if version and isinstance(version, list):
                        version = version[0]
                    try:
                        with module_loader_registry.load(root_dir, source, version) as content:
                            if not content.loaded():
                                continue

                            self._internal_dir_load(directory=content.path(),
                                                    module_loader_registry=module_loader_registry,
                                                    dir_filter=dir_filter, specified_vars=specified_vars,
                                                    module_load_context=module_load_context,
                                                    keys_referenced_as_modules=keys_referenced_as_modules)

                            module_definitions = {path: self.out_definitions[path] for path in
                                                  list(self.out_definitions.keys()) if
                                                  os.path.dirname(path) == content.path()}

                            if not module_definitions:
                                continue

                            # NOTE: Modules are put into the main TF definitions structure "as normal" with the
                            #       notable exception of the file name. For loaded modules referrer information is
                            #       appended to the file name to create this format:
                            #         <file_name>[<referred_file>#<referrer_index>]
                            #       For example:
                            #         /the/path/module/my_module.tf[/the/path/main.tf#0]
                            #       The referrer and index allow a module allow a module to be loaded multiple
                            #       times with differing data.
                            #
                            #       In addition, the referring block will have a "__resolved__" key added with a
                            #       list pointing to the location of the module data that was resolved. For example:
                            #         "__resolved__": ["/the/path/module/my_module.tf[/the/path/main.tf#0]"]

                            resolved_loc_list = module_call_data.get(RESOLVED_MODULE_ENTRY_NAME)
                            if resolved_loc_list is None:
                                resolved_loc_list = []
                                module_call_data[RESOLVED_MODULE_ENTRY_NAME] = resolved_loc_list

                            # NOTE: Modules can load other modules, so only append referrer information where it
                            #       has not already been added.
                            keys = list(module_definitions.keys())
                            for key in keys:
                                if key.endswith("]") or file.endswith("]"):
                                    continue
                                keys_referenced_as_modules.add(key)
                                new_key = f"{key}[{file}#{module_index}]"
                                module_definitions[new_key] = module_definitions[key]
                                del module_definitions[key]
                                del self.out_definitions[key]
                                if new_key not in resolved_loc_list:
                                    resolved_loc_list.append(new_key)
                            resolved_loc_list.sort()        # For testing, need predictable ordering

                            deep_merge.merge(all_module_definitions, module_definitions)
                    except Exception as e:
                        logging.warning("Unable to load module (source=\"%s\" version=\"%s\"): %s",
                                        source, version, e)
                        pass

        if all_module_definitions:
            deep_merge.merge(self.out_definitions, all_module_definitions)
            deep_merge.merge(self.out_evaluations_context, all_module_evaluations_context)
        return skipped_a_module

    def parse_hcl_module(self, source_dir, source, parsing_errors=None):
        tf_definitions = {}
        download_external_modules = os.environ.get('DOWNLOAD_EXTERNAL_MODULES', 'false').lower() == 'true'
        self.parse_directory(directory=source_dir, out_definitions=tf_definitions, out_evaluations_context={},
                             out_parsing_errors=parsing_errors if parsing_errors is not None else {},
                             download_external_modules=download_external_modules,
                             external_modules_download_path=external_modules_download_path)
        tf_definitions = Parser._hcl_boolean_types_to_boolean(tf_definitions)
        return self.parse_hcl_module_from_tf_definitions(tf_definitions, source_dir, source)

    def parse_hcl_module_from_tf_definitions(self, tf_definitions, source_dir, source):
        module = self.get_new_module(source_dir)
        self.add_tfvars(module, source)
        module_dependency_map, tf_definitions = self.get_module_dependency_map(tf_definitions)
        copy_of_tf_definitions = deepcopy(tf_definitions)
        for file_path in copy_of_tf_definitions:
            blocks = copy_of_tf_definitions.get(file_path)
            for block_type in blocks:
                try:
                    module.add_blocks(block_type, blocks[block_type], file_path, source)
                except Exception as e:
                    logging.error(f'Failed to add block {blocks[block_type]}. Error:')
                    logging.error(e, exc_info=True)
        return module, module_dependency_map, tf_definitions

    @staticmethod
    def _hcl_boolean_types_to_boolean(conf: dict) -> dict:
        sorted_keys = list(conf.keys())
        if len(conf.keys()) > 0 and all(isinstance(x, type(list(conf.keys())[0])) for x in conf.keys()):
            sorted_keys = sorted(filter(lambda x: x is not None, conf.keys()))
        # Create a new dict where the keys are sorted alphabetically
        sorted_conf = {key: conf[key] for key in sorted_keys}
        for attribute, values in sorted_conf.items():
            if attribute is 'alias':
                continue
            if isinstance(values, list):
                sorted_conf[attribute] = Parser._hcl_boolean_types_to_boolean_lst(values)
            elif isinstance(values, dict):
                sorted_conf[attribute] = Parser._hcl_boolean_types_to_boolean(conf[attribute])
            elif isinstance(values, str) and values in ('true', 'false'):
                sorted_conf[attribute] = True if values == 'true' else False
        return sorted_conf

    @staticmethod
    def _hcl_boolean_types_to_boolean_lst(values: list) -> list:
        for i in range(len(values)):
            val = values[i]
            if isinstance(val, dict):
                values[i] = Parser._hcl_boolean_types_to_boolean(val)
            elif isinstance(val, list):
                values[i] = Parser._hcl_boolean_types_to_boolean_lst(val)
            elif isinstance(val, str):
                if val == 'true':
                    values[i] = True
                elif val == 'false':
                    values[i] = False
        str_values_in_lst = [val for val in values if isinstance(val, str)]
        str_values_in_lst.sort()
        result_values = [val for val in values if not isinstance(val, str)]
        result_values.extend(str_values_in_lst)
        return result_values

    @staticmethod
    def get_module_dependency_map(tf_definitions):
        """
        :param tf_definitions, with paths in format 'dir/main.tf[module_dir/main.tf#0]'
        :return module_dependency_map: mapping between directories and the location of its module definition:
                {'dir': 'module_dir/main.tf'}
        :return tf_definitions: with paths in format 'dir/main.tf'
        """
        module_dependency_map = {}
        copy_of_tf_definitions = {}
        for file_path in tf_definitions.keys():
            path, module_dependency, _ = remove_module_dependency_in_path(file_path)
            dir_name = os.path.dirname(path)
            if not module_dependency_map.get(dir_name):
                module_dependency_map[dir_name] = set()
            module_dependency_map[dir_name].add(module_dependency)
            copy_of_tf_definitions[file_path] = deepcopy(tf_definitions[file_path])
        return module_dependency_map, copy_of_tf_definitions

    @staticmethod
    def get_new_module(source_dir):
        return Module(source_dir, encode=False)

    def add_tfvars(self, module, source):
        if not self.external_variables_data:
            return
        for (var_name, default, path) in self.external_variables_data:
            if ".tfvars" in path:
                block = {var_name: {"default": default}}
                module.add_blocks(BlockType.TF_VARIABLE, block, path, source)

def _load_or_die_quietly(file: os.PathLike, parsing_errors: Dict,
                         clean_definitions: bool = True) -> Optional[Mapping]:
    """
Load JSON or HCL, depending on filename.
    :return: None if the file can't be loaded
    """

    file_path = os.fspath(file)
    file_name = os.path.basename(file_path)

    try:
        with open(file, "r") as f:
            if file_name.endswith(".json"):
                return json.load(f)
            else:
                raw_data = hcl2.load(f)
                non_malformed_definitions = _validate_malformed_definitions(raw_data)
                if clean_definitions:
                    return _clean_bad_definitions(non_malformed_definitions)
                else:
                    return non_malformed_definitions
    except Exception as e:
        logging.debug(f'failed while parsing file {file}', exc_info=e)
        parsing_errors[file_path] = e
        return None


def _is_valid_block(block):
    if not isinstance(block, dict):
        return True
    entity_name, _ = next(iter(block.items()))
    if re.fullmatch(r'[^\W0-9][\w-]*', entity_name):
        return True
    return False


def _validate_malformed_definitions(raw_data):
    raw_data_cleaned = copy.deepcopy(raw_data)
    for block_type, blocks in raw_data.items():
        raw_data_cleaned[block_type] = [block for block in blocks if _is_valid_block(block)]

    return raw_data_cleaned


def _clean_bad_definitions(tf_definition_list):
    return {
        block_type: list(filter(lambda definition_list: block_type == 'locals' or
                                                        not isinstance(definition_list, dict)
                                                        or len(definition_list.keys()) == 1,
                                tf_definition_list[block_type]))
        for block_type in tf_definition_list.keys()
    }


def _to_native_value(value: str) -> Any:
    if value.startswith('"') or value.startswith("'"):
        return value[1:-1]
    else:
        return eval_string(value)


def _remove_module_dependency_in_path(path):
    """
    :param path: path that looks like "dir/main.tf[other_dir/x.tf#0]
    :return: only the outer path: dir/main.tf
    """
    resolved_module_pattern = r'\[.+\#.+\]'
    if re.findall(resolved_module_pattern, path):
        path = re.sub(resolved_module_pattern, '', path)
    return path


def _safe_index(sequence_hopefully, index) -> Optional[Any]:
    try:
        return sequence_hopefully[index]
    except IndexError as e:
        logging.debug(f'Failed to parse index int ({index}) out of {sequence_hopefully}')
        logging.debug(e, stack_info=True)
        return None


def is_acceptable_module_param(value: Any) -> bool:
    """
    This function determines if a value should be passed to a module as a parameter. We don't want to pass
    unresolved var, local or module references because they can't be resolved from the module, so they need
    to be resolved prior to being passed down.
    """
    if isinstance(value, dict):
        for k, v in value.items():
            if not is_acceptable_module_param(v) or not is_acceptable_module_param(k):
                return False
        return True
    if isinstance(value, set) or isinstance(value, list):
        for v in value:
            if not is_acceptable_module_param(v):
                return False
        return True

    if not isinstance(value, str):
        return True

    for vbm in find_var_blocks(value):
        if vbm.is_simple_var():
            return False
    return True
