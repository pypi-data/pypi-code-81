from csvObject import CsvObject, write_csv

from pathlib import Path
import pickle
import json
import yaml
import gzip
import csv
import os


def directory_iterator(directory, file_only=True):
    """
    This takes a directory and returns a list of entries within that directory, if file_only is selected only
    files as apposed to directories will be returned

    :param directory: The directory you wish to iterate through
    :type directory: str

    :param file_only: Defaults to true where the return is just a list of files
    :type file_only: bool

    :return: List of entries from the directory
    :rtype: list
    """

    if file_only:
        return [file for file in os.listdir(directory) if os.path.isfile(f"{directory}/{file}")]
    else:
        return [file for file in os.listdir(directory)]


def load_json(path):
    """
    Read in a json file
    """
    with open(path) as ff:
        return json.load(ff)


def write_json(write_data, write_directory, write_name):
    """
    This writes out a json file

    :param write_data: Data you want to write out to a json file
    :type: write_data: Any

    :param write_directory: Where to write the json file
    :type write_directory: str

    :param write_name: Name of the database you want to write
    :type write_name: str

    :return: Nothing, just write out the file to the specified directory named the specified name
    :rtype: None
    """
    with open(f"{write_directory}/{write_name}.txt", "w", encoding="utf-8") as json_saver:
        json.dump(write_data, json_saver, ensure_ascii=False, indent=4, sort_keys=True)


def load_yaml(path_to_file):
    """
    Load the yaml file from package into scope
    """
    with open(path_to_file, "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError:
            raise yaml.YAMLError


def load_pickle(directory, file_name):
    """Load Pickle Data"""
    with open(Path(directory, file_name), 'rb') as handle:
        return pickle.load(handle)


def write_pickle(directory, file_name, data):
    """Write Pickle Data"""
    with open(Path(directory, file_name), 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def extract_headers(path):
    """
    Extract the first row from the file and return it as a list
    """
    with open(path) as header_extract:
        csv_data = csv.reader(header_extract)
        for row in csv_data:
            return row


def rename_headers(csv_file_path, new_headers, write_dir, write_name):
    """
    This will take a path to a csv file, and then re-write the file with a new set of headings. Headers to be replaced
    are accessed via key's from a dict of new_headers where the old headers to be replaced are the keys and the new
    headers to replace them the values

    :param write_name: Write Name
    :param write_dir: Write directory
    :param csv_file_path: path to a csv file
    :param new_headers: dict of Old Header: New Header
    :return: Nothing, override file with new headers
    """
    current_file = CsvObject(csv_file_path)

    # Change Headers that are within the new header Dict, otherwise just keep the old header
    reformed_headers = []
    for header in current_file.headers:
        try:
            reformed_headers.append(new_headers[header])
        except KeyError:
            reformed_headers.append(header)

    write_csv(write_dir, write_name, reformed_headers, current_file.row_data)


def open_setter(path):
    """
    Some files may be zipped, opens files according to the zip status

    :param path: File path
    :type path: Path
    :return: gzip.open if the file is gzipped else open
    """
    if path.suffix == ".gz":
        return gzip.open
    else:
        return open


def decode_line(line, zip_status):
    """
    Some files may be zipped, when we open zipped files we will need to decode them

    :param line: Current line from open file, zipped or otherwise
    :param zip_status: If the file is zipped or not
    :return: decoded line from the open file
    """
    if zip_status:
        return line.decode("utf-8").split()
    else:
        return line.split()


def validate_path(path, allow_none=True):
    """
    When we have multiple types of files and directories, some may be allow to be None as they will not be required
    whilst others like the working directory will always be required. This method is a generalisation of individual
    setters.

    :param path: Path to a directory or file
    :type path: str

    :param allow_none: Defaults to True, if true if a path is set to none it will just return None. If False, an
        assertion will be run to validate that it is not none. In both cases, should the file not be None, then the
        path is validated via Path.exists()
    :type allow_none: Bool

    :return: Path to the current file or directory if None return is not allowed, otherwise the Path return is
        optional and the return may be none.
    """
    if allow_none and not path:
        return None
    else:
        assert path and Path(path).exists(), f"Path is invalid: {path}"
        return Path(path)
