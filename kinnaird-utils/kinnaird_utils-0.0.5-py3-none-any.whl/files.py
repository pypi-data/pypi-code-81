import os
import logging
import csv
import json
import yaml

logger = logging.getLogger(__name__)


def read_yaml_file(filename: str) -> dict:
    """
    Reads a YAML file, safe loads, and returns the dictionary

    :param filename: name of the yaml file
    :return: dictionary of YAML file contents
    """
    with open(filename, "r") as yaml_file:
        cfg = yaml.safe_load(yaml_file)
    return cfg


def read_csv_file(filename: str, delimiter: str = ",") -> list:
    results = []
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)
        for row in csv_reader:
            results.append(row)
    return results


def read_json_file(file: str) -> dict:
    with open(file) as f:
        contents = f.read()
        try:
            results = json.loads(contents)
        except json.decoder.JSONDecodeError as error:
            logger.debug(error)
            decoded_data = contents.encode().decode("utf-8-sig")
            results = json.loads(decoded_data)
    return results


def write_json_to_file(file: str, content: str) -> None:
    if os.path.exists(file):
        logger.debug("%s exists. Removing the file and replacing its contents." % file)
        os.remove(file)

    with open(file, "w") as f:
        json.dump(content, f, indent=4)


def write_file(file: str, content: str) -> None:
    if os.path.exists(file):
        logger.debug("%s exists. Removing the file and replacing its contents." % file)
        os.remove(file)
    with open(file, "w") as f:
        f.write(content)


def read_file(file: str) -> str:
    with open(file, "r") as f:
        content = f.read()
    return content


def remove_file_if_exists(file: str) -> None:
    if os.path.exists(file):
        logger.debug("%s exists. Removing" % file)
        os.remove(file)
