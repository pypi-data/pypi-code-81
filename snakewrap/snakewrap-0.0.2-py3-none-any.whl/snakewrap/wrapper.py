# -*- coding: utf-8 -*-
""" Core module of SnakeWrap Library  

This module represents your main starting point for a snakemake pipeline

The most important class of the whole library is the SnakeApp class
it is an abstract class that needs to inherited from to get a concrete
implementation of a snakemake app.

The followinng represents a minimum vialble app
    

Attributes:
    debug (bool): Set to True if you dare


Example Use

.. code-block:: python 
    :linenos:
    

    import os

    class App(SnakeApp):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs) #initialize parent class
     
        def args_to_config_dict(self):
            config = vars(self.args) # just turn namespace to dict and return it
            return config 

        def get_argparser(self):
            parser = argparse.ArgumentParser()
            parser.add_argument("--input")
            parser.add_argument("--config")
            parser.add_argument("-o", "--outdir", type=os.path.realpath, default=".")
            return parser # return a argument parser
        
        def init_setup(self):
            if self.args.outdir is not None:
                self.set_workdir(self.args.outdir) # set working directory
            
    # Actually create an instance of our app
    app = App("dummyapp")
    app.set_snakefile("Snakefile")
    app.add_log_file("logfile.log")
    app.run(["--input", "testdir", "-o", "testout"])


"""

from __future__ import annotations
from . import utils 
from . import sample_manager
import abc
import argparse 
import logging
import pprint
import os
import re
import subprocess
import yaml


class SNAKEMAKE_RUN_ERROR(Exception):
    def __init__(self, ret, stdout="", stderr="", call=""):
        self.ret = ret
        self.stdout = stdout
        self.stderr = stderr
        self.msg = "Snakemake call returned non zero exit status"
        super().__init__(self.msg)

class ConfigOptionNameNotFound(Exception):
    def __init__(self, optname):
        self.optname = optname
        self.msg = ("looked for config parameter named \"{opt}\""
                    "and was not able to find it.\n"
                    "Please add the option to the relevant argument parser\n"
                    "or adjust the code accordingly".format(opt=optname)) 

class TypeNotArgumentParser(Exception):
    def __init__(self, _type):
        self.msg = "Expected ArgumentParser and not {_t}".format(_t=_type) 
        super().__init__(_type) 

class ArgumentsNotParsedError(Exception):
    def __init__(self):
        self.msg = "Arguments not parsed. Please set proper Argumentparser!"
        super().__init__(self.msg)


class CONFIGURATION_ERROR(Exception):
    def __init__(self, errlist=[], user_needs_usage=False):
        self.errlist = errlist
        self.user_needs_usage = user_needs_usage
        self.numerrs = len(errlist)
        self.multierr = self.numerrs > 1
        if self.multierr:
            preformated_error = "\n\n".join(
                    ["  Error {idx}:\n\t{err}".format(idx=idx+1,
                                                      err=err.replace("\n",
                                                                      "\n\t"))
                     for idx, err in enumerate(errlist)])
        else:
            preformated_error = "\t" + self.errlist[0].replace("\n","\n\t")
        self.message = (
                "Configuratio Error\n"
                "Whilst validating the run configuration"
                " {grammar1} found!\n\n"
                "{grammar2}:\n"
                "{errors}\n".format(
                    grammar1="several inconsistencies were"
                              if self.multierr
                              else "an inconsitency was",
                    grammar2="Errors" if self.multierr else "Error",
                    errors=preformated_error) )
        super().__init__(self.message)


class SAMPLE_CONFIG_ERROR(Exception):
    def __init__(self, errlist=[]):
        self.errlist = errlist
        self.numerrs = len(errlist)
        self.multierr = self.numerrs > 1
        if self.multierr:
            preformated_error = "\n\n".join(
                    ["  Error {idx}:\n\t{err}".format(idx=idx+1,
                                                      err=err.replace("\n",
                                                                      "\n\t"))
                     for idx, err in enumerate(errlist)])
        else:
            preformated_error = "\t" + self.errlist[0].replace("\n","\n\t")
        self.message = (
                "Sample Config Error\n"
                "Whilst validating the sample configuration"
                " {grammar1} found!\n\n"
                "{grammar2}:\n"
                "{errors}\n".format(
                    grammar1="several inconsistencies were"
                              if self.multierr
                              else "an inconsitency was",
                    grammar2="Errors" if self.multierr else "Error",
                    errors=preformated_error) )
        super().__init__(self.message)

def get_snakemake_info():
    return utils.ToolInfo("snakemake", ["snakemake", "--version"])

class ConfigManager():
    def __init__(self):
        self.config = {}


    def get(self, optname):
        return self.config[optname]

    def set(self, optname, value):
        self.config[optname] = value

    def to_yaml_str(self) -> str:
        return yaml.dump(self.config) 

    def to_yaml_file(self, filename):
        """ writing config to yaml file
        """
        try:
            print(self.to_yaml_str(), sep="", end="", file=filename)
        except AttributeError as e:
            with open(filename, "w") as w_fh:
                print(self.to_yaml_str(), sep="", end="", file=w_fh)

    def from_yaml_file(self, yaml_file):
        self.config = yaml.load(yaml_file)

    def update_from_dict(self, _dict):
        for key in _dict:
            self.set(key, _dict[key])

    def update_from_yaml_file(self, yaml_file):
        tmp_config = yaml.load(yaml_file)
        self.update_from_dict(tmp_config) 


class SnakeApp(abc.ABC):
    """Main Class for creation of new snakemake apps

    This class is abstract and needs to be subclassed to create a concrete
    implementation.

    Building Block System:

    It uses a building block concept to allow for maximum flexibility.

    ConfigManager:

        Configs are managed by :obj:`ConfigManager` classes that can freely be
        replaced by user classes that implement the same interface.

        Config Manager are activated by registering them via the
        :obj:`SnakeApp.register_config_manager` method

    SampleManager:

        Sample Parsing is delegated to the :obj:`sample_manager.base.SampleManager` class family 
        inheriting from the same named superclass. 
        This allows to swap out a Illumina detecting fastq parser with one working
        on pacbio longreads without interfering with the program flow. 
    """
    def __init__(
            self,           
            appname="snakeapp", 
            config_name="snake_config.yaml"):
        """
        Args:
            appname (:obj:`str`): (optional, default="snakeapp") name of application
            config_name (:obj:`str`): (optional, default="snake_config.yaml")
                base name of config file used for this application
        """
        super().__init__()
        #: (:obj:`int`): cpus to use in snakemake call (default: 4) 
        self.cpus = 4
        #: (:obj:`str`): appname to use set by __init__ param  
        self.appname = appname
        self.config = None
        """ (:obj:`ConfigManager`): set by :obj:`register_config_manager` method
                and is None when invalid. 
        """
        self.blame = True
        """(:obj:`bool`): showing error producing lines in snakemake file,
            if set to True (default :obj:`True`)"""
        self.conda_prefix = None
        """(:obj:`str`): path to use as condaprefix allows quicker conda
            updates and minimizes disc clutter. (default: :obj:`None`)
            Not active if set to :obj:`None`.
        """
        self.config_file_name = config_name 
        self.input_config_path = None
        self.register_config_manager() 
        self.register_sample_manager()
        self.params_change_reexec = True
        self.code_change_reexec = False 
        self.app_splash = ""
        self.inputs = []
        self.parser = None
        self.sample_manager = None
        # Logging 
        self.logging_formatter = logging.Formatter(
                fmt='%(asctime)s - %(name)s - %(levelname)s: '
                    '>>>\n %(message)s\n<<<',
                datefmt='%d-%m-%Y %I:%M:%S %p')
        self.logger = None 
        self.log_file = None 
        self.args = None
        self.unknown_args = None
        self.prerun_snakecall = ["snakemake"] 
        self.reexec_dict = {}
        self.run_snakecall = ["snakemake"] 
        self.parser = self.get_argparser() 
        self.workdir = None
        self.snakefile = None
        self.user_needs_usage = False
        self.set_snakefile(os.path.join(os.path.dirname(__file__),
                           "Snakefile"))
        if not isinstance(self.parser, argparse.ArgumentParser):
            raise TypeNotArgumentParser(type(self.parser))
    
    def run(self, cmd=None):
        self.args, self.unknown_args = self.parser.parse_known_args(cmd)
        if self.logger is None:
           self._initialize_logging()
        self.init_setup() 
        utils.eprint(self.app_splash)
        self.set_config(self.args_to_config_dict())
        self.logger.info(
                "  Current Working Directory:\n"
                "     {cwd}\n"
                "\n"
                "  Command Line:\n"
                "     {cmd}\n"
                "\n"
                "  Log File:\n"
                "     {log}\n"
                "\n".format(
                      cmd=" ".join(sys.argv 
                                   if cmd is None 
                                   else [__file__] + cmd),
                      log=self.log_file,
                      cwd=os.path.realpath(".")))
        self.write_config_files()
        self.setup_run()
        try:
            self.prep_snake_ctrl()
            self.real_snake_call()
        except SNAKEMAKE_RUN_ERROR as e:
            self.logger.error("Encountered ERROR while running snakemake\n")
            self.logger.error("\n\nSnakemake Error Log:\n{elog}".format(elog=e.stdout))
            self.logger.error("\n\nSnakemake Stdout:\n{slog}".format(slog=e.stderr))
            raise e
        
    def _initialize_logging(self, level=logging.INFO):
        self.logger = logging.getLogger(self.appname)
        self.logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(self.logging_formatter)
        self.logger.addHandler(ch)

    def add_log_file(self, _file, level=logging.INFO):
        fh = logging.FileHandler(_file)
        fh.setLevel(level)
        fh.setFormatter(self.logging_formatter)
        try:
            self.logger.addHandler(fh)
        except AttributeError:
            self._initialize_logging()
            self.logger.addHandler(fh) 
        self.log_file = _file

    def register_config_manager(self, manager=ConfigManager):
        self.config = manager()

    def register_sample_manager(
            self, 
            manager=sample_manager.base.DummySampleManager):
        self.sample_manager = manager() 
        
    def set_config(self, config):
        if len(config) == 0:
            logger.warning("Config is empty!!")
        if not isinstance(config, dict):
            raise TypeError("Expected config dictionary not type {ty}".format(ty=type(config))) 
        self.config.update_from_dict(config)
        
    def _validate_config(self):
        errors = self.validate_config() 
        if errors:
            raise CONFIGURATION_ERROR(
                    errors, 
                    user_needs_usage=self.user_needs_usage)
    
    def validate_config(self) -> list:
        """ function designed to be overwritten 

        You should compile a list of errors based on
        the user errors encountered in the input.
        
        Returns:
            List[str]: The errors 
        """
        out = []
        return out
 
    def set_user_needs_usage(self):
        self.user_needs_usage = True

    def set_snakefile(self, _file):
        self.snakefile = os.path.realpath(_file)  
    
    def get_snakefile(self):
        return utils.check_if_file(self.snakefile)

    def set_app_splash(self, string):
        self.app_splash = string

    def get_app_splash(self):
        return self.app_splash
    
    def set_workdir(self, path):
        self.workdir = os.path.realpath(path) 
    
    def get_workdir(self):
        return utils.check_if_directory(self.workdir)
    
    def get_base_snakecall(self):
        return ["snakemake", "-s", self.get_snakefile(), 
                '--configfile', self.get_out_config_path(),
                "-d", self.get_workdir()]
    
    def set_cpus(self, num):
        self.cpus = num

    def get_cpus(self):
        return self.cpus
  
    def get_conda_prefix(self):
        return self.conda_prefix

    def set_conda_prefix(self, conda_dir):
        self.conda_prefix = conda_dir

    def get_snakefile_dir(self):
        return os.path.dirname(self.get_snakefile())
    
    def get_rerun_files(self):
        return [str(x) for x in self.reexec_dict]

    def get_out_config_path(self):
        return os.path.join(self.workdir, self.config_file_name)
    
    def get_input_config_path(self):
        return self.input_config_path
      
    def init_setup(self):
        """Optional Method for Initial setup after argument parsing

        Highly recommended to overide, if logging paths need customization or other
        lower level changes in the basic setup need to tale place.
        It is executed just after the arguments are parsed and you have 
        access to self.args.
        """
        pass

    def setup_run(self):
        """Optional Method that can be overriden for added functionality

        It is always being executed just before calling snakemake the first
        time and the optimal location for last minute setups. 
        """
        pass
         
    def register_logger(self, logger):
        """utility function that registers a logger"""
        if True:
            self.logger = logger
        
    @abc.abstractmethod     
    def get_argparser(self) -> argparse.ArgumentParser:
        """abstract method that returns an argument parser object"""
    
    @abc.abstractmethod     
    def args_to_config_dict(self) -> dict:
        """abstract method turns args namespace into config dict
        
        This method needs to be implemented when inheriting from this class

        Returns:
            :class:`dict`: it must return a dictionary that will then be
                translated into the proper config manager object

        """    
    
    def load_args_opt(self, config_opt_name="config"):
        """load argument namespace option
        
        Args:
            config_opt_name(:class:`str`): config value key
        Raises:
            ConfigOptionNameNotFound
        """
        try: 
            self._load_config_from_file(
                vars(self.args)[config_opt_name])
        except TypeError:
            raise ArgumentsNotParserError()
        except KeyError as e:
            raise ConfigOptionNameNotFound(config_opt_name)  
             
    
    def _load_config_from_file(self, config):
        if config is not None:
            with open(config, "r") as cfh:
                self.config = yaml.load(cfh, Loader=yaml.FullLoader) 
                self.input_config_path = os.path.realpath(config) 
    
    def load_config_if_exists(self):
        pass

    def write_config_files(self, overwrite=True):
        """ Write config files
        """
        conf_path = self.get_out_config_path()
        if not overwrite and os.path.isfile(conf_path):
            conf_path = self._handle_existing_file(conf_path)
        self.config.to_yaml_file(conf_path)


    def _handle_existing_file(self, conf_path):     
        conf_hash_old = utils.hashfile(conf_path)
        conf_strip = strip_empty_lines(conf.as_yaml().splitlines())
        conf_hash_new = utils.hashstring("\n".join(conf_strip))
        if conf_hash_old != conf_hash_new:
            logger.debug("Main Config has changed:\n"
                   "old: {conf_hash_old}\n"
                   "new: {conf_hash_new}".format(conf_hash_old=conf_hash_old,
                                                 conf_hash_new=conf_hash_new))
            conf_path = os.path.join(
                    os.path.dirname(conf_path),
                    "{timestamp}-{filename}".format(
                        timestamp=datetime.now().strftime("%Y%m%d-%H%M%S"),
                        filename=os.path.basename(conf_path)))
        return conf_path
    
    def prep_snake_ctrl(self):
        """ Snakemake Pre Run Control Logic based on ARGS from ArgumentParser

        Snakemake has the option to rerun if rule parameters changed.
        This is especially nice when benchmarking, because it only reruns
        rules affected by changed parameters.
        It also offers the ability detect code changes in rules
        """
        rerun_dict = {}
        snake_cmd=self.get_base_snakecall()
        snake_cmd.extend(["-n"])
        if self.params_change_reexec:
            self.prep_snake_call(
                snake_cmd + ["--list-params-changes"],
                "PARAMS_CHANGED")
        if self.code_change_reexec:
            self.prep_snake_call(
                snake_cmd + ["--list-code-changes"],
                "CODE_CHANGED")

    def prep_snake_call(self, snake_cmd, name="Change"):
        """ Subprocess Call for Pre Runs of Snakemake

        Rather convoluted attempt at getting the filenames of things
        to be reexecuted and error messages, if snakemake encounters error.

        rerun dict gets filled with filenames as keys, that contain a list of
        reasons for reexecution. This dict is also returned
        """
        self.logger.debug("Prep Snakemake Call that determines reexecution:\n" 
                     + " ".join(snake_cmd))
        try:
            with subprocess.Popen(snake_cmd, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE) as prep_proc:
                outs, err = prep_proc.communicate()
                ret = prep_proc.wait()
                if ret!=0:
                    handle_snakemake_syntax_error(
                            "{err}\n{out}".format(err=utils.mod_string(err),
                                                  out=utils.mod_string(outs)),
                                                  self.blame,
                                                  self.get_snakefile_dir())
                    raise SNAKEMAKE_RUN_ERROR(ret, call=' '.join(snake_cmd),
                                              stdout=utils.mod_string(outs),
                                              stderr=utils.mod_string(err))
                else:

                    for line in utils.mod_string(outs).splitlines():
                        if line.startswith("Building DAG of jobs"):
                            continue
                        if line not in self.reexec_dict:
                            self.reexec_dict[line] = []
                        self.reexec_dict[line]+=[name]
        except PermissionError as e:
            self.logger.error("Error in initial prep run while executing:\n", 
                         *snake_cmd)
            raise e

    def real_snake_call(self):
        """Run all the actual snakemake call

        Append the Reexecuted Files and all the options  that were not recognized
        by this script.
        """
        rerun_list = self.get_rerun_files()
        if rerun_list:
            rerun_list = ["-R"] + rerun_list

        conda_prefix = []
        if self.get_conda_prefix() is not None:
            conda_prefix = ['--conda-prefix', self.get_conda_prefix()]

        snake_cmd= (self.get_base_snakecall() 
                    + [ "--cores", str(self.get_cpus()) ] 
                    + rerun_list + self.unknown_args 
                    + ["--use-conda"] + conda_prefix)

        short_snake_cmd = (self.get_base_snakecall()
                           + [ "--cores", str(self.get_cpus()) ] 
                           + self.unknown_args 
                           + ["--use-conda"] + conda_prefix)
        if self.unknown_args:
            self.logger.info("Arguments not known are being appended to the snakemake call.\n"
                        "Please refer to the snakemake help for issues encountered.\n"
                        "     The arguments are:\n"
                        "{args}"
                        "".format(args=pprint.pformat(self.unknown_args)))
        self.logger.debug("Full Snakemake Call with reexec:\n" + " ".join(snake_cmd))
        self.logger.info("#---------------------------------------------------------------#\n"
                    "Snakemake command line to reproduce run follows:\n"
                    "(Notice: the full command is only available with --debug enabled)\n"
                    "-----------------------------------------------------------------\n"
                    "{cmd}\n"
                    "\n"
                    "#---------------------------------------------------------------#"
                    "".format(cmd=" ".join(short_snake_cmd)))
        with subprocess.Popen(snake_cmd) as main_proc:
            ret = main_proc.wait()
            if ret!=0:
                self.logger.error("Snakemake ecountered am Error")
                self.logger.debug("Snakemake Had Error: COMMAND LINE TO RECREATE BELOW\n"
                       "{snake_cmd}\n".format(snake_cmd=' '.join(snake_cmd)))
                raise SNAKEMAKE_RUN_ERROR(ret, call=" ".join(snake_cmd) )
        self.logger.info("Pipeline run succeded!\n"
                    "\n"
                    "Have a nice day.\n")



def handle_snakemake_syntax_error(string, blame, root_dir):
    """ Expand Error Messages with line number

    when in blame mode, run git blame on the 10 Surrounding lines
    """
    for line in string.splitlines():
        match = re.match(
                r".*(?P<stat>(Error|Exit|Exception)) in line (?P<line>\d+) of (?P<file>.*):", line)
        if match:
            match=match.groupdict()
            _file = match["file"]
            lnum = int(match["line"])
            if lnum < 19:
                start = 1
                end = 20
            else:
                start = lnum - 10
                end = lnum + 10
            if blame:
                try: 
                    run_blame(line, lnum, start, end, _file, root_dir)
                except subprocess.CalledProcessError:
                    run_awk(line, lnum, start, end, _file, root_dir) 
            else:
                run_awk(line, lnum, start, end, _file, root_dir) 

def run_blame(line, lnum, start, end, _file, root_dir):
    blame_pattern = (
            r"(?P<msg>[^\s]+ \([^)]+)\s+(?P<linenum>\d+)\)(?P<line>.+)")
    basic_blame_pattern = (
            r"(?P<msg>[^)]+)\)(?P<line>.+)")

    bounds = "{start},{end}".format(start=start,
                                    end=end)
    old_cwd = os.getcwd()
    try:
        os.chdir(root_dir)
        blame_cmd = ["git","blame", _file,
                     "-L{bounds}".format(bounds=bounds)]
        utils.eprint("")
        utils.eprint(*blame_cmd)
        response = utils.mod_string(subprocess.check_output(blame_cmd)).strip()
        for blame_line in response.splitlines():
            blame_dict = re.match(blame_pattern,
                                  blame_line).groupdict()
            sblame_dict = re.match(basic_blame_pattern,
                                   blame_line)
            if lnum != int(blame_dict["linenum"]):
                utils.eprint("{msg})     {line}".format(
                    msg=sblame_dict["msg"],
                    line=sblame_dict["line"]))
            else:
                utils.eprint("{msg}) >>> {line}".format(
                    msg=sblame_dict["msg"],
                    line=sblame_dict["line"]))
        utils.eprint("")
    finally:
        os.chdir(old_cwd)

def run_awk(line, lnum, start, end, _file, root_dir):
    old_cwd = os.getcwd()
    try:
        os.chdir(root_dir)
        awk_cmd = [
            "awk",
            "-vstart={start}".format(start=start),
            "-vend={end}".format(end=end),
            "-vln={ln}".format(ln=lnum),""" 
                (NR < start) {next} 
                 {if(NR==ln){ 
                    printf("%i >>> %s\\n", NR, $0)
                 }else{
                    printf("%i     %s\\n", NR, $0)
                 }}
                 (NR > end) {exit} """, _file]
        utils.eprint("\nError:")
        utils.eprint(line)
        utils.eprint("Culprit line in:\n{f}\n".format(f=_file))
        response = utils.mod_string(subprocess.check_output(awk_cmd)).strip()
        utils.eprint(response) 
    finally:
        os.chdir(old_cwd)
    

