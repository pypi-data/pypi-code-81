# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions for running the preset
mode of the script.
"""

from __future__ import print_function

import logging
import sys

from .support.presets import \
    get_all_preset_names, get_composing_preset_prefix, \
    get_configuration_preset_prefix, get_preset_options

from .util import shell


def show_presets(file_names):
    """
    Shows the available presets and returns the end code of this
    execution. This function isn't pure as it prints out the
    names of the presets.

    file_names -- The preset file names from which the preset
    names are read.
    """
    logging.info("The available presets are:")

    all_preset_names = get_all_preset_names(file_names)
    preset_names = []

    for name in all_preset_names:
        stripped_name = None

        if name.startswith(get_configuration_preset_prefix()):
            stripped_name = name[len(get_configuration_preset_prefix()):]
        elif name.startswith(get_composing_preset_prefix()):
            stripped_name = name[len(get_composing_preset_prefix()):]
        else:
            stripped_name = name

        if stripped_name not in preset_names:
            preset_names.append(stripped_name)

    for name in sorted(preset_names, key=str.lower):
        print(name)

    return 0


def _compose_preset_option_list(preset_options):
    """
    Composes the given dictionary of parsed preset options to a
    list of strings.

    preset_options -- The dictionary containing the parsed preset
    options.
    """
    argument_list = []
    for key, value in preset_options.items():
        if value:
            argument_list.append("--{}={}".format(key, value))
        else:
            argument_list.append("--{}".format(key))
    return argument_list


def compose_preset_call(arguments, file_names):
    """
    Creates the call used to call the script in preset mode. This
    function isn't pure.

    arguments -- The parsed command line arguments of the script.

    file_names -- The preset file names from which the preset
    names are read.
    """
    preset_options, preset_options_after_end = get_preset_options(
        preset_file_names=file_names,
        preset_name=arguments.preset,
        run_mode=arguments.preset_run_mode,
        substitutions=None
    )

    build_call = [sys.argv[0]]

    build_call.append(arguments.preset_run_mode)

    if arguments.dry_run:
        build_call.append("--dry-run")
    build_call.extend(["--jobs", str(arguments.jobs)])
    if arguments.clean:
        build_call.append("--clean")
    if arguments.print_debug:
        build_call.append("--print-debug")
    if arguments.in_tree_build:
        build_call.append("--in-tree-build")
    if arguments.github_auth_file:
        build_call.extend([
            "--github-auth-file",
            str(arguments.github_auth_file)
        ])
    if arguments.github_user_agent:
        build_call.extend([
            "--github-user-agent",
            str(arguments.github_user_agent)
        ])
    if arguments.github_api_token:
        build_call.extend([
            "--github-api-token",
            str(arguments.github_api_token)
        ])

    preset_arguments = _compose_preset_option_list(preset_options)
    preset_arguments_after_end = _compose_preset_option_list(
        preset_options_after_end
    )

    build_call.extend(preset_arguments)
    # TODO: build_call.append("--")
    build_call.extend(preset_arguments_after_end)

    return build_call


def print_script_invocation(build_call, preset_name, executable):
    """
    Prints the script invocation that is expanded from a preset.
    This function isn't pure as its purpose is to print the
    invocation.

    build_call -- The script call that is expanded from the
    preset.

    preset_name -- Name of the preset that was used.

    executable -- The Python executable that will be used.
    """
    logging.info(
        "Using preset '%s', which expands to \n\n%s\n",
        preset_name,
        shell.quote_command(build_call)
    )

    logging.debug(
        "The script will use '%s' as the Python executable\n",
        executable
    )
