# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""This support module parses presets of the scripts."""

import logging
import sys

from .mode_names import get_composing_mode_name, get_configuring_mode_name

if sys.version_info.major == 2:
    import ConfigParser as configparser
else:
    import configparser


def get_configuration_preset_prefix():
    """
    Gives the prefix used in front of the prefix portions used
    only in the configuration mode.
    """
    return "configure:"


def get_composing_preset_prefix():
    """
    Gives the prefix used in front of the prefix portions used
    only in the composing mode.
    """
    return "compose:"


def _create_configuration_parser(substitutions=None):
    """
    Creates the configuration parser for parsing the preset
    files.

    substitutions -- The values that should override the
    arguments in the preset files. The substitutions are
    currently disabled.
    """
    substitute_values = {} if not substitutions else substitutions
    return configparser.ConfigParser(substitute_values, allow_no_value=True)


def get_mixin_option_name():
    """
    Gives the name of the option that provides mix-in preset.
    """
    return "mix-in-preset"


def get_dash_dash_option_name():
    """
    Gives the name of the option that acts as the double dash.
    """
    return "dash-dash"


def _read_preset(parser, name, run_mode, substitutions=None):
    """
    Reads the options from the given preset loaded into the
    configuration parser.

    Returns three values: the first one is a dictionary
    containing the names of the preset options and the values
    associated with them, the second one is a dictionary
    containing the names of the preset options and the values
    associated with them that are given after the double dash,
    and the third one contains a list of the erroneous options.

    parser -- The parser from which the preset options are read.

    name -- The name of the preset.

    run_mode -- The mode in which the script is invoked in.

    substitutions -- The values that should override the
    arguments in the preset files. The substitutions are
    currently disabled.
    """
    logging.debug("Starting to read a preset with the name %s", name)

    is_mode_only_preset = name.startswith(get_configuration_preset_prefix()) \
        or name.startswith(get_composing_preset_prefix())

    mode_only_name = None

    if run_mode == get_configuring_mode_name():
        mode_only_name = "{}{}".format(get_configuration_preset_prefix(), name)
        logging.debug(
            "Checking whether a mode-specific preset portion '%s' exists for "
            "the preset '%s'",
            mode_only_name,
            name
        )
    elif run_mode == get_composing_mode_name():
        mode_only_name = "{}{}".format(get_composing_preset_prefix(), name)
        logging.debug(
            "Checking whether a mode-specific preset portion '%s' exists for "
            "the preset '%s'",
            mode_only_name,
            name
        )

    if name not in parser.sections() \
            and mode_only_name not in parser.sections():
        return None

    # The variables inside the function are modified often but
    # the changing state isn't exposed to the scope outside the
    # function.
    options = {}
    options_after_end = {}
    missing_options = []
    dash_dash_seen = False

    for option in parser.options(name):
        value = None

        try:
            value = parser.get(section=name, option=option)
        except configparser.InterpolationMissingOptionError as e:
            # e.reference contains the correctly formatted
            # option.
            missing_options.append(e.reference)

        if substitutions and option in substitutions:
            # TODO Substitute the value
            pass

        if option == get_mixin_option_name() and not is_mode_only_preset:
            # Multiple mix-in presets are allowed in one option.
            mixins = [mixin.strip() for mixin in value.splitlines()]

            for mixin in mixins:
                (mixin_options,
                 mixin_options_after_end,
                 missing_mixin_options) = _read_preset(
                    parser=parser,
                    name=mixin,
                    run_mode=run_mode,
                    substitutions=substitutions
                )
                options.update(mixin_options)
                options_after_end.update(mixin_options_after_end)
                missing_options.extend(missing_mixin_options)

        elif option == get_dash_dash_option_name():
            dash_dash_seen = True
        else:
            pair_to_add = {option: value}
            if dash_dash_seen:
                options_after_end.update(pair_to_add)
            else:
                options.update(pair_to_add)

    if mode_only_name and mode_only_name in parser.sections():
        (mode_options,
         mode_options_after_end,
         missing_mode_options) = _read_preset(
            parser=parser,
            name=mode_only_name,
            run_mode=run_mode,
            substitutions=substitutions
        )
        options.update(mode_options)
        options_after_end.update(mode_options_after_end)
        missing_options.extend(missing_mode_options)

    return options, options_after_end, missing_options


def get_preset_options(
    preset_file_names,
    preset_name,
    run_mode,
    substitutions=None
):
    """
    Gets the options in the given preset. This function isn't
    pure as it reads the given preset files.

    Returns two values: the first one is a dictionary containing
    the names of the preset options and the values associated
    with them and the second one is a dictionary containing the
    names of the preset options and the values associated with
    them that are given after the double dash.

    preset_file_names -- The files from which the presets are
    read.

    preset_name -- The name of the preset that is read.

    run_mode -- The mode in which the script is invoked in.

    substitutions -- The values that should override the
    arguments in the preset files. The substitutions are
    currently disabled.
    """
    config_parser = _create_configuration_parser(substitutions=substitutions)

    files_read = config_parser.read(preset_file_names)

    if files_read == []:
        logging.warning(
            "The preset files aren't found (tried %s)",
            preset_file_names
        )
        return []

    options, options_after_end, missing_options = _read_preset(
        parser=config_parser,
        name=preset_name,
        run_mode=run_mode,
        substitutions=substitutions
    )

    if not options and not options_after_end:
        logging.warning("No options were found for preset '%s'", preset_name)

    if missing_options:
        logging.warning(
            "The missing options for preset '%s': %s",
            preset_name,
            ", ".join(missing_options)
        )

    return options, options_after_end


def get_all_preset_names(preset_file_names):
    """
    Gets the names of the presets in a preset file. This function
    isn't pure as it reads the given preset files.

    preset_file_names -- The files from which the presets are
    read.
    """
    config_parser = _create_configuration_parser()
    files_read = config_parser.read(preset_file_names)
    if files_read == []:
        logging.warning(
            "The preset files aren't found (tried %s)",
            preset_file_names
        )
        return []
    return config_parser.sections()
