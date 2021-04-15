from typing import List, Dict, Any, Union

Json = Union[List[Any], Dict[Any, Any], str]

# TODO: i think it may be more helpful to name functions like `yaml_read` as `yaml_from_string` or `yaml_to_json`


def yaml_files(path, *, include_yml_extensions: bool = False):
    """."""
    from d8s_file_system import directory_file_names_matching

    # TODO (oct 2020): in this example, we are potentially running the directory_file_names_matching function twice - I'm ok with this for now, but would like to consider caching results

    pattern = '*.yaml'
    files = directory_file_names_matching(path, pattern)

    if include_yml_extensions:
        yml_pattern = '*.yml'
        files.extend(directory_file_names_matching(path, yml_pattern))

    return files


def yaml_read(yaml_data: str):
    import yaml

    parsed_yaml_data = yaml.load(yaml_data, Loader=yaml.Loader)
    return parsed_yaml_data


def is_yaml(possible_yaml_data: str) -> bool:
    try:
        yaml_read(possible_yaml_data)
    except:
        return False
    else:
        return True


# todo: are there other input types possible?
def yaml_write(data: Json, **kwargs) -> str:
    import yaml

    result = yaml.dump(data, **kwargs)
    return result


# todo: are there other input types possible?
def yaml_clean(yaml_data: str) -> str:
    """Standardize the given yaml data."""
    return yaml_standardize(yaml_data)


# todo: are there other input types possible?
def yaml_standardize(yaml_data: str) -> str:
    """Standardize the given yaml data by reading and writing it."""
    read_data = yaml_read(yaml_data)
    sorted_data = yaml_write(read_data)
    return sorted_data


# todo: are there other input types possible?
def yaml_sort(yaml_data: str) -> str:
    return yaml_standardize(yaml_data)
