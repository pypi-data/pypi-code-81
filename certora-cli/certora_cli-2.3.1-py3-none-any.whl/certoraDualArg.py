import argparse
import re
from certora_cli.certoraUtils import print_warning   # type: ignore


"""

This file is here to handle dually-defined arguments: command line arguments that can also be passed as a setting.
For example, we can use either '--rule law' or '--settings -rule=law'
Another example is: '--loop_iter 2' or '--settings -b=2'

The argparser does not handle the value of --settings at all. This is so the jar developers can add flags quickly
 without changing the scripts.
"""

# Note: we do not check if the argument is defined in the ArgumentParser.
arg_to_setting = {
    'loop_iter': 'b',
    'method': 'method',
    'rule': 'rule'
}


def __check_single_arg_and_setting_consistency(args: argparse.Namespace, arg_name: str, setting_name: str) -> None:

    """
    We accept two syntaxes for settings: --rule or --settings -rule.
    This function checks that:
    1. The two syntaxes are consistent within the same command line (do not have contradicting values)
    2. The --settings syntax is consistent (gets a single setting -setting_name at most)
    3. If we use both the setting and the argument, warn of the redundancy

    After running this function, the value will be stored both in the settings and in the argument namespace.
    The arguments in settings may now be unsorted.

    @param args: a namespace containing command line arguments
    @param arg_name: name of the argument, for example: --rule or --loop_iterations
    @param setting_name: name of the setting, for example: -rule or -b
    @raises argparse.ArgumentTypeError if there is an inconsistent use of the argument.
    """
    setting_value = None
    all_settings_vals = set()
    if args.settings is not None:
        for setting in args.settings:
            setting_match = re.search(r'^-' + setting_name + r'(\S*)', setting)

            if setting_match is not None:
                curr_val = setting_match[1]
                if curr_val == "" or curr_val == "=":
                    raise argparse.ArgumentTypeError(f"No value was provided for setting {setting_name}")
                if re.search(r"^=[^=\s]+", curr_val):
                    if curr_val in all_settings_vals:
                        print_warning(f"Used --settings -{setting_name} more than once with the same value: {setting}")
                    all_settings_vals.add(curr_val[1:])  # remove the leading =
                elif not re.search(r"^\w+(=[^=\s]+)?$", curr_val):
                    # there might a setting for which this setting is a substring, like -rule and -ruleSanityChecks
                    raise argparse.ArgumentTypeError(f"wrong syntax for --settings -{arg_name}: {setting}")

        if len(all_settings_vals) > 1:
            all_vals_str = ' '.join(sorted(list(all_settings_vals)))
            raise argparse.ArgumentTypeError(
                f"Multiples values were given to setting {setting_name}: {all_vals_str}")
        if len(all_settings_vals) > 0:
            setting_value = list(all_settings_vals)[0]

    arg_val = getattr(args, arg_name, None)
    if arg_val is not None:
        arg_val = arg_val.replace(' ', '')
        # needed in case where we have --method foo(bool,address),
        # as we include an artificial space after the comma inside the parenthesis

    if arg_val is None and setting_value is None:
        return

    # given both as an argument and as a setting
    if arg_val is not None and setting_value is not None and arg_val != setting_value:
        raise argparse.ArgumentTypeError(
            f"There is a conflict between argument {arg_name} value of {arg_val} "
            f"and --settings -{setting_name} value of {setting_value}")

    if arg_val is None:  # add value to the argument
        setattr(args, arg_name, setting_value)  # settings value is not None

    if setting_value is None:  # add value to settings
        settings_str = f'-{setting_name}={arg_val}'
        if args.settings is None:
            args.settings = list()
        args.settings.append(settings_str)  # it is now unsorted!


def check_arg_and_setting_consistency(args: argparse.Namespace) -> None:
    """
    Check consistency for all dually-defined arguments.
    An argument is consistent if it has at most a single value.
    If an argument is defined both as a command-line argument and inside settings, we warn the user.
    At the end of this functions, all the dually-defined argument values will appears in both the argument namespace and
     inside the settings list in the namespace.
    args.settings will be sorted in ascending order.
    @param args: a namespace containing command line arguments
    @raises argparse.ArgumentTypeError if there is a dually-defined argument.
    """
    for (argument, settings) in arg_to_setting.items():
        __check_single_arg_and_setting_consistency(args, argument, settings)

    if args.settings is not None:
        args.settings.sort()
