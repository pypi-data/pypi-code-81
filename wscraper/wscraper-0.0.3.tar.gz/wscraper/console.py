# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.

import sys
import argparse

from .base import *


help_string = """
wscraper

Wikipedia Scraper
    language model using Wikipedia

Command:
    wscraper initialize
        make root directory of wscraper and config file
    wscraper init
        same as `wscraper initialize`
    wscraper new [task_name]
        create pattern named [task_name]
    wscraper status
        describe status of current task
    wscraper switch [task_name]
        change task to [task_name]
    wscraper import [xml path] [options]
        read [xml path] and locate wikipedia resource directory
    wscraper set [parameters]
        set parameters
    wscraper unset [parameters]
        unset parameters
    wscraper model new [model_name] [algorithm_name]
        create model for current task
    wscraper model delete [model_name]
        delete model for current task
    wscraper model build [model_name list]
        build model
    wscraper tokenizer [tokenizer_method]
        set tokenizer
    wscraper root status
        check root configuration
    wscraper root set [parameters]
        set root parameters
    wscraper root unset [parameters]
        unset root parameters
    wscraper list
        list tasks and wikipedia resources
    wscraper database status
        check database status for current task
    wscraper database set [parameters]
        set parameters for the database of current task
    wscraper database migrate [options]
        create tables of database
    wscraper database seed [names] [options]
        save data into database
"""


def command():
    if len(sys.argv) < 2:
        sys.stdout.write(help_string.lstrip())
        sys.exit(0)

    name = sys.argv[1]
    args = sys.argv[2:]

    map_command_function = {
        "new": command_new,
        "status": command_status,
        "switch": command_switch,
        "import": command_import,
        "set": command_set,
        "unset": command_unset,
        "model": command_model,
        "tokenizer": command_tokenizer,
        "root": command_root,
        "list": command_list,
        "database": command_database
    }

    if name in ["help", "--help"]:
        sys.stdout.write(help_string.lstrip())
    elif name in ["initialize", "init"]:
        command_initialize(args)
    elif name in map_command_function:
        map_command_function[name](args)
    else:
        sys.stderr.write(f"No such command `{name}`.\n{help_string}")
        sys.exit(1)


def command_initialize(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper initialize",
        description = "Command `wscraper initialize` creates primary files and directories."
    )

    args = parser.parse_args(args)

    Config.command_initialize()


def command_new(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper new",
        description = "Command `wscraper new` creates task."
    )

    parser.add_argument("name", help = "task name")

    args = parser.parse_args(args)

    Config.command_new(args.name)


def command_import(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper import",
        description = "Command `wscraper import` move a wikipedia.xml file to wscraper directory and split one to small files."
    )

    parser.add_argument("source", help = "source wikipedia.xml file")
    parser.add_argument("-n", "--name", help = "target directory name")
    parser.add_argument("-m", "--move", action = "store_true", help = "move file to wscraper directory for backup")
    parser.add_argument("-c", "--copy", action = "store_true", help = "copy file to wscraper directory for backup")
    parser.add_argument("-r", "--reset", action = "store_true", help = "remove existing file")

    args = parser.parse_args(args)

    if args.move and args.copy:
        sys.stderr.write("Both --move (-m) and --copy (-c) are given.\n")
        sys.exit(1)

    from .analysis.builder import Builder

    Builder.command_import(args.source, args.name, move = args.move, copy = args.copy, reset = args.reset)


def command_switch(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper import",
        description = "Command `wscraper import` move a wikipedia.xml file to wscraper directory and split one to small files."
    )

    parser.add_argument("name", help = "task name")

    args = parser.parse_args(args)

    Config.command_switch(args.name)


def command_status(args):
    if len(args) != 0:
        sys.stderr.write("No arguments required for `wscraper status`.")
        sys.exit(1)

    Config.command_status()


def command_model(args):
    if len(args) == 0:
        sys.stderr.write("Few arguments for wscraper model.\n")
        sys.stderr.write("wscraper model [name] [arguments]\n")
        sys.exit(1)

    name = args[0]
    args = args[1:]

    if name == "new":
        command_model_new(args)
    elif name == "delete":
        command_model_delete(args)
    elif name == "build":
        command_model_build(args)
    else:
        sys.stderr.write(f"No such command {name} for wscraper model.\n")
        sys.exit(1)


def command_model_new(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper model new",
        description = "Command `wscraper model new` creates model status."
    )

    parser.add_argument("name", help = "your favorite name for model")
    parser.add_argument("algorithm", help = "model algorithm")

    args = parser.parse_args(args)

    Config.command_model_new(args.name, args.algorithm)


def command_model_delete(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper model delete",
        description = "Command `wscraper model delete` creates model status."
    )

    parser.add_argument("name", help = "your favorite name for model")

    args = parser.parse_args(args)

    Config.command_model_delete(args.name)


def command_model_build(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper model build",
        description = "Command `wscraper model build` creates models for preserved algorithms and arguments."
    )

    parser.add_argument("name", nargs="*", help = "model name. Nothing indicates all models.")
    parser.add_argument("-r", "--reset", action = "store_true", help = "truncate existing models")

    args = parser.parse_args(args)

    from .algorithm import Algorithm

    Algorithm.command_build(model_name_list = args.name, reset = args.reset)


def command_root(args):
    if len(args) == 0:
        sys.stderr.write("wscraper root\n\n")
        sys.stderr.write("  wscraper root status\n")
        sys.stderr.write("  wscraper root set [options]\n")
        sys.stderr.write("  wscraper root delete [options]\n")
        sys.exit(1)

    name = args[0]

    if name == "status":
        command_root_status(args[1:])
    elif name == "set":
        command_root_set(args[1:])
    elif name == "unset":
        command_root_delete(args[1:])
    else:
        sys.stderr.write(f"No such command {name}.\n")
        sys.stderr.write("Command `wscraper root` takes `status`, `set` or `unset` for first argument.\n")
        sys.exit(1)


def command_root_status(args):
    if len(args) != 0:
        sys.stderr.write("No arguments required for `wscraper root status`.\n")
        sys.exit(1)

    Config.command_root_status()


def command_root_set(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper root set",
        description = "Command `wscraper root` describes or changes default value."
    )

    parser.add_argument("--wikipedia", help = "Wikipedia name")
    parser.add_argument("--worker", type=int, help = "the number of threads for working")
    parser.add_argument("--language", help = "Wikipedia language")
    parser.add_argument("--page_chunk", type=int, help = "page per xml file")

    args = parser.parse_args(args)

    Config.command_root_set(wikipedia = args.wikipedia, worker = args.worker, language = args.language, page_chunk = args.page_chunk)


def command_root_unset(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper root unset",
        description = "Command `wscraper root delete` deletes default config value."
    )

    parser.add_argument("--wikipedia", action = "store_true", help = "Wikipedia name")
    parser.add_argument("--worker", action = "store_true", help = "the number of threads for working")
    parser.add_argument("--language", action = "store_true", help = "Wikipedia language")

    args = parser.parse_args(args)

    Config.command_root_unset(wikipedia = args.wikipedia, worker = args.worker, language = args.language)


def command_set(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper set",
        description = "Command `wscraper set` sets value of parameter."
    )

    parser.add_argument("--wikipedia", help = "Wikipedia name")
    parser.add_argument("--worker", help = "the number of threads for working")
    parser.add_argument("--language", help = "Wikipedia language")

    args = parser.parse_args(args)

    Config.command_set(wikipedia = args.wikipedia, worker = args.worker, language = args.language)


def command_unset(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper unset",
        description = "Command `wscraper unset` unsets value of parameter."
    )

    parser.add_argument("--wikipedia", action = "store_true", help = "Wikipedia name")
    parser.add_argument("--worker", action = "store_true", help = "the number of threads for working")
    parser.add_argument("--language", action = "store_true", help = "Wikipedia language")

    args = parser.parse_args(args)

    Config.command_unset(wikipedia = args.wikipedia, worker = args.worker, language = args.language)


def command_tokenizer(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper tokenizer",
        description = "Command `wscraper tokenizer` set tokenizer."
    )

    parser.add_argument("method", help = "tokenizer method")

    args = parser.parse_args(args)

    Config.command_tokenizer(args.method)


def command_list(args):
    if len(args) != 0:
        sys.stderr.write("Command `wscraper list` requires no arguments.\n")
        sys.exit(1)

    Config.command_list()


def command_database(args):
    if len(args) == 0:
        sys.stderr.write("wscraper database\n\n")
        sys.stderr.write("  wscraper database status\n")
        sys.stderr.write("  wscraper database set [options]\n")
        sys.stderr.write("  wscraper database migrate\n")
        sys.stderr.write("  wscraper database seed\n")
        sys.exit(1)

    name = args[0]

    if name == "status":
        command_database_status(args[1:])
    elif name == "set":
        command_database_set(args[1:])
    elif name == "migrate":
        command_database_migrate(args[1:])
    elif name == "seed":
        command_database_seed(args[1:])
    else:
        sys.stderr.write(f"No such command {name}.\n")
        sys.stderr.write("Command `wscraper database` takes `status`, `set` or `save` for first argument.\n")
        sys.exit(1)


def command_database_status(args):
    if len(args) != 0:
        sys.stderr.write("Command `wscraper database status` requires no arguments.\n")
        sys.exit(1)

    Config.command_database_status()


def command_database_set(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper database set",
        description = "Command `wscraper database set` sets config of database."
    )

    parser.add_argument("--dialect", help = "dialect")
    parser.add_argument("--driver", help = "driver")
    parser.add_argument("--user", help = "user name")
    parser.add_argument("--password", help = "password")
    parser.add_argument("--host", help = "host")
    parser.add_argument("--port", type = int, help = "port")
    parser.add_argument("--database", help = "database name")
    parser.add_argument("--charset", help = "charset")

    args = parser.parse_args(args)

    Config.command_database_set(vars(args))


def command_database_migrate(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper database migrate",
        description = "Command `wscraper database migrate` creates tables of database."
    )

    parser.add_argument("-r", "--reset", action = "store_true", help = "drop tables if exist")

    args = parser.parse_args(args)

    from .database.database_handler import DatabaseHandler

    DatabaseHandler.command_database_migrate(reset = args.reset)


def command_database_seed(args):
    parser = argparse.ArgumentParser(
        prog = "wscraper database seed",
        description = "Command `wscraper database seed` inserts records into database."
    )

    parser.add_argument("-r", "--reset", action = "store_true", help = "drop tables if exist")
    parser.add_argument("names", nargs = "*", help = "target data you want, nothing to all")

    args = parser.parse_args(args)

    from .database.database_handler import DatabaseHandler

    DatabaseHandler.command_database_seed(args.names, reset = args.reset)
