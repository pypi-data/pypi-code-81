# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""This support module contains path constants."""

import logging
import os


def get_preset_file_path():
    """
    Gives the path to the default build preset file relative to
    the Ode repository.
    """
    return os.path.join("util", "composer-presets.ini")


def get_old_project_values_file_path():
    """
    Gives the deprecated path to the file that contains constants
    of the project this script acts on relative to the Ode
    repository.
    """
    return os.path.join("util", "values.json")


def get_project_values_file_path():
    """
    Gives the path to the file that contains constants of the
    project this script acts on relative to the Ode repository.
    """
    return os.path.join("util", "project.json")


def get_product_file_path():
    """
    Gives the path to the file that contains constants of the
    project this script acts on relative to the Ode repository.
    """
    return "product.json"


def get_project_dependencies_file_path(source_root):
    """
    Gives the path to the file that contains constants of the
    dependencies of the project this script acts on relative to
    the Ode repository.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    old_file = os.path.join("util", "dependencies.json")
    if os.path.isfile(os.path.join(source_root, old_file)):
        logging.warning(
            "The file '%s' for providing dependency information is "
            "deprecated; use %s instead",
            old_file,
            get_project_values_file_path()
        )
        return old_file
    if os.path.isfile(
        os.path.join(source_root, get_project_values_file_path())
    ):
        logging.warning(
            "The file '%s' for providing dependency information is "
            "deprecated; use %s instead",
            get_project_values_file_path(),
            get_product_file_path()
        )
        return get_project_values_file_path()
    return get_product_file_path()


def get_github_api_file_path():
    """
    Gives the relative default path to the file where the
    information required to access the version 4 of the GitHub
    API can be found.
    """
    return os.path.join("util", ".github_api")
