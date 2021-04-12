# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains type DependencyData for creating the
dependencies and the functions for handling the creation of
DependencyData objects for each dependency for the project.
"""

import importlib
import logging

from collections import namedtuple

from functools import partial

from .project_names import get_project_package_name


# The type 'DependencyData' represents the data to construct a
# dependency. Thus, the tuple contains various functions that the
# script utilizes when it constructs the dependencies.
#
# TODO: Functions
DependencyData = namedtuple("DependencyData", [
    "get_key",
    "get_name",
    "get_required_version",
    "should_install",
    "install_dependency"
])


def _should_install_dependency(
    module,
    data_node,
    build_test,
    build_benchmark,
    dependencies_root,
    version,
    target,
    host_system,
    installed_version
):
    """
    Tells whether the build of the dependency should be skipped.

    module -- The module from which the various functions are
    got.

    data_node -- The entry in the dependency JSON file containing
    the data for the dependency in question.

    build_test -- Whether or not the tests should be built.

    build_benchmark -- Whether or not the benchmarks should be
    built.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    version -- The full version number of the dependency.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    installed_version -- The version of the dependecy that is
    written to the JSON file containing the currently installed
    versions of the dependencies.
    """
    if "testonly" in data_node:
        logging.warning(
            "The use of 'testonly' for determining whether a dependency is "
            "built only when the tests are built is deprecated; use "
            "'testOnly' instead"
        )
        if data_node["testonly"] and not build_test:
            return False
    else:
        if data_node["testOnly"] and not build_test:
            return False
    if "benchmarkonly" in data_node:
        logging.warning(
            "The use of 'benchmarkonly' for determining whether a dependency "
            "is built only when the tests are built is deprecated; use "
            "'benchmarkOnly' instead"
        )
        if data_node["benchmarkonly"] and not build_benchmark:
            return False
    else:
        if data_node["benchmarkOnly"] and not build_benchmark:
            return False
    return getattr(module, "should_install")(
        dependencies_root=dependencies_root,
        version=version,
        target=target,
        host_system=host_system,
        installed_version=installed_version
    )


def create_dependency_data(module_name, data_node):
    """
    Creates a common DependencyData object of a dependency. This
    function isn't totally pure as it imports the module using
    importlib.

    module_name -- The name of the module from which the various
    functions are got.

    data_node -- The entry in the dependency JSON file containing
    the data for the dependency in question.
    """
    package_name = "{}.dependencies.{}".format(
        get_project_package_name(),
        module_name
    )
    dependency_module = importlib.import_module(package_name)
    return DependencyData(
        get_key=lambda: module_name,
        get_name=lambda: data_node["name"],
        get_required_version=lambda target, host_system: data_node["version"],
        should_install=partial(
            _should_install_dependency,
            module=dependency_module,
            data_node=data_node
        ),
        install_dependency=getattr(dependency_module, "install_dependency")
    )
