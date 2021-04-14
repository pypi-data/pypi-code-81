"""Commands to provide additional feature on app, such as list all the apps"""
from deepchain import log

from ._utils import (
    display_apps_infos,
    display_config_info,
    get_apps_config,
    remove_app,
    reset_apps,
)


def apps_args_configuration(sub_parser):
    """
    Main parser for apps info
    Define 'Deploy' as default function
    """
    login_parser = sub_parser.add_parser(
        name="apps", help="give infos on apps create locally"
    )

    login_parser.add_argument(
        "--infos",
        action="store_const",
        default=False,
        const=True,
        help="list all apps' infos",
    )

    login_parser.add_argument(
        "--reset",
        action="store_const",
        default=False,
        const=True,
        help="!reset all apps",
    )

    login_parser.add_argument(
        "--delete",
        type=str,
        help="delete selected app",
    )

    login_parser.add_argument(
        "--config",
        action="store_const",
        default=False,
        const=True,
        help="show URL deployement config",
    )

    login_parser.set_defaults(func=apps_actions)


def apps_actions(args):
    """main function for list apps infos"""
    if args.infos:
        config = get_apps_config()

        if len(config) == 0:
            print("-------------------")
            print("No apps to display")
            print("-------------------")
        else:
            display_apps_infos(config)

    if args.config:
        display_config_info()

    if args.reset:
        msg = "You are about to delete all your apps, do you want to continue? (y/n) "
        answer = input(msg)
        while answer not in ["y", "n"]:
            answer = input(msg)

        if answer == "y":
            reset_apps()

    if args.delete:
        msg = f"You are about to delete {args.delete}' files, do you want to continue? (y/n) "
        answer = input(msg)
        while answer not in ["y", "n"]:
            answer = input(msg)

        if answer == "y":
            remove_app(args.delete)
            log.info("Remove App %s", args.delete)
