import coloredlogs
import logging
from tqdm import tqdm
import argparse
import os
import os.path as osp
from copy import deepcopy
from typing import List

from .funcs.fun import *
from .iterator.randgen import *
from .config.config import *
from .util.reader import Reader


def file_from_directory(path: str) -> List[str]:
    files = list()
    for f in os.listdir(path):
        new_path = osp.join(path, f)
        if osp.isfile(new_path) and new_path.endswith(".mtx"):
            files.append(new_path)
        else:
            files += file_from_directory(new_path)
    
    return files


def main():
    # Set-up the logger
    logger = logging.getLogger(__name__)
    coloredlogs.install(level="DEBUG")
    logger.debug("Initialising ...")

    # Set-up the argument parser
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-d', '--dirs',   required=False, help="The directories with the matrix files", nargs="+", default=[])
    argparser.add_argument('-f', '--files',  required=False, help="The files containing the matrices",     nargs="+", default=[])
    argparser.add_argument('-c', '--conf',   required=False, help="Configuration for creating matrix",     nargs="+", default=[])
    argparser.add_argument('-o', '--output', required=True,  help="The output directory",                  type=str)
    argparser.add_argument('-i', '--info',   required=True,  help="Json file with info abount #matrices",  type=str)
    args = argparser.parse_args()

    # The info file must exists
    if not osp.isfile(args.info):
        logger.error("The file {} doesn't exists".format(args.info))
        return

    # At least one option between dirs and files has to be given.
    if not (args.dirs or args.files or args.conf):
        logger.error("At least one option between -d, -f and -c has to be given!")
        return 
    
    # If the given out dir doesn't exists, it has to be created.
    if not osp.isdir(args.output):
        os.system("mkdir -p {}".format(args.output))

    # Check if the given directory, or files does exists.
    new_src = args.dirs + args.files + args.conf
    cp_src = deepcopy(new_src)
    removed = False
    for file in new_src:
        if not (osp.isfile(file) or osp.isdir(file)):
            logger.error(f"{file} isn't neither a file or a directory ... dropped")
            cp_src.remove(file)
            removed = True
    
    new_src = cp_src
    
    if removed:
        logger.warning("Remainig just with this valid input: ")
        print()
        for idx, file in enumerate(new_src):
            tipo = "dir" if osp.isdir(file) else "file"
            print("{%d} [%s] -> %s" % (idx, tipo, file))
        print()
    else:
        logger.info("No input has be dropped")

    # List with matrices files initialized
    files = [x for x in new_src if osp.isfile(x) and x.endswith(".mtx")]
    logger.debug("List with matrices files initialized with:")
    print()
    print("\n".join(["{%d} -> %s" % (idx, f) for idx, f in enumerate(files)]) if files else "[]")
    print()

    # If -d option was given, I have to take all the .mtx files from the directories
    logger.debug("Checking for directories")
    directories = [x for x in new_src if osp.isdir(x)]

    if directories:
        logger.debug("Directories found")
        print()
        print("\n".join(["{%d} -> %s" % (idx, f) for idx, f in enumerate(directories)]))
        print()
        dirs_file = []
        for d in directories:
            dirs_file += file_from_directory(d)
        
        # If the result list have more than one occurrence for a file, It has to be removed
        old_file_list = deepcopy(files)
        files += dirs_file
        files = list(set(files))

        if old_file_list == files:
            logger.info("No new file has been pushed")
        else:
            logger.info("The new file list contain")
            print()
            print("\n".join(["{%d} -> %s" % (idx, f) for idx, f in enumerate(files)]))
            print()

    else:
        logger.info("No directories passed as input")

    # If -c option was given, I have to take all the configuration and create the .mtx file (if needed)
    logger.debug("Checking for configurations")
    conf_files = [x for x in new_src if x.endswith(".conf")]

    if conf_files:
        logger.debug("Configurations file found")
        print()
        print("\n".join(["{%d} -> %s" % (idx, f) for idx, f in enumerate(conf_files)]))
        print()

        # Recall the configuration extrapolator from module config.config
        configuration_dict = asyncio.run(ConfigExtrapolator.extrapolate_from_list(conf_files, logger))

        printable = ""
        for k, v in configuration_dict.items():
            printable += k + " -> "
            stringa = str(v[-1]) if len(v) == 1 else "(\n" + "\n".join([f"    {conf}" for conf in v]) + "\n)"
            printable += stringa + "\n\n"

        logger.debug("Extracted configurations")
        print()
        print(printable)
        print()

        logger.debug("Create and saving matrix into files")
        configuration_dict, returned_files = MatrixGen.save_matrices_from_configurations(configuration_dict, args.info)
        old_file_list = deepcopy(files)
        files += returned_files
        files = list(set(files))

        if old_file_list == files:
            logger.info("No new file has been pushed")
        else:
            logger.info("The new file list contain")
            print()
            print("\n".join(["{%d} -> %s" % (idx, f) for idx, f in enumerate(files)]))
            print()
    
    else:
        logger.info("No configurations file passed as input")

    # Starting to read from files
    logger.debug("Starting to read ...")
    ms = Reader.read_files(files, args.info)
    logger.debug("Finished reading from files ...")
    
    # Get matrices from the remaining configurations
    logger.debug("Getting matrices from the remaining configurations ...")
    ms += MatrixGen.get_matrix_from_configuration(configuration_dict)
    logger.debug("Finished getting matrices ...")



if __name__ == "__main__":
    print()
    main() 
    print()
