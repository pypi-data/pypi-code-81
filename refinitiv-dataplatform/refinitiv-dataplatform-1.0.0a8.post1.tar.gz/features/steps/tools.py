import fnmatch
import os
import json
import logging


def make_remove(config_path):
    def remove(filepath=None):
        path = filepath or config_path()

        if os.path.exists(path):
            try:
                os.remove(path)
            except PermissionError:
                pass

    return remove


def make_write(remove, config_path):
    def write(config, filepath=None, is_remove=True, silent=False):
        is_remove and remove(filepath)
        path = filepath or config_path()
        if not is_remove:
            with open(path, 'r') as f:
                d = {}
                try:
                    d = json.loads(f.read())
                except Exception as e:
                    if not silent:
                        raise e

            config.update(d)
        with open(path, 'w') as f:
            s = json.dumps(config)
            f.write(s)

    return write


def parse_path_value(path_value):
    *path, last = path_value.split('.')
    path_tail, value = last.split(':')
    path.append(path_tail)
    return path, value


def create_obj_with_value_by_path(path, value):
    res = root = {}

    if isinstance(path, list):
        *keys, last = path
    elif isinstance(path, str):
        *keys, last = path.split('.')
    else:
        raise Exception(path)

    for key in keys:
        next = {}
        root[key] = next
        root = next
    root[last] = value
    return res


def delete_file_by_path(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            logging.info("Deleted file: " + path)
        except PermissionError as err:
            logging.error("No permissions to delete the file: " + path)
            logging.error(err)
    else:
        logging.info("File does not exist: " + path)


def find_all_files_by_pattern(pattern, path):
    results = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                results.append(os.path.join(root, name))
    return results


def delete_all_custom_config_files_except_default(default_config_file_name):
    """
    This method searches all the config files in project root folder
    and deletes all found files skipping the default config file provided in parameter,
    and also config files in other test folders not related to bdd framework
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    config_files = find_all_files_by_pattern("rdplibconfig.*.json", project_root)
    for file in config_files:
        if file.__contains__(default_config_file_name) or \
                file.__contains__("client_test"):
            logging.info("Skipping the default config file: " + file)
        else:
            delete_file_by_path(file)
