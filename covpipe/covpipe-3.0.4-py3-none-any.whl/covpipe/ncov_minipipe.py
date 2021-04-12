#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from sys import version_info
from datetime import datetime, timedelta
from . import __version__ as version

import argparse
import glob
import hashlib
import json
import logging
import numpy as np
import os
import pandas
import pprint
import re
import shlex
import strictyaml
import subprocess
import sys
import time
import traceback
import urllib3
import yaml

version.get_more_info()

#   > 1. Parser Setup
#       > 1.2 Validation Functions for Argument Parsing
#   > 2 MAIN CONTROL FLOW
#   > 3 Dealing with configuration files
#       > 3.1 Validation
#       > 3.2 Construction
#           > 3.2.1 Config Utility Functions
#           > 3.2.2 Sample Config Setup
#       > 3.3 Dumping Configs to files
#   > 4. Calling Snakemake
#   > 5. Utility Section




class SNAKEMAKE_RUN_ERROR(Exception):
    def __init__(self, ret, stdout="", stderr="", call=""):
        self.ret = ret
        self.stdout = stdout
        self.stderr = stderr
        self.call = call
        self.message = "Snakemake call returned non zero exit status"
        super().__init__(self.message)

class NO_SAMPLES_ERROR(Exception):
    pass

class NO_CONFIG_FOUND_ERROR(Exception):
    def __init__(self, config_location):
        self.config_location = config_location


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

class QUIT_SAFE_ERROR(Exception):
    pass


SOURCE_DIR = os.path.dirname(os.path.realpath(__file__))
SNAKEFILE = os.path.join(SOURCE_DIR,"ncov_minipipe.snake")
DEFAULT_CONFIG_NAME = "ncov_minipipe.config"
DEFAULT_SAMPLE_CONFIG_NAME = "sample.config.yaml"
DEFAULT_CONFIG_TEMPLATE = os.path.join(SOURCE_DIR,"ncov_minipipe.config")
DEFAULT_DATA_DIR = os.path.join(SOURCE_DIR, "data")
DEFAULT_ADAPTERS = os.path.join(DEFAULT_DATA_DIR, "adapters")
DEFAULT_REFERENCE = os.path.join(DEFAULT_DATA_DIR, "NC_045512.2.fasta")
DEFAULT_ANNOTATION = os.path.join(DEFAULT_DATA_DIR, "NC_045512.2.gff")
BASIC_SNAKE_CALL = ["snakemake", "-s", SNAKEFILE]
ILLUMINA_LEGAL = "Oligonucleotide sequences © 2020 Illumina, Inc."

workdir_is_set = False
config_is_set = False

LEGACY_YAML_CONFIG_SCHEMA =  strictyaml.Map(
    {"samples": strictyaml.Str(),
     "output": strictyaml.Str(),
     "reference": strictyaml.Str(),
     "run_id": strictyaml.Str(),
     "var_annotation": strictyaml.Bool(),
     "cns_annotation": strictyaml.Str(), 
     "pangolin": strictyaml.Str(),
     "primer": strictyaml.Str(),
     "adapter": strictyaml.Str(),
     "var_special_interest": strictyaml.Str(),
     "var_call_cov": strictyaml.Int(),
     "var_call_count": strictyaml.Int(),
     "var_call_frac": strictyaml.Float(),
     "var_filter_mqm": strictyaml.Int(),
     "var_filter_sap": strictyaml.Int(),
     "var_filter_qual": strictyaml.Int(),
     strictyaml.Optional("read_filter_len"): strictyaml.Int(),
     strictyaml.Optional("read_filter_qual"): strictyaml.Int(),
     "cns_min_cov": strictyaml.Int(),
     "cns_gt_adjust": strictyaml.Float(),
     "krakenDb": strictyaml.Str(),
     "krakenTaxID": strictyaml.Int()})

# Settings for Default Config Schema
STRICT_YAML_CONFIG_SCHEMA = strictyaml.Map(
    {"samples": strictyaml.Str(),
     "output": strictyaml.Str(),
     "reference": strictyaml.Str(),
     "run_id": strictyaml.Str(),
     "var_annotation": strictyaml.Bool(),
     "cns_annotation": strictyaml.Str(), 
     "pangolin": strictyaml.Str(),
     "primer": strictyaml.Str(),
     "adapter": strictyaml.Str(),
     "var_special_interest": strictyaml.Str(),
     "var_call_cov": strictyaml.Int(),
     "var_call_count": strictyaml.Int(),
     "var_call_frac": strictyaml.Float(),
     "var_filter_mqm": strictyaml.Int(),
     "var_filter_sap": strictyaml.Int(),
     "var_filter_qual": strictyaml.Int(),
     "read_filter_len": strictyaml.Int(),
     "read_filter_qual": strictyaml.Int(),
     "cns_min_cov": strictyaml.Int(),
     "cns_gt_adjust": strictyaml.Float(),
     "krakenDb": strictyaml.Str(),
     "krakenTaxID": strictyaml.Int()})

# Default Filename Validation Schema to detect paired end data


DEFAULT_FILENAME_PATTERNS = [
    ("illumina_some_institute_1",{
        "regex":r"(?P<date>\d+)_(?P<lab_id>\d{2}-\d{4,5}(-[^_]+)?)_(?P<sample_id>.+)"
                r"_(?P<snum>S\d+)_(?P<lane>L\d{3})_(?P<read>R[12])"
                r"_(?P<running>\d{3})",
        "ambig": ["lane","running"]
        }),
    ("illumina1",{
        "regex":r"(?P<sample_id>.+)_(?P<snum>S[\d]+)_(?P<lane>L[\d]{3})_"
                r"(?P<read>R[12])_(?P<running>\d{3})",
        "ambig":["lane","running"] }),
    ("illumina2",{
        "regex":r"(?P<sample_id>.+)_(?P<snum>S[\d]+)_"
                r"(?P<read>R[12])_(?P<running>\d{3})",
        "ambig":["running"] }),
    ("illumina3",{
        "regex":r"(?P<sample_id>.+)_(?P<snum>S[0-9]+)_(?P<lane>L[0-9]{3})_"
                r"(?P<read>R[12])",
        "ambig":["lane"] }),
    ("illumina4",{
        "regex":r"(?P<sample_id>.+)_S(?P<snum>[0-9]+)_"
                r"(?P<read>R[12])",
        "ambig":[] }),
    ("illumina_fallback",{
        "regex":r"(?P<sample_id>.+)_"
                r"(?P<read>R[12])(?P<residual>_.+)?",
        "ambig":[] }),
    ("SRA",{
         "regex":r"(?P<sample_id>SR.+)_(?P<read>[12])",
         "ambig":[] }),

    ("fallback1",{
         "regex":r"(?P<sample_id>.+)_(?P<read>[A-Za-z0-9]+)",
         "ambig":[] }),
    ("fallback2",{
         "regex":r"(?P<sample_id>.+)\.(?P<read>[A-Za-z0-9]+)",
         "ambig":[],
         "sep":"."})
    ]

PAIRED_READ_REF = {
        "1":1,
        "2":2,
        "R1":1,
        "R2":2,
        "FORWARD":1,
        "REVERSE":2,
        "FWD":1,
        "REV":2,
        "F":1,
        "R":2,
        "P":1,
        "M":2,
        "PLUS":1,
        "MINUS":2,
        "SENSE":1,
        "ANTI":2
        }


class ToolInfoNotFoundError(Exception):
    def __init__(self, msg, ToolInfo):
        self.msg = (msg + 
                "\n > {call}: was not found in path\n "
                "and is also unreachable from the current working"
                "directory".format(call=ToolInfo.call)) 
        super().__init__(self.msg)

class ToolInfo():
    version_parser = lambda x: x
    def __init__(self, call,  version_call=[], version_parser=lambda x: x):
        self.call = call
        self.version_call = version_call
        self.version_parser = lambda x: x
        self.tool_found=False
        self.version_set=False
        self.path = None
        self.version= None
        self.get_tool_path() 
        self.get_version()
    
    def get_tool_path(self):
        self.tool_found = False
        try:
            response = mod_string(
                    subprocess.check_output(["which", self.call])).strip()
            self.path = response
            self.tool_found = True
        except:
            raise ToolNotFoundError("Could not find Tool", self)


    def get_version(self):
        self.version_set=False
        if not self.version_call:
            self.version = "UNKNOWN"
        else:
            try:
                response = mod_string(
                        subprocess.check_output(self.version_call)).strip()
                self.version = response
                self.version_set = True
            except:
                self.version = "NO_VERSION_FOUND"
                raise ToolInfoNotFoundError("Could not find Tool", self)
        
    

def get_snakemake_info():
    return ToolInfo("snakemake", ["snakemake", "--version"]) 
    

def main(snakemake=None,cmd=None):
    supress_error = False
    if snakemake is not None:
        cmd = get_snakecmd(snakemake) # Snakemake Support in >Utility Section<
    version_string = ("Version: {vers} - {ahead} ({commit}) {branch}".format(
                        vers=version.VERSION,
                        branch=(" | Branch: " + version.BRANCH)
                                if version.BRANCH != "master"
                                and version.AHEAD!=0
                                else "",
                        ahead=version.AHEAD if version.AHEAD != 0
                              else "release",
                        commit=version.COMMIT)
                      if version.ADVANCED_SET
                      else "Version: {vers} - release".format(vers=version.VERSION) )
    parser = get_parser(version_string=version_string)
    snake_info = get_snakemake_info()
    try:
        try:
            args, unknown_args = parser.parse_known_args(cmd)
            init_logging()
            if args.output is None:
                if args.conf is not None:    
                    args.output = str(load_config_allow_error(
                        args.conf, 
                        STRICT_YAML_CONFIG_SCHEMA)["output"])    
                else:
                    args.output = os.path.realpath(".")
            logpath = setup_log_dir(args)
            activate_logfile(logpath, 
                             logging.DEBUG 
                             if args.debug 
                             else logging.INFO)
            newer_version = get_newer_version()
            if newer_version is not None:
                logger.warning("!!There is a newer version available!!\n"
                               "You are using         {vers}\n"
                               "The newest release is {new_vers}\n\n"
                               "Install it with \"pip install covpipe --upgrade\""
                               "".format(vers=version.VERSION, 
                                         new_vers=newer_version))
            logger.info("\n"
                        "  ################################\n"
                        "  #                              #\n"
                        "  #  CovPipe a.k.a ncov_minipipe #\n"
                        "  #                              #\n"
                        "  ################################\n"
                        "\n"
                        "  Running Version:\n"
                        "     {vers}\n" 
                        "    (snakemake version): {snake_vers}\n"
                        "    (snakemake path): {snake_path}\n"
                        "\n"
                        "  Current Working Directory:\n"
                        "     {cwd}\n"
                        "\n"
                        "  Command Line:\n"
                        "     {cmd}\n"
                        "\n"
                        "  Log File:\n"
                        "     {log}\n"
                        "\n"
                        "".format(vers=version_string,
                                  snake_vers=snake_info.version,
                                  snake_path=snake_info.path,
                                  cmd=" ".join(sys.argv 
                                               if cmd is None 
                                               else [__file__] + cmd),
                                  log=logpath,
                                  cwd=os.path.realpath(".")))
            run_pipe(args,unknown_args)
        except NO_SAMPLES_ERROR :
            logger.error(
                    "\nERROR: Missing sample input!!!\n\n"
                    "{ignore_samples}".format(ignore_samples =
                        "You ran with the option --ignore_old_samples set!\n"
                        "That means you are ignoring the sample_config\n"
                        "specified in the main config file.\n\n"
                        if args.ignore_old_samples else "") +
                    "No fastq files where found in:\n"
                    "    -  Input command line argument (see help below)\n"
                    "{sample_config_opt}".format(sample_config_opt=
                        "" if args.ignore_old_samples
                        else
                        "    -  Sample config referenced in config.yaml also does not\n"
                        "       contain valid fastqs\n") +
                    "    -  Last resort lookup of files in current working "
                    "directory.\n"
                    "       and its subdirectories yielded no files\n\n"
                    "Please try again and provide input fastqs.\n\n")
            parser.print_help()
            raise QUIT_SAFE_ERROR()
        except CONFIGURATION_ERROR as e:
            logger.exception(e)
            if e.user_needs_usage:
                parser.print_help()
            raise QUIT_SAFE_ERROR()
        except SAMPLE_CONFIG_ERROR as e:
            logger.exception(e)
            raise QUIT_SAFE_ERROR()
        except SNAKEMAKE_RUN_ERROR as e:
            logger.error("Encountered ERROR while running snakemake\n")
            #logger.exception(e)
            logger.error("\n\nSnakemake Stdout Log:\n{elog}".format(elog=e.stdout))
            logger.error("\n\nSnakemake Error Log:\n{elog}".format(elog=e.stderr))
            supress_error = True
            raise e
    except QUIT_SAFE_ERROR:
        logger.error("\nQuitting because program encountered Error")
        exit(1)
    except Exception as e:
        logger.error(
               "\n\n==== Encountered unexpected ERROR ==== \n\n"
               'Sorry, this should not have happened!\n'
               "If you feel so inclined, please browse through the issues at\n"
               "https://gitlab.com/RKIBioinformaticsPipelines/ncov_minipipe/-/issues\n"
               "\n"
               "Hopefully this will resolve the Error you encountered.\n"
               "    Otherwise feel free to raise a new Issue.\n"
               "If you choose to do so, please provide the stack trace below\n"
               ", the operating system , a brief description how you ran the\n"
               "program and what you where trying to achieve.\n\n"
               "Alternatively you can write an email to:\n\n"
               "incoming+rkibioinformaticspipelines-ncov-minipipe-17578161-issue-@incoming.gitlab.com\n"
               )

        if not supress_error:
            logger.exception(e)
        exit(2)


def get_newer_version(proxy_par=None):
    retval = None
    url = "http://gitlab.com/api/v4/projects/17578161/releases"
    try:
        if proxy_par is None:
            proxy_par = os.getenv("HTTP_PROXY")
        if proxy_par is not None:
            proxy = urllib3.ProxyManager(proxy_par)
            r = proxy.request("GET", url)
        else:
            http = urllib3.PoolManager()
            r = http.request("GET", url)
        data = json.loads(r.data)
        new_vers_string = data[0]["tag_name"].strip("v")
        new_vers = tuple(new_vers_string.split("."))
        if tuple(version.VERSION.strip("v").split(".")) < new_vers:  
            retval = new_vers_string
    except json.decoder.JSONDecodeError:
        pass
    return retval


#   # 1. Parser Setup

def get_parser(version_string="Version: {vers} "
                              "- release".format(vers=version.VERSION)):
    """Setting up Argumentparser with help
    """

    parser = argparse.ArgumentParser(prog="ncov_minipipe",
                                     description=version_string)
    parser.add_argument("--input",  nargs="*",
                        help="Folders containing or Fastq files. "
                             "Can be specified multiple times",
                        default=[],
                        action='append', type=check_if_file_or_directory)
    parser.add_argument("--search_depth", default=2,type=int,
                        help="Maximum search depth for finding fastq files"
                             " in folders. Default is 2. "
                             "Set to 0 for unlimited searching")
    parser.add_argument("-o", "--outputfolder", help="Output Folder to use",
                        type=lambda x: workdir_set(mkdir_if_not_exists(x)),
                        dest="output")
    parser.add_argument("-V", "--variants_of_interest", dest="var_special_interest", 
                        help="VCF-File with variants of interest",
                        type=realpathify(validate_vcf_ext))
    parser.add_argument("--reference", 
                        help="Reference file to use (fasta). "
                             "Defaults to Sars-Cov-2 Wuhan sequence NC_045512.2"
                             ", if not set and --search_ncbi is not used.",
                        type=realpathify(validate_fasta_ext))
    parser.add_argument("--search_ncbi", 
                        help="Search query used to download annotation"
                        " and sequence file, if user wishes it. "
                        "Should be very specific.") 
    parser.add_argument("-k", "--kraken",
                         help="Kraken DB path. Should be a directory.",
                         type=check_if_directory)
    parser.add_argument("--log", help="logfile prefix to write to")
    parser.add_argument("--debug", action="store_true", 
                        help="Activate Debug level logging")
    parser.add_argument("--run_id" , help="Id used to identify runs."
                                          " Can be used multiple times for multiple ids",
                        action="append")
    parser.add_argument("--taxid",
                        help="Kraken Database taxonomy id to use for virus "
                             "read extraction. Default: 2697049",
                        default=2697049)
    parser.add_argument("--no-var-annotation", action="store_false", dest="var_annotation",
                        help="Disable annotation of genomic varaints with SnpEFF. Annotation"
                             "will be performed if this option is not set")
    parser.add_argument("--annotation_gff", "-A", dest="cns_annotation",
                        help="Annotation of genes in the consensus output sequence."
                             " Annotion file needs to be supplied in Gff format", 
                        type=realpathify(validate_gff_ext)) 
    parser.add_argument("--pangolin", "-P", type=get_pangolin_location,
                        help="Pangolin environment location."
                             "If provided, it runs pangolin from the environment"
                             )
    parser.add_argument("--use_last_config", action="store_true",
                        help="When this option is used, the pipeline uses "
                             "the newest config, already present in "
                             "output directory, as base configuration. "
                             "You can still augment this by supplying "
                             "parameters from the command line")
    #parser.add_argument("--annotation-file", help="GFF Annotation file",
    #                    type=validate_gff_ext)
    illuminagroup = parser.add_argument_group("Illumina Specific Settings")
    illuminagroup.add_argument("--adapter",
                                help="Illumina adapter sequences as fasta."
                                     ' Defaults to "Illumina Nextera Transposase adapter" '
                                     "{blurb}".format(blurb=ILLUMINA_LEGAL),
                                 type=realpathify(select_adapter))

    parser.add_argument("--cpus", type=int, default=4,
                        help="Jobs to allowed to run in parallel")
    parser.add_argument("-c","--conf", 
                        type=lambda x: config_set(check_if_file(x)),
                        help="Config file from previous run or manually"
                             " composed by user")
    parser.add_argument("--sample_conf", type=check_if_file,
                        help="User provided yaml file with samples")
    parser.add_argument("--primer", type=realpathify(lambda x: x),
                        help="Bedfile that contains the amplicon locations"
                             "needs to be compatible with bamclipper."
                             "https://bedtools.readthedocs.io/en/latest/content/general-usage.html#bedpe-format")
    parser.add_argument("--ignore_parameter_changes", action="store_true")
    parser.add_argument("--cns_min_cov", default=20, type=int,
                        help="The minimum number of reads required so"
                             " that the respective position in the"
                             " consensus sequence is NOT hard masked."
                             " Default: 20")
    parser.add_argument("--cns_gt_adjust", default=.9, type=float, 
                        help="Minimum fraction of reads supporting a "
                             "variant which leads to an explicit call "
                             "of this variant (genotype adjustment)."
                             " The value has to be greater than 0.5"
                             " but not greater than 1. "
                             "To turn genotype adjustment this off," 
                             " leave the value empty."
                             " Default: .9")
    parser.add_argument("--conda_prefix", type=realpathify(mkdir_if_not_exists),
                        default=os.getenv("SNAKE_CONDA_PREFIX"),
                        help="Specify a common directory to store conda environments."
                             " Default is using the value of the environment variable SNAKE_CONDA_PREFIX."
                             " If said env var is unset, use the current working directory")
    readgroup = parser.add_argument_group("Read Filter Options")
    readgroup.add_argument("--read_filter_len", default=50, type=int,
                           help="Minimum Read length. "
                                "Defaults to 50 BP "
                                "and should be lowered when using very short read protocols")
    readgroup.add_argument("--read_filter_qual", default=20, type=int,
                           help="Quality threshold for qualified quality "
                                 "of read as a Phredscore. Default: 20")
    vargroup = parser.add_argument_group("Variation Calling in Filter Options")
    vargroup.add_argument("--var_call_cov", default=20, type=int, 
                          help="Minimum coverage value to use for variant call."
                               " Default: 20")
    vargroup.add_argument("--var_call_count", default=10, type=int, 
                          help="Minimum read counts required for variant call."
                               " Default: 10")
    vargroup.add_argument("--var_call_frac", default=.1, type=float,
                          help="minimum fraction of obsevations supporting an"
                               "alternate allel in one sample. "
                               " Default: .1")
    vargroup.add_argument("--var_filter_mqm", default=40, type=int,
                          help="minimal mean mapping quality of observed"
                               " alternate alleles."
                               "The mapping quality (MQ) measures how good"
                               " reads align to the respective reference "
                               "genome region. Good mapping qualities are"
                               " around MQ 60. GATK recommends hard filtering"
                               " of variants with MQ less than 40."
                               " Default: 40")

    vargroup.add_argument("--var_filter_sap", default=-1, type=int,
                          help="Please define the strand balance probability"
                               "for the alternate allele (SAP)."
                               " The SAP is the Phred-scaled probability"
                               " that there is strand bias at the respective"
                               " site. A value near 0 indicates little or no"
                               " strand bias."
                               " For our use with Cleanplex TM Amplicons a strict"
                               " filter of 60 sufficed. But we recieved reports"
                               " of NimaGen Kit users, that reported missed variants"
                               " and decided to ignore the filter per default."
                               " Default: -1 meaning that no "
                               " strand bias filtering is performed")
    vargroup.add_argument("--var_filter_qual", default=10, type=int,
                          help="Please define the minimal variant call"
                               " quality. Freebayes produces a general"
                               " judgement of the variant call."
                               " Default=10")

    confgroup=parser.add_argument_group("Config Options")
    confgroup.add_argument("--overwrite_config", action="store_true")
    confgroup.add_argument("--ignore_old_samples", action="store_true")

    devgroup = parser.add_argument_group("Development Options")
    devgroup.add_argument("--blame", action="store_true")
    devgroup.add_argument("--code_reexec", action="store_true",
                          help="Reexec for files if snakemake detects that"
                               " rule content changed")
    return parser


#       # 1.2 Validation Functions for Argument Parsing

def check_if_file(_file):
    if not os.path.isfile(_file):
        raise ValueError("{_file} cannot be found".format(_file=_file))
    return _file

def workdir_set(_dir):
    global workdir_is_set 
    if _dir is None:
        workdir_is_set = False
    else:
        workdir_is_set = True
    return _dir

def config_set(config):
    global config_is_set
    if config is None:
        config_is_set = True
    else:
        config_is_set = False
    return config 
         
def select_adapter(adaptername):
    try:
        adapter = check_if_file(adaptername)
    except ValueError:
        adapters = files_from_dir(DEFAULT_ADAPTERS, adaptername)
        if len(adapters) == 1:
            adapter = os.path.join(DEFAULT_ADAPTERS, adapters[0])
        else:
            raise ValueError(
                    "No adapter file found for name/filepath:\n"
                    "{name}\n Please provide a valid filepath or"
                    "recognized names (see help)."
                    "".format(name=adaptername) 
                    if len(adapters) == 0 
                    else "Found to many possible adapter files:\n"
                         "{li}"
                        "".format(li="\n".join(
                            [os.path.basename(f) for f in adapters])))
    return validate_fasta_ext(adapter)



def check_if_directory(_dir):
    if not os.path.isdir(_dir):
        raise ValueError("{_dir} not a reachable directory".format(_dir=_dir))
    return _dir

def check_if_file_or_directory(_file_dir):
    if not os.path.isfile(_file_dir) and not os.path.isdir(_file_dir):
        raise ValueError("{_file_dir} cannot be found".format(_file_dir=_file_dir))
    return _file_dir

def validate_tsv_ext(_file, check_exists=True):
    """ Utility function that checks if tsv has correct extension

    Also checks if file exists
    """
    if not re.match(r'.*(.tab$|.tsv$)', _file):
        raise ValueError("{_file}: does not have a "
                         "standard fasta extension".format(_file=_file))
    if check_exists and not os.path.isfile(_file):
        raise ValueError("{_file}: does not exist".format(_file=_file))
    return _file

def validate_vcf_ext(_file, check_exists=True):
    """ Utility function that checks if tsv has correct extension

    Also checks if file exists
    """
    if not re.match(r'.*(.vcf$|.vcf.gz$)', _file):
        raise ValueError("{_file}: does not have a "
                         "standard fasta extension".format(_file=_file))
    if check_exists and not os.path.isfile(_file):
        raise ValueError("{_file}: does not exist".format(_file=_file))
    return _file

def validate_fasta_ext(_file, check_exists=True):
    """ Utility function that checks if fasta has correct extension

    Also checks if file exists
    """
    if not re.match(r'.*(.fa$|.fasta$|.fna$|.fn$)', _file):
        raise ValueError("{_file}: does not have a "
                         "standard fasta extension".format(_file=_file))
    if check_exists and not os.path.isfile(_file):
        raise ValueError("{_file}: does not exist".format(_file=_file))
    return _file

def validate_gff_ext(_file, check_exists=True):
    """ Utility function that checks if fasta has correct extension

    Also checks if file exists
    """
    if not re.match(".*.gff([23])?$", _file):
        raise ValueError("{_file}: does not have a "
                         "standard gff extension".format(_file=_file))
    if check_exists and not os.path.isfile(_file):
        raise ValueError("{_file}: does not exist".format(_file=_file))
    return _file

def realpathify(func):
    def realpathed_fun(*args, **kwargs):
        return os.path.realpath(func(*args, **kwargs))
    return realpathed_fun


def get_pangolin_location(pangolin):
    ranking_locations = [
            os.getenv("SNAKE_CONDA_PREFIX", 
                      default=DEFAULT_DATA_DIR),
            DEFAULT_DATA_DIR,
            "."]
    has_pangolin = False
    is_conda, prefix, has_pangolin = check_pangolin(pangolin, "pangolin")
    if is_conda and not has_pangolin:
        raise ValueError("Error with Pangolin Environment!:\n"
                         " Pangolin Not Found in Environment\n"
                         "Prefix: {prefix}\n"
                         "".format(prefix=prefix))
    if not is_conda:
        for location in ranking_locations:
            is_conda, prefix, has_pangolin = check_pangolin(
                    os.path.join(location, pangolin), "pangolin")  
            if is_conda and not has_pangolin:
                raise ValueError("Error with Pangolin Environment!:\n"
                                 " Pangolin Not Found in Environment\n"
                                 "Prefix: {prefix}\n"
                                 "".format(prefix=prefix))
            if has_pangolin:
                break
    if not is_conda:
        is_conda, prefix, has_pangolin = check_pangolin(None, pangolin)
        if is_conda and not has_pangolin:
            raise ValueError("Error with Pangolin Environment!:\n"
                             " Pangolin Not Found in Environment\n"
                             "Prefix: {prefix}\n"
                             "".format(prefix=prefix))
    if not is_conda:
        raise ValueError("No valid pangolin environment found!\n"
                         "input: {_input}\n"
                         "".format(_input=pangolin))
    return prefix


    

def check_pangolin(prefix, name):
    is_conda = False
    parsed_prefix = None
    found_pangolin = False
    prefix = prefix_augment(prefix) 
    try:
        call = ["conda", "list"] 
        if prefix is None:
            call.extend(["-n", shlex.quote(name)])
        else:
            call.extend(["--prefix", shlex.quote(prefix)])
        env_list = subprocess.check_output(
                """eval "$(conda shell.bash hook)"; {call}""".format(
                    call=" ".join(call)),
                shell=True,
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
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        pass
    return is_conda, parsed_prefix, found_pangolin


def prefix_augment(prefix):
    if prefix is None:
        return None
    if not prefix.endswith('/'):
        prefix = prefix + "/" 
    return prefix


def setup_log_dir(args):
    outdir = args.output
    if args.log is None:
        log_prefix = os.path.join(outdir, "ncov-minipipe-logs") 
        mkdir_if_not_exists(log_prefix) 
        logfile = "ncov-minipipe" 
        file_prefix = os.path.join(log_prefix,logfile)
        if os.path.isfile(file_prefix +".log"):
            logfile= "{_file}_{timestamp}.log".format(
                    _file=file_prefix, 
                    timestamp=datetime.now().strftime("%Y%m%d-%H%M%S"))
        else:
            logfile = file_prefix + ".log"
    else:
        logfile = args.log
    return logfile

def init_logging(level=logging.INFO):
    global logger
    logger = logging.getLogger("ncov-minipipe")
    logger.setLevel(level)
    formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s: '
                '>>>\n %(message)s\n<<<',
            datefmt='%d-%m-%Y %I:%M:%S %p')
    ch=logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def activate_logfile(log_path, level=logging.INFO):
    global logger
    logger.setLevel(level)
    formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s: '
                '>>>\n %(message)s\n<<<',
            datefmt='%d-%m-%Y %I:%M:%S %p')
    fh=logging.FileHandler(log_path)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


#   # 2 MAIN CONTROL FLOW

def run_pipe(args, unknown_args):
    """ Calling the Program

    Arguments:
        args: namespace generated by ArgumentParser
        unknown_args: list of commands that will be passed to snakemake
    """
    #import pdb; pdb.set_trace()
    rerun_dict = {}
    start_processing = time.time()
    logger.info("Building pipeline config and parsing samples...")
    config, sample_config, sample_conf_path, sample_data = build_config_from_args(args)
    done_parsing = time.time()
    logger.info("Done building configs and parsing samples.\n"
                "Took {time}".format(time=done_parsing - start_processing))
    logger.info("Writing config files...")
    config_path, sample_config_path = write_config_files(
                config, sample_config, str(config["output"]),
                args.overwrite_config, 
                sample_conf_path, sample_data=sample_data)
    logger.info("Done writing config files.")
    logger.info("Initial Snakmake prep run starting shortly...")
    prepared_snakemake_files = time.time()
    if os.path.isdir(os.path.join(args.output,".snakemake")):
        rerun_dict = prep_snake_ctrl(args, config_path, sample_config_path)
    if args.debug:
        with open(os.path.join(args.output, "rerun_list.yaml"), "w") as fh:
            yaml.dump(rerun_dict, fh)
    
    done_determining_reexec = time.time()
    logger.info("Snakemake prep run has finished succesfully.\n"
                "Took {time}".format(time=done_determining_reexec 
                                          - done_parsing))
    #epprint(rerun_dict)
    logger.info("Wrapper done with preperations.\n"
                "Running main pipeline shortly...")
    
    real_snake_call(args, unknown_args, config_path, sample_config_path,
                    list(rerun_dict.keys()))
    done_with_snakemake = time.time()
    logger.info("\nTotal Time: {ttime}\n"
                "The Pipeline took {stime} to finish.\n"
                "Wrapper preperations took {ptime}\n"
                "".format(ttime=format_time(done_with_snakemake 
                                            - start_processing),
                          stime=format_time(done_with_snakemake 
                                            - done_determining_reexec),
                          ptime=format_time(done_determining_reexec
                                            - start_processing)))


def format_time(seconds):
    return "{:0>8}".format(str(timedelta(seconds=seconds))) 

#   # 3 Dealing with configuration files

#       # 3.1 Validation
def validate_main_config(config):
    # Required Options
    errors = []
    user_needs_usage = False
    try:
        validate_fasta_ext(str(config["reference"]))
    except ValueError as e:
        errors.append(
                "Reference file provided does not meet specifications!\n"
                "{error}\n"
                "Please set a valid one by using the"
                " --reference option or\n"
                "setting the reference file in the config".format(error=e))
        user_needs_usage = True
    #   Adapter File
    try:
        validate_fasta_ext(str(config["adapter"]))
    except ValueError as e:
        errors.append(
                "Adapter file provided does not meet specifications!\n"
                "{error}\n"
                "Please set a valid one by using the"
                " --adapter option or\n"
                'setting the "adapter_list" field in the config'.format(
                    error=e))
        user_needs_usage = True

    # Amplicon Mode

    try:
        check_if_file(str(config["primer"]))
    except ValueError as e:
        if "PATH/TO" in str(config["primer"]).upper() or len(str(config["primer"])) == 0:
            config["primer"] = ""
        else:
            errors.append(
                    "Primer bedpe does not meet specifications!\n"
                    "{error}\n"
                    "When running in amplicon mode, the user needs to provide"
                    " a bed file containing the amplicon positions.\n"
                    "Use the --primer option or\n"
                    'set the "primer" field'
                    ' in the config you are using.\n\n'
                    "If you do not want to run in amplicon mode, you can"
                    "".format(error=e))
        
    if errors:
        raise CONFIGURATION_ERROR(errors, user_needs_usage=user_needs_usage)

    return config

def validate_sample_config(config, mixture=False,  paired=True,
                           check_files_exist=True):
    errors = []
    num_samples = len(config)
    paired_reads = []
    single_reads = []
    samples_broken_files = []
    no_reads = []
    if len(config) == 0:
        raise NO_SAMPLES_ERROR("No Samples selected to run!!!")
    for sample in config:
        reads = [(read, read in config[sample])
                 for read in ["read1", "read2"]]
        num_readfiles = sum(v for _, v in  reads)
        if check_files_exist:
            readfiles_2_check = [(config[sample][read],
                                  os.path.isfile(config[sample][read]))
                                 for read, kexist in reads if kexist]

            if sum(not v for _, v in readfiles_2_check) != 0:
                samples_broken_files.append(
                    "Sample: {sample} file(s) do not exist:\n  "
                    "{file_list}"
                    "".format(sample=sample,
                              file_list="\n  ".join(
                                  [f for f, e in readfiles_2_check
                                   if not e])))


        if num_readfiles == 2:
            paired_reads.append(sample)
        elif num_readfiles == 1:
            single_reads.append(sample)
        else:
            no_reads.append(sample)
    # What if no read file provided
    if no_reads:
        errors.append(
                "Found {numreads} samples with neither a read1 or read2"
                " field in the sample config.\n"
                " Please make sure to specify at least one of them"
                "\n {only5}\n"
                "Samples Missing Read Files:\n\t"
                "{samples}".format(
                        numreads=len(no_reads),
                        only5="Note - Only showing 5\n"
                              if len(no_reads) > 5 else "",
                              samples="\n\t".join(no_reads[:5])))
    # What about the files that have broken links
    if samples_broken_files:
        errors.append(
                "Found {numreads} samples with non existent files.\n"
                "Please ensure that the filepaths are accessible from the"
                "working directory\n"
                "{only5}\n"
                "Samples Missing Read Files:\n  "
                "{samples}".format(
                        numreads=len(samples_broken_files),
                        only5="\nNote - Only showing 5\n"
                              if len(samples_broken_files) > 5 else "",
                              samples="\n  ".join(samples_broken_files[:5])))

    if ((paired and len(paired_reads) == num_samples) or
            (not paired and len(single_reads) == num_samples)):
        if errors:
            raise SAMPLE_CONFIG_ERROR(errors)
        return config
    # Validation for difficult cases
    if not mixture and paired and single_reads:
        errors.append(
                "Found {numreads} single end sample(s).\n"
                "Paired end reads in two separate files are needed\n"
                "Example for valid input files:\n"
                "   Sample1_R1.fastq.gz (R1|1|P|PLUS|FWD|SENSE)\n"
                "   Sample1_R2.fastq.gz (R2|2|M|MINUS|REV|ANTI)\n"
                "   Sample2_S2_L001_R1_001.fastq.gz\n"
                "   Sample2_S2_L001_R2_001.fastq.gz\n"
                "Deinterleave the files first, "
                "if you are sure they are paired!\n"
                "{only5}\n"
                "Samples missing a second file:\n  "
                "{samples}".format(
                        numreads=len(single_reads),
                        only5="\nNote - Only showing 5\n"
                              if len(samples_broken_files) > 5 else "",
                              samples="\n  ".join(single_reads[:5])))


    if errors:
        raise SAMPLE_CONFIG_ERROR(errors)

    return config

#       # 3.2 Construction

def build_config_from_args(args):
    config={}
    sample_config={}
    sample_manager_dict={}
    #  Assume config is located in working directory
    config_location=os.path.realpath(".")
    if args.output:
        config_location=args.output
    schema = STRICT_YAML_CONFIG_SCHEMA
    fallbackSchema = LEGACY_YAML_CONFIG_SCHEMA 
    found_config = False
    sample_conf_path = None
    config_file_path = None
    template_config = True

    with open(DEFAULT_CONFIG_TEMPLATE, "r") as conf_fh:
        try:
            config = strictyaml.load(conf_fh.read(), schema)
        except strictyaml.exceptions.YAMLValidationError as og_e:
            try: 
                conf_fh.seek(0)
                config = strictyaml.load(conf_fh.read(), fallbackSchema) 
            except strictyaml.exceptions.YAMLValidationError as e:
                context = og_e.args[2]
                logger.error(
                    "Error in Config:\n{before}\n"
                    " #vvvv Error Line vvvv#{lines}".format(
                        lines=context.lines(),
                        before=context.lines_before(10)))
                logger.exception(og_e)
                raise og_e 
        sample_conf_path=config["samples"].data
    # Check user provided
    if args.conf is not None:
        config=load_config_allow_error(args.conf, schema, config)
        config_file_path = args.conf
        sample_conf_path=config["samples"].data
        template_config = False  # User set config
    else:
        if args.use_last_config:
            try:
                config, config_file_path = find_newest_config(config_location,
                                                              schema, config)
                template_config = False # User set config
                sample_conf_path=config["samples"].data
            except NO_CONFIG_FOUND_ERROR:
                logger.warning("Warning: No old config found in Workdir")
    if args.sample_conf:
        sample_conf_path = args.sample_conf
    try:
        if sample_conf_path is not None:
            with open(sample_conf_path, "r") as samp_h:
                sample_config = yaml.safe_load(samp_h)
    except FileNotFoundError as e:
        if not template_config:
            logger.warning("Warning: Could not find valid sample yaml in \n"
                   "         user provided config",e)
    finally:
        sample_manager_dict = sample_builder(args, sample_config)
        sample_data = sample_manager_dict["sample_data"]
        sample_config = generate_sample_config(sample_data)
    config = augment_config_with_args(args, config)
    validate_main_config(config)
    validate_sample_config(sample_config)
    return config, sample_config, config_file_path, sample_data

def find_newest_config(config_location, schema, config,  warn=False):
    candidate_list = sorted(glob.glob(os.path.join(config_location,
                                      "*{def_conf}".format(
                                          def_conf=DEFAULT_CONFIG_NAME))),
                                      reverse=True)
    if len(candidate_list) > 1:
        logger.info("FOUND MULTIPLE CONFIGS!!!\n"
               "Consider setting the --overwrite_config flag\n%s"
               % ("\n".join(candidate_list)))
        logger.info('Choosing (Newest):\n',candidate_list[1])
        candidate = candidate_list[1]
    if len(candidate_list) == 1:
        candidate = candidate_list[0]
    if len(candidate_list) == 0:
        raise NO_CONFIG_FOUND_ERROR(config_location)
    config = load_config_allow_error(candidate, schema, config)
    config_file_path = candidate
    return config, config_file_path

#           # 3.2.1 Config Utility Functions

def load_config_allow_error(_file, schema, config={}):
    """ Function that loads and replaces a config file with strictyaml
    """
    with open(_file, "r") as conf_fh:
        #logger.info("Trying to load config:\n {_file}".format(_file=_file))
        try:
            config = strictyaml.load(
                    "\n".join(strip_empty_lines(conf_fh.readlines())),
                    schema)
        except strictyaml.exceptions.YAMLValidationError as e:
            #logger.info(e,"\n Found Config does not conform to schema")
            context = e.args[2]
            logger.warning("Error in Config:\n{before}\n"
                           " #vvvv Error Line vvvv#{lines}\n"
                           " Error: {exc}".format(lines=context.lines(),
                                                  before=context.lines_before(10),
                                                  exc=str(e)))

            conf_fh.seek(0)
            new_conf = strictyaml.load(
                    "\n".join(strip_empty_lines(conf_fh.readlines())))
            for key in new_conf:
                config[str(key)] = new_conf[key]
    return config


def augment_config_with_args(args, config):
    config["var_annotation"]=strict_bool(args.var_annotation)
    if args.reference is not None:
        config["reference"] = args.reference
    if args.run_id is not None:
        if not isinstance(args.run_id, list):
            args.run_id = [args.run_id]
        config["run_id"] = ",".join(args.run_id)
    # Annotation File
    if args.cns_annotation:
        config["cns_annotation"] = args.cns_annotation
    else:
        try:
            config["cns_annotation"] = validate_gff_ext(str(config["cns_annotation"]))
        except ValueError as e:
            if "PATH/TO" not in str(config["cns_annotation"]).upper():
                logger.warning("Annotation file in provided config not found!"
                               "\n File: {f}".format(f=str(config["cns_annotation"]))) 
            config["cns_annotation"] = ""
    # Illumina Adapter
    if args.adapter:
        config["adapter"] = args.adapter
    else:
        try:
            config["adapter"] = validate_fasta_ext(str(config["adapter"]))
            logger.info("Using adapter file provided in config")
        except ValueError as e:
            logger.info("No valid adpater fasta file provided!\nFalling back to "
                   '"Illumina Nextera Transposase adapter"'
                   '\n{blurb}'.format(blurb=ILLUMINA_LEGAL))
            config["adapter"] = validate_fasta_ext(
                    select_adapter("NexteraTransposase"))
    #  Amplification Primer
    if args.primer:
        config["primer"] = args.primer
    else:
        try:
            config["primer"] = str(config["primer"])
            logger.info("Using primer bedpe provided in config")
        except ValueError as e:
            pass
    if args.pangolin:
        config["pangolin"] = args.pangolin
    else:
        try:
            config["pangolin"] = get_pangolin_location(str(config["pangolin"]))
            logger.info("Using pangolin environment")
        except ValueError as e:
            logger.warning("Fallback pangolin environment from config not used."
                           "Directory not found: {env}".format(env=config["pangolin"]))
            config["pangolin"] =  ""
    # Variation Options
    config["var_call_cov"] = args.var_call_cov
    config["var_call_count"] = args.var_call_count
    config["var_call_frac"] = args.var_call_frac
    config["var_filter_mqm"] = args.var_filter_mqm
    config["var_filter_sap"] = args.var_filter_sap
    config["var_filter_qual"] = args.var_filter_qual
    
    config["read_filter_len"] = args.read_filter_len
    config["read_filter_qual"] = args.read_filter_qual
    config["cns_min_cov"] = args.cns_min_cov
    config["cns_gt_adjust"] = args.cns_gt_adjust
    if args.var_special_interest:
        config["var_special_interest"] = args.var_special_interest
    else:
        vcf_val =  str(config["var_special_interest"])
        try:
            config["var_special_interest"] = validate_vcf_ext(vcf_val)
        except ValueError as e:
            if "path/to" not in vcf_val or len(vcf_val) > 0:
                logger.warning("You need to provide a valid vcf file!\n"
                               "Falling back to not checking for variants of"
                               " interest.\n File: {f}\n"
                               "is not a proper vcf file. {e}"
                               "".format(f=vcf_val, e=str(e)))
            config["var_special_interest"] = ""

    # Secondary Primer Fasta

    if args.output:
        config["output"] = args.output
    else:
        if config["output"] is None or not os.path.isdir(str(config["output"])):
            config["output"] = os.path.realpath(".")
            args.output = str(config["output"])
    #  Kraken Database
    if args.kraken:
        config["krakenDb"] = args.kraken
    else:
        if config["krakenDb"] is None or not os.path.isdir(str(config["krakenDb"])):
            config["krakenDb"] = ""
    #  Tax ID
    if args.taxid:
        config["krakenTaxID"] = args.taxid
    else:
        if config["krakenTaxID"] is None or not str(config["kraken"]):
            config["krakenTaxID"] = ""

    if args.search_ncbi is None and args.reference is None:
        config["reference"] = DEFAULT_REFERENCE
        if args.cns_annotation is None:
            config["cns_annotation"] = DEFAULT_ANNOTATION

    return config



#           # 3.2.2 Sample Config Setup

def sample_builder(args, sample_config):
    rename = True
    res={"sample_data":pandas.DataFrame(
                columns=["path", "unambig_id", "ambig_id","read", "read_id",
                         "sample_id", "sub_sample_id",
                         "alt_sample_id", "alt_sub_sample_id",
                         "file","match","regex", "state"],
                ),
         "delta_files":[],
         "num_prev_samples":len(sample_config)}
    res['sample_data'].set_index(["path","unambig_id","ambig_id","read"], inplace=True, drop=False)
    #import pdb; pdb.set_trace()
    file_samples_alt_id =((sample_config[sample][key], sample,
                        default_if_not("alt_id", sample_config[sample],
                                       "PLACE_HOLDER"))
                        for sample in sample_config
                        for key in sample_config[sample]
                        if re.match("read[12]",key))
    # Add files from previously found sample file
    if args.ignore_old_samples:
        logger.warning("Warning: Skipping samples in config from old run")
    else:
        for (_file, sample, alt_id) in file_samples_alt_id:
            check_and_add_fastq([_file], res, None, sample_names=[sample],
                                alt_ids=[alt_id])

    # Add files added on the command line
    max_level=args.search_depth
    df_2_check = args.input
    df_2_check = [x for input_list in args.input for x in input_list]
    if len(sample_config) == 0 and len(df_2_check) == 0:
        df_2_check = [os.path.realpath(".")]
    for dirfile in df_2_check:
        if os.path.isfile(dirfile):
            check_and_add_fastq([dirfile], res, None)
        else:
            for pdir, _dir, _files in walklevel(dirfile, max_level):
                check_and_add_fastq(_files, res, pdir)

    # Modify Constructed Sample List
    # Ckeck how to deal with sampel names
    samp_data = res["sample_data"]
    resolve_sample_id_conflicts(args, samp_data)
    #eprint(res["sample_data"])
    return res

def check_and_add_fastq(_files, res, pdir, sample_names=None, alt_ids=None):
    single_mode = len(_files) == 1 and sample_names is not None
    patterns=dict(DEFAULT_FILENAME_PATTERNS)
    patterns_in_order = [key for key, _ in DEFAULT_FILENAME_PATTERNS]
    end=r'.(fq|fnq|fastq)(.gz)?'
    for _file in (fl for fl in _files if re.match(".*{end}".format(end=end),
                                                  fl)):
        if pdir is None:
            path = os.path.dirname(os.path.realpath(_file))
        else:
            path = os.path.realpath(pdir)
        _file = os.path.basename(_file)
        for pnum, pattern in enumerate(patterns_in_order):
            regex_string = ('{patternregex}{end}'.format(
                                patternregex=patterns[pattern]["regex"],
                                end=end))
            match = re.match(regex_string, _file)
            if match is None:
                if pnum-1 == len(patterns):
                    logger.error("FastQ does not meet any known spec:\n"
                           "file: {_file}".format(
                               _file=os.path.join(path,_file)))
                continue
            sep = default_if_not("sep", patterns[pattern],"_")
            ambig_keys=default_if_not("ambig",patterns[pattern], [])
            match_dict = match.groupdict()
            ambig = sep.join(match_dict[a]
                             for a in sorted(ambig_keys))
            nonambig = sep.join(match_dict[na]
                                for na in sorted(match_dict.keys())
                                if na not in ambig_keys + ["read"] 
                                and match_dict[na] is not None)
            sub_sample_id = sep.join(
                    [val if val is not None else ""  
                     for (_id, val) in list(match.groupdict().items())
                     if _id not in ["read"]])
            if pattern.startswith("illumina_some_institute"):
                matchdict = match.groupdict()
                sub_sample_id = "{sid}_{lid}".format(
                        sid=matchdict["sample_id"],
                        lid=matchdict["lab_id"])


            read = "R1"
            read_id = 1
            try:
                read = match_dict["read"]
            except KeyError:
                pass
            try:
                read_id = PAIRED_READ_REF[read.upper()]
            except KeyError:
                logger.warning("Warning: Read name \"",read,"\" not known")
                logger.warning("         Using Regex-pattern: {patt}\n"
                       "           {regex}\n"
                       "         File:\n"
                       "           {_file}"
                       "".format(patt=pattern, regex=regex_string,
                                 _file=_file))


            key=(path,nonambig,ambig,read)
            if key in res["sample_data"].index:
                break
            new_entry=pandas.DataFrame(dict(zip(res["sample_data"].columns,
                    ([a]
                     for a
                     in  [path, nonambig, ambig, read, read_id,
                          "PLACE_HOLDER",
                          sample_names[0] if single_mode
                                         and sample_names is not None
                                         else sub_sample_id,
                          "PLACE_HOLDER",
                          alt_ids[0] if single_mode
                                     and alt_ids is not None
                                     else "PLACE_HOLDER",
                          _file, pattern,
                          '{regexpattern}{end}'.format(
                              regexpattern=patterns[pattern]["regex"],end=end),
                          "new"]))))
            new_entry.set_index(["path","unambig_id","ambig_id","read"],inplace=True, drop=False)
            res["sample_data"]= res["sample_data"].append(new_entry)
            break
            #eprint(read, nonambig, ambig,  pattern, _file, path, sep='\t')
    #eprint(res["sample_data"][["sub_sample_id", "alt_sub_sample_id"]])


def resolve_sample_id_conflicts(args,  sample_data):
    generate_alternative_ids(sample_data)
    prelim_groups = sample_data.groupby(["sub_sample_id"]).groups
    for sub_id in prelim_groups:
        paths_subgroup = sample_data[
                sample_data.sub_sample_id == sub_id].groupby(level="path").groups
        num_subids = len(paths_subgroup)
        if  num_subids == 1:
            continue
        logger.warning("Warning: Found multiple samples "
                "({num}) with sample id {sub}!\n".format(num=num_subids,
                                                       sub=sub_id) +
                '"DUPLICATE_[Number]_" will be prepended to duplicates')
        for (_id, path) in enumerate(paths_subgroup):
            if _id == 0: # Skip first occurance
                continue
            sample_data.loc[((sample_data.sub_sample_id == sub_id) &
                             (sample_data.path == path)) ,
                             "sub_sample_id"] = "Duplicate_{_id}_{samp}".format(
                                     _id=_id, samp=sub_id)



def generate_alternative_ids(sample_data):
    if not ((sample_data["alt_sub_sample_id"]=="PLACE_HOLDER").any()):
        # All Samples known and will just be passed on
        return
    old_samples = sample_data.loc[
            sample_data.alt_sub_sample_id != "PLACE_HOLDER"].copy()
    old_sample_groups = old_samples.groupby(
            level=["path", "unambig_id"]).groups
    num_old_samples = len(old_sample_groups)
    new_samples = sample_data.loc[
            sample_data.alt_sub_sample_id == "PLACE_HOLDER"].copy()
    new_sample_groups = new_samples.groupby(
            level=["path","unambig_id"]).groups
    for key in (key
                for key in new_sample_groups if key in old_sample_groups):
        new_sample_data = sample_data.loc[new_sample_groups[key]].copy()
        old_sample_data = sample_data.loc[old_sample_groups[key]].copy()
        old_sample_sub_groups = old_sample_data.groupby(
                level=["ambig_id"]).groups
        new_sample_sub_groups = new_sample_data.groupby(
                level=["ambig_id"]).groups
        for sub_key in (s_key
                    for s_key in new_sample_sub_groups
                    if s_key in old_sample_sub_groups):
            old_alt_id = old_sample_data.loc[
                    old_sample_sub_groups[sub_key]].alt_sub_sample_id[0]
            sample_data.loc[
                    new_sample_sub_groups[sub_key],
                    "alt_sub_sample_id"] = old_alt_id

        for sub_key in (skey
                    for skey in new_sample_sub_groups
                    if skey not in old_sample_sub_groups):
            raise RuntimeError(
                    "Use of given sample names and conflict resolution through"
                    " longest common prefix is not implemented yet!!!")

    new_samples = sample_data.loc[
            sample_data.alt_sub_sample_id == "PLACE_HOLDER"].copy()
    new_sample_groups = new_samples.groupby(
            level=["path","unambig_id"]).groups
    for (_id,(path, unambig)) in enumerate(new_sample_groups):
        main_name = "Sample_{nid}".format(nid=_id + 1 + num_old_samples)
        sample_data.loc[
                new_sample_groups[(path, unambig)],
                                  "alt_sample_id" ] = main_name
        sub_groups = sample_data[
                sample_data.alt_sample_id == main_name].groupby(
                        level=["ambig_id"]).groups
        if len(sub_groups)==1:
            # Easy Case when Sample not split between lanes or
            # in multiple files with differing running number
            sample_data.loc[sample_data.alt_sample_id == main_name,
                            "alt_sub_sample_id"] = main_name
        else:
            #import pdb; pdb.set_trace()
            for (_id, ambig) in enumerate(sub_groups):
                sample_data.loc[((sample_data.alt_sample_id == main_name) &
                               (sample_data.ambig_id == ambig)),
                              "alt_sub_sample_id"] = "{sid}.{nid}".format(
                                      sid=main_name, nid=_id+1)
    if (sample_data["alt_sub_sample_id"]=="PLACE_HOLDER").any():
        logger.debug(sample_data[["sub_sample_id","alt_sub_sample_id"]])
        raise RuntimeError("Some unique ids could not be assigned")


def generate_sample_config(sample_data):
    samples = dict(
          (key, dict(("read{read}".format(read=read_id), os.path.join(
                            sample_data[(
                                (sample_data.sub_sample_id==key) &
                                (sample_data.read_id == read_id))].path[0],
                            sample_data[(
                                (sample_data.sub_sample_id==key) &
                                (sample_data.read_id == read_id))].file[0]
                            ))
                     for read_id in sample_data[
                         sample_data.sub_sample_id==key].read_id ))
          for key in sample_data.sub_sample_id)
    for key in samples:
        samples[key]["alt_id"] = sample_data[
                sample_data.sub_sample_id==key].alt_sub_sample_id[0]
    return samples


#       # 3.3 Dumping Configs to files

def write_config_files(conf, samp_conf, outdir, conf_path,
                       overwrite=False, sample_data=None):
    """ Write config files
    """
    if not conf_path:
        conf_path = os.path.realpath(
                os.path.join(outdir, DEFAULT_CONFIG_NAME))
    samp_path = os.path.realpath(
            os.path.join(outdir, DEFAULT_SAMPLE_CONFIG_NAME))


    if not overwrite and os.path.isfile(samp_path):
        samp_hash_old = hashfile(samp_path)
        samp_hash_new = hashstring(yaml.dump(samp_conf))
        if samp_hash_old != samp_hash_new:
            logger.debug("Sample Config hash changed:\n"
                    "old: {samp_hash_old}\n"
                    "new: {samp_hash_new}".format(samp_hash_old=samp_hash_old,
                                                  samp_hash_new=samp_hash_new))
            samp_path = os.path.join(
                    os.path.dirname(samp_path),
                    '{timestamp}-{filename}'.format(
                        timestamp=datetime.now().strftime("%Y%m%d-%H%M%S"),
                        filename=os.path.basename(samp_path)))

    if not overwrite and os.path.isfile(conf_path):
        conf_hash_old = hashfile(conf_path)
        conf_strip = strip_empty_lines(conf.as_yaml().splitlines())
        conf_hash_new = hashstring("\n".join(conf_strip))
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
    if sample_data is not None:
        with open(os.path.join(os.path.dirname(conf_path),
                               "sample_parse.tsv"), "w") as tsv_fh:
            sample_data.to_csv(tsv_fh, sep="\t")
    conf["samples"]=samp_path
    with open(conf_path,"w") as conf_fh:
        strip_yaml = strip_empty_lines(conf.as_yaml().splitlines())
        print("\n".join(strip_yaml), file=conf_fh)
    with open(samp_path,"w") as samp_fh:
        yaml.dump(samp_conf, samp_fh)
    return conf_path, samp_path


#   # 4. Calling Snakemake



def prep_snake_ctrl(args, config_path, sample_config_path):
    """ Snakemake Pre Run Control Logic based on ARGS from ArgumentParser

    Snakemake has the option to rerun if rule parameters changed.
    This is especially nice when benchmarking, because it only reruns
    rules affected by changed parameters.
    It also offers the ability detect code changes in rules
    """
    rerun_dict = {}
    snake_cmd=BASIC_SNAKE_CALL + ["-d", args.output,
                                  '--configfile', config_path] + ["-n"]
    if not args.ignore_parameter_changes:
        rerun_dict = prep_snake_call(args, rerun_dict,
                                     snake_cmd + ["--list-params-changes"],
                                     "PARAMS_CHANGED")
    if args.code_reexec:
        rerun_dict = prep_snake_call(args, rerun_dict,
                                     snake_cmd + ["--list-code-changes"],
                                     "CODE_CHANGED")
    return rerun_dict

def prep_snake_call(args, rerun_dict, snake_cmd, name="Change"):
    """ Subprocess Call for Pre Runs of Snakemake

    Rather convoluted attempt at getting the filenames of things
    to be reexecuted and error messages, if snakemake encounters error.

    rerun dict gets filled with filenames as keys, that contain a list of
    reasons for reexecution. This dict is also returned
    """
    logger.debug("Prep Snakemake Call that determines reexecution:\n" 
                 + " ".join(snake_cmd))
    try:
        with subprocess.Popen(snake_cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as prep_proc:
            outs, err = prep_proc.communicate()
            ret = prep_proc.wait()
            if ret!=0:
                try:
                    handle_snakemake_syntax_error(
                            "{err}\n{out}".format(err=mod_string(err),
                                                  out=mod_string(outs)),
                                                  args.blame)
                except AttributeError:
                    pass
                raise SNAKEMAKE_RUN_ERROR(ret, call=' '.join(snake_cmd),
                                          stdout=mod_string(outs),
                                          stderr=mod_string(err))
            else:

                for line in mod_string(outs).splitlines():
                    if line.startswith("Building DAG of jobs") or line.startswith("Migrati"):
                        continue
                    if line not in rerun_dict:
                        rerun_dict[line] = []
                    rerun_dict[line]+=[name]
    except PermissionError as e:
        logger.error("Error in initial prep run while executing:\n", 
                     *snake_cmd)
        raise e
    return rerun_dict

def real_snake_call(args, unknown_args, conf, samp_conf, rerun_list):
    """Run all the actual snakemake call

    Append the Reexecuted Files and all the options  that were not recognized
    by this script.
    """

    rerun_list = [str(x) for x in rerun_list ]
    if rerun_list:
        rerun_list = ["-R"] + rerun_list
    conda_prefix = []
    if args.conda_prefix is not None:
        conda_prefix = ["-d", args.output,
                        '--conda-prefix', args.conda_prefix]
    snake_cmd=(BASIC_SNAKE_CALL + [ "--cores", str(args.cpus) ] +  ["--configfile", conf] +
               rerun_list + unknown_args + ["--use-conda"] + conda_prefix)
    short_snake_cmd =(BASIC_SNAKE_CALL + [ "--cores", str(args.cpus) ] +  ["--configfile", conf] +
                      unknown_args + ["--use-conda"] + conda_prefix)
    if unknown_args:
        logger.info("Arguments not known are being appended to the snakemake call.\n"
                    "Please refer to the snakemake help for issues encountered.\n"
                    "     The arguments are:\n"
                    "{args}"
                    "".format(args=pprint.pformat(unknown_args)))
    logger.debug("Full Snakemake Call with reexec:\n" + " ".join(snake_cmd))
    logger.info("#---------------------------------------------------------------#\n"
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
            logger.error("Snakemake ecountered am Error")
            logger.debug("Snakemake Had Error: COMMAND LINE TO RECREATE BELOW\n"
                   "{snake_cmd}\n".format(snake_cmd=' '.join(snake_cmd)))
            raise SNAKEMAKE_RUN_ERROR(ret, call=' '.join(snake_cmd),
                                      stdout="Snakemake call returned non zero exit status",
                                      stderr="not found")
    logger.info("Pipeline run succeded!\n"
                "\n"
                "Have a nice day.\n")



#   # 5. Utility Section

def get_snakecmd(snakemake):
    """Snake rule compatibility
    """
    return None

def mkdir_if_not_exists(_dir):
    """ Make direectory if it does not exist

    python 3.2 added the used exist_ok flag # PY3.2<
    """
    if _dir is None:
        return None
    os.makedirs(_dir, exist_ok=True)
    return os.path.realpath(_dir)


def eprint(*args, **kwargs):
    """Utillity function that prints to stderr
    """
    print(*args, file=sys.stderr, **kwargs)

def epprint(*args, **kwargs):
    """eprint for pprint"""
    pprint.pprint(*args, stream=sys.stderr, **kwargs)


# Sugar


def handle_snakemake_syntax_error(string, blame):
    """ Expand Error Messages with line number

    when in blame mode, run git blame on the 10 Surrounding lines
    """
    for line in string.splitlines():
        match = re.match(
                r".*(?P<stat>(Error|Exit|Exception)) in line (?P<line>\d+) of (?P<file>.*):", line)
        blame_pattern = (
                r"(?P<msg>[^\s]+ \([^)]+)\s+(?P<linenum>\d+)\)(?P<line>.+)")
        basic_blame_pattern = (
                r"(?P<msg>[^)]+)\)(?P<line>.+)"
                )
        if blame and match:
            match=match.groupdict()
            lnum = int(match["line"])
            if lnum < 19:
                bounds = "1,20"
            else:
                bounds = "{start},{end}".format(start=lnum-10,
                                                end=lnum+10)
            old_cwd = os.getcwd()
            try:
                os.chdir(SOURCE_DIR)
                _file = match["file"]
                blame_cmd = ["git","blame",  match["file"],
                             "-L{bounds}".format(bounds=bounds)]
                eprint("")
                eprint(*blame_cmd)
                response = mod_string(subprocess.check_output(blame_cmd)).strip()
                for blame_line in response.splitlines():
                    blame_dict = re.match(blame_pattern,
                                          blame_line).groupdict()
                    sblame_dict = re.match(basic_blame_pattern,
                                           blame_line)
                    if lnum != int(blame_dict["linenum"]):
                        eprint("{msg})     {line}".format(
                            msg=sblame_dict["msg"],
                            line=sblame_dict["line"]))
                    else:
                        eprint("{msg}) >>> {line}".format(
                            msg=sblame_dict["msg"],
                            line=sblame_dict["line"]))
                eprint("")
            finally:
                os.chdir(old_cwd)


def walklevel(some_dir, level=1):
    """ os walk with recursion limit

    Thanks to Stackoverflow User nosklo
    https://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
    """
    if level==0:
        yield os.walk(some_dir)
        return
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir, topdown=True):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def hashfile(_file, BLOCK_SIZE = 65536):
        """generate a Hash for a file

        straight copy and paste from
        https://nitratine.net/blog/post/how-to-hash-files-in-python/ (2020)
	"""
        # The size of each read from the file
        file_hash = hashlib.sha256()
        with open(_file, 'rb') as f:
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE)
        return file_hash.hexdigest()

def hashstring(string):
    string_hash = hashlib.sha256()
    string_hash.update(string.encode())
    return string_hash.hexdigest()


def default_if_not(key, _dict, default):
    try:
        return _dict[key]
    except KeyError:
        return default


def mod_string(string):
    if (version_info > (3, 0)):
        return string.decode()
    else:
        return string

def strip_empty_lines(string):
    return filter(lambda x: not re.match(r'^\s*$', x), string)


def strict_bool(b, choice=["false","true"]):
    return strictyaml.load(choice[b],strictyaml.Bool())

def files_from_dir(_dir, name):
    return [ f for f in os.listdir(_dir) if name.upper() in f.upper() ]



if __name__ == "__main__":
    """ Main Entry point when run from command line
    """
    main()
