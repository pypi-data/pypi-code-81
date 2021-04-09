import os
import platform
import fnmatch
import logging
from pathlib import Path

from .utils.exceptions import MissingDefinitionFile

import yaml
import unidecode

__LOGGER__ = logging.getLogger(__name__)


class Helpers:

    __techniques = {}
    TECHNIQUE_DIRECTORY_PATTERN = 'T*'


    def __get_file_name(self, path):
        return path.strip('/').strip('\\').split('/')[-1].split('\\')[-1].split('.')[0]

    def get_platform(self):
        """
        Gets the current platform
        """
        plat = platform.system().lower()
        if plat == "darwin":
            # 'macos' is the term that is being used within the .yaml files.
            plat = "macos"
        return plat

    def get_self_path(self):
        """
        Gets the full path to this script's directory
        """
        return os.path.dirname(os.path.abspath(__file__))

    def find_atomics(self, path, pattern='atomics/T*/T*.yaml'):
        """[summary]

        Args:
            path ([type]): [description]
        """
        result = []
        for path in Path(path).rglob(pattern):
            result.append(os.path.abspath(path))
        return result

    def load_technique(self, path_to_dir):
        """
        Loads the YAML content of a technique from its directory. (T*)
        """
        # Load and parses its content.
        # Add logic to identify location of atomics
        with open(path_to_dir, 'r', encoding="utf-8") as f:
            return yaml.load(f.read(), Loader=yaml.SafeLoader)

    def load_techniques(self, atomics_path):
        """
        Loads multiple techniques from the 'atomics' directory
        """
        print(atomics_path)
        if not os.path.exists(os.path.abspath(atomics_path)):
            atomics_path = self.find_atomics(self.get_self_path())
            if not atomics_path:
                raise Exception('Unable to find any atomics folder')
        else:
            atomics_path = self.find_atomics(atomics_path)
            if not atomics_path:
                raise Exception('Unable to find any atomics folder')
        
        # For each tech directory in the main directory.
        for atomic_entry in atomics_path:
            technique = self.__get_file_name(atomic_entry)
            if not self.__techniques.get(technique):
                self.__techniques[technique] = self.load_technique(atomic_entry)
                
        #print(".")
        return self.__techniques

    def check_dependencies(executor, cwd):
        dependencies            = "dependencies"
        dependencies_executor   = "dependency_executor_name"
        prereq_command          = "prereq_command"
        get_prereq_command      = "get_prereq_command"
        input_arguments         = "input_arguments"
        
        # If the executor doesn't have dependencies_executor key it doesn't have dependencies. Skip
        if dependencies not in executor or dependencies not in executor:
            print("No '{}' or '{}' section found in the yaml file. Skipping dependencies check.".format(dependencies_executor,dependencies))
            return True
        
        launcher = executor[dependencies_executor]    
        
        for dep in executor[dependencies]:
            args = executor[input_arguments] if input_arguments in executor else {}
            final_parameters = set_parameters(args, {})         
            command = build_command(launcher, dep[prereq_command], final_parameters, cwd)

            p = subprocess.Popen(launcher, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, env=os.environ, cwd=cwd)       

            p.communicate(bytes(command, "utf-8") + b"\n", timeout=COMMAND_TIMEOUT)
            # If the dependencies are not satisfied the command will exit with code 1, 0 otherwise.
            if p.returncode != 0:
                print("Dependencies not found. Fetching them...")
                if get_prereq_command not in dep:
                    print("Missing {} commands in the yaml file. Can't fetch requirements".format(get_prereq_command))          
                    return False
                command = build_command(launcher, dep[get_prereq_command], final_parameters, cwd)
                d = subprocess.Popen(launcher, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, env=os.environ, cwd=cwd)   
                out, err = d.communicate(bytes(command, "utf-8") + b"\n", timeout=COMMAND_TIMEOUT)
            p.terminate()        

        return True
