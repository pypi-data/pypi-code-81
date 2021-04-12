#!/usr/bin/env python
import argparse
import os
import re
import subprocess
import contextlib 
import shlex
from sys import version_info
from covpipe.ncov_minipipe import DEFAULT_DATA_DIR


class ToolNotFoundError(Exception):

    def __init__(self, errorlist, msg=""):
        if not isinstance(errorlist, list):
            errorlist = [errorlist]
        self.msg = ("ToolsNotFound: {msg}\n"
                    "Errors found while checking tool availability!\nErrors:\n "
                    "{errs}"
                    "".format(msg=msg,errs="\n ".join(errorlist)))
        super().__init__(self.msg)

class CondaEnvironmentCreateError(Exception):
    def __init__(self, call, output):
        if not instance(call, list):
            call = [call]
        self.msg = ("Error while trying to create Conda environment!\n"
                    "Call: {call}\n"
                    "Output: \n{err}".format(call=" ".join(call),
                                             err=output))

class ErrorGettingGitRepo(Exception):
    def __init__(self, call, output):
        if not instance(call, list):
            call = [call]
        self.msg = ("Error while trying to clone git repository!\n"
                    "Call: {call}\n"
                    "Output: \n{err}".format(call=" ".join(call),
                                             err=output))

def main(CMD=None, snakemake=None):
    parser = get_argument_parser() 
    args, unknown_args = parser.parse_known_args(CMD)
    covpipe_default_location = os.getenv("SNAKE_CONDA_PREFIX", 
                                         default=DEFAULT_DATA_DIR)
    prefix = args.prefix
    if prefix is not None and args.use_conda_default:
        parser.error("Cannot use --prefix option together with"
                     " --use-conda-default")
        exit(2)
    try:
        if not args.use_conda_default:
            prefix = os.path.join(covpipe_default_location, args.name)
            print("Checking Environment Availability:\n", prefix)
        tool_availability()
        has_conda, parsed_prefix, found_pangolin = (
                setup_environment(prefix, args.name)) 
        has_pango_git = pango_env_has_git(parsed_prefix) 
        print("CondaPrefix:                {p}\n"
              "Valid:                      {v}\n"
              "pangolin installed:         {pa}\n"
              "contains pangolin git repo: {g}"
              "".format(p=parsed_prefix, v=has_conda, pa=found_pangolin,
                        g=has_pango_git))
        if found_pangolin:
            if args.pre_release:
                git_manual_update(parsed_prefix)
            else:
                pangolin_simple_update(parsed_prefix)
        else:
            install_fresh_pangolin(parsed_prefix) 

    except ToolNotFoundError as e:
        print(str(e))
        exit(3)


def get_argument_parser():
    parser = argparse.ArgumentParser("update_pangolin")
    parser.add_argument("-p", "--prefix", help=
                           "Path where to put pangolin environment (includes evironment name)."
                           " Connot be used with --use-default or --name option !",
                        type=prefix_augment)
    parser.add_argument("--use-conda-default", action="store_true", 
                          help="Just put the environment into the"
                               " default location specified in your conda settings")
    parser.add_argument("-n", "--name", 
                        help="Name of environment."
                             " Cannot be used with prefix command",
                        default="pangolin") 
    parser.add_argument("--pre-release",  action="store_true",
                        help="Download pre-release changes directly from"
                             "git master branch.")
    
    return parser

def tool_availability():
    errors = []
    tools = {
            "conda": {"cmd": ["conda", "--version"], "available": False},
            "git": {"cmd": ["git", "--version"], "available": False}}

    for tool in tools:
        try: 
            tools[tool]["available"] = check_tool_presence(tools[tool]["cmd"]) 
        except FileNotFoundError:
            errors.append("Tool \"{tool}\" is not available!\n  "
                          "Call used to check presence: {call}".format(
                                tool=tool,
                                call=" ".join(tools[tool]["cmd"])))
    if errors:
        raise ToolNotFoundError(errors) 
    return errors 

def check_tool_presence(call):
    subprocess.check_output(call)
    return True

def setup_environment(prefix, name, no_recursion=False):
    is_conda = False
    parsed_prefix = None
    found_pangolin = False
    try:
        call = ["conda", "list"] 
        if prefix is None:
            call.extend(["-n", shlex.quote(name)])
        else:
            call.extend(["--prefix", shlex.quote(prefix)])
        env_list = subprocess.check_output(
                call,
                stderr=subprocess.STDOUT, 
                universal_newlines=True)
        is_conda = True
        env_list_lines = env_list.split("\n")
        found_pangolin = any("pangolin" in line for line in env_list_lines[3:])
        try:
            parsed_prefix = prefix_augment(
                    re.match('.*in environment at (.+):[\s]*$', 
                             env_list_lines[0]).group(1))
        except AttributeError as e:
            pass
    except subprocess.CalledProcessError as e:
        create_call =  ["conda", "create", "--yes", "--offline", "python"]
        try: 
            if prefix is None: 
                create_call.extend(["-n", shlex.quote(name)])
            else: 
                create_call.extend(["--prefix", shlex.quote(prefix)])
            print("Building Environment: \n", " ".join(create_call))
            out = subprocess.check_output(
                       create_call, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise CondaEnvironmentCreateError(create_call,e.output)
        is_conda, parsed_prefix,  found_pangolin = (
                setup_environment(name, prefix, no_recursion=True))

    return is_conda, parsed_prefix, found_pangolin


def pangolin_simple_update(prefix):
    run_unsafe_command_in_pangolin(prefix, "pangolin --update")


def pango_env_has_git(prefix):
    with pushd(prefix):
        return os.path.isdir(os.path.join("opt","pangolin",".git"))
    
def install_fresh_pangolin(prefix):
    if not pango_env_has_git(prefix):
        get_pango_git(prefix)
    git_manual_update(prefix)

def get_pango_git(prefix):
    with pushd(prefix):
        mkdir_if_not_exists("opt")
        with pushd("opt"):
            try:
                out = subprocess.check_output(
                    ["git","clone", 
                     "https://github.com/cov-lineages/pangolin.git"],
                    stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                raise ErrorGettingGitRepo(create_call,e.output)


def git_manual_update(prefix):
    if not pango_env_has_git(prefix):
        get_pango_git(prefix)
    with pushd(prefix):
        pangolin_git = os.path.join("opt","pangolin")
        with pushd(pangolin_git):
            print("\nUpdating git repo..")
            out = subprocess.check_output(
                    ["git","pull"],
                    stderr=subprocess.PIPE)
            try:
                print("Updating conda environment...")
                run_unsafe_command_in_pangolin(
                        prefix,
                        "conda env update --prefix ./ -f {env}".format(
                            env=os.path.join(pangolin_git, "environment.yml")))
            except subprocess.CalledProcessError as e:
                print(e.output)
                raise 
            print("Updating PangoLearn...")
            run_unsafe_command_in_pangolin(
                    prefix,
                    "python -m pip install {git} --upgrade".format(
                        git="git+https://github.com/cov-lineages/pangoLEARN.git"))
            print("Installing Latest Pangolin...")
            run_unsafe_command_in_pangolin(
                    prefix,
                    "python -m pip install {git}".format(git=pangolin_git))
            print("Done with all steps")


def run_unsafe_command_in_pangolin(prefix, cmd):
    with pushd(prefix):
        out = subprocess.check_output(
                """ eval "$(conda shell.bash hook)"; conda activate ./ && {cmd} && conda deactivate""".format(cmd=cmd),
                shell=True)



@contextlib.contextmanager
def pushd(new_dir):
    """Mechanism for ensuring return to old directory after changing it
       Thanks to github user spiralman
       https://stackoverflow.com/questions/6194499/pushd-through-os-system
    """
    old_wd = os.getcwd()
    os.chdir(new_dir)
    try:
        yield os.path.realpath(os.getcwd())
    finally:
        os.chdir(old_wd)

def prefix_augment(prefix):
    if not prefix.endswith('/'):
        prefix = prefix + "/" 
    return prefix

def mod_string(string):
    if (version_info > (3, 0)):
        return string.decode()
    else:
        return string

def mkdir_if_not_exists(_dir):
    """ Make direectory if it does not exist

    python 3.2 added the used exist_ok flag # PY3.2<
    """
    if _dir is None:
        return None
    os.makedirs(_dir, exist_ok=True)
    return os.path.realpath(_dir)

if __name__ == "__main__":
    main()
