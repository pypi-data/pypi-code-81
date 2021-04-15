# Copyright (c) 2021 T.Furukawa
# This software is released under the MIT License, see LICENSE.


import re
import os
import sys
import shutil
import glob

from .constant import *
from .w_scraper_exception import *
from ..utility import *


class WScraperConfigError(WScraperException):
    pass


class Config:

    template_root_config = {
        "wikipedia": None,
        "worker": 1,
        "language": None,
        "page_chunk": 10000
    }

    template_config = {
        "wikipedia": None,
        "worker": None,
        "language": None,
        "tokenizer": {},
        "model": {},
        "database": {
            "dialect": None,
            "driver": None,
            "user": None,
            "password": None,
            "host": None,
            "port": None,
            "database": None,
            "charset": None
        }
    }

    template_root_status = {
        "current": None
    }

    @classmethod
    def check_root_directory_exists(cls):
        if not os.path.isdir(Constant.root_directory):
            message = f"Root directory {Constant.root_directory} does not exist."
            message += " Did you run `wscraper initialize`?"
            raise WScraperConfigError(message)

        if not os.path.isfile(Constant.root_config):
            raise WScraperConfigError(f"Root config file {Constant.root_config} does not exist.")

        if not os.path.isfile(Constant.root_status):
            raise WScraperConfigError(f"Root status file {Constant.root_status} does not exist.")

        if not os.path.isdir(Constant.wikipedia_directory):
            raise WScraperConfigError(f"Wikipedia directory {Constant.wikipedia_directory} does not exist.")

        if not os.path.isdir(Constant.task_directory):
            raise WScraperConfigError(f"Task directory {Constant.task_directory} does not exist.")

    @classmethod
    def command_root_status(cls):
        cls.check_root_directory_exists()

        config = cls.load_root_config()
        sys.stdout.write("\nRoot Status\n\n")
        sys.stdout.write(f"wikipedia: {config['wikipedia'] or '[not set]'}\n")
        sys.stdout.write(f"worker: {config['worker'] or '[not set]'}\n")
        sys.stdout.write(f"language: {config['language'] or '[not set]'}\n")
        sys.stdout.write(f"page_chunk: {config['page_chunk']}\n")
        sys.stdout.write("\n")

    @classmethod
    def command_root_set(cls, wikipedia, worker, language, page_chunk):
        cls.check_root_directory_exists()

        config = cls.load_root_config()

        if wikipedia is not None:
            if not os.path.isdir(os.path.join(Constant.wikipedia_directory, wikipedia)):
                raise WScraperConfigError(f"No such wikipedia resource {wikipedia}.")

            config["wikipedia"] = wikipedia

        if worker is not None:
            if not (worker >= Constant.min_worker and worker <= Constant.max_worker):
                raise WScraperConfigError(f"Worker should be integer in range from {Constant.min_worker} to {Constant.max_worker}.")

            config["worker"] = worker

        if language is not None:
            if language not in Constant.available_languages:
                raise WScraperConfigError(f"language `{language}` is not supported.")

            config["language"] = language

        if page_chunk is not None:
            if not (page_chunk >= Constant.min_page_chunk and page_chunk <= Constant.max_page_chunk):
                raise WScraperConfigError(f"page_chunk should satisfy {Constant.min_page_chunk} <= page_chunk <= {Constant.max_page_chunk}.")

            config["page_chunk"] = page_chunk

        FileManager.save_json(Constant.root_config, config)

    @classmethod
    def command_root_unset(cls, wikipedia, worker, language):
        cls.check_root_directory_exists()

        config = cls.load_root_config()

        if wikipedia:
            config["wikipedia"] = None

        if worker:
            config["worker"] = None

        if language:
            config["language"] = None

        FileManager.save_json(Constant.root_config, config)

    @classmethod
    def command_initialize(cls):
        if os.path.isdir(Constant.root_directory):
            sys.stdout.write(f"Root directory {Constant.root_directory} already exists.\n")

            if os.path.isfile(Constant.root_config):
                sys.stdout.write(f"Root config {Constant.root_config} already exists.\n")
            else:
                FileManager.save_json(Constant.root_config, cls.template_root_config)
                sys.stdout.write(f"Root config {Constant.root_config} was created.\n")

            if os.path.isfile(Constant.root_status):
                sys.stdout.write(f"Root status {Constant.root_status} already exists.\n")
            else:
                FileManager.save_json(Constant.root_status, cls.template_root_status)
                sys.stdout.write(f"Root status {Constant.root_status} was created.\n")

            if os.path.isdir(Constant.wikipedia_directory):
                sys.stdout.write(f"Wikipedia directory {Constant.wikipedia_directory} already exists.\n")
            else:
                os.makedirs(Constant.wikipedia_directory)
                sys.stdout.write(f"Wikipedia directory {Constant.wikipedia_directory} was created.\n")

            if os.path.isdir(Constant.task_directory):
                sys.stdout.write(f"Task directory {Constant.task_directory} already exists.\n")
            else:
                os.makedirs(Constant.task_directory)
                sys.stdout.write(f"Task directory {Constant.task_directory} was created.\n")
        else:
            os.makedirs(Constant.root_directory)
            sys.stdout.write(f"Root directory {Constant.root_directory} was created.\n")
            FileManager.save_json(Constant.root_config, cls.template_root_config)
            sys.stdout.write(f"Root config {Constant.root_config} was creaetd.\n")
            FileManager.save_json(Constant.root_status, cls.template_root_status)
            sys.stdout.write(f"Root status {Constant.root_status} was created.\n")
            os.makedirs(Constant.wikipedia_directory)
            sys.stdout.write(f"Wikipedia directory {Constant.wikipedia_directory} was created.\n")
            os.makedirs(Constant.task_directory)
            sys.stdout.write(f"Task directory {Constant.task_directory} was created.\n")

    @classmethod
    def command_new(cls, name):
        cls.check_root_directory_exists()

        name_format = r"^[a-zA-Z0-9_\-]+$"

        if re.search(name_format, name) is None:
            raise WScraperConfigError(f"Task name format shoud be composed of alphabet, number, underscore or hyphen.")

        new_directory = os.path.join(Constant.task_directory, name)

        if os.path.exists(new_directory):
            raise WScraperConfigError(f"Task name {repr(name)} already exists.")

        os.makedirs(new_directory)
        sys.stdout.write(f"New task was created at {new_directory}.\n")

        path_config = os.path.join(new_directory, "config.yml")
        path_status = os.path.join(new_directory, "status.yml")

        FileManager.save_json(path_config, cls.template_config)
        sys.stdout.write(f"Config file was created at {path_config}.\n")
        FileManager.save_json(path_status, {})
        sys.stdout.write(f"Status file was created at {path_status}.\n")

    @classmethod
    def command_switch(cls, name):
        cls.check_root_directory_exists()

        if not os.path.isdir(os.path.join(Constant.task_directory, name)):
            raise WScraperConfigError(f"Task name {name} does not exist.")

        path = os.path.join(Constant.root_directory, "status.yml")
        status = FileManager.load_json(path)
        status["current"] = name
        FileManager.save_json(path, status)
        sys.stdout.write(f"Task switched to {name}.\n")

    @classmethod
    def command_set(cls, wikipedia, worker, language):
        cls.check_root_directory_exists()

        config = Config()

        if wikipedia is not None:
            config.set_wikipedia(wikipedia)

        if worker is not None:
            config.set_worker(int(worker))

        if language is not None:
            config.set_language(language)

        config.save()

    @classmethod
    def command_unset(cls, wikipedia, worker, language):
        cls.check_root_directory_exists()

        config = Config()

        if wikipedia:
            config.unset_wikipedia()

        if worker:
            config.unset_worker()

        if language:
            config.unset_language()

        config.save()

    @classmethod
    def command_status(cls):
        cls.check_root_directory_exists()

        Config().print_status()

    @classmethod
    def command_model_new(cls, name, algorithm):
        cls.check_root_directory_exists()

        config = Config()
        config.create_model(name, algorithm)

    @classmethod
    def command_model_delete(cls, name):
        cls.check_root_directory_exists()

        config = Config()
        config.delete_model(name)

    @classmethod
    def command_tokenizer(cls, name):
        if name not in Constant.available_tokenizers:
            raise WScraperConfigError(f"No such tokenizer `{name}`.")

        config = Config()
        config.set_tokenizer(name)

    @classmethod
    def command_list(cls):
        sys.stdout.write("\n")

        list_task = []

        for path in glob.glob(os.path.join(Constant.task_directory, "*")):
            if os.path.isdir(path):
                list_task.append(os.path.basename(path))

        if len(list_task) == 0:
            sys.stdout.write("Available task is nothing.\n")
        else:
            sys.stdout.write("Available Task:\n")
            for item in list_task:
                sys.stdout.write(f"  - {item}\n")

        sys.stdout.write("\n")

        list_wikipedia = cls.list_wikipedia()

        if len(list_wikipedia) == 0:
            sys.stdout.write("Available Wikipedia is nothing.\n")
        else:
            sys.stdout.write("Available Wikipedia:\n")
            for item in list_wikipedia:
                sys.stdout.write(f"  - {item}\n")

        sys.stdout.write("\n")

    @classmethod
    def command_database_status(cls):
        cls.check_root_directory_exists()

        Config().print_database_status()

    @classmethod
    def command_database_set(cls, parameters):
        cls.check_root_directory_exists()

        config = Config()
        config.set_database_parameters(parameters)

    @classmethod
    def list_wikipedia(cls):
        items = []

        for path in glob.glob(os.path.join(Constant.wikipedia_directory, "*")):
            if os.path.isdir(path):
                items.append(os.path.basename(path))

        return items

    @classmethod
    def load_root_config(cls):
        return FileManager.load_json(Constant.root_config)

    @classmethod
    def load_root_status(cls):
        return FileManager.load_json(Constant.root_status)

    @classmethod
    def load_config_by_name(cls, name):
        path = os.path.join(Constant.task_directory, name, "config.yml")

        if not os.path.isfile(path):
            raise WScraperConfigError(f"Task name {name} does not exist.")

        return FileManager.load_json(path)

    @classmethod
    def load_status_by_name(cls, name):
        path = os.path.join(Constant.task_directory, name, "status.yml")

        if not os.path.isfile(path):
            raise WScraperConfigError(f"Task name {name} does not exist.")

        return FileManager.load_json(path)

    def __init__(self, name = None):
        self.check_root_directory_exists()

        if name is None:
            status = FileManager.load_json(Constant.root_status)
            name = status["current"]
            if name is None:
                raise WScraperConfigError("Current name is not set.")

        self.name = name
        self.config = self.load_config_by_name(name)
        self.root_config = self.load_root_config()
        self.status = self.load_status_by_name(name)
        self.root_status = self.load_root_status()
        self.this_directory = os.path.join(Constant.task_directory, self.name)

    def save(self):
        path = os.path.join(self.this_directory, "config.yml")
        FileManager.save_json(path, self.config)

    def print_status(self):
        print("\ncurrent task:", self.name)

        print()

        wikipedia = self.config["wikipedia"]

        if wikipedia is None:
            print("wikipedia [default]:", self.root_config["wikipedia"] or "[not set]")
        else:
            print("wikipedia:", wikipedia)

        worker = self.config["worker"]

        if worker is None:
            print("worker [default]:", self.root_config["worker"] or "[not set]")
        else:
            print("worker:", worker)

        language = self.config["language"]

        if language is None:
            print("language [defalt]:", self.root_config["language"] or "[not set]")
        else:
            print("language:", language)

        tokenizer = self.config["tokenizer"]

        if len(tokenizer) == 0:
            print("tokenizer: [not set]")
        else:
            print("tokenizer:")
            print("  method:", tokenizer["method"])
            print("  arguments:")
            for key, value in sorted(tokenizer["arguments"].items()):
                print(f"    {key}: {value}")

        model = self.config["model"]

        if len(model) == 0:
            print("model: [no model]")
        else:
            print("model:")
            for key in sorted(model.keys()):
                print(f"  {key}:")
                print(f"    algorithm: {model[key]['algorithm']}")
                print("    arguments:")
                for k, v in model[key]["arguments"].items():
                    print(f"      {k}: {v}")

        database = self.config["database"]

        if len([v for v in database.values() if v is not None]) == 0:
            print("database: [not set]")
        else:
            print("database:")
            for key, value in sorted(database.items()):
                print(f"  {key}: {value}")

        print()

    def get_parameter(self, key, *, must = False):
        data = self.config

        for k in key.split("."):
            if data is not None:
                data = data.get(k)

        if data is None and key in self.template_root_config:
            data = self.root_config[key]

        if data is None and must:
            raise WScraperConfigError(f"Key {key} must exist but None.")

        return data

    def set_wikipedia(self, name = None):
        wikipedia_list = self.list_wikipedia()

        if len(wikipedia_list) == 0:
            raise WScraperConfigError("There are no wikipedia resources.")

        if name is None:
            value_map = {}

            sys.stdout.write("Please select from these candidates.\n")

            for i, value in enumerate(wikipedia_list):
                value_map[i] = value
                sys.stdout.write(f"{i}: {value}\n")

            while name is None:
                user_input = input("Please select by number: ")

                try:
                    name = value_map[int(user_input)]
                except (ValueError, KeyError):
                    sys.stdout.write("Input value is invalid. Please try again.\n")
                except KeyboardInterrupt:
                    sys.stdout.write("Interrupted and not set.\n")
        else:
            if name not in wikipedia_list:
                raise WScraperConfigError(f"No such wikipedia resource {name}.")

        self.config["wikipedia"] = name
        self.save()

    def unset_wikipedia(self):
        self.config["wikipedia"] = None
        self.save()

    def set_worker(self, number):
        if not (type(number) == int and number in range(1, 64 + 1)):
            raise WScraperConfigError(f"Argument worker must satisfy 1 <= worker <= 64.")

        self.config["worker"] = number
        self.save()

    def unset_worker(self):
        self.config["worker"] = None
        self.save()

    def get_worker(self, must = False):
        return self.get_parameter("worker", must = must)

    def set_language(self, language):
        if language not in Constant.available_languages:
            raise WScraperConfigError(f"Language `{language}` is not supported.")

        self.config["language"] = language
        self.save()

    def unset_language(self):
        self.config["language"] = None
        self.save()

    def get_language(self, must = False):
        return self.get_parameter("language", must = must)

    def create_model(self, name, algorithm, arguments = None):
        if name in self.config["model"]:
            raise WScraperConfigError(f"Model {name} already exists.")

        if algorithm not in Constant.available_algorithms:
            raise WScraperConfigError(f"Algorithm {algorithm} is not supported.")

        if arguments is None:
            arguments = {}

        self.config["model"][name] = {
            "algorithm": algorithm,
            "arguments": arguments
        }

        self.save()

    def delete_model(self, name):
        if name not in self.config["model"]:
            raise WScraperConfigError(f"Config: Model \"{name}\" does not exist.")

        del self.config["model"][name]

        self.save()

    def delete_model_arguments(self, name, arguments = None):
        if name not in self.config["model"]:
            raise WScraperConfigError(f"Model {name} does not exist.")

        if arguments is None:
            self.config["model"][name]["arguments"] = {}
            self.save()
            sys.stdout.write(f"Arguments of model {name} was made empty.\n")
            return

        for arg in arguments:
            if arg in self.config["model"][name]["arguments"]:
                del self.config["model"][name]["arguments"][arg]
                sys.stdout.write(f"Argument {arg} is deleted.\n")
            else:
                sys.stdout.write(f"No such argument {arg}. Skipped.\n")

        self.save()

    def update_model_arguments(self, name, arguments = None):
        if name not in self.config["model"]:
            raise WScraperConfigError(f"Model {name} does not exist.")

        for key in arguments:
            self.config["model"][name]["arguments"][key] = arguments[key]

    def get_model(self, name = None, must = False):
        if name is not None:
            return self.get_parameter(f"model.{name}", must = must)
        else:
            return self.get_parameter("model", must = must)

    def model_name_exists(self, name):
        item = self.get_parameter("model", must = True)
        return name in item

    def confirm_model_names_exist(self, model_name_list):
        no_existing_list = []

        item = self.get_parameter("model", must = True)

        for model_name in model_name_list:
            if model_name not in item:
                no_existing_list.append()

    def set_tokenizer(self, method = None, arguments = None):
        if method is None:
            method = self.get_parameter("tokenizer.method", must = False)
            if method is None:
                raise WScraperConfigError(f"Tokenizer method is not set.")
        else:
            if method not in Constant.available_tokenizers:
                raise WScraperConfigError(f"Tokenizer `{method}` is not supported.")

        if arguments is None:
            arguments = {}

        self.config["tokenizer"] = {
            "method": method,
            "arguments": arguments
        }

        self.save()

    def unset_tokenizer(self):
        self.config["tokenizer"] = {}
        self.save()

    def get_tokenizer(self, must):
        return self.get_parameter("tokenizer", must = must)

    def get_wikipedia_xml(self, *, must = True):
        wikipedia_name = self.get_parameter("wikipedia", must = True)
        wikipedia_xml = os.path.join(Constant.wikipedia_directory, wikipedia_name + ".xml")

        if must and not os.path.isfile(wikipedia_xml):
            raise WScraperConfigError(f"No such file {wikipedia_xml}.")

        return wikipedia_xml

    def get_wikipedia_xml_directory(self, *, must = True, optional = False):
        wikipedia_name = self.get_parameter("wikipedia", must = True)
        wikipedia_xml_directory = os.path.join(Constant.wikipedia_directory, wikipedia_name)

        if must and not os.path.isdir(wikipedia_xml_directory):
            raise WScraperConfigError(f"No such directory {wikipedia_xml_directory}.")

        return wikipedia_xml_directory

    def make_workspace(self, workspace_name, exist_ok = True):
        target_directory = os.path.join(self.this_directory, "workspace", workspace_name)
        os.makedirs(target_directory, exist_ok = exist_ok)
        return target_directory

    def make_model_directory(self, exist_ok = True):
        model_directory = os.path.join(self.this_directory, "model")
        os.makedirs(model_directory, exist_ok = exist_ok)
        return model_directory

    def print_database_status(self):
        database = self.get_parameter("database", must = True)

        print("current task:", self.name)

        print("")
        print("database:")

        print("  dialect:", database.get("dialect") or "[not set]")
        print("  driver:", database.get("driver") or "[not set]")
        print("  user:", database.get("user") or "[not set]")
        print("  password:", database.get("password") or "[not set]")
        print("  host:", database.get("host") or "[not set]")
        print("  port:", database.get("port") or "[not set]")
        print("  database:", database.get("database") or "[not set]")
        print("  charset:", database.get("charset") or "[not set]")


    def set_database_parameters(self, parameters):
        database = self.get_parameter("database", must = True)

        for key, value in parameters.items():
            if value is None:
                continue

            before = database.get(key) or "[not set]"
            after = value
            database[key] = after
            sys.stdout.write(f"database config `{key}` changed: `{before}` -> `{after}`\n")

        self.config["database"] = database
        self.save()
