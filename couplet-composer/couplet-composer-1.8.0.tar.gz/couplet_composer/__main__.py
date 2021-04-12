# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""The entry point of Couplet Composer."""

from __future__ import print_function

import logging
import os
import platform
import sys

import distro

from collections import namedtuple

from datetime import datetime

from .support.environment import is_path_source_root

from .support.mode_names import \
    get_composing_mode_name, get_configuring_mode_name, get_preset_mode_name

from .support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from .support.project_names import get_ode_repository_name, get_project_name

from .support.project_values import \
    get_anthem_name, get_anthem_version, get_ode_name, get_ode_version, \
    get_project_version

from .util.date import date_difference, to_date_string

from .util.target import parse_target_from_argument_string

from .__version__ import __version__

from . import args, modes


def _create_argument_parser():
    """
    Creates the argument parser for the script and returns the
    namespace containing the parsed arguments. This function
    isn't pure but depends on the global Python variable
    containing the command line arguments.
    """
    return args.create_argument_parser()


def _parse_arguments(parser):
    """
    Creates the argument values for the script and returns the
    namespace containing the parsed arguments. This function
    isn't pure but depends on the global Python variable
    containing the command line arguments.

    parser -- The argument parser that is used to parse the
    arguments.
    """
    return parser.parse_known_args()


def _set_logging_level(print_debug):
    """
    Sets the logging level according to the given parameters.
    This function isn't pure.

    print_debug -- Whether or not the debug-level logging should
    be allowed.
    """
    log_format = "%(message)s"
    if print_debug:
        logging.basicConfig(format=log_format, level=logging.DEBUG)
    else:
        logging.basicConfig(format=log_format, level=logging.INFO)


def _check_and_print_python_version():
    """
    Checks the current Python version and prints it. This
    function isn't pure.
    """
    if sys.version_info.major == 2:
        if sys.version_info.minor < 7:
            logging.critical(
                "You're using Python %s, and the smallest supported version "
                "is %s",
                sys.version,
                "2.7"
            )
        else:
            logging.warning("You're using Python %s", sys.version)
            logging.warning(
                "You should really update to Python 3 to make the world a "
                "better place!"
            )
            # The end-of-life time of Python 2
            python2_end_of_life = datetime.strptime(
                "2020-01-01 00:00:00",
                "%Y-%m-%d %H:%M:%S"
            )
            now = datetime.now()
            logging.warning(
                "Also, the end of life of Python 2.7 was %s ago, on 1 "
                "January, 2020",
                to_date_string(date_difference(python2_end_of_life, now))
            )
            logging.warning(
                "Starting at version %s, %s will end supporting Python "
                "2.7",
                "2.0",
                get_project_name()
            )
    else:
        logging.debug("You're using Python %s", sys.version)
        logging.debug("You seem to have an excellent taste!")


def _resolve_running_function(mode, argument_parser):
    """
    Resolves the function that is chiefly responsible for running
    the script according to the mode in which the script is run.
    Returns a function.

    mode -- The name of the mode in which the script was run.

    argument_parser -- The parser used to parse the command line
    arguments of the script.
    """
    if mode == get_preset_mode_name():
        return modes.run_in_preset_mode
    elif mode == get_configuring_mode_name():
        return modes.run_in_configuring_mode
    elif mode == get_composing_mode_name():
        return modes.run_in_composing_mode
    else:
        def _(_1, _2):
            argument_parser.error("{} wasn't in valid mode".format(
                get_project_name()
            ))
            return 1
        return _


def run_script(runner, arguments, source_root):
    """
    Runs the script with the given runner and arguments and
    returns the end code of the program. This function isn't pure
    as the functions called by it may modify the file system and
    run other scripts.

    runner -- The function that runs the preferred mode of the
    script.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    return runner(arguments=arguments, source_root=source_root)


def _main():
    """
    Enters the program and runs it. This function isn't pure.
    """
    argument_parser = _create_argument_parser()
    arguments, unknown_arguments = _parse_arguments(argument_parser)

    # The logging level is the first thing to be set so it can be
    # utilized throughout the rest of the run.
    _set_logging_level(print_debug=arguments.print_debug)

    logging.info("Running %s version %s", get_project_name(), __version__)

    if unknown_arguments:
        logging.warning(
            "The following command line arguments weren't "
            "recognized:\n{}".format(
                "\n".join(unknown_arguments)
            )
        )

    source_root = os.getcwd()

    if not is_path_source_root(source_root, arguments.in_tree_build):
        logging.critical(
            "The source root directory is invalid: %s",
            source_root
        )
        if arguments.in_tree_build:
            logging.warning(
                "The script didn't find the required file '%s'",
                os.path.join(source_root, "CMakeLists.txt")
            )
        else:
            logging.warning(
                "The script didn't find the required file '%s'",
                os.path.join(
                    source_root,
                    get_ode_repository_name(),
                    "CMakeLists.txt"
                )
            )
        sys.exit(1)

    if arguments.composer_mode == get_configuring_mode_name() or \
            arguments.composer_mode == get_composing_mode_name():
        # If no project version is got from command line, it
        # should be read from the source root.
        default_version = str(get_project_version(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        ))
        if not arguments.ode_version:
            read_version = get_ode_version(
                source_root=source_root,
                in_tree_build=arguments.in_tree_build
            )
            if not read_version or read_version.lower() == "shared":
                arguments.ode_version = default_version
            # TODO Deprecated functionality
            if read_version.lower() == "default":
                logging.warning(
                    "The value 'default' for the shared version is "
                    "deprecated; use the value 'shared' instead"
                )
                arguments.ode_version = default_version
        else:
            logging.warning(
                "The command line option '--ode-version' is deprecated"
            )
        if not arguments.anthem_version:
            read_version = get_anthem_version(
                source_root=source_root,
                in_tree_build=arguments.in_tree_build
            )
            if not read_version or read_version.lower() == "shared":
                arguments.anthem_version = default_version
            # TODO Deprecated functionality
            if read_version.lower() == "default":
                logging.warning(
                    "The value 'default' for the shared version is "
                    "deprecated; use the value 'shared' instead"
                )
                arguments.anthem_version = default_version
        else:
            logging.warning(
                "The command line option '--anthem-version' is deprecated"
            )

        # TODO Remove this.
        if "{env." in arguments.ode_version:
            start = arguments.ode_version.find("{env.") + len("{env.")
            end = arguments.ode_version.find("}", start)
            variable_name = arguments.ode_version[start:end]
            logging.debug(
                "Trying to replace the environment variable '%s' in the "
                "version string of %s",
                variable_name,
                get_ode_name()
            )
            format_dict = {}
            format_dict[variable_name] = os.getenv(variable_name, "notfound")
            VariableTuple = namedtuple("VariableTuple", sorted(format_dict))
            format_tuple = VariableTuple(**format_dict)
            logging.debug(
                "The dictionary used in the replacement is %s",
                format_tuple
            )
            arguments.ode_version = arguments.ode_version.format(
                env=format_tuple
            )
            logging.warning(
                "Please note that using environment variables in version "
                "numbers is depracated functionality and will be removed in "
                "future version of Couplet Composer"
            )

        # TODO Remove this.
        if "{env." in arguments.anthem_version:
            start = arguments.anthem_version.find("{env.") + len("{env.")
            end = arguments.anthem_version.find("}", start)
            variable_name = arguments.anthem_version[start:end]
            logging.debug(
                "Trying to replace the environment variable '%s' in the "
                "version string of %s",
                variable_name,
                get_ode_name()
            )
            format_dict = {}
            format_dict[variable_name] = os.getenv(variable_name, "notfound")
            VariableTuple = namedtuple("VariableTuple", sorted(format_dict))
            format_tuple = VariableTuple(**format_dict)
            logging.debug(
                "The dictionary used in the replacement is %s",
                format_tuple
            )
            arguments.anthem_version = arguments.anthem_version.format(
                env=format_tuple
            )
            logging.warning(
                "Please note that using environment variables in version "
                "numbers is depracated functionality and will be removed in "
                "future version of Couplet Composer"
            )

        # Only configuring and composing modes have the option
        # for host target.
        host_target = parse_target_from_argument_string(arguments.host_target)

        if host_target.system == get_linux_system_name():
            logging.info("Running on %s %s", distro.name(), distro.version())
        elif host_target.system == get_darwin_system_name():
            logging.info("Running on %s %s", "macOS", platform.mac_ver()[0])
        elif host_target.system == get_windows_system_name():
            logging.info(
                "Running on %s %s",
                "Windows",
                platform.win32_ver()[0]
            )
        else:
            logging.warning("Running on an unknown platform")

        logging.info("The current build target is %s", arguments.host_target)

    _check_and_print_python_version()

    if arguments.in_tree_build:
        logging.debug(
            "The source root '%s' is valid and the required file '%s' exists",
            source_root,
            os.path.join(source_root, "CMakeLists.txt")
        )
    else:
        logging.debug(
            "The source root '%s' is valid and the required file '%s' exists",
            source_root,
            os.path.join(
                source_root,
                get_ode_repository_name(),
                "CMakeLists.txt"
            )
        )

    cmake_deprecated_replaced = [
        "ODE_BUILD_TEST",
        "ODE_TEST_BENCHMARKING",
        "ODE_BUILD_DOCS",
        "ODE_CODE_COVERAGE",
        "ODE_CXX_VERSION",
        "ODE_DEPENDENCY_PREFIX",
        "ODE_OPENGL_VERSION_MAJOR",
        "ODE_OPENGL_VERSION_MINOR",
        "ODE_VERSION",
        "ANTHEM_VERSION",
        "ODE_NAME",
        "ANTHEM_NAME"
    ]
    cmake_replacements = [
        "COMPOSER_BUILD_TEST",
        "COMPOSER_BUILD_BENCHMARK",
        "COMPOSER_BUILD_DOCS",
        "COMPOSER_CODE_COVERAGE",
        "COMPOSER_CPP_STD",
        "COMPOSER_LOCAL_PREFIX",
        "COMPOSER_OPENGL_VERSION_MAJOR",
        "COMPOSER_OPENGL_VERSION_MINOR",
        "COMPOSER_ODE_VERSION",
        "COMPOSER_ANTHEM_VERSION",
        "COMPOSER_ODE_NAME",
        "COMPOSER_ANTHEM_NAME"
    ]
    cmake_removed = [
        "ODE_DEVELOPER",
        "ODE_BUILD_STATIC",
        "ODE_BUILD_SHARED",
        "ANTHEM_BUILD_STATIC",
        "ANTHEM_BUILD_SHARED",
        "ODE_TEST_USE_NULL_SINK",
        "ODE_DISABLE_GL_CALLS",
        "ODE_SCRIPTS_BASE_DIRECTORY"
    ]

    logging.warning(
        "Please note the CMake options {}, and {} are deprecated".format(
            ", ".join(cmake_deprecated_replaced[:-1]),
            cmake_deprecated_replaced[-1]
        )
    )
    logging.warning("They will be replaced by {}, and {} respectively".format(
        ", ".join(cmake_replacements[:-1]),
        cmake_replacements[-1]
    ))
    logging.warning(
        "Please note that the CMake options {}, and {} are deprecated and "
        "removed in the next major version".format(
            ", ".join(cmake_removed[:-1]),
            cmake_removed[-1]
        )
    )

    deprecated_options = [
        "--print-debug",
        "--in-tree-build",
        "--github-auth-file",
        "--github-user-agent",
        "--github-api-token",
        "--compiler-toolchain",
        "--clang",
        "--gcc",
        "--msvc",
        "--compiler-version",
        "--host-cc",
        "--host-cxx",
        "--host-compiler",
        "--host-msbuild",
        "--clang-tidy-binary",
        "--clang-apply-replacements-binary",
        "--enable-xvfb",
        "--opengl-version",
        "--ode-static-lib",
        "--ode-shared-lib",
        "--anthem-static-lib",
        "--anthem-shared-lib",
        "--skip-build",
        "--export-linter-fixes",
        "--use-artefact-directory",
        "--ode-binaries-name",
        "--anthem-binaries-name",
        "--anthem-artefacts-name",
        "--anthem-artifacts-name",
        "--assertions",
        "--no-assertions",
        "--developer-build",
        "--test-logging"
    ]

    logging.warning(
        "Please note that the command line options {}, and {} are deprecated "
        "and removed in the next major version".format(
            ", ".join(deprecated_options[:-1]),
            deprecated_options[-1]
        )
    )

    return run_script(
        runner=_resolve_running_function(
            mode=arguments.composer_mode,
            argument_parser=argument_parser
        ),
        arguments=arguments,
        source_root=source_root
    )


def run():
    """Runs the script when Couplet Composer is invoked."""
    sys.exit(_main())


# The script can also be invoked by calling this script
if __name__ == "__main__":
    sys.exit(_main())
